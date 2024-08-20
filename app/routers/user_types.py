from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.database.schemas.user_types as schemas
import app.database.models.user_types as models
from app.controllers import user_types_crud as crud
from app.database.database import get_db
from app.utils import error_responses, enums

router = APIRouter(prefix="/user_types", tags=["User Types"])


@router.get('/count/', response_model=int)
def get_user_types_count(db: Session = Depends(get_db)):
    """
    This function returns the number of user types in the database
    :param db: The database session to use
    :return: The number of user types in the database
    """
    return db.query(models.UserType).count()


@router.get('/{user_type_id}', response_model=schemas.UserType)
def get_user_types(user_type_id: int, db: Session = Depends(get_db)):
    """
    This path operation returns one UserType using the crud.get_user_type_by_id() function
    :param user_type_id: The id of the user type
    :param db: The database session to use
    :return: The UserType instance
    """
    db_user_type = crud.get_user_type_by_id(db, user_type_id=user_type_id)
    if not db_user_type:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user_type


@router.get('/name/{name}', response_model=schemas.UserType)
def get_user_type_by_name(name: str, db: Session = Depends(get_db)):
    """
    This path operation returns one UserType using the crud.get_user_type_by_name() function
    :param name: The name of the user type
    :param db: The database session to use
    :return: The UserType instance
    """
    db_user_type = crud.get_user_type_by_name(db, name=name)
    if not db_user_type:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user_type


@router.get('/', response_model=list[schemas.UserType])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    This path operation returns a list of user types using the crud.get_user_types() function
    :param skip: The number of items to skip at the beginning of the list
    :param limit: The maximum number of items to return
    :param db: The database session to use
    :return: The list of user types
    """
    user_types = crud.get_user_types(db, skip=skip, limit=limit)
    return user_types


@router.post('/', response_model=schemas.UserTypeCreate)
def create_user_type(user_type: schemas.UserTypeCreate, db: Session = Depends(get_db)):
    """
    This path operation creates a new user type using the crud.create_user_type() function.
    :param user_type: The schemas.UserTypeCreate instance.
    :param db: The database session to use.
    :return: The created user type.
    """
    errors = []

    # Check if the user type name already exists
    db_user_type = crud.get_user_type_by_name(db, name=user_type.name)
    if db_user_type:
        error_responses.add_error(
            errors=errors,
            loc=[enums.Location.BODY, "name"],
            msg="User Type already exists"
        )

    # If there are any errors, return them in a Pydantic-style error response
    if errors:
        return error_responses.pydantic_error_response(errors)

    # Create and return the new user type
    create_db_user_type = crud.create_user_type(db=db, user_type=user_type)
    return create_db_user_type


@router.delete('/{user_type_id}', response_model=schemas.UserType)
def delete_user_type(user_type_id: int, db: Session = Depends(get_db)):
    """
    This path operation deletes a user type using the crud.delete_user_type() function
    :param user_type_id: The id of the user type
    :param db: The database session to use
    :return: Deleted user type
    """

    db_user_type = crud.get_user_type_by_id(db, user_type_id=user_type_id)
    if not db_user_type:
        raise HTTPException(status_code=404, detail="User not found")

    crud.delete_user_type(db, user_type_id=user_type_id)
    return db_user_type
