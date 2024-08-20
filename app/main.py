from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from .initial_records import default_users, default_enrollments, default_courses
from . import models, schemas
from .controllers import crud
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
from fastapi.responses import JSONResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Inner join to get the user_type_id name:
# select users.user_id, users.first_name, users.last_name, users.username, users.email, user_types.user_type_id, user_types.name from users inner join user_types on users.user_type_id = user_types.user_type_id;

# Inner join to get all users that match the given user_type_id:
# select user_types.user_type_id, user_types.name, users.user_id, users.first_name, users.last_name, users.username, users.email from user_types inner join users on users.user_type_id = user_types.user_type_id where users.user_type_id = 1;

# TODO: Implement some sort of "TRUNCATE DATABASE" function:
# truncate user_types, users, courses, enrollments;

# Left join from users over enrollments onto courses:
# select users.user_id, users.first_name, users.email, courses.course_id, courses.name from users left join enrollments on users.user_id = enrollments.user_id left join courses on enrollments.course_id = courses.course_id;

# Inner join from users over enrollments onto courses;
# select users.user_id, users.first_name, users.email, courses.course_id, courses.name from users inner join enrollments on users.user_id = enrollments.user_id inner join courses on enrollments.course_id = courses.course_id;

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:63342",
    "file://",
    "null",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------------------------------------------------------
# Functions specifically using `db.execute`
# -------------------------------------------------------------------------------------------------

def reset_auto_increment(db: Session, table_name: str, column_name: str):
    """
    This function resets the autoincrement sequence in a given table
    :param db: The
    :param table_name:
    :param column_name:
    :return:
    """
    # alter sequence user_types_user_type_id_seq restart with 1;
    reset_sql = text(f"alter sequence {table_name}_{column_name}_seq restart with 1")
    db.execute(reset_sql)
    db.commit()


def truncate_db(db: Session):
    truncate_sql = text("truncate user_types, users, courses, enrollments;")
    result = db.execute(truncate_sql)
    db.commit()
    return result


# -------------------------------------------------------------------------------------------------
# Seeding functions
# -------------------------------------------------------------------------------------------------

def seed_user_types(db: Session):
    """
    This function seeds the user_types table with some initial values
    :param db:
    :return:
    """
    if db.query(models.UserType).count() == 0:
        reset_auto_increment(db, 'user_types', 'user_type_id')

        default_user_types = ['Admin', 'Student']

        # results = []

        for user_type in default_user_types:
            db.add(models.UserType(name=user_type))
        db.commit()


def seed_users(db: Session):
    """
    This function seeds the users table with some initial values
    :param db:
    :return:
    """
    if db.query(models.User).count() == 0:
        reset_auto_increment(db, 'users', 'user_id')

        for user in default_users:
            db.add(models.User(**user))
        db.commit()


def seed_courses(db: Session):
    """
    This function seeds the courses table with some initial values
    :param db:
    :return:
    """
    if db.query(models.Course).count() == 0:
        reset_auto_increment(db, 'courses', 'course_id')

        for course in default_courses:
            db.add(models.Course(**course))
        db.commit()


def seed_enrollments(db: Session):
    """
    This function seeds the enrollments table with some initial values
    :param db:
    :return:
    """
    if db.query(models.Enrollment).count() == 0:

        for enrollment in default_enrollments:
            db.add(models.Enrollment(**enrollment))
        db.commit()


def seed(db: Session):
    seed_user_types(db)
    seed_users(db)
    seed_courses(db)
    seed_enrollments(db)

# -------------------------------------------------------------------------------------------------
# App startup specific path operation
# -------------------------------------------------------------------------------------------------

@app.on_event("startup")
def on_startup():
    """
    On server startup, the seeding gets executed
    :return:
    """
    db = SessionLocal()
    seed(db)
    db.close()


# -------------------------------------------------------------------------------------------------
# Utility functions and Enums
# -------------------------------------------------------------------------------------------------

class ErrorType(str, Enum):
    VALUE_ERROR = "value_error"
    TYPE_ERROR = "type_error"


class Location(str, Enum):
    BODY = "body"
    QUERY = "query"
    PATH = "path"


def pydantic_error_response(errors: list[dict]) -> JSONResponse:
    """Utility function to create a Pydantic-style error response with accumulated errors"""
    return JSONResponse(
        status_code=422,
        content={
            "detail": errors
        }
    )


def add_error(errors: list[dict], loc: list[Location | str], msg: str, error_type: ErrorType = ErrorType.VALUE_ERROR):
    """Utility function to add an error to the errors list"""
    errors.append({
        "loc": loc,
        "msg": msg,
        "type": error_type.value
    })


# -------------------------------------------------------------------------------------------------
# Root specific path operation
# -------------------------------------------------------------------------------------------------

@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World!"}


# -------------------------------------------------------------------------------------------------
# Path operation's not specific to one Model
# -------------------------------------------------------------------------------------------------

@app.delete('/truncate_db/', tags=["TRUNCATE DATABASE"])
def truncate_database(db: Session = Depends(get_db)):
    """
    This function truncates every table in the database
    :param db: The database to truncate
    :return: The truncated database
    """
    result = truncate_db(db)
    return result


