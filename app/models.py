import datetime
from sqlalchemy import Column, Integer, DateTime, String
from .database import Base


class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
