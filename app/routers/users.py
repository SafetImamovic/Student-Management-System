from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.database.schemas.users as schemas
import app.database.models.users as models
from app.controllers import users_crud, user_types_crud
from app.database.database import get_db
from app.utils import error_responses, enums

router = APIRouter(prefix="/users", tags=["Users"])


@router.get('/count/', response_model=int, tags=["Users"])
def get_users_count(db: Session = Depends(get_db)):
    """
    This function returns the number of users in the database
    :param db: The database session to use
    :return: The number of users in the database
    """
    return db.query(models.User).count()


@router.get('/{user_id}', response_model=schemas.User, tags=["Users"])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    This path operation returns a User based on the given id using the crud.get_user_by_id() function
    :param user_id: The given User id
    :param db: The database session to use
    :return: The User instance
    """
    db_user = users_crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/email/{email}", response_model=schemas.User, tags=["Users"])
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """
    This path operation returns the user with the given email using the crud.get_user_by_email() function
    :param email: The email of the user
    :param db: The database session to use
    :return: The User instance
    """
    db_user = users_crud.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/", response_model=list[schemas.User], tags=["Users"])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    This path operation returns a list of users using the crud.get_users() function
    :param skip: The number of items to skip at the beginning of the list
    :param limit: The maximum number of items to return
    :param db: The database session to use
    :return: The list of users
    """
    users = users_crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    This path operation creates a new user using the crud.create_user() function.
    :param user: schemas.UserCreate
    :param db: The database session to use.
    :return: Created User instance.
    """
    errors = []

    db_user = users_crud.get_user_by_email(db, email=user.email)
    if db_user:
        error_responses.add_error(
            errors=errors,
            loc=[enums.Location.BODY, "email"],
            msg="Email already registered"
        )

    db_user_type = user_types_crud.get_user_type_by_id(db, user.user_type_id)
    if db_user_type is None:
        error_responses.add_error(
            errors=errors,
            loc=[enums.Location.BODY, "user_type_id"],
            msg="User Type doesn't exist"
        )

    if errors:
        return error_responses.pydantic_error_response(errors)

    return users_crud.create_user(db=db, user=user)


@router.put("/{user_id}", response_model=schemas.User, tags=["Users"])
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    """
    This path operation performs a deactivation (soft delete) on a user by setting the is_active field to False.
    :param user_id: The id of the user
    :param db: The database session to use
    :return: The User instance with is_active set to False
    """
    db_user = users_crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user = users_crud.deactivate_user(db, user_id=user_id)

    return db_user


@router.put("/users/reactivate/{user_id}", response_model=schemas.User, tags=["Users"])
def activate_user(user_id: int, db: Session = Depends(get_db)):
    """
    This path operation reactivates a user by setting the is_active field to True.
    :param user_id: The id of the user
    :param db: The database session to use
    :return: The reactivated User instance
    """
    db_user = users_crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.is_active:
        raise HTTPException(status_code=400, detail="User is already active")

    db_user = users_crud.activate_user(db, user_id=user_id)

    return db_user