@app.post('/re_seed_db/', tags=["RE-SEED DATABASE"])
def re_seed_database(db: Session = Depends(get_db)):
    """
    This function re-seeds some tables in the database based on the default values
    :param db: The database to re-seed
    :return: The re-seeded database
    """
    seed(db)


# -------------------------------------------------------------------------------------------------
# User specific CRUD operations, # of functions = 7
# -------------------------------------------------------------------------------------------------

@app.get('/users/count/', response_model=int, tags=["Users"])
def get_users_count(db: Session = Depends(get_db)):
    """
    This function returns the number of users in the database
    :param db: The database session to use
    :return: The number of users in the database
    """
    return db.query(models.User).count()


@app.get('/users/{user_id}', response_model=schemas.User, tags=["Users"])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    This path operation returns a User based on the given id using the crud.get_user_by_id() function
    :param user_id: The given User id
    :param db: The database session to use
    :return: The User instance
    """
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/email/{email}", response_model=schemas.User, tags=["Users"])
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """
    This path operation returns the user with the given email using the crud.get_user_by_email() function
    :param email: The email of the user
    :param db: The database session to use
    :return: The User instance
    """
    db_user = crud.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/", response_model=list[schemas.User], tags=["Users"])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    This path operation returns a list of users using the crud.get_users() function
    :param skip: The number of items to skip at the beginning of the list
    :param limit: The maximum number of items to return
    :param db: The database session to use
    :return: The list of users
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/users/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    This path operation creates a new user using the crud.create_user() function.
    :param user: schemas.UserCreate
    :param db: The database session to use.
    :return: Created User instance.
    """
    errors = []

    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        add_error(
            errors=errors,
            loc=[Location.BODY, "email"],
            msg="Email already registered"
        )

    if crud.get_user_type_by_id(db, user.user_type_id) is None:
        add_error(
            errors=errors,
            loc=[Location.BODY, "user_type_id"],
            msg="User Type doesn't exist"
        )

    if errors:
        return pydantic_error_response(errors)

    return crud.create_user(db=db, user=user)


