from datetime import datetime

from sqlalchemy import Column, Integer, String, CheckConstraint, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.database import Base


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
