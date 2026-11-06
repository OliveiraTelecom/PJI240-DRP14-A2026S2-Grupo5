import pytest
import app as webapp

@pytest.fixture(autouse=True)
def isolated_test_config(monkeypatch):
    monkeypatch.setitem(webapp.app.config, "TESTING", True)
    monkeypatch.setitem(webapp.app.config, "CSRF_ENABLED", False)
