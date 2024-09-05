from fastapi.testclient import TestClient
from main import app, prefix
from app.database.models.user_types import UserType

client = TestClient(app)


def test_get_count():
    response = client.get(prefix + "/user_types/count/")

    assert response.status_code == 200

    assert isinstance(response.json(), int)


def test_get_by_id(create_user_type):
    user_type_id = create_user_type['user_type_id']

    response = client.get(prefix + f"/user_types/{user_type_id}")

    assert response.status_code == 200

    user_type = response.json()

    assert user_type['user_type_id'] == user_type_id

    assert user_type['name'] == "Test User Type"


def test_get_by_id_not_found():
    response = client.get(prefix + f"/user_types/0")

    assert response.status_code == 404


def test_get_by_name(create_user_type):
    name = create_user_type['name']

    response = client.get(prefix + f"/user_types/name/{name}")

    assert response.status_code == 200

    user_type = response.json()

    assert user_type['name'] == name


def test_get_all():
    response = client.get(prefix + "/user_types/")

    assert response.status_code == 200

    user_types = response.json()

    assert isinstance(user_types, list)


def test_create_user_type(db_session):
    user_type_data = {"name": "Test User Type 2"}

    response = client.post(prefix + "/user_types/", json=user_type_data)

    assert response.status_code == 201

    user_type = response.json()

    assert user_type['name'] == "Test User Type 2"

    db_session.query(UserType).filter(UserType.user_type_id == user_type['user_type_id']).delete()

    db_session.commit()


def test_create_user_type_conflict(db_session):
    user_type_data = {"name": "Test User Type 2"}

    first_object = client.post(prefix + "/user_types/", json=user_type_data)

    response = client.post(prefix + "/user_types/", json=user_type_data)

    assert response.status_code == 409

    user_type = first_object.json()

    assert user_type['name'] == "Test User Type 2"

    db_session.query(UserType).filter(UserType.user_type_id == user_type['user_type_id']).delete()

    db_session.commit()


def test_create_user_type_wrong_field_types():
    user_type_data = {"name": 1}

    response = client.post(prefix + "/user_types/", json=user_type_data)

    assert response.status_code == 422


def test_delete_user_type(create_user_type):
    user_type_id = create_user_type['user_type_id']

    response = client.delete(prefix + f"/user_types/{user_type_id}")

    assert response.status_code == 200

    deleted_user_type = response.json()

    assert deleted_user_type['user_type_id'] == user_type_id

    response = client.get(prefix + f"/user_types/{user_type_id}")

    assert response.status_code == 404
