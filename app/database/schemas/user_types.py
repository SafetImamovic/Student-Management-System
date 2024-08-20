from datetime import datetime

from pydantic import BaseModel, Field


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
