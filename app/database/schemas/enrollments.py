from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, FieldValidationInfo


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
