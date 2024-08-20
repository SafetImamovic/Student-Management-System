from sqlalchemy.orm import Session
from app.database.models import user_types as models
from app.database.schemas import user_types as schemas


def get_user_type_by_id(db: Session, user_type_id: int) -> models.UserType:
    """
    This function queries the models for the UserType with the given user_type_id
    :param db: The models session
    :param user_type_id: The user_type_id
    :return: The UserType with the given user_type_id
    """
    return db.query(models.UserType).filter(models.UserType.user_type_id == user_type_id).first()


def get_user_type_by_name(db: Session, name: str) -> models.UserType:
    """
    This function queries the models for the UserType with the given name
    :param db: The models session
    :param name: The user_type_name
    :return: The UserType with the given name
    """
    return db.query(models.UserType).filter(models.UserType.name == name).first()


def get_user_types(db: Session, skip: int = 0, limit: int = 10) -> list[models.UserType]:
    """
    This function queries the models for the UserType with the given skip and limit boundaries
    and returns a list of UserTypes
    :param db: The models session
    :param skip: Starting index of the list, 0 by default
    :param limit: Ending index (skip + limit), 10 by default
    :return: List[Type[models.UserType]]:
    """
    return db.query(models.UserType).offset(skip).limit(limit).all()


def create_user_type(db: Session, user_type: schemas.UserTypeCreate) -> models.UserType:
    """
    This function creates a new UserType
    :param db: The models session
    :param user_type: schemas.UserTypeCreate
    :return: The created UserType
    """
    db_user_type = models.UserType(
        **user_type.dict()
    )
    db.add(db_user_type)
    db.commit()
    db.refresh(db_user_type)
    return db_user_type


def delete_user_type(db: Session, user_type_id: int) -> models.UserType:
    """
    This function deletes a User Type based on the given user_type_id
    :param db: The models session
    :param user_type_id: The user_type_id
    :return: Deleted UserType
    """

    db_user_type = db.query(models.UserType).filter(models.UserType.user_type_id == user_type_id).first()
    db.delete(db_user_type)
    db.commit()
    return db_user_type
