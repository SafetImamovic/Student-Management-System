from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.controllers.user_types_controller import UserTypeController
from app.database.schemas.user_types import (
    UserType as UserTypeSchema,
    UserTypeCreate as UserTypeCreateSchema
)
from app.utils import error_responses, enums

router = APIRouter(prefix="/user_types", tags=["User Types"])


@router.get(
    '/count/',
    responses={

    },
    response_model=int
)
def get_count(
    controller: Annotated[UserTypeController, Depends(UserTypeController)]
):
    """
    This function returns the number of user types in the database
    :param controller:
    :return:
    """

    return controller.get_count()


@router.get(
    '/{user_type_id}',
    responses={

    },
    response_model=UserTypeSchema)
def get_by_id(
    user_type_id: int,
    controller: Annotated[UserTypeController, Depends(UserTypeController)]
):
    """
    This path operation returns one UserType using the crud.get_user_type_by_id() function
    :param controller:
    :param user_type_id: The id of the user type
    :return: The UserType instance
    """

    return controller.get_by_id(user_type_id)


@router.get(
    '/name/{name}',
    responses={

    },
    response_model=UserTypeSchema
)
def get_by_name(
    name: str,
    controller: Annotated[UserTypeController, Depends(UserTypeController)]
):
    """
    This path operation returns one UserType using the crud.get_user_type_by_name() function
    :param controller:
    :param name: The name of the user type

    :return: The UserType instance
    """

    return controller.get_by_name(name)


@router.get(
    '/',
    responses={

    },
    response_model=list[UserTypeSchema]
)
def get_all(
    controller: Annotated[UserTypeController, Depends(UserTypeController)],
    skip: int = 0,
    limit: int = 10
):
    """
    This path operation returns a list of user types using the crud.get_user_types() function
    :param controller:
    :param skip: The number of items to skip at the beginning of the list
    :param limit: The maximum number of items to return
    :return: The list of user types
    """

    return controller.get_all(skip=skip, limit=limit)


@router.post(
    '/',
    response_model=UserTypeSchema,
    status_code=status.HTTP_201_CREATED
)
def create(
    user_type: UserTypeCreateSchema,
    controller: Annotated[UserTypeController, Depends(UserTypeController)]
):
    """
    This path operation creates a new user type using the crud.create_user_type() function.
    :param controller:
    :param user_type: The schemas.UserTypeCreate instance.
    :return: The created user type.
    """

    return controller.create(user_type)


@router.delete(
    '/{user_type_id}',
    responses={

    },
    response_model=UserTypeSchema
)
def delete(
    user_type_id: int,
    controller: Annotated[UserTypeController, Depends(UserTypeController)]
) -> UserTypeSchema:
    """
    This path operation deletes a user type using the crud.delete_user_type() function
    :param controller:
    :param user_type_id: The id of the user type
    :return: Deleted user type
    """

    return controller.delete(user_type_id=user_type_id)
