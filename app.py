"""Aplicação acadêmica de gerenciamento logístico baseada no esquema SQL original."""
import os
from decimal import Decimal, InvalidOperation
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, url_for, abort
import psycopg
from psycopg.rows import dict_row
from psycopg.errors import IntegrityError

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "development-only-change-me")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://logistica:logistica@localhost:5432/pi_logistica")

TABLES = {
    "clientes": {"table": "cliente", "title": "Clientes", "fields": [("nome_razao", "Nome / razão social", "text", True), ("cpf_cnpj", "CPF / CNPJ", "text", True), ("telefone", "Telefone", "text", False), ("endereco_base", "Endereço", "text", False)]},
    "motoristas": {"table": "motorista", "title": "Motoristas", "fields": [("nome_completo", "Nome completo", "text", True), ("cnh_numero", "Número da CNH", "text", True), ("categoria_cnh", "Categoria CNH", "text", True), ("possui_ear", "Possui EAR", "checkbox", False), ("status", "Status", "select:disponivel,em_viagem,ferias,inativo", True)]},
    "veiculos": {"table": "veiculo", "title": "Veículos", "fields": [("placa", "Placa", "text", True), ("tipo", "Tipo", "text", True), ("marca_modelo", "Marca / modelo", "text", True), ("ano_fabricacao", "Ano", "number", True), ("capacidade_kg", "Capacidade (kg)", "number", True), ("status", "Status", "select:operacional,manutencao,baixado", True)]},
}
STATUSES = ("pendente", "em_transito", "concluida", "cancelada")


def connect():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def query(sql, params=(), one=False):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone() if one else cur.fetchall()


def write(sql, params):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)


def safe_write(sql, params, target):
    try:
        write(sql, params)
        flash("Operação realizada com sucesso.", "success")
    except (IntegrityError, ValueError, InvalidOperation) as exc:
        flash("Não foi possível salvar: verifique campos obrigatórios, valores e duplicidades.", "danger")
    return redirect(target)


@app.route("/")
def dashboard():
    summary = query("SELECT (SELECT COUNT(*) FROM cliente) AS clientes, (SELECT COUNT(*) FROM motorista) AS motoristas, (SELECT COUNT(*) FROM veiculo) AS veiculos, (SELECT COUNT(*) FROM entrega) AS entregas", one=True)
    statuses = query("SELECT status, COUNT(*) AS quantidade FROM entrega GROUP BY status ORDER BY status")
    recent = query("SELECT e.id, c.nome_razao AS cliente, e.status, e.cep_destino, e.valor_frete FROM entrega e JOIN cliente c ON c.id=e.cliente_id ORDER BY e.data_saida DESC NULLS LAST, e.id DESC LIMIT 10")
    return render_template("dashboard.html", summary=summary, statuses=statuses, recent=recent)


@app.route("/<kind>", methods=["GET", "POST"])
def records(kind):
    if kind not in TABLES:
        abort(404)
    config = TABLES[kind]
    if request.method == "POST":
        columns = [f[0] for f in config["fields"]]
        values = [(request.form.get(c) == "on") if c == "possui_ear" else (request.form.get(c) or None) for c in columns]
        if any(values[i] in (None, "") for i, field in enumerate(config["fields"]) if field[3]):
            flash("Preencha todos os campos obrigatórios.", "danger")
            return redirect(url_for("records", kind=kind))
        placeholders = ", ".join(["%s"] * len(columns))
        sql = f"INSERT INTO {config['table']} ({', '.join(columns)}) VALUES ({placeholders})"
        return safe_write(sql, values, url_for("records", kind=kind))
    rows = query(f"SELECT * FROM {config['table']} ORDER BY 2")
    return render_template("records.html", kind=kind, config=config, rows=rows)


@app.post("/<kind>/<uuid:item_id>/delete")
def delete_record(kind, item_id):
    if kind not in TABLES:
        abort(404)
    return safe_write(f"DELETE FROM {TABLES[kind]['table']} WHERE id=%s", (str(item_id),), url_for("records", kind=kind))


@app.route("/entregas", methods=["GET", "POST"])
def entregas():
    if request.method == "POST":
        keys = ("cliente_id", "motorista_id", "veiculo_id", "cep_origem", "cep_destino", "distancia_km", "valor_frete")
        vals = [request.form.get(k) or None for k in keys]
        if any(not vals[i] for i in (0, 1, 2, 3, 4, 6)):
            flash("Preencha os campos obrigatórios da entrega.", "danger")
            return redirect(url_for("entregas"))
        return safe_write("INSERT INTO entrega (cliente_id,motorista_id,veiculo_id,cep_origem,cep_destino,distancia_km,valor_frete,status) VALUES (%s,%s,%s,%s,%s,%s,%s,'pendente')", vals, url_for("entregas"))
    rows = query("SELECT e.*, c.nome_razao AS cliente, m.nome_completo AS motorista, v.placa FROM entrega e JOIN cliente c ON c.id=e.cliente_id JOIN motorista m ON m.id=e.motorista_id JOIN veiculo v ON v.id=e.veiculo_id ORDER BY e.data_saida DESC NULLS LAST, e.id DESC")
    return render_template("entregas.html", rows=rows, clientes=query("SELECT id,nome_razao AS label FROM cliente ORDER BY nome_razao"), motoristas=query("SELECT id,nome_completo AS label FROM motorista WHERE status <> 'inativo' ORDER BY nome_completo"), veiculos=query("SELECT id,placa AS label FROM veiculo WHERE status='operacional' ORDER BY placa"), statuses=STATUSES)


@app.post("/entregas/<uuid:item_id>/status")
def update_status(item_id):
    status = request.form.get("status")
    if status not in STATUSES:
        abort(400)
    sql = "UPDATE entrega SET status=%s, data_saida=CASE WHEN %s='em_transito' AND data_saida IS NULL THEN CURRENT_TIMESTAMP ELSE data_saida END, data_chegada=CASE WHEN %s='concluida' THEN CURRENT_TIMESTAMP WHEN %s IN ('pendente','em_transito') THEN NULL ELSE data_chegada END WHERE id=%s"
    return safe_write(sql, (status, status, status, status, str(item_id)), url_for("entregas"))


@app.get("/relatorios")
def relatorios():
    billing = query("SELECT c.nome_razao, COUNT(e.id) AS total, COALESCE(SUM(e.valor_frete),0) AS faturamento FROM cliente c LEFT JOIN entrega e ON e.cliente_id=c.id GROUP BY c.id ORDER BY faturamento DESC")
    status = query("SELECT status, COUNT(*) AS total, COALESCE(SUM(distancia_km),0) AS km FROM entrega GROUP BY status ORDER BY status")
    return render_template("relatorios.html", billing=billing, status=status)


@app.get("/health")
def health():
    try:
        query("SELECT 1", one=True)
        return {"status": "ok", "database": "connected"}
    except psycopg.Error:
        return {"status": "error", "database": "unavailable"}, 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
