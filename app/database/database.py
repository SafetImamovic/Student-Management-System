import os
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from dotenv import load_dotenv
from .check_and_create_db import check_and_create_database

load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_NAME")

engine: Engine = check_and_create_database(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)

SessionLocal: Session = sessionmaker(bind=engine)

Base: DeclarativeBase = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
