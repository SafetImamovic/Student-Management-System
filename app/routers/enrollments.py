from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

import app.database.schemas.enrollments as schemas
from app.controllers.courses_controller import CourseController
from app.controllers.enrollments_controller import EnrollmentController
from app.controllers.users_controller import UserController
from app.utils import error_responses, enums

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.get(
    '/count/',
    responses={

    },
    response_model=int
)
def get_count(
    controller: Annotated[EnrollmentController, Depends(EnrollmentController)]
):
    """
    This function returns the number of enrollments in the database
    :return: The number of enrollments in the database
    """

    return controller.get_count()


@router.get(
    '/{user_id}/{course_id}',
    responses={

    },
    response_model=schemas.Enrollment)
def get_by_id(
    user_id: int,
    course_id: int,
    controller: Annotated[EnrollmentController, Depends(EnrollmentController)]
):
    """
    This path operation returns an Enrollment based on the user_id and course_id composite key
    :param controller:
    :param user_id: The user id
    :param course_id: The course id
    :return: The Enrollment instance
    """

    db_enrollment = controller.get_by_id(user_id=user_id, course_id=course_id)

    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    return db_enrollment


@router.get(
    '/',
    responses={

    },
    response_model=list[schemas.Enrollment])
def get_all(
    controller: Annotated[EnrollmentController, Depends(EnrollmentController)],
    skip: int = 0,
    limit: int = 10
):
    """
    This path operation returns a list of Enrollments using the crud.get_enrollments() function
    :param controller:
    :param skip: The number of items to skip at the beginning of the list
    :param limit: The maximum number of items to return
    :return: The list of Enrollments
    """

    db_enrollments = controller.get_all(skip=skip, limit=limit)

    return db_enrollments


@router.post(
    '/',
    response_model=schemas.Enrollment
)
def create(
    enrollment: schemas.EnrollmentCreate,
    user_controller: Annotated[UserController, Depends(UserController)],
    course_controller: Annotated[CourseController, Depends(CourseController)],
    enrollment_controller: Annotated[EnrollmentController, Depends(EnrollmentController)]
):
    """
    This path operation creates an Enrollment using the crud.create_enrollment() function
    :param enrollment_controller:
    :param course_controller:
    :param user_controller:
    :param enrollment: schemas.EnrollmentCreate
    :return: The Enrollment instance
    """

    errors = []

    db_exists = enrollment_controller.get_by_id(user_id=enrollment.user_id, course_id=enrollment.course_id)

    if db_exists:
        error_responses.add_error(
            errors=errors,
            loc=[enums.Location.BODY, "user_id", "course_id"],
            msg="Enrollment already exists"
        )

    db_user = user_controller.get_by_id(user_id=enrollment.user_id)

    if not db_user:
        error_responses.add_error(
            errors=errors,
            loc=[enums.Location.BODY, "user_id"],
            msg=f"User not found for User ID: {enrollment.user_id}"
        )

    db_course = course_controller.get_by_id(course_id=enrollment.course_id)

    if not db_course:
        error_responses.add_error(
            errors=errors,
            loc=[enums.Location.BODY, "course_id"],
            msg=f"Course not found for Course ID: {enrollment.course_id}"
        )

    if errors:
        return error_responses.pydantic_error_response(errors)

    db_enrollment = enrollment_controller.create(enrollment)

    return db_enrollment
