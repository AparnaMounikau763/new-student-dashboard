import pytest
from app import create_app
from app.extensions import db

@pytest.fixture(scope="session")
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()