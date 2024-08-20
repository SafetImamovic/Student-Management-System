from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Enrollment(Base):
    __tablename__ = 'enrollments'

    enrolled_date = Column(Date, default=date)
    end_date = Column(Date, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    associative_data = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False, primary_key=True)

    user = relationship('User', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')
