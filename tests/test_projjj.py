from bungee_gum.models import User, Post
from flask_login import current_user
import responses

# thing(defs?) name should be started with "test_", classes names should start with a capital t test "Test" or smth

#
# def test_home(client):
#     response = client.get("/")  # there's client.put, client.post
#
#     assert b'<h1 class="text1">Wubba Lubba dub-dub</h1>' in response.data
#     # response.data is a byte type, though can be decoded
#
#
# def test_registration(client, app):
#     response = client.post("/register/", data={"username": "user1", "email": "test1@test.com", "password": "password"})
#     # "username" is either model field name or a tag class, likely 1st
#
#     with app.app_context():
#         assert User.query.count() == 2
#         assert User.query.first().email == "test@test.com"
#
#
# @responses.activate
# def test_login(client, app):
#     # responses.add(
#     #     responses.GET,
#     #     ""
#     # )   #  API stuff that I don't have in my app
#
#     client.post("/register/", data={"username": "user1", "email": "test1@test.com", "password": "password"})
#     # without a response it;s just a command to do ig
#     client.post("/login/", data={"email": "test@test.com", "password": "password"})
#
#     response = client.post("/post/new", data={"title": "title1", "content": "content1"})  # removing last slash fixed
#     with app.app_context():
#         assert Post.query.count() == 2
#         assert Post.query.first().title == "title"
#
#
# def test_403(client):
#     client.post("/register/", data={"username": "user1", "email": "test1@test.com", "password": "password"})
#     client.post("/login/", data={"email": "test1@test.com", "password": "password"})
#
#     response = client.post("/post/1/modify", data={"title": "title1", "content": "content1"})
#
#     assert response.status_code == 403
#
#
# def test_404(client):
#     response = client.get("/post/102")
#
#     assert response.status_code == 404
