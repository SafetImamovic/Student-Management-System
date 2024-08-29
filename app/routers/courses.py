from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.controllers.courses_controller import CourseController
from app.database.schemas.courses import (
    Course as CourseSchema,
    CourseCreate as CourseCreateSchema
)
from app.utils import error_responses, enums

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get(
    '/count/',
    responses={

    },
    response_model=int
)
def get_count(
    controller: Annotated[CourseController, Depends(CourseController)]
):
    """
    This function returns the number of courses in the database
    :return: The number of courses in the database
    """

    return controller.get_count()


@router.get(
    '/{course_id}',
    responses={

    },
    response_model=CourseSchema)
def get_by_id(
    course_id: int,
    controller: Annotated[CourseController, Depends(CourseController)]
):
    """
    This path operation returns the course using the crud.get_course_by_id() function
    :param controller:
    :param course_id: The id of the course
    :return: The Course instance
    """

    return controller.get_by_id(course_id)


@router.get(
    '/name/{name}',
    responses={

    },
    response_model=CourseSchema
)
def get_by_name(
    name: str,
    controller: Annotated[CourseController, Depends(CourseController)]
):
    """
    This path operation returns a Course using the crud.get_course_by_name() function
    :param controller:
    :param name: The name of the course
    :return: The Course instance
    """

    return controller.get_by_name(name)


@router.get(
    '/',
    responses={

    },
    response_model=list[CourseSchema]
)
def get_all(
    controller: Annotated[CourseController, Depends(CourseController)],
    skip: int = 0,
    limit: int = 10,
):
    """
    This path operation returns a list of courses using the crud.get_courses() function
    :param controller:
    :param skip: The number of items to skip at the beginning of the list
    :param limit: The maximum number of items to return
    :return: The list of Courses
    """

    return controller.get_all(skip=skip, limit=limit)


@router.post(
    '/',
    responses={

    },
    response_model=CourseSchema
)
def create(
    course: CourseCreateSchema,
    controller: Annotated[CourseController, Depends(CourseController)]
):
    """
    This path operation creates a new course using the crud.create_course() function.
    :param controller:
    :param course: schemas.CourseCreate
    :return: Created Course instance.
    """

    return controller.create(course)


@router.put(
    "/{course_id}",
    responses={

    },
    response_model=CourseSchema
)
def deactivate(
    course_id: int,
    controller: Annotated[CourseController, Depends(CourseController)]
):
    """
    This path operation performs a deactivation (soft delete) on a course by setting the is_active field to False.
    :param controller:
    :param course_id: The id of the course
    :return: The Course instance with is_active set to False
    """

    return controller.deactivate(course_id)


@router.put(
    "/activate/{course_id}",
    response_model=CourseSchema
)
def activate(
    course_id: int,
    controller: Annotated[CourseController, Depends(CourseController)]
):
    """
    This path operation reactivates a course by setting the is_active field to True.
    :param controller:
    :param course_id: The id of the course
    :return: The reactivated Course instance
    """

    return controller.activate(course_id)
