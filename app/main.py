from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

from . import crud, models, schemas
from .database import SessionLocal, engine

from fastapi.middleware.cors import CORSMiddleware

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


def reset_auto_increment(db: Session, table_name: str, column_name: str):
    # alter sequence user_types_user_type_id_seq restart with 1;
    reset_sql = text(f"alter sequence {table_name}_{column_name}_seq restart with 1")
    db.execute(reset_sql)
    db.commit()


default_users = [
    {
        "first_name": "Safet",
        "last_name": "Imamovic",
        "username": "admin",
        "email": "safet.imamovic.22@size.ba",
        "age": 21,
        "is_active": True,
        "user_type_id": 1,
        "hashed_password": "admin"
    },
    {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe123",
        "email": "john.doe@example.com",
        "age": 21,
        "is_active": True,
        "user_type_id": 2,
        "hashed_password": "password1"
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "username": "janedoe69",
        "email": "jane.smith@example.com",
        "age": 22,
        "is_active": True,
        "user_type_id": 2,
        "hashed_password": "password2"
    }
]


default_courses = [
    {
        "name": "Python 101",
        "description": "Basic Python",
        "start_date": "2024-08-17T15:02:49.434Z",
        "end_date": "2024-08-17T15:02:49.434Z",
        "is_active": True
    },
    {
        "name": "Alembic 101",
        "description": "World Database Migration",
        "start_date": "2024-08-17T15:02:49.434Z",
        "end_date": "2024-08-17T15:02:49.434Z",
        "is_active": True
    },
]


def seed_user_types(db: Session):
    if db.query(models.UserType).count() == 0:
        reset_auto_increment(db, 'user_types', 'user_type_id')

        default_user_types = ['Admin', 'Student']

        # results = []

        for user_type in default_user_types:
            db.add(models.UserType(name=user_type))
        db.commit()


def seed_users(db: Session):
    if db.query(models.User).count() == 0:
        reset_auto_increment(db, 'users', 'user_id')

        for user in default_users:
            db.add(models.User(**user))
        db.commit()


def seed_courses(db: Session):
    if db.query(models.Course).count() == 0:
        reset_auto_increment(db, 'courses', 'course_id')

        for course in default_courses:
            db.add(models.Course(**course))
        db.commit()


def truncate_db(db: Session):
    truncate_sql = text("truncate user_types, users, courses, enrollments;")
    result = db.execute(truncate_sql)
    db.commit()
    return result


@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    seed_user_types(db)
    seed_users(db)
    seed_courses(db)
    db.close()


@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World!"}


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
    seed_user_types(db)
    seed_users(db)
    seed_courses(db)


# -------------------------------------------------------------------------------------------------
# User specific CRUD operations, # of functions = 6
# -------------------------------------------------------------------------------------------------

@app.get('/users_count/', response_model=int, tags=["Users"])
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
    This path operation creates a new user using the crud.create_user() function
    :param user: schemas.UserCreate
    :param db: The database session to use
    :return: Created User instance
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if crud.get_user_type_by_id(db, user.user_type_id) is None:
        raise HTTPException(status_code=404, detail="User Type doesn't exist")

    return crud.create_user(db=db, user=user)


@app.delete("/delete_users/{user_id}", response_model=schemas.User, tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    This path operation deletes a user using the crud.delete_user() function
    :param user_id: The id of the user
    :param db: The database session to use
    :return: Deleted User instance
    """
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    crud.delete_user(db, user_id=user_id)

    return db_user


# -------------------------------------------------------------------------------------------------
# User Type specific CRUD operations, # of functions = 5
# -------------------------------------------------------------------------------------------------

@app.get('/user_types_count/', response_model=int, tags=["User Types"])
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


@app.post('/user_types/', response_model=schemas.UserType, tags=["User Types"])
def create_user_type(user_type: schemas.UserTypeCreate, db: Session = Depends(get_db)):
    """
    This path operation creates a new user type using the crud.create_user_type() function
    :param user_type: The schemas.UserType instance
    :param db: The database session to use
    :return: The created user type
    """
    db_user_type = crud.get_user_type_by_name(db, name=user_type.name)
    if db_user_type:
        raise HTTPException(status_code=400, detail="User Type already exists")

    create_db_user_type = crud.create_user_type(db=db, user=user_type)

    return create_db_user_type


@app.delete('/delete_user_types/{user_type_id}', response_model=schemas.UserType, tags=["User Types"])
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
# Course specific CRUD operations, # of functions = 5
# -------------------------------------------------------------------------------------------------

@app.get('/courses_count/', response_model=int, tags=["Courses"])
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
    This path operation creates a new course using the crud.create_course() function
    :param course: schemas.CourseCreate
    :param db: The database session to use
    :return: Created Course instance
    """
    db_course = crud.get_course_by_name(db, name=course.name)
    if db_course:
        raise HTTPException(status_code=400, detail="Course already exists")

    return crud.create_course(db=db, course=course)


@app.delete('/delete_course/{course_id}', response_model=schemas.Course, tags=["Courses"])
def delete_course(course_id: int, db: Session = Depends(get_db)):
    """
    This path operation deletes a course using the crud.delete_course() function
    :param course_id: The id of the course
    :param db: The database session to use
    :return: The Deleted Course instance
    """
    db_course = crud.get_course_by_id(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    crud.delete_course(db, course_id=course_id)

    return db_course


# -------------------------------------------------------------------------------------------------
# Enrollment specific CRUD operations, # of functions = 5
# -------------------------------------------------------------------------------------------------

@app.get('/enrollments_count/', response_model=int, tags=["Enrollments"])
def get_enrollments_count(db: Session = Depends(get_db)):
    """
    This function returns the number of enrollments in the database
    :param db: The database session to use
    :return: The number of enrollments in the database
    """
    return db.query(models.Enrollment).count()


@app.get('/enrollments/{enrollment_id}', response_model=schemas.Enrollment, tags=["Enrollments"])
def get_enrollment_by_id(enrollment_id: int, db: Session = Depends(get_db)):
    """
    This path operation returns an Enrollment using the crud.get_enrollment_by_id() function
    :param enrollment_id: The id of the enrollment
    :param db: The database session to use
    :return: The Enrollment instance
    """
    db_enrollment = crud.get_enrollment_by_id(db, enrollment_id=enrollment_id)
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
    db_enrollment = crud.create_enrollment(db, enrollment)
    return db_enrollment

