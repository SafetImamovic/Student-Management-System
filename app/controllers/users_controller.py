from sqlalchemy.orm import Session
from app.database.models import users as models
from app.database.schemas import users as schemas


def get_users_count(db: Session) -> int:
    """
    This function returns the number of users in the database
    :param db:
    :return:
    """
    return db.query(models.User).count()


def get_user_by_id(db: Session, user_id: int) -> schemas.User:
    """
    This function queries the models for the User with the given user_id
    and returns the User with the given user_id
    :param db: The models session
    :param user_id:
    :return User:
    """
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    """
    This function queries the models for the User with the given email
    and returns the User with the given email
    :param db: The models session
    :param email:
    :return User:
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[models.User]:
    """
    This function queries the models for Users with the given skip and limit boundaries
    and returns a list of Users
    :param db: The models session
    :param skip: Starting index of the list, 0 by default
    :param limit: Ending index (skip + limit), 10 by default
    :return List[Type[models.User]]:
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    This function creates a new User

    It uses a fake hashing 'algorithm', just appends "fakehashed" to the given password.

    TODO: Change the hashing
    :param db: The models session
    :param user: schemas.UserCreate
    :return: User
    """
    hashed_password = user.password + "fakehashed"

    db_user = models.User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        age=user.age,
        is_active=user.is_active,
        user_type_id=user.user_type_id,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def deactivate_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        db_user.is_active = False
        db.commit()
        db.refresh(db_user)
    return db_user


def activate_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        db_user.is_active = True
        db.commit()
        db.refresh(db_user)
    return db_user
