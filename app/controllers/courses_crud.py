from sqlalchemy.orm import Session
from app import models, schemas


def get_course_by_id(db: Session, course_id: int) -> models.Course:
    """
    This function queries the database for the Course with the given course_id
    and returns the Course with the given course_id
    :param db: The database session
    :param course_id: Pydantic Course model
    :return: Course with the given course_id
    """
    return db.query(models.Course).filter(models.Course.course_id == course_id).first()


def get_course_by_name(db: Session, name: str) -> models.Course:
    """
    This function queries the database for the Course with the given name
    :param db: The database session
    :param name: Course name
    :return: Course with given name
    """
    return db.query(models.Course).filter(models.Course.name == name).first()


def get_courses(db: Session, skip: int = 0, limit: int = 10) -> list[models.Course]:
    """
    This function queries the database for the Course with the given skip and limit boundaries
    and returns a list of Courses
    :param db: The database session
    :param skip: The starting index of the list, 0 by default
    :param limit: The ending index (skip + limit), 10 by default
    :return: List[Type[models.Course]]:
    """
    return db.query(models.Course).offset(skip).limit(limit).all()


def create_course(db: Session, course: schemas.CourseCreate) -> models.Course:
    """
    This function creates a new Course based on the given course pydantic model
    :param db: The database session
    :param course: Pydantic Course model
    :return: Created Course
    """
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def deactivate_course(db: Session, course_id: int):
    db_course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if db_course:
        db_course.is_active = False
        db.commit()
        db.refresh(db_course)
    return db_course


def activate_course(db: Session, course_id: int):
    db_course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if db_course:
        db_course.is_active = True
        db.commit()
        db.refresh(db_course)
    return db_course