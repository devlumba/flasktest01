
def test_403(client):
    client.post("/register/", data={"username": "user1", "email": "test1@test.com", "password": "password"})
    client.post("/login/", data={"email": "test1@test.com", "password": "password"})

    response = client.post("/post/1/modify", data={"title": "title1", "content": "content1"})

    assert response.status_code == 403


def test_404(client):
    response = client.get("/post/102")

    assert response.status_code == 404
