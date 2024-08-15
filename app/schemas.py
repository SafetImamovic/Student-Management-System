from typing import Optional
from pydantic import BaseModel
from datetime import datetime


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


class UserCreate(UserBase):
    password: str
    user_type_id: int


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
    start_date: datetime
    end_date: datetime
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
    enrolled_date: datetime
    end_date: Optional[datetime] = None
    associative_data: Optional[str] = None
    user_id: int
    course_id: int


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(EnrollmentBase):
    pass


class Enrollment(EnrollmentBase):
    enrollment_id: int
    updated_at: datetime

    class Config:
        orm_mode = True
