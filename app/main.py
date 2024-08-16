from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

from . import crud, models, schemas
from .database import SessionLocal, engine

from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


def seed_user_types(db: Session):
    if db.query(models.UserType).count() == 0:
        reset_auto_increment(db, 'user_types', 'user_type_id')

        default_user_types = ['Admin', 'Student', 'Instructor']

        for user_type in default_user_types:
            db.add(models.UserType(name=user_type))
        db.commit()


def seed_users(db: Session):
    if db.query(models.User).count() == 0:
        reset_auto_increment(db, 'users', 'user_id')

        default_users = [
            {
                "first_name": "Safet",
                "last_name": "Imamovic",
                "username": "admin",
                "email": "safet.imamovic.22@size.ba",
                "age": 21,
                "is_active": True,
                "user_type_id": 1,
                "password": "admin"
            }
        ]

        for user in default_users:
            db.add(models.User(**user))
        db.commit()


@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    seed_user_types(db)
    seed_users(db)
    db.close()


@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World!"}


# -------------------------------------------------------------------------------------------------
# User specific CRUD operations, # of functions = 5
# -------------------------------------------------------------------------------------------------


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
    db_user_type = crud.create_user_type(db, user_type=user_type)
    if db_user_type:
        raise HTTPException(status_code=400, detail="User Type already exists")

    return db_user_type


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
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
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
