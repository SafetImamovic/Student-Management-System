from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.database.schemas.enrollments as schemas
from app.controllers import users_controller, courses_controller, enrollments_controller
from app.database.database import get_db
from app.utils import error_responses, enums

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.get('/count/', response_model=int)
def get_enrollments_count(db: Session = Depends(get_db)):
    """
    This function returns the number of enrollments in the database
    :param db: The database session to use
    :return: The number of enrollments in the database
    """
    return enrollments_controller.get_enrollments_count(db)


@router.get('/{user_id}/{course_id}', response_model=schemas.Enrollment)
def get_enrollment_by_ids(user_id: int, course_id: int, db: Session = Depends(get_db)):
    """
    This path operation returns an Enrollment based on the user_id and course_id composite key
    :param user_id: The user id
    :param course_id: The course id
    :param db: The database session to use
    :return: The Enrollment instance
    """
    db_enrollment = enrollments_controller.get_enrollment_by_ids(db, user_id=user_id, course_id=course_id)

    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    return db_enrollment


@router.get('/', response_model=list[schemas.Enrollment])
def get_enrollments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    This path operation returns a list of Enrollments using the crud.get_enrollments() function
    :param skip: The number of items to skip at the beginning of the list
    :param limit: The maximum number of items to return
    :param db: The database session to use
    :return: The list of Enrollments
    """
    db_enrollments = enrollments_controller.get_enrollments(db, skip=skip, limit=limit)

    return db_enrollments


@router.post('/', response_model=schemas.Enrollment)
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    """
    This path operation creates an Enrollment using the crud.create_enrollment() function
    :param enrollment: schemas.EnrollmentCreate
    :param db: The database session to use
    :return: The Enrollment instance
    """
    errors = []

    db_exists = enrollments_controller.get_enrollment_by_ids(db, user_id=enrollment.user_id, course_id=enrollment.course_id)
    if db_exists:
        error_responses.add_error(
            errors=errors,
            loc=[enums.Location.BODY, "user_id", "course_id"],
            msg="Enrollment already exists"
        )

    db_user = users_controller.get_user_by_id(db, user_id=enrollment.user_id)
    if not db_user:
        error_responses.add_error(
            errors=errors,
            loc=[enums.Location.BODY, "user_id"],
            msg=f"User not found for User ID: {enrollment.user_id}"
        )

    db_course = courses_controller.get_course_by_id(db, course_id=enrollment.course_id)
    if not db_course:
        error_responses.add_error(
            errors=errors,
            loc=[enums.Location.BODY, "course_id"],
            msg=f"Course not found for Course ID: {enrollment.course_id}"
        )

    if errors:
        return error_responses.pydantic_error_response(errors)

    db_enrollment = enrollments_controller.create_enrollment(db, enrollment)
    return db_enrollment
