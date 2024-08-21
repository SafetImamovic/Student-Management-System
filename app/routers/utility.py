from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.database import get_db
from app.utils import seeding

router = APIRouter()


@router.delete('/truncate_db/', tags=["TRUNCATE DATABASE"])
def truncate_db(db: Session = Depends(get_db)):
    truncate_sql = text("truncate user_types, users, courses, enrollments;")
    result = db.execute(truncate_sql)
    db.commit()
    return result


@router.post('/re_seed_db/', tags=["RE-SEED DATABASE"])
def re_seed_database(db: Session = Depends(get_db)):
    """
    This function re-seeds some tables in the database based on the default values
    :param db: The database to re-seed
    :return: The re-seeded database
    """
    seeding.seed(db)

