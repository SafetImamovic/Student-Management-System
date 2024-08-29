from sqlalchemy.orm import Session
from app.database.models.courses import Course
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


class CourseService:
    @staticmethod
    def get_count(session: Session) -> int:
        return session.query(Course).count()

    @staticmethod
    def get_by_id(session: Session, course_id: int) -> Course:
        db_course = session.query(Course).filter(Course.course_id == course_id).first()

        if not db_course:
            raise HTTPException(status_code=404, detail="Course not found")

        return db_course

    @staticmethod
    def get_by_name(session: Session, name: str) -> Course:
        db_course = session.query(Course).filter(Course.name == name).first()

        if not db_course:
            raise HTTPException(status_code=404, detail="Course not found")

        return db_course

    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 10) -> list[Course]:
        return session.query(Course).offset(skip).limit(limit).all()

    @staticmethod
    def create(session: Session, course: Course) -> Course:

        db_course = session.query(Course).filter(Course.name == course.name).first()

        if db_course:
            raise HTTPException(status_code=409, detail="Course already exists")

        db_course_create = Course(**course.dict())

        try:
            session.add(db_course_create)

            session.commit()

            session.refresh(db_course_create)

        except IntegrityError as e:
            session.rollback()

            raise HTTPException(status_code=409, detail=str(e))

        return db_course_create

    @staticmethod
    def deactivate(session: Session, course_id: int) -> Course:
        db_course = session.query(Course).filter(Course.course_id == course_id).first()

        if not db_course:
            raise HTTPException(status_code=404, detail="Course not found")

        if not db_course.is_active:
            raise HTTPException(status_code=409, detail="Course is already not active")

        try:
            db_course.is_active = False

            session.commit()

            session.refresh(db_course)
        except IntegrityError as e:
            session.rollback()

            raise HTTPException(status_code=409, detail=str(e))

        return db_course

    @staticmethod
    def activate(session: Session, course_id: int) -> Course:
        db_course = session.query(Course).filter(Course.course_id == course_id).first()

        if not db_course:
            raise HTTPException(status_code=404, detail="Course not found")

        if db_course.is_active:
            raise HTTPException(status_code=409, detail="Course is already active")

        try:
            db_course.is_active = True

            session.commit()

            session.refresh(db_course)

        except IntegrityError as e:
            session.rollback()

            raise HTTPException(status_code=409, detail=str(e))

        return db_course
