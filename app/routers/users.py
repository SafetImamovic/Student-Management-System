from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

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

    db_user = controller.get_by_id(user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


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

    db_user = controller.get_by_email(email=email)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@router.get(
    "/",
    responses={

    },
    response_model=list[UserSchema]
)
def get_all(
    controller: Annotated[UserController, Depends(UserController)],
    skip: int = 0,
    limit: int = 10,
):
    """
    This path operation returns a list of users using the crud.get_users() function
    :param controller:
    :param skip: The number of items to skip at the beginning of the list
    :param limit: The maximum number of items to return
    :return: The list of users
    """

    users = controller.get_all(skip=skip, limit=limit)

    return users


@router.post(
    "/",
    responses={

    },
    response_model=UserSchema,
)
def create(
    user: UserCreateSchema,
    user_controller: Annotated[UserController, Depends(UserController)],
    user_type_controller: Annotated[UserTypeController, Depends(UserTypeController)]
):
    """
    This path operation creates a new user using the crud.create_user() function.
    :param user_type_controller:
    :param user_controller:
    :param user: schemas.UserCreate
    :return: Created User instance.
    """

    errors = []

    db_user = user_controller.get_by_email(email=user.email)

    if db_user:
        error_responses.add_error(
            errors=errors,
            loc=[enums.Location.BODY, "email"],
            msg="Email already registered"
        )

    db_user_type = user_type_controller.get_by_id(user.user_type_id)

    if db_user_type is None:
        error_responses.add_error(
            errors=errors,
            loc=[enums.Location.BODY, "user_type_id"],
            msg="User Type doesn't exist"
        )

    if errors:
        return error_responses.pydantic_error_response(errors)

    return user_controller.create(user=user)


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

    db_user = controller.get_by_id(user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user = controller.deactivate(user_id=user_id)

    return db_user


@router.put(
    "/users/reactivate/{user_id}",
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

    db_user = controller.get_by_id(user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.is_active:
        raise HTTPException(status_code=400, detail="User is already active")

    db_user = controller.activate(user_id=user_id)

    return db_user
