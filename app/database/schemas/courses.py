from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, FieldValidationInfo


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
