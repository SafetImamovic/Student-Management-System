import pytest
from fastapi.testclient import TestClient
from main import app, prefix
from app.database.models.users import User

client = TestClient(app)


def test_get_count():
    response = client.get(prefix + "/users/count/")

    assert response.status_code == 200

    assert isinstance(response.json(), int)


@pytest.mark.parametrize("create_user", [True], indirect=True)
def test_get_by_id(create_user):
    user_id = create_user['user_id']

    response = client.get(prefix + f"/users/{user_id}")

    assert response.status_code == 200

    json_data = response.json()

    assert 'user_id' in json_data and json_data['user_id'] == user_id

    assert 'email' in json_data


@pytest.mark.parametrize("create_user", [True], indirect=True)
def test_get_by_email(create_user):
    email = create_user['email']

    response = client.get(prefix + f"/users/email/{email}")

    assert response.status_code == 200

    json_data = response.json()

    assert 'email' in json_data and json_data['email'] == email


def test_get_all():
    response = client.get(prefix + "/users/")

    assert response.status_code == 200

    json_data = response.json()

    assert isinstance(json_data, list)

    assert len(json_data) <= 10


def test_create_user(db_session, create_user_type):
    user_data = {
        "first_name": "Test2",
        "last_name": "User2",
        "username": "testuser2",
        "email": "testuser2@example.com",
        "age": 25,
        "user_type_id": create_user_type['user_type_id'],
        "password": "securepassword"
    }

    response = client.post(prefix + "/users/", json=user_data)

    assert response.status_code == 201

    user = response.json()

    assert user['email'] == "testuser2@example.com"

    db_session.query(User).filter(User.user_id == user['user_id']).delete()

    db_session.commit()


@pytest.mark.parametrize("create_user", [True], indirect=True)
def test_deactivate_user(create_user):
    user_id = create_user['user_id']

    response = client.put(prefix + f"/users/{user_id}")

    assert response.status_code == 200

    json_data = response.json()

    assert not json_data['is_active']


@pytest.mark.parametrize("create_user", [False], indirect=True)
def test_activate_user(create_user):
    user_id = create_user['user_id']

    response = client.put(prefix + f"/users/activate/{user_id}")

    assert response.status_code == 200

    json_data = response.json()

    assert json_data['is_active']
