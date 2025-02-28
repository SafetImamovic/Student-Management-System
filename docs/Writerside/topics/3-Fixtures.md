# 3. Fixtures

## What Are Fixtures?

Following the [Pytest Fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html).

More on the [Pytest Anatomy of Tests](https://docs.pytest.org/en/stable/explanation/anatomy.html#test-anatomy).

Fixtures are functions that provide data to test functions.

They are used to set up the initial state of the application before running tests.

Fixtures can be used to create test data,
set up database connections,
or perform any other setup tasks required for testing.

## Why use Fixtures?

This is an example of a test function that creates a `user`:

```python
def test_create_user():
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser",
        "email": "testuser@example.com",
        "age": 25,
        "password": "securepassword",
        "is_active": True,
        "user_type_id": 1
    }
    response = client.post(prefix + "/users/", json=user_data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data['email'] == "testuser@example.com"
```

If this user doesn't exist in the database already, and we run this once a response of `200` will be returned.

However, if we run this test again, it will fail with a response of `409 CONFLICT` because the user already exists.

We need some way to clean up the database after each test run.

This is where fixtures come in.

## How to Use Fixtures

Firstly a new `conftest.py` file is added to the `tests` module.

We can place all the fixtures in the `conftest.py` file,
which pytest automatically discovers and makes available to all test files.

Fixtures are defined using the `@pytest.fixture` decorator.

```python
imports {...}

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


@pytest.fixture
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

```

#### 1. **`db_session` Fixture**

```python
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
```

- **Purpose**: Provides a fresh database session for each test function.

- **Scope**: `scope="function"` means that this fixture is invoked once per test function. Each test will get its own fresh instance of `db_session`.

- **Functionality**:
    - `db = next(get_db())`: Creates a new database session by calling `get_db()`. This should return a new session object.
    - `yield db`: Passes the database session to the test function. The `yield` statement is used to provide the fixture value to the test.
    - `finally: db.close()`: Ensures that the database session is closed after the test function has completed, regardless of whether the test passed or failed. This prevents resource leaks.

#### 2. **`create_user` Fixture**

```python
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
```

- **Purpose**: Creates a user and provides the user data to the test functions. Ensures that the user is deleted after the test to avoid clutter.

- **Scope**: `scope="function"` means this fixture will be created fresh for each test function that uses it.

- **Functionality**:
    - **User Creation**:
        - `user_data`: Defines the data for the test user.
        - `response = client.post(prefix + "/users/", json=user_data)`: Sends a POST request to create the user using FastAPI's `TestClient`.
        - `assert response.status_code == 200`: Checks that the user was created successfully by asserting that the HTTP status code is 200 (OK).
        - `user = response.json()`: Parses the response JSON to get the user data.
        - `assert user['email'] == "testuser@example.com"`: Confirms that the email in the response matches the expected value.
    - **Yield**:
        - `yield user`: Passes the created user’s data to the test functions that use this fixture.
    - **User Cleanup**:
        - `db_session.query(User).filter(User.user_id == user['user_id']).delete()`: Deletes the user from the database using SQLAlchemy. It filters the user by ID and deletes the record.
        - `db_session.commit()`: Commits the transaction to the database to apply the changes.


#### 3. **Using Fixtures in Test Functions**

To use the `create_user` fixture in a test function, we can include it as an argument in the test function definition:

```python
def test_get_by_email(create_user):
    email = create_user['email']

    response = client.get(prefix + f"/users/email/{email}")

    assert response.status_code == 200

    json_data = response.json()

    assert 'email' in json_data and json_data['email'] == email
```

This will automatically call the `create_user` fixture before running the test function and pass the user data to the test function.

By using fixtures, we can ensure that the test environment is properly set up and cleaned up for each test, making our tests more reliable and repeatable.


