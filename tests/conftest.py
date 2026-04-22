import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True

    with app.app_context():
        db.drop_all()     # 🔥 clear old data
        db.create_all()   # 🔥 fresh DB

    yield app


@pytest.fixture
def client(app):
    return app.test_client()