import pytest
from unittest.mock import patch, MagicMock

import main as myapp


@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    monkeypatch.setenv("MYSQL_USERNAME", "user")
    monkeypatch.setenv("MYSQL_PASSWORD", "pass")
    monkeypatch.setenv("MYSQL_ADDRESS", "localhost:3306")
    monkeypatch.setenv("MYSQL_DBNAME", "testdb")


def test_verifica_variaveis_ambiente_ok():
    vals = myapp.verifica_variaveis_ambiente()
    assert vals == ["user", "pass", "localhost:3306", "testdb"]


def test_verifica_variaveis_ambiente_missing(monkeypatch):
    monkeypatch.delenv("MYSQL_PASSWORD", raising=False)

    with patch("builtins.exit") as mock_exit:
        myapp.verifica_variaveis_ambiente()
        mock_exit.assert_called_once_with(1)


def test_root_route_success(monkeypatch):
    fake_user = myapp.Usuario(
        FirstName="John", LastName="Doe", Age=30, Height=1.8
    )

    app = myapp.create_app()

    mock_session = MagicMock()
    mock_session.query.return_value.all.return_value = [fake_user]

    monkeypatch.setattr(myapp.db, "session", mock_session)

    client = app.test_client()
    resp = client.get("/")

    assert resp.status_code == 200
    assert b"Funciona!" in resp.data
    assert b"John Doe" in resp.data


def test_root_route_exception(monkeypatch):
    mock_session = MagicMock()
    mock_session.query.side_effect = Exception("DB error")

    app = myapp.create_app()

    monkeypatch.setattr(myapp.db, "session", mock_session)

    client = app.test_client()
    resp = client.get("/")

    assert resp.status_code == 200
    assert b"Something is broken." in resp.data
    assert b"DB error" in resp.data
