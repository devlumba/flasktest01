

def test_home(client):
    response = client.get("/")  # there's client.put, client.post

    assert response.status_code == 200
    # response.data is a byte type, though can be decoded


def test_my_page(client):
    client.post("/login/", data={"email": "test@test.com", "password": "password"})

    response = client.get("/my-account/")

    assert response.status_code == 200


def test_all_posts(client):
    response = client.get("/all-posts/")

    assert response.status_code == 200


def test_all_users(client):
    response = client.get("/all-users/")

    assert response.status_code == 200


def test_post_ideas(client):
    response = client.get("/all-posts/ideas")

    assert response.status_code == 200


def test_post_programming(client):
    response = client.get("/all-posts/programming")

    assert response.status_code == 200


def test_posts_paginated(client):
    response = client.get("/all-posts/paginated/")

    assert response.status_code == 200


def test_post_view(client):
    response = client.get("/post/1")

    assert response.status_code == 200


def test_user_view(client):
    response = client.get("/user/1")

    assert response.status_code == 200




