from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
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

    @validator('end_date')
    def validate_date_range(cls, end_date, values):
        start_date = values.get('start_date')
        if start_date and end_date < start_date:
            raise ValueError('End date must be later than the start date')
        return end_date


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

    @validator('end_date')
    def validate_end_date(cls, end_date, values):
        enrolled_date = values.get('enrolled_date')
        if enrolled_date and end_date and end_date < enrolled_date:
            raise ValueError('End date must be later than the enrolled date')
        return end_date


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
