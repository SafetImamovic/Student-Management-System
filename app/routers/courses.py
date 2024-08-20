from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.database.schemas.courses as schemas
import app.database.models.courses as models
from app.controllers import courses_crud as crud
from app.database.database import get_db
from app.utils import error_responses, enums

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get('/count/', response_model=int)
def get_courses_count(db: Session = Depends(get_db)):
    """
    This function returns the number of courses in the database
    :param db: The database session to use
    :return: The number of courses in the database
    """
    return db.query(models.Course).count()


@router.get('/{course_id}', response_model=schemas.Course)
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


@router.get('/name/{name}', response_model=schemas.Course)
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


@router.get('/', response_model=list[schemas.Course])
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


@router.post('/', response_model=schemas.Course)
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
        error_responses.add_error(
            errors=errors,
            loc=[enums.Location.BODY, "name"],
            msg="Course already exists"
        )

    if errors:
        return error_responses.pydantic_error_response(errors)

    return crud.create_course(db=db, course=course)


@router.put("/{course_id}", response_model=schemas.Course)
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


@router.put("/reactivate/{course_id}", response_model=schemas.Course)
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

