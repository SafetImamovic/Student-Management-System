# 3. Pydantic Models

## Objective

Just like in the official [FastAPI docs](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-pydantic-models), to avoid confusion between the SQLAlchemy models and the Pydantic models, we will have the file models.py with the SQLAlchemy models, and the file schemas.py with the Pydantic models.

These Pydantic models define more or less a "schema" (a valid data shape).

So this will help us avoiding confusion while using both.

So a new file `schemas.py` will be created in the `app` directory.

## Pydantic Models

Create an StudentBase, CourseBase and EnrollmentBase Pydantic schemas to have common attributes while creating or reading data.

And create an StudentCreate, CourseCreate and EnrollmentCreate that inherit from them (so they will have the same attributes), plus any additional data (attributes) needed for creation.

So, the student will also have a password when creating it.

But for security, the password won't be in other Pydantic schemas, for example, it won't be sent from the API when reading a student.

The `schemas.py` file will contain the Pydantic models for the students, courses and enrollments data.



```Python
from pydantic import BaseModel


```