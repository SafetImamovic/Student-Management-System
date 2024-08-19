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
from pydantic import BaseModel, EmailStr, Field, validator, field_validator, FieldValidationInfo
from datetime import datetime, date


class UserTypeBase(BaseModel):
name: str = Field(..., min_length=3, max_length=50)


class UserTypeCreate(UserTypeBase):
pass


class UserTypeUpdate(UserTypeBase):
pass


class UserType(UserTypeBase):
user_type_id: int
created_at: datetime
updated_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
first_name: str = Field(..., min_length=1, max_length=50)
last_name: str = Field(..., min_length=1, max_length=50)
username: str = Field(..., min_length=1, max_length=50)
email: EmailStr
age: Optional[int] = Field(None, gt=0)
is_active: bool = True
user_type_id: int


class UserCreate(UserBase):
password: str = Field(..., min_length=6)


class UserUpdate(UserBase):
hashed_password: Optional[str] = Field(None, min_length=6)
user_type_id: Optional[int] = None


class User(UserBase):
user_id: int
created_at: datetime
updated_at: datetime
last_login: Optional[datetime]

    class Config:
        orm_mode = True


class CourseBase(BaseModel):
name: str = Field(..., min_length=3, max_length=100)
description: Optional[str] = Field(None, max_length=255)
start_date: date
end_date: date
is_active: bool = True

    @field_validator('end_date')
    def validate_date_range(cls, end_date, info: FieldValidationInfo):
        start_date = info.data.get('start_date')
        if start_date and end_date < start_date:
            raise ValueError('End date must be later than the start date')
        return end_date

    # @validator('end_date')
    # def validate_date_range(cls, end_date, values):
    #     start_date = values.get('start_date')
    #     if start_date and end_date < start_date:
    #         raise ValueError('End date must be later than the start date')
    #     return end_date


class CourseCreate(CourseBase):
pass


class CourseUpdate(CourseBase):
name: Optional[str] = Field(None, min_length=3, max_length=100)
start_date: Optional[date] = None
end_date: Optional[date] = None


class Course(CourseBase):
course_id: int
created_at: datetime
updated_at: datetime

    class Config:
        orm_mode = True


class EnrollmentBase(BaseModel):
enrolled_date: date
end_date: Optional[date] = None
associative_data: Optional[str] = Field(None, max_length=255)
user_id: int
course_id: int

    @field_validator('end_date')
    def validate_date_range(cls, end_date: date, info: FieldValidationInfo) -> date:
        enrolled_date = info.data.get('enrolled_date')
        if end_date < enrolled_date:
            raise ValueError('End date must be later than the enrolled date')
        return end_date

    # @validator('end_date')
    # def validate_end_date(cls, end_date, values):
    #     enrolled_date = values.get('enrolled_date')
    #     if end_date < enrolled_date:
    #         raise ValueError('End date must be later than the enrolled date')
    #     return end_date


class EnrollmentCreate(EnrollmentBase):
pass


class EnrollmentUpdate(EnrollmentBase):
enrolled_date: Optional[date] = None
end_date: Optional[date] = None
associative_data: Optional[str] = Field(None, max_length=255)
user_id: Optional[int] = None
course_id: Optional[int] = None


class Enrollment(EnrollmentBase):
updated_at: datetime

    class Config:
        orm_mode = True


]]>
</code-block>


Here's a breakdown of the schema:

### 1. **UserType Models**
- **`UserTypeBase`**:
    - The base model for user types. It contains a `name` field that must be a string with a length between 3 and 50 characters.
- **`UserTypeCreate` and `UserTypeUpdate`**:
    - These models inherit from `UserTypeBase`. They don't add any new fields, but they're useful for separating concerns (e.g., different validations or operations during creation and updates).
- **`UserType`**:
    - Inherits from `UserTypeBase` and adds additional fields like `user_type_id`, `created_at`, and `updated_at`.
    - `orm_mode = True` in the `Config` class indicates that this model can be used with ORM (Object-Relational Mapping) objects, enabling seamless conversion between database records and Pydantic models.

### 2. **User Models**
- **`UserBase`**:
    - The base model for users, containing fields like `first_name`, `last_name`, `username`, `email`, `age`, `is_active`, and `user_type_id`.
    - `EmailStr` ensures that the `email` field contains a valid email address.
    - The `age` field is optional (`Optional[int]`), and if provided, it must be greater than 0.
- **`UserCreate`**:
    - Extends `UserBase` and adds a `password` field, which must be at least 6 characters long.
- **`UserUpdate`**:
    - Extends `UserBase` and adds an optional `hashed_password` and makes `user_type_id` optional.
- **`User`**:
    - Inherits from `UserBase` and adds fields like `user_id`, `created_at`, `updated_at`, and `last_login`.
    - `orm_mode = True` enables this model to work seamlessly with ORM objects.

### 3. **Course Models**
- **`CourseBase`**:
    - The base model for courses, containing fields like `name`, `description`, `start_date`, `end_date`, and `is_active`.
    - It includes a custom validator (`@field_validator('end_date')`) to ensure that `end_date` is not earlier than `start_date`.
- **`CourseCreate` and `CourseUpdate`**:
    - `CourseCreate` inherits directly from `CourseBase`.
    - `CourseUpdate` makes some fields optional, allowing for partial updates of the course data.
- **`Course`**:
    - Inherits from `CourseBase` and adds fields like `course_id`, `created_at`, and `updated_at`.
    - `orm_mode = True` is set for ORM compatibility.

### 4. **Enrollment Models**
- **`EnrollmentBase`**:
    - The base model for enrollments, containing fields like `enrolled_date`, `end_date`, `associative_data`, `user_id`, and `course_id`.
    - It includes a custom validator (`@field_validator('end_date')`) to ensure that `end_date` is not earlier than `enrolled_date`.
- **`EnrollmentCreate` and `EnrollmentUpdate`**:
    - `EnrollmentCreate` inherits from `EnrollmentBase`.
    - `EnrollmentUpdate` makes several fields optional, allowing for partial updates of enrollment data.
- **`Enrollment`**:
    - Inherits from `EnrollmentBase` and adds an `updated_at` field.
    - `orm_mode = True` is set for ORM compatibility.

### 5. **Validators**
- **`@field_validator`**:
    - Used in `CourseBase` and `EnrollmentBase` to enforce rules on specific fields (`end_date` in this case).
    - It checks that the `end_date` is not earlier than another related date field (`start_date` or `enrolled_date`).
- **`@validator`**:
    - An alternative to `@field_validator`, shown here in commented-out form. This older version of validation uses a different syntax (`values` dictionary) but performs similar tasks. The newer `@field_validator` is preferred in Pydantic v1.10 and later.

