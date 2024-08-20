# 5. Path Operations

## Description

Path operations are the functions that FastAPI will call when it receives a request to a specific path (like `/items/{item_id}`), with a specific HTTP method (like `GET`).

These functions will call the different CRUD functions to interact with the database and return the necessary responses.

It can also include additional logic to process the request, validate data, and handle errors.

## Validation

It is important to note the format of the JSON Error response Pydantic generates when a validation error occurs. This is the default error response format when a request fails validation:

```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

So e.g. when creating a Course with the end date being older than the start date:

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": [
        "body",
        "end_date"
      ],
      "msg": "Value error, End date must be later than the start date",
      "input": "2024-08-09",
      "ctx": {
        "error": {}
      }
    }
  ]
}
```

This is important to note because when implementing custom validation inside the path operations, the way we
raise HTTP errors will impact how the response is parsed by the client.

If we follow the same structure as Pydantic, it will be easier for the client to handle the error responses consistently.

This is why a custom utility function in `main.py` is defined:

```Python
def pydantic_error_response(errors: list):
    """Utility function to create a Pydantic-style error response with accumulated errors"""
    return JSONResponse(
        status_code=422,
        content={
            "detail": errors
        }
    )
```


## Example for Creating an Enrollment
Before Pydantic style error response:
```Python
@app.post('/enrollments/', response_model=schemas.Enrollment, tags=["Enrollments"])
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    """
    This path operation creates an Enrollment using the crud.create_enrollment() function
    :param enrollment: schemas.EnrollmentCreate
    :param db: The database session to use
    :return: The Enrollment instance
    """
    db_exists = crud.get_enrollment_by_ids(db, user_id=enrollment.user_id, course_id=enrollment.course_id)

    if db_exists:
        raise HTTPException(status_code=400, detail="Enrollment already exists")

    db_user = crud.get_user_by_id(db, user_id=enrollment.user_id)
    db_course = crud.get_course_by_id(db, course_id=enrollment.course_id)

    if not db_course and not db_user:
        raise HTTPException(status_code=404,
                            detail=f"Course and User not found for Course ID: {enrollment.course_id} and User ID: {enrollment.user_id}")

    if not db_user and db_course:
        raise HTTPException(status_code=404, detail=f"User not found for User ID: {enrollment.user_id}")

    if not db_course and db_user:
        raise HTTPException(status_code=404, detail=f"Course not found for Course ID: {enrollment.course_id}")

    db_enrollment = crud.create_enrollment(db, enrollment)

    return db_enrollment
```

After:
```Python
@app.post('/enrollments/', response_model=schemas.Enrollment, tags=["Enrollments"])
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
"""
This path operation creates an Enrollment using the crud.create_enrollment() function
:param enrollment: schemas.EnrollmentCreate
:param db: The database session to use
:return: The Enrollment instance
"""
db_exists = crud.get_enrollment_by_ids(db, user_id=enrollment.user_id, course_id=enrollment.course_id)

    if db_exists:
        return pydantic_error_response(
            loc=["body", "user_id", "course_id"],
            msg="Enrollment already exists"
        )

    db_user = crud.get_user_by_id(db, user_id=enrollment.user_id)
    db_course = crud.get_course_by_id(db, course_id=enrollment.course_id)

    if not db_user:
        return pydantic_error_response(
            loc=["body", "user_id"],
            msg=f"User not found for User ID: {enrollment.user_id}"
        )

    if not db_course:
        return pydantic_error_response(
            loc=["body", "course_id"],
            msg=f"Course not found for Course ID: {enrollment.course_id}"
        )

    db_enrollment = crud.create_enrollment(db, enrollment)
    return db_enrollment
```


## Creating a Database Session
   ```python
   db = SessionLocal()
   ```
   Here, `SessionLocal` is typically a factory function or class that creates a new database session. This session object is used to interact with the database. `SessionLocal` is often defined using SQLAlchemy's `sessionmaker` function and is used to create a new session instance.


   ```python
   try:
       yield db
   ```

- `yield db` is used to return the `db` session object to whatever part of the code is requesting it. In the context of FastAPI, this allows dependency injection to provide the `db` session to route handlers or other functions.
- The `yield` statement here is used to produce a value and pause the function, allowing the caller to use the database session (`db`). This pattern is known as a generator function in Python.


   ```python
   finally:
       db.close()
   ```
- The `finally` block ensures that the `db.close()` method is called after the `yield` statement, no matter what happens (whether an exception occurs or not). This is important for releasing database resources and closing the connection properly.
- `db.close()` is used to close the database session, freeing up any resources associated with it.

Certainly! Here's a detailed breakdown of each route in this FastAPI application:


## User Specific Endpoints

Here’s a detailed explanation of each of the provided endpoints:

### 1. **Get Users Count Endpoint**

```python
@app.get('/users/count/', response_model=int, tags=["Users"])
def get_users_count(db: Session = Depends(get_db)):
    """
    This function returns the number of users in the database.
    :param db: The database session to use.
    :return: The number of users in the database.
    """
    return db.query(models.User).count()
```

- **Decorator**: `@app.get('/users_count/')` specifies that this function handles HTTP GET requests to the `/users_count/` URL.
- **Parameters**:
    - `db` (injected): A `Session` object provided by the `get_db` dependency.
- **Function Body**:
    - `db.query(models.User).count()` queries the database to count the number of `User` records.
- **Response Model**: `response_model=int` specifies that the response will be an integer representing the count of users.

### 2. **Get User by ID Endpoint**

