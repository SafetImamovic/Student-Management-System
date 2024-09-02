import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app, prefix
from app.database.models.users import User
from app.database.database import get_db

client = TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    """
    Fixture to provide a test database session.
    """

    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def create_user(db_session: Session):
    """
    Fixture to create and clean up a test user.

    This is created so that the test_get_by_email() and test_get_by_id() methods pass.
    """

    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser",
        "email": "testuser@example.com",
        "age": 25,
        "user_type_id": 1,
        "password": "securepassword"
    }

    response = client.post(prefix + "/users/", json=user_data)

    assert response.status_code == 200

    user = response.json()

    assert user['email'] == "testuser@example.com"

    yield user

    db_session.query(User).filter(User.user_id == user['user_id']).delete()

    db_session.commit()
