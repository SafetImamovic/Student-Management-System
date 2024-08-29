from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.user_types_controller import UserTypeController
from app.controllers.users_controller import UserController
from app.database.schemas.users import (
    User as UserSchema,
    UserCreate as UserCreateSchema
)
from app.utils import error_responses, enums

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    '/count/',
    responses={

    },
    response_model=int
)
def get_count(
    controller: Annotated[UserController, Depends(UserController)]
):
    """
    This function returns the number of users in the database
    :param controller: UserController Dependency
    :return: The number of users in the database
    """

    return controller.get_count()


@router.get(
    '/{user_id}',
    responses={

    },
    response_model=UserSchema,
)
def get_by_id(
    user_id: int,
    controller: Annotated[UserController, Depends(UserController)]
):
    """
    This path operation returns a User based on the given id using the crud.get_user_by_id() function
    :param controller:
    :param user_id: The given User id
    :return: The User instance
    """

    return controller.get_by_id(user_id)


@router.get(
    "/email/{email}",
    responses={

    },
    response_model=UserSchema
)
def get_by_email(
    email: str,
    controller: Annotated[UserController, Depends(UserController)]
):
    """
    This path operation returns the user with the given email using the crud.get_user_by_email() function
    :param controller:
    :param email: The email of the user
    :return: The User instance
    """

    return controller.get_by_email(email)


@router.get(
    "/",
    responses={

    },
    response_model=list[UserSchema]
)
def get_all(
    controller: Annotated[UserController, Depends(UserController)],
    user_type_id: int = None,
    skip: int = 0,
    limit: int = 10
):
    """
    Path operation which returns all the users in the database.

    It has skip and limit query parameters.

    It has user_type_id query parameter which returns all users which match that user_type_id.

    :param controller:
    :param user_type_id:
    :param skip:
    :param limit:
    :return:
    """

    return controller.get_all(user_type_id, skip, limit)


@router.post(
    "/",
    responses={

    },
    response_model=UserSchema,
)
def create(
    user: UserCreateSchema,
    controller: Annotated[UserController, Depends(UserController)],
):
    """
    This path operation creates a new user using the crud.create_user() function.
    :param user:
    :param controller:
    :return:
    """

    return controller.create(user=user)


@router.put(
    "/{user_id}",
    responses={

    },
    response_model=UserSchema,
)
def deactivate(
    user_id: int,
    controller: Annotated[UserController, Depends(UserController)]
):
    """
    This path operation performs a deactivation (soft delete) on a user by setting the is_active field to False.
    :param controller:
    :param user_id: The id of the user
    :return: The User instance with is_active set to False
    """

    return controller.deactivate(user_id=user_id)


@router.put(
    "/activate/{user_id}",
    responses={

    },
    response_model=UserSchema,
)
def activate(
    user_id: int,
    controller: Annotated[UserController, Depends(UserController)]
):
    """
    This path operation reactivates a user by setting the is_active field to True.
    :param controller:
    :param user_id: The id of the user
    :return: The reactivated User instance
    """

    return controller.activate(user_id=user_id)
