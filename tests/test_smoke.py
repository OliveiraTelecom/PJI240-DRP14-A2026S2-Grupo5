"""Testes básicos independentes de um banco PostgreSQL externo."""
from unittest.mock import patch
import app as webapp


def test_paginas_de_cadastro():
    for kind in ("clientes", "motoristas", "veiculos"):
        with patch.object(webapp, "query", return_value=[]):
            response = webapp.app.test_client().get("/" + kind)
        assert response.status_code == 200


def test_entregas_e_relatorios():
    with patch.object(webapp, "query", return_value=[]):
        assert webapp.app.test_client().get("/entregas").status_code == 200
    with patch.object(webapp, "query", return_value=[]):
        assert webapp.app.test_client().get("/relatorios").status_code == 200


def test_registro_obrigatorio():
    with patch.object(webapp, "write") as write:
        response = webapp.app.test_client().post("/clientes", data={}, follow_redirects=True)
    assert response.status_code == 200
    write.assert_not_called()


def test_tipo_invalido():
    assert webapp.app.test_client().get("/qualquer").status_code == 404
