import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app, prefix
from app.database.models.users import User
from app.database.models.user_types import UserType
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


@pytest.fixture
def create_user_type(db_session: Session):
    """
    Fixture to create and clean up a user type for testing.
    """

    user_type_data = {"name": "Test User Type"}

    response = client.post(prefix + "/user_types/", json=user_type_data)

    assert response.status_code == 200

    user_type = response.json()

    yield user_type

    db_session.query(UserType).filter(UserType.user_type_id == user_type['user_type_id']).delete()

    db_session.commit()


@pytest.fixture
def create_user(db_session: Session, create_user_type, request):
    """
    Fixture to create and clean up a test user with a specified initial state.

    The initial state (active or inactive) is determined by a parameter.
    """

    # user_state = request.param if hasattr(request, 'param') else True
    user_state = request.param

    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser",
        "email": "testuser@example.com",
        "age": 25,
        "user_type_id": create_user_type['user_type_id'],
        "password": "securepassword",
        "is_active": user_state
    }

    response = client.post(prefix + "/users/", json=user_data)

    assert response.status_code == 200

    user = response.json()

    assert user['email'] == "testuser@example.com"

    yield user

    db_session.query(User).filter(User.user_id == user['user_id']).delete()

    db_session.commit()
