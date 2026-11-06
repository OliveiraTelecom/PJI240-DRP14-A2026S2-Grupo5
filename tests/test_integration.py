"""Aceitação com PostgreSQL real em esquema temporário, sem alterar dados existentes."""
import os
from pathlib import Path
from uuid import uuid4

import psycopg
from psycopg import sql
from psycopg.conninfo import make_conninfo
import pytest
import app as webapp


@pytest.fixture
def banco_real(monkeypatch):
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Defina TEST_DATABASE_URL para validar PostgreSQL real")
    schema = "aceitacao_" + uuid4().hex
    with psycopg.connect(url, autocommit=True) as conn:
        conn.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))
    test_url = make_conninfo(url, options=f"-csearch_path={schema},public")
    try:
        with psycopg.connect(test_url) as conn:
            conn.execute(Path("sql/01_criacao_e_insercao.sql").read_text(), prepare=False)
        monkeypatch.setattr(webapp, "DATABASE_URL", test_url)
        monkeypatch.setitem(webapp.app.config, "TESTING", True)
        yield webapp.app.test_client()
    finally:
        with psycopg.connect(url, autocommit=True) as conn:
            conn.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))


def test_fluxo_completo_postgresql(banco_real):
    client = banco_real
    assert client.get("/health").json == {"status": "ok", "database": "connected"}
    for path in ("/", "/clientes", "/motoristas", "/veiculos", "/entregas", "/relatorios"):
        assert client.get(path).status_code == 200

    records = {
        "clientes": {"nome_razao": "Cliente Aceitação", "cpf_cnpj": "TESTE-ACEITE"},
        "motoristas": {"nome_completo": "Motorista Aceitação", "cnh_numero": "TESTE-ACEITE", "categoria_cnh": "D", "possui_ear": "on", "status": "disponivel"},
        "veiculos": {"placa": "TST1A23", "tipo": "Caminhão", "marca_modelo": "Frota Teste", "ano_fabricacao": "2024", "capacidade_kg": "1000", "status": "operacional"},
    }
    ids = {}
    for kind, data in records.items():
        response = client.post("/" + kind, data=data, follow_redirects=True)
        assert response.status_code == 200
        assert "Operação realizada com sucesso" in response.text
        config = webapp.TABLES[kind]
        key = {"clientes": "cpf_cnpj", "motoristas": "cnh_numero", "veiculos": "placa"}[kind]
        row = webapp.query(f"SELECT id FROM {config['table']} WHERE {key}=%s", (data[key],), one=True)
        ids[kind] = str(row["id"])

    data = {"cliente_id": ids["clientes"], "motorista_id": ids["motoristas"], "veiculo_id": ids["veiculos"], "cep_origem": "01001-000", "cep_destino": "13010-000", "distancia_km": "100.50", "valor_frete": "250.75"}
    response = client.post("/entregas", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert "Operação realizada com sucesso" in response.text
    entrega = webapp.query("SELECT * FROM entrega WHERE cliente_id=%s", (ids["clientes"],), one=True)
    assert entrega["status"] == "pendente"
    for status in ("em_transito", "concluida"):
        response = client.post(f"/entregas/{entrega['id']}/status", data={"status": status}, follow_redirects=True)
        assert response.status_code == 200
        saved = webapp.query("SELECT * FROM entrega WHERE id=%s", (entrega["id"],), one=True)
        assert saved["status"] == status
        assert saved["data_saida"] is not None
    assert saved["data_chegada"] is not None
    assert "Cliente Aceitação" in client.get("/relatorios").text
    assert "250.75" in client.get("/relatorios").text

    duplicate = client.post("/clientes", data=records["clientes"], follow_redirects=True)
    assert duplicate.status_code == 200
    assert "Não foi possível salvar" in duplicate.text
    for kind, item_id in ids.items():
        response = client.post(f"/{kind}/{item_id}/delete", follow_redirects=True)
        assert response.status_code == 200
        assert "Não foi possível salvar" in response.text
        assert webapp.query(f"SELECT id FROM {webapp.TABLES[kind]['table']} WHERE id=%s", (item_id,), one=True)
    assert client.get("/health").status_code == 200


@pytest.mark.parametrize("field,value", [("ano_fabricacao", "abc"), ("capacidade_kg", "invalido"), ("placa", "X" * 30)])
def test_dados_invalidos_nao_geram_erro_500(banco_real, field, value):
    data = {"placa": "TST2A34", "tipo": "Van", "marca_modelo": "Teste", "ano_fabricacao": "2024", "capacidade_kg": "500", "status": "operacional"}
    data[field] = value
    response = banco_real.post("/veiculos", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert "Não foi possível salvar" in response.text
