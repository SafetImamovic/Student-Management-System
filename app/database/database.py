import os

from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

from .check_and_create_db import check_and_create_database

load_dotenv()

db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")
db_user = os.getenv("POSTGRES_USER")
db_pass = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_NAME")

engine: Engine = check_and_create_database(db_user, db_pass, db_host, db_port, db_name)

SessionLocal: Session = sessionmaker(bind=engine)

Base: DeclarativeBase = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