```python
@app.get('/users/{user_id}', response_model=schemas.User, tags=["Users"])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    This path operation returns a User based on the given ID using the crud.get_user_by_id() function.
    :param user_id: The given User ID.
    :param db: The database session to use.
    :return: The User instance.
    """
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
```

- **Decorator**: `@app.get('/users/{user_id}')` specifies that this function handles HTTP GET requests to the `/users/{user_id}` URL, where `{user_id}` is a path parameter.
- **Parameters**:
    - `user_id`: The path parameter specifying the ID of the user to retrieve.
    - `db` (injected): A `Session` object provided by the `get_db` dependency.
- **Function Body**:
    - `crud.get_user_by_id(db, user_id=user_id)` retrieves a user from the database by ID.
    - If the user is not found (`db_user` is `None`), an HTTP 404 error is raised with the message "User not found".
    - If found, the user instance is returned.
- **Response Model**: `response_model=schemas.User` specifies that the response will be a `User` Pydantic model.

### 3. **Get User by Email Endpoint**

```python
@app.get("/users/email/{email}", response_model=schemas.User, tags=["Users"])
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """
    This path operation returns the user with the given email using the crud.get_user_by_email() function.
    :param email: The email of the user.
    :param db: The database session to use.
    :return: The User instance.
    """
    db_user = crud.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
```

- **Decorator**: `@app.get("/users/email/{email}")` specifies that this function handles HTTP GET requests to the `/users/email/{email}` URL, where `{email}` is a path parameter.
- **Parameters**:
    - `email`: The path parameter specifying the email of the user to retrieve.
    - `db` (injected): A `Session` object provided by the `get_db` dependency.
- **Function Body**:
    - `crud.get_user_by_email(db, email=email)` retrieves a user from the database by email.
    - If the user is not found (`db_user` is `None`), an HTTP 404 error is raised with the message "User not found".
    - If found, the user instance is returned.
- **Response Model**: `response_model=schemas.User` specifies that the response will be a `User` Pydantic model.

### 4. **Read Users Endpoint**

```python
@app.get("/users/", response_model=list[schemas.User], tags=["Users"])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    This path operation returns a list of users using the crud.get_users() function.
    :param skip: The number of items to skip at the beginning of the list.
    :param limit: The maximum number of items to return.
    :param db: The database session to use.
    :return: The list of users.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
```

- **Decorator**: `@app.get("/users/")` specifies that this function handles HTTP GET requests to the `/users/` URL.
- **Parameters**:
    - `skip`: The number of users to skip, defaulting to 0.
    - `limit`: The maximum number of users to return, defaulting to 10.
    - `db` (injected): A `Session` object provided by the `get_db` dependency.
- **Function Body**:
    - `crud.get_users(db, skip=skip, limit=limit)` retrieves a list of users from the database with pagination.
    - The list of users is returned.
- **Response Model**: `response_model=list[schemas.User]` specifies that the response will be a list of `User` Pydantic models.

### 5. **Create User Endpoint**

```python
@app.post("/users/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    This path operation creates a new user using the crud.create_user() function.
    :param user: schemas.UserCreate
    :param db: The database session to use.
    :return: Created User instance.
    """
    errors = []

    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        add_error(
            errors=errors,
            loc=[Location.BODY, "email"],
            msg="Email already registered"
        )

    if crud.get_user_type_by_id(db, user.user_type_id) is None:
        add_error(
            errors=errors,
            loc=[Location.BODY, "user_type_id"],
            msg="User Type doesn't exist"
        )

    if errors:
        return pydantic_error_response(errors)

    return crud.create_user(db=db, user=user)
```

- **Decorator**: `@app.post("/users/")` specifies that this function handles HTTP POST requests to the `/users/` URL.
- **Parameters**:
    - `user`: The request body, which is expected to be a `UserCreate` Pydantic model.
    - `db` (injected): A `Session` object provided by the `get_db` dependency.
- **Function Body**:
    - `crud.get_user_by_email(db, email=user.email)` checks if a user with the provided email already exists.
    - If a user is found (`db_user` is not `None`), an error is added to the list.
    - `crud.get_user_type_by_id(db, user.user_type_id)` checks if the provided user type ID exists.
    - If the user type ID does not exist, an error is added to the list.
    - If there are any accumulated errors, a structured Pydantic-style error response is returned.
    - If no errors, the new user is created and returned.
- **Response Model**: `response_model=schemas.User` specifies that the response will be a `User` Pydantic model representing the created user.


Here’s the updated documentation based on the new soft delete mechanic for users:

### 6. **Soft Delete User Endpoint**

```python
@app.delete("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    This path operation performs a soft delete on a user by setting the is_active field to False.
    :param user_id: The ID of the user to soft delete.
    :param db: The database session to use.
    :return: The User instance with is_active set to False.
    """
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user = crud.soft_delete_user(db, user_id=user_id)

    return db_user
```

- **Decorator**: `@app.delete("/users/{user_id}")` specifies that this function handles HTTP DELETE requests to the `/users/{user_id}` URL.
- **Parameters**:
  - `user_id`: The path parameter specifying the ID of the user to soft delete.
  - `db` (injected): A `Session` object provided by the `get_db` dependency.
- **Function Body**:
  - `crud.get_user_by_id(db, user_id=user_id)` retrieves the user from the database by ID.
  - If the user is not found (`db_user` is `None`), an HTTP 404 error is raised with the message "User not found".
  - If found, the user is soft deleted by setting the `is_active` field to `False` using `crud.soft_delete_user(db, user_id=user_id)`.
  - The updated user instance is returned with the `is_active` field set to `False`.
- **Response Model**: `response_model=schemas.User` specifies that the response will be a `User` Pydantic model representing the soft-deleted user.