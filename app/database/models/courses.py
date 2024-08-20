from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.database.database import Base


class Course(Base):
    __tablename__ = 'courses'

    course_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, nullable=False, default=True)

    enrollments = relationship('Enrollment', back_populates='course')
