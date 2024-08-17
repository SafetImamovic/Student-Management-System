from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Date, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base


class UserType(Base):
    __tablename__ = 'user_types'

    user_type_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    name = Column(String(50), nullable=False, unique=True)

    users = relationship('User', back_populates='user_type')


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    age = Column(Integer, CheckConstraint('age > 0'), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_type_id = Column(Integer, ForeignKey('user_types.user_type_id'), nullable=False)

    user_type = relationship('UserType', back_populates='users')
    enrollments = relationship('Enrollment', back_populates='user')

    __table_args__ = (
        UniqueConstraint('email', name='uq_users_email'),
    )


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
