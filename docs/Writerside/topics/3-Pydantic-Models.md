# 3. Pydantic Models

## Objective

Just like in the official [FastAPI docs](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-pydantic-models), to avoid confusion between the SQLAlchemy models and the Pydantic models, we will have the file models.py with the SQLAlchemy models, and the file schemas.py with the Pydantic models.

These Pydantic models define more or less a "schema" (a valid data shape).

So this will help us avoiding confusion while using both.

So a new file `schemas.py` will be created in the `app` directory.

## Pydantic Models

Pydantic models are used to define the structure of the data that will be received and returned by the API.

The general way of creating Pydantic models is to create a class that inherits from `BaseModel` from the `pydantic` module.

That class itself will act as a base class for all the Pydantic models that we will create.

e.g. we create a `UserBase` Pydantic model (or let's say "schema") to have common attributes while creating or reading data.

Then we create a `UserCreate` model that inherits from `UserBase` (so it will have the same attributes), plus any additional data (attributes) needed for creation.

So, the user will also have a password when creating it.

But for security, the password won't be in other Pydantic models, for example, it won't be sent from the API when reading a user.



<code-block lang="python" collapsed-title="schemas.py" collapsible="true">
<![CDATA[
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserTypeBase(BaseModel):
    name: str


class UserTypeCreate(UserTypeBase):
    pass


class UserTypeUpdate(UserTypeBase):
    pass


class UserTypeInDB(UserTypeBase):
    user_type_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    age: Optional[int] = None
    is_active: bool = True


class UserCreate(UserBase):
    hashed_password: str
    user_type_id: int


class UserUpdate(UserBase):
    hashed_password: Optional[str] = None
    user_type_id: Optional[int] = None


class UserInDB(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime
    last_login: datetime

    class Config:
        orm_mode = True


class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    is_active: bool = True


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    pass


class CourseInDB(CourseBase):
    course_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class EnrollmentBase(BaseModel):
    enrolled_date: datetime
    end_date: Optional[datetime] = None
    associative_data: Optional[str] = None
    user_id: int
    course_id: int


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(EnrollmentBase):
    pass


class EnrollmentInDB(EnrollmentBase):
    enrollment_id: int
    updated_at: datetime

    class Config:
        orm_mode = True

]]>
</code-block>