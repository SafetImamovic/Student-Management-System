from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


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
