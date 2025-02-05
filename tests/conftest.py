import pytest
from bungee_gum import create_app, db, bcrypt
from bungee_gum.models import User, Post



@pytest.fixture()
def app():
    app = create_app(database_uri="sqlite://", wtf_csrf=False)  # separate sqlite database in memory

    with app.app_context():
        db.create_all()
        hashed_password = bcrypt.generate_password_hash("password").decode("utf-8")
        user = User(username="username", email="test@test.com", password=hashed_password)
        db.session.add(user)
        post = Post(title="title", content="content", user_id=1)
        db.session.add(post)
        db.session.commit()

    print("dap me up my boy")

    yield app


@pytest.fixture()
def client(app):  # pytest checks it by the name and passes other fixture, even though it's put as a parameter
    return app.test_client()

