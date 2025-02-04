from bungee_gum.models import User

# thing(defs?) name should be started with "test_", classes names should start with a capital t test "Test" or smth


def test_home(client):
    response = client.get("/")  # there's client.put, client.post

    assert b'<h1 class="text1">Wubba Lubba dub-dub</h1>' in response.data
    # response.data is a byte type, though can be decoded


def test_registration(client, app):
    response = client.post("/register/", data={"username": "user1", "email": "test@test.com", "password": "password"})

    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "test@test.com"


