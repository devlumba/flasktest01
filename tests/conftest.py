import pytest
from bungee_gum import create_app, db


@pytest.fixture()
def app():
    app = create_app(database_uri="sqlite://", wtf_csrf=False)  # separate sqlite database in memory

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app):  # pytest checks it by the name and passes other fixture, even though it's put as a parameter
    return app.test_client()

