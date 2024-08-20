from sqlalchemy.orm import Session
from app.database.models import enrollments as models
from app.database.schemas import enrollments as schemas


def get_enrollment_by_ids(db: Session, user_id: int, course_id: int) -> models.Enrollment:
    """
    This function returns the Enrollment based on the given user_id and course_id composite key
    :param user_id: The user id
    :param course_id: The given course_id
    :return: Enrollment based on the given user_id and course_id composite key
    """
    db_enrollment = db.query(models.Enrollment).filter(models.Enrollment.user_id == user_id,
                                                         models.Enrollment.course_id == course_id).first()

    return db_enrollment


def get_enrollments(db: Session, skip: int = 0, limit: int = 10) -> list[models.Enrollment]:
    """
    This function queries the models for the Enrollment with the given skip and limit boundaries
    and returns a list of Enrollments
    :param db: The models session
    :param skip: The starting index of the list, 0 by default
    :param limit: The ending index (skip + limit), 10 by default
    :return: List[models.Enrollment]:
    """
    return db.query(models.Enrollment).offset(skip).limit(limit).all()


def create_enrollment(db: Session, enrollment: schemas.EnrollmentCreate) -> models.Enrollment:
    """
    This function creates a new Enrollment based on the given enrollment pydantic model
    :param db: The models session
    :param enrollment: The given enrollment pydantic model
    :return: Created Enrollment instance
    """
    db_enrollment = models.Enrollment(**enrollment.dict())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


def delete_enrollment(db: Session, enrollment_id: int) -> models.Enrollment:
    """
    This function deletes a Enrollment based on the given enrollment_id
    :param db: The models session
    :param enrollment_id: The given enrollment_id
    :return: The deleted Enrollment instance
    """
    db_enrollment = db.query(models.Enrollment).filter(models.Enrollment.enrollment_id == enrollment_id).first()
    db.delete(db_enrollment)
    db.commit()
    return db_enrollment
