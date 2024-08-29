from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

import app.database.schemas.enrollments as schemas
from app.controllers.courses_controller import CourseController
from app.controllers.enrollments_controller import EnrollmentController
from app.controllers.users_controller import UserController
from app.utils import error_responses, enums
from app.database.schemas.enrollments import Enrollment

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

    return controller.get_by_id(user_id, course_id)


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

    return controller.get_all(skip=skip, limit=limit)


@router.post(
    '/',
    response_model=schemas.Enrollment
)
def create(
    enrollment: schemas.EnrollmentCreate,
    controller: Annotated[EnrollmentController, Depends(EnrollmentController)]
):
    """
    This path operation creates an Enrollment using the crud.create_enrollment() function
    :param enrollment:
    :param controller:
    :return:
    """

    return controller.create(enrollment)


@router.delete(
    '/{user_id}/{course_id}',
    response_model=schemas.Enrollment
)
def delete(
    user_id: int,
    course_id: int,
    controller: Annotated[EnrollmentController, Depends(EnrollmentController)]
) -> Enrollment:
    """
    This path operation deletes an Enrollment based on the user_id and course_id composite key
    :param user_id:
    :param course_id:
    :param controller:
    :return:
    """

    return controller.delete(user_id, course_id)
