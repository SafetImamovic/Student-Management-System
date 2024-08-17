from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date


class UserTypeBase(BaseModel):
    name: str


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
    first_name: str
    last_name: str
    username: str
    email: str
    age: Optional[int] = None
    is_active: bool = True
    user_type_id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    hashed_password: Optional[str] = None
    user_type_id: Optional[int] = None


class User(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime
    last_login: datetime

    class Config:
        orm_mode = True


class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    is_active: bool = True


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    pass


class Course(CourseBase):
    course_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class EnrollmentBase(BaseModel):
    enrolled_date: date
    end_date: Optional[date] = None
    associative_data: Optional[str] = None
    user_id: int
    course_id: int


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(EnrollmentBase):
    pass


class Enrollment(EnrollmentBase):
    updated_at: datetime

    class Config:
        orm_mode = True
