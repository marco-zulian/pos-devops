import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import main as myapp


@pytest.fixture
def app(monkeypatch):
    """
    A fixture to create and configure a new app instance for each test.
    """
    monkeypatch.setenv("MYSQL_USERNAME", "user")
    monkeypatch.setenv("MYSQL_PASSWORD", "pass")
    monkeypatch.setenv("MYSQL_ADDRESS", "ignored")
    monkeypatch.setenv("MYSQL_DBNAME", "ignored")

    app = myapp.create_app(
        {
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "TESTING": True,
        }
    )

    with app.app_context():
        myapp.Base.metadata.create_all(bind=myapp.db.engine)

    yield app

    with app.app_context():
        myapp.Base.metadata.drop_all(bind=myapp.db.engine)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


def test_root_with_no_users(client):
    """Test the root route when the database is empty."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"<h1>Funciona!</h1>" in resp.data
    assert b"<h2>" not in resp.data


def test_root_with_users(app, client):
    """Test the root route after adding a user to the database."""
    with app.app_context():
        user = myapp.Usuario(
            FirstName="Alice", LastName="Smith", Age=25, Height=1.65
        )
        myapp.db.session.add(user)
        myapp.db.session.commit()

    resp = client.get("/")
    assert resp.status_code == 200
    assert b"<h1>Funciona!</h1>" in resp.data

    assert b"<h2>Alice Smith, 25, 1.65</h2>" in resp.data