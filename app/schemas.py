from datetime import date

from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_id: int
    is_active: bool

    class Config:
        orm_mode = True


class CourseBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    description: str


class CourseCreate(CourseBase):
    pass


class Item(CourseBase):
    course_id: int

    class Config:
        orm_mode = True
