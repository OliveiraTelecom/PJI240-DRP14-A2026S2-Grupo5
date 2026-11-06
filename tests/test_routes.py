from unittest.mock import patch
import app as webapp


def test_dashboard():
    webapp.app.config['TESTING'] = True
    with patch.object(webapp, 'query', side_effect=[{'clientes': 2, 'motoristas': 1, 'veiculos': 2, 'entregas': 1}, [], []]):
        response = webapp.app.test_client().get('/')
    assert response.status_code == 200
    assert 'Painel operacional' in response.get_data(as_text=True)


def test_invalid_status():
    webapp.app.config['TESTING'] = True
    response = webapp.app.test_client().post('/entregas/11111111-1111-1111-1111-111111111111/status', data={'status': 'invalido'})
    assert response.status_code == 400


def test_health_unavailable():
    import psycopg
    with patch.object(webapp, 'query', side_effect=psycopg.OperationalError('offline')):
        response = webapp.app.test_client().get('/health')
    assert response.status_code == 503
