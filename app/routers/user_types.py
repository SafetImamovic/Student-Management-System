from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

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
def get_all(
    user_type_id: int,
    controller: Annotated[UserTypeController, Depends(UserTypeController)]
):
    """
    This path operation returns one UserType using the crud.get_user_type_by_id() function
    :param controller:
    :param user_type_id: The id of the user type
    :return: The UserType instance
    """

    db_user_type = controller.get_by_id(user_type_id=user_type_id)

    if not db_user_type:
        raise HTTPException(status_code=404, detail="User Type not found")

    return db_user_type


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

    db_user_type = controller.get_by_name(name=name)

    if not db_user_type:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user_type


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

    user_types = controller.get_all(skip=skip, limit=limit)

    return user_types


@router.post(
    '/',
    response_model=UserTypeSchema
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

    errors = []

    db_user_type = controller.get_by_name(name=user_type.name)

    if db_user_type:
        error_responses.add_error(
            errors=errors,
            loc=[enums.Location.BODY, "name"],
            msg="User Type already exists"
        )

    if errors:
        return error_responses.pydantic_error_response(errors)

    create_db_user_type = controller.create(user_type=user_type)

    return create_db_user_type


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
