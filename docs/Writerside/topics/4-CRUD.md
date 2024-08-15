# 4. CRUD

We create a `crud.py` file to handle the CRUD operations inside the `app/` directory.

CRUD comes from: **C**reate, **R**ead, **U**pdate, and **D**elete.

### `crud.py`
```Python
from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = user.password + "fakehashed"
    db_user = models.User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        age=user.age,
        is_active=user.is_active,
        user_type_id=1,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

```

### `main.py`
<code-block collapsible="true" collapsed-title="main.py" lang="python">
<![CDATA[
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World!"}


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/{email}", response_model=schemas.User)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user;

]]>
</code-block>



1. **Creating a Database Session**:
   ```python
   db = SessionLocal()
   ```
   Here, `SessionLocal` is typically a factory function or class that creates a new database session. This session object is used to interact with the database. `SessionLocal` is often defined using SQLAlchemy's `sessionmaker` function and is used to create a new session instance.

2. **Using a Context Manager**:
   ```python
   try:
       yield db
   ```
    - `yield db` is used to return the `db` session object to whatever part of the code is requesting it. In the context of FastAPI, this allows dependency injection to provide the `db` session to route handlers or other functions.
    - The `yield` statement here is used to produce a value and pause the function, allowing the caller to use the database session (`db`). This pattern is known as a generator function in Python.

3. **Closing the Database Session**:
   ```python
   finally:
       db.close()
   ```
    - The `finally` block ensures that the `db.close()` method is called after the `yield` statement, no matter what happens (whether an exception occurs or not). This is important for releasing database resources and closing the connection properly.
    - `db.close()` is used to close the database session, freeing up any resources associated with it.

Certainly! Here's a detailed breakdown of each route in this FastAPI application:


### 1. **Get Users Endpoint**

```python
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
```

- **Decorator**: `@app.get("/users/")` specifies that this function will handle HTTP GET requests to the `/users/` URL.
- **Parameters**:
    - `skip` (optional): An integer query parameter for pagination, specifying the number of items to skip.
    - `limit` (optional): An integer query parameter for pagination, specifying the maximum number of items to return.
    - `db` (injected): A `Session` object provided by the `get_db` dependency. This is used to interact with the database.
- **Dependency Injection**: `db: Session = Depends(get_db)` means that FastAPI will automatically call `get_db()` to provide a `Session` object to this function.
- **Function Body**:
    - `crud.get_users(db, skip=skip, limit=limit)` is a call to a `crud` function that fetches user records from the database with the specified pagination parameters.
    - The result is returned as a JSON response.
- **Response Model**: `response_model=list[schemas.User]` specifies that the response will be a list of `User` Pydantic models, ensuring that the data conforms to the schema defined in `schemas.User`.

### 2. **Create User Endpoint**

```python
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
```

- **Decorator**: `@app.post("/users/")` specifies that this function will handle HTTP POST requests to the `/users/` URL.
- **Parameters**:
    - `user`: The request body, which is expected to be a `UserCreate` Pydantic model. This model includes the data for creating a new user.
    - `db` (injected): A `Session` object provided by the `get_db` dependency.
- **Function Body**:
    - `crud.get_user_by_email(db, email=user.email)` checks if a user with the provided email already exists in the database.
    - If a user is found (`db_user` is not `None`), an HTTP 400 error is raised with a detail message "Email already registered".
    - If no user is found, `crud.create_user(db=db, user=user)` is called to create a new user in the database.
- **Response Model**: `response_model=schemas.User` specifies that the response will be a `User` Pydantic model, representing the created user.

### 3. **Get User by Email Endpoint**

```python
@app.get("/users/{email}", response_model=schemas.User)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
```

- **Decorator**: `@app.get("/users/{email}")` specifies that this function will handle HTTP GET requests to the `/users/{email}` URL, where `{email}` is a path parameter.
- **Parameters**:
    - `email`: The path parameter that specifies the email of the user to retrieve.
    - `db` (injected): A `Session` object provided by the `get_db` dependency.
- **Function Body**:
    - `crud.get_user_by_email(db, email=email)` is called to fetch a user from the database by email.
    - If no user is found (`db_user` is `None`), an HTTP 404 error is raised with a detail message "User not found".
    - If a user is found, it is returned as a JSON response.
- **Response Model**: `response_model=schemas.User` specifies that the response will be a `User` Pydantic model, representing the retrieved user.

### Summary

- **Routes**: Define how different URLs and HTTP methods (GET, POST) are handled.
- **Dependency Injection**: `Depends(get_db)` provides a `Session` object for interacting with the database.
- **Pydantic Models**: Ensure that request and response data conform to the specified schemas.
- **CRUD Operations**: Functions like `crud.get_users`, `crud.get_user_by_email`, and `crud.create_user` handle the actual database interactions.