@app.put("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    """
    This path operation performs a deactivation (soft delete) on a user by setting the is_active field to False.
    :param user_id: The id of the user
    :param db: The database session to use
    :return: The User instance with is_active set to False
    """
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user = crud.deactivate_user(db, user_id=user_id)

    return db_user


@app.put("/users/reactivate/{user_id}", response_model=schemas.User, tags=["Users"])
def activate_user(user_id: int, db: Session = Depends(get_db)):
    """
    This path operation reactivates a user by setting the is_active field to True.
    :param user_id: The id of the user
    :param db: The database session to use
    :return: The reactivated User instance
    """
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.is_active:
        raise HTTPException(status_code=400, detail="User is already active")

    db_user = crud.activate_user(db, user_id=user_id)

    return db_user


# -------------------------------------------------------------------------------------------------
# User Type specific CRUD operations, # of functions = 6
# -------------------------------------------------------------------------------------------------

@app.get('/user_types/count/', response_model=int, tags=["User Types"])
def get_user_types_count(db: Session = Depends(get_db)):
    """
    This function returns the number of user types in the database
    :param db: The database session to use
    :return: The number of user types in the database
    """
    return db.query(models.UserType).count()


@app.get('/user_types/{user_type_id}', response_model=schemas.UserType, tags=["User Types"])
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


@app.get('/user_types/name/{name}', response_model=schemas.UserType, tags=["User Types"])
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


@app.get('/user_types/', response_model=list[schemas.UserType], tags=["User Types"])
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


@app.post('/user_types/', response_model=schemas.UserTypeCreate, tags=["User Types"])
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
        add_error(
            errors=errors,
            loc=[Location.BODY, "name"],
            msg="User Type already exists"
        )

    # If there are any errors, return them in a Pydantic-style error response
    if errors:
        return pydantic_error_response(errors)

    # Create and return the new user type
    create_db_user_type = crud.create_user_type(db=db, user_type=user_type)
    return create_db_user_type


@app.delete('/user_types/{user_type_id}', response_model=schemas.UserType, tags=["User Types"])
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


# -------------------------------------------------------------------------------------------------
# Course specific CRUD operations, # of functions = 7
# -------------------------------------------------------------------------------------------------

@app.get('/courses/count/', response_model=int, tags=["Courses"])
def get_courses_count(db: Session = Depends(get_db)):
    """
    This function returns the number of courses in the database
    :param db: The database session to use
    :return: The number of courses in the database
    """
    return db.query(models.Course).count()


@app.get('/courses/{course_id}', response_model=schemas.Course, tags=["Courses"])
def get_course_by_id(course_id: int, db: Session = Depends(get_db)):
    """
    This path operation returns the course using the crud.get_course_by_id() function
    :param course_id: The id of the course
    :param db: The database session to use
    :return: The Course instance
    """
    db_course = crud.get_course_by_id(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    return db_course


@app.get('/courses/name/{name}', response_model=schemas.Course, tags=["Courses"])
def get_course_by_name(name: str, db: Session = Depends(get_db)):
    """
    This path operation returns a Course using the crud.get_course_by_name() function
    :param name: The name of the course
    :param db: The database session to use
    :return: The Course instance
    """
    db_course = crud.get_course_by_name(db, name=name)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    return db_course


@app.get('/courses/', response_model=list[schemas.Course], tags=["Courses"])
def read_courses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    This path operation returns a list of courses using the crud.get_courses() function
    :param skip: The number of items to skip at the beginning of the list
    :param limit: The maximum number of items to return
    :param db: The database session to use
    :return: The list of Courses
    """
    courses = crud.get_courses(db, skip=skip, limit=limit)
    return courses


@app.post('/courses/', response_model=schemas.Course, tags=["Courses"])
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    """
    This path operation creates a new course using the crud.create_course() function.
    :param course: schemas.CourseCreate
    :param db: The database session to use.
    :return: Created Course instance.
    """
    errors = []

    db_course = crud.get_course_by_name(db, name=course.name)
    if db_course:
        add_error(
            errors=errors,
            loc=[Location.BODY, "name"],
            msg="Course already exists"
        )

    if errors:
        return pydantic_error_response(errors)

    return crud.create_course(db=db, course=course)


@app.put("/courses/{course_id}", response_model=schemas.Course, tags=["Courses"])
def deactivate_course(course_id: int, db: Session = Depends(get_db)):
    """
    This path operation performs a deactivation (soft delete) on a course by setting the is_active field to False.
    :param course_id: The id of the course
    :param db: The database session to use
    :return: The Course instance with is_active set to False
    """
    db_course = crud.get_course_by_id(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    db_course = crud.deactivate_course(db, course_id=course_id)

    return db_course


@app.put("/courses/reactivate/{course_id}", response_model=schemas.Course, tags=["Courses"])
def activate_course(course_id: int, db: Session = Depends(get_db)):
    """
    This path operation reactivates a course by setting the is_active field to True.
    :param course_id: The id of the course
    :param db: The database session to use
    :return: The reactivated Course instance
    """
    db_course = crud.get_course_by_id(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    if db_course.is_active:
        raise HTTPException(status_code=400, detail="Course is already active")

    db_course = crud.activate_course(db, course_id=course_id)

    return db_course


# -------------------------------------------------------------------------------------------------
# Enrollment specific CRUD operations, # of functions = 4
# -------------------------------------------------------------------------------------------------

@app.get('/enrollments/count/', response_model=int, tags=["Enrollments"])
def get_enrollments_count(db: Session = Depends(get_db)):
    """
    This function returns the number of enrollments in the database
    :param db: The database session to use
    :return: The number of enrollments in the database
    """
    return db.query(models.Enrollment).count()


@app.get('/enrollments/{user_id}/{course_id}', response_model=schemas.Enrollment, tags=["Enrollments"])
def get_enrollment_by_ids(user_id: int, course_id: int, db: Session = Depends(get_db)):
    """
    This path operation returns an Enrollment based on the user_id and course_id composite key
    :param user_id: The user id
    :param course_id: The course id
    :param db: The database session to use
    :return: The Enrollment instance
    """
    db_enrollment = crud.get_enrollment_by_ids(db, user_id=user_id, course_id=course_id)

    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    return db_enrollment


@app.get('/enrollments/', response_model=list[schemas.Enrollment], tags=["Enrollments"])
def get_enrollments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    This path operation returns a list of Enrollments using the crud.get_enrollments() function
    :param skip: The number of items to skip at the beginning of the list
    :param limit: The maximum number of items to return
    :param db: The database session to use
    :return: The list of Enrollments
    """
    db_enrollments = crud.get_enrollments(db, skip=skip, limit=limit)
    return db_enrollments


@app.post('/enrollments/', response_model=schemas.Enrollment, tags=["Enrollments"])
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    """
    This path operation creates an Enrollment using the crud.create_enrollment() function
    :param enrollment: schemas.EnrollmentCreate
    :param db: The database session to use
    :return: The Enrollment instance
    """
    errors = []

    db_exists = crud.get_enrollment_by_ids(db, user_id=enrollment.user_id, course_id=enrollment.course_id)
    if db_exists:
        add_error(
            errors=errors,
            loc=[Location.BODY, "user_id", "course_id"],
            msg="Enrollment already exists"
        )

    db_user = crud.get_user_by_id(db, user_id=enrollment.user_id)
    if not db_user:
        add_error(
            errors=errors,
            loc=[Location.BODY, "user_id"],
            msg=f"User not found for User ID: {enrollment.user_id}"
        )

    db_course = crud.get_course_by_id(db, course_id=enrollment.course_id)
    if not db_course:
        add_error(
            errors=errors,
            loc=[Location.BODY, "course_id"],
            msg=f"Course not found for Course ID: {enrollment.course_id}"
        )

    if errors:
        return pydantic_error_response(errors)

    db_enrollment = crud.create_enrollment(db, enrollment)
    return db_enrollment
