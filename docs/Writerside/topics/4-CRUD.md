# 4. CRUD Operations

We create a `crud.py` file to handle the CRUD operations inside the `app/` directory.

CRUD comes from: **C**reate, **R**ead, **U**pdate, and **D**elete.

```python
import app.database.schemas.enrollments
import app.database.schemas.courses
import app.database.schemas.users
import app.database.schemas.user_types
from sqlalchemy.orm import Session
from . import models, schemas


# -------------------------------------------------------------------------------------------------
# User specific CRUD operations, # of functions = 5
# -------------------------------------------------------------------------------------------------
def get_user_by_id(db: Session, user_id: int) -> app.database.schemas.users.User:
    """
    This function queries the database for the User with the given user_id
    and returns the User with the given user_id
    :param db: The database session
    :param user_id:
    :return User:
    """
    return db.query(app.database.schemas.users.User).filter(app.database.schemas.users.User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str) -> app.database.schemas.users.User:
    """
    This function queries the database for the User with the given email
    and returns the User with the given email
    :param db: The database session
    :param email:
    :return User:
    """
    return db.query(app.database.schemas.users.User).filter(app.database.schemas.users.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[app.database.schemas.users.User]:
    """
    This function queries the database for Users with the given skip and limit boundaries
    and returns a list of Users
    :param db: The database session
    :param skip: Starting index of the list, 0 by default
    :param limit: Ending index (skip + limit), 10 by default
    :return List[Type[database.User]]:
    """
    return db.query(app.database.schemas.users.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: app.database.schemas.users.UserCreate) -> app.database.schemas.users.User:
    """
    This function creates a new User

    It uses a fake hashing 'algorithm', just appends "fakehashed" to the given password.

    TODO: Change the hashing
    :param db: The database session
    :param user: schemas.UserCreate
    :return: User
    """
    hashed_password = user.password + "fakehashed"

    db_user = app.database.schemas.users.User(
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


# def delete_user(db: Session, user_id: int) -> database.User:
#     """
#     This function deletes a User based on the given user_id
#     :param db: The database session
#     :param user_id:
#     :return: deleted User
#     """
#     db_user = db.query(database.User).filter(database.User.user_id == user_id).first()
#     db.delete(db_user)
#     db.commit()
#     return db_user


def soft_delete_user(db: Session, user_id: int):
    db_user = db.query(app.database.schemas.users.User).filter(
        app.database.schemas.users.User.user_id == user_id).first()
    if db_user:
        db_user.is_active = False
        db.commit()
        db.refresh(db_user)
    return db_user


def reactivate_user(db: Session, user_id: int):
    db_user = db.query(app.database.schemas.users.User).filter(models.user_id == user_id).first()
    if db_user:
        db_user.is_active = True
        db.commit()
        db.refresh(db_user)
    return db_user


# -------------------------------------------------------------------------------------------------
# User Type specific CRUD operations, # of functions = 5
# -------------------------------------------------------------------------------------------------

def get_user_type_by_id(db: Session, user_type_id: int) -> app.database.schemas.user_types.UserType:
    """
    This function queries the database for the UserType with the given user_type_id
    :param db: The database session
    :param user_type_id: The user_type_id
    :return: The UserType with the given user_type_id
    """
    return db.query(app.database.schemas.user_types.UserType).filter(
        app.database.schemas.user_types.UserType.user_type_id == user_type_id).first()


def get_user_type_by_name(db: Session, name: str) -> app.database.schemas.user_types.UserType:
    """
    This function queries the database for the UserType with the given name
    :param db: The database session
    :param name: The user_type_name
    :return: The UserType with the given name
    """
    return db.query(app.database.schemas.user_types.UserType).filter(
        app.database.schemas.user_types.UserType.name == name).first()


def get_user_types(db: Session, skip: int = 0, limit: int = 10) -> list[app.database.schemas.user_types.UserType]:
    """
    This function queries the database for the UserType with the given skip and limit boundaries
    and returns a list of UserTypes
    :param db: The database session
    :param skip: Starting index of the list, 0 by default
    :param limit: Ending index (skip + limit), 10 by default
    :return: List[Type[database.UserType]]:
    """
    return db.query(app.database.schemas.user_types.UserType).offset(skip).limit(limit).all()


def create_user_type(db: Session,
                     user_type: app.database.schemas.user_types.UserTypeCreate) -> app.database.schemas.user_types.UserType:
    """
    This function creates a new UserType
    :param db: The database session
    :param user_type: schemas.UserTypeCreate
    :return: The created UserType
    """
    db_user_type = app.database.schemas.user_types.UserType(
        **user_type.dict()
    )
    db.add(db_user_type)
    db.commit()
    db.refresh(db_user_type)
    return db_user_type


def delete_user_type(db: Session, user_type_id: int) -> app.database.schemas.user_types.UserType:
    """
    This function deletes a User Type based on the given user_type_id
    :param db: The database session
    :param user_type_id: The user_type_id
    :return: Deleted UserType
    """

    db_user_type = db.query(app.database.schemas.user_types.UserType).filter(
        app.database.schemas.user_types.UserType.user_type_id == user_type_id).first()
    db.delete(db_user_type)
    db.commit()
    return db_user_type


# -------------------------------------------------------------------------------------------------
# Course specific CRUD operations, # of functions = 5
# -------------------------------------------------------------------------------------------------

def get_course_by_id(db: Session, course_id: int) -> app.database.schemas.courses.Course:
    """
    This function queries the database for the Course with the given course_id
    and returns the Course with the given course_id
    :param db: The database session
    :param course_id: Pydantic Course model
    :return: Course with the given course_id
    """
    return db.query(app.database.schemas.courses.Course).filter(
        app.database.schemas.courses.Course.course_id == course_id).first()


def get_course_by_name(db: Session, name: str) -> app.database.schemas.courses.Course:
    """
    This function queries the database for the Course with the given name
    :param db: The database session
    :param name: Course name
    :return: Course with given name
    """
    return db.query(app.database.schemas.courses.Course).filter(
        app.database.schemas.courses.Course.name == name).first()


def get_courses(db: Session, skip: int = 0, limit: int = 10) -> list[app.database.schemas.courses.Course]:
    """
    This function queries the database for the Course with the given skip and limit boundaries
    and returns a list of Courses
    :param db: The database session
    :param skip: The starting index of the list, 0 by default
    :param limit: The ending index (skip + limit), 10 by default
    :return: List[Type[database.Course]]:
    """
    return db.query(app.database.schemas.courses.Course).offset(skip).limit(limit).all()


def create_course(db: Session,
                  course: app.database.schemas.courses.CourseCreate) -> app.database.schemas.courses.Course:
    """
    This function creates a new Course based on the given course pydantic model
    :param db: The database session
    :param course: Pydantic Course model
    :return: Created Course
    """
    db_course = app.database.schemas.courses.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


# def delete_course(db: Session, course_id: int) -> database.Course:
#     """
#     This function deletes a Course based on the given course_id
#     :param db: The database session
#     :param course_id: The given course_id
#     :return: Deleted Course instance
#     """
#     db_course = db.query(database.Course).filter(database.Course.id == course_id).first()
#     db.delete(db_course)
#     db.commit()
#     return db_course


def soft_delete_course(db: Session, course_id: int):
    db_course = db.query(app.database.schemas.courses.Course).filter(
        app.database.schemas.courses.Course.user_id == course_id).first()
    if db_course:
        db_course.is_active = False
        db.commit()
        db.refresh(db_course)
    return db_course


def reactivate_course(db: Session, course_id: int):
    db_course = db.query(app.database.schemas.courses.Course).filter(
        app.database.schemas.courses.Course.course_id == course_id).first()
    if db_course:
        db_course.is_active = True
        db.commit()
        db.refresh(db_course)
    return db_course


# -------------------------------------------------------------------------------------------------
# Enrollment specific CRUD operations, # of functions = 4
# -------------------------------------------------------------------------------------------------

def get_enrollment_by_ids(db: Session, user_id: int, course_id: int) -> app.database.schemas.enrollments.Enrollment:
    """
    This function returns the Enrollment based on the given user_id and course_id composite key
    :param user_id: The user id
    :param course_id: The given course_id
    :return: Enrollment based on the given user_id and course_id composite key
    """
    db_enrollment = db.query(app.database.schemas.enrollments.Enrollment).filter(
        app.database.schemas.enrollments.Enrollment.user_id == user_id,
        app.database.schemas.enrollments.Enrollment.course_id == course_id).first()

    return db_enrollment


def get_enrollments(db: Session, skip: int = 0, limit: int = 10) -> list[app.database.schemas.enrollments.Enrollment]:
    """
    This function queries the database for the Enrollment with the given skip and limit boundaries
    and returns a list of Enrollments
    :param db: The database session
    :param skip: The starting index of the list, 0 by default
    :param limit: The ending index (skip + limit), 10 by default
    :return: List[database.Enrollment]:
    """
    return db.query(app.database.schemas.enrollments.Enrollment).offset(skip).limit(limit).all()


def create_enrollment(db: Session,
                      enrollment: app.database.schemas.enrollments.EnrollmentCreate) -> app.database.schemas.enrollments.Enrollment:
    """
    This function creates a new Enrollment based on the given enrollment pydantic model
    :param db: The database session
    :param enrollment: The given enrollment pydantic model
    :return: Created Enrollment instance
    """
    db_enrollment = app.database.schemas.enrollments.Enrollment(**enrollment.dict())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


def delete_enrollment(db: Session, enrollment_id: int) -> app.database.schemas.enrollments.Enrollment:
    """
    This function deletes a Enrollment based on the given enrollment_id
    :param db: The database session
    :param enrollment_id: The given enrollment_id
    :return: The deleted Enrollment instance
    """
    db_enrollment = db.query(app.database.schemas.enrollments.Enrollment).filter(
        app.database.schemas.enrollments.Enrollment.enrollment_id == enrollment_id).first()
    db.delete(db_enrollment)
    db.commit()
    return db_enrollment
```