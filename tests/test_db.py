from bungee_gum.models import User, Post
from flask_login import current_user
import responses

# thing(defs?) name should be started with "test_", classes names should start with a capital t test "Test" or smth


def test_registration(client, app):
    response = client.post("/register/", data={"username": "user1", "email": "test1@test.com", "password": "password"})
    # "username" is either model field name or a tag class, likely 1st

    with app.app_context():
        assert User.query.count() == 2
        assert User.query.first().email == "test@test.com"


@responses.activate
def test_login(client, app):
    # responses.add(
    #     responses.GET,
    #     ""
    # )   #  API stuff that I don't have in my app

    client.post("/register/", data={"username": "user1", "email": "test1@test.com", "password": "password"})
    # without a response it;s just a command to do ig
    client.post("/login/", data={"email": "test@test.com", "password": "password"})

    response = client.post("/post/new", data={"title": "title1", "content": "content1"})  # removing last slash fixed
    with app.app_context():
        assert Post.query.count() == 2
        assert Post.query.first().title == "title"


def test_post_new(client, app):
    client.post("/login/", data={"email": "test@test.com", "password": "password"})

    response = client.post("/post/new", data={"title": "newpost", "content": "content123"})

    with app.app_context():
        assert Post.query.filter_by(title="newpost").first().title == "newpost"


def test_post_modify(client, app):
    client.post("/login/", data={"email": "test@test.com", "password": "password"})

    response = client.post("/post/1/modify", data={"title": "newpostmodified", "content": "content1234"})

    assert response.status_code == 302  # I'm assuming 302 is just redirecting so it prob means I'm good


def test_post_delete(client, app):
    client.post("/login/", data={"email": "test@test.com", "password": "password"})

    response = client.post("/post/1/delete")

    assert response.status_code == 302  # I'm assuming 302 is just redirecting so it prob means I'm good
