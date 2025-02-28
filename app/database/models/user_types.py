from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class UserType(Base):
    __tablename__ = 'user_types'

    user_type_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    name = Column(String(50), nullable=False, unique=True)

    users = relationship('User', back_populates='user_type')
