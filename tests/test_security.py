from unittest.mock import patch
import app as webapp

def test_post_without_csrf_is_rejected(monkeypatch):
    monkeypatch.setitem(webapp.app.config, "CSRF_ENABLED", True)
    with patch.object(webapp, "write") as write:
        response = webapp.app.test_client().post("/clientes", data={"nome_razao":"Teste","cpf_cnpj":"DEMO"})
    assert response.status_code == 400
    write.assert_not_called()

def test_valid_csrf_reaches_validation(monkeypatch):
    monkeypatch.setitem(webapp.app.config, "CSRF_ENABLED", True)
    client = webapp.app.test_client()
    with patch.object(webapp, "query", return_value=[]):
        assert client.get("/clientes").status_code == 200
    with client.session_transaction() as session:
        token = session["_csrf_token"]
    with patch.object(webapp, "write") as write:
        response = client.post("/clientes", data={"_csrf_token":token})
    assert response.status_code == 302
    write.assert_not_called()

def test_invalid_cep_is_rejected():
    data={"cliente_id":"c","motorista_id":"m","veiculo_id":"v","cep_origem":"abc","cep_destino":"13010-000","valor_frete":"20"}
    with patch.object(webapp, "write") as write:
        response=webapp.app.test_client().post("/entregas",data=data)
    assert response.status_code==302
    write.assert_not_called()
