from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_users():
    response = client.get("/api/v0/users/")
    assert response.status_code == 200


# def test_read_users_fail():
#     response = client.get("/api/v0/users/")
#     assert response.status_code == 404
