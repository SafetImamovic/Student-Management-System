from sqlalchemy.orm import Session
from app.database.models.enrollments import Enrollment
from fastapi import HTTPException
from app.database.schemas.enrollments import EnrollmentCreate
from sqlalchemy.exc import IntegrityError


class EnrollmentsService:
    @staticmethod
    def get_count(session: Session) -> int:
        return session.query(Enrollment).count()

    @staticmethod
    def get_by_id(session: Session, user_id: int, course_id) -> Enrollment:
        db_enrollment = session.query(Enrollment).filter(Enrollment.user_id == user_id,
                                                         Enrollment.course_id == course_id).first()

        if not db_enrollment:
            raise HTTPException(status_code=404, detail="Enrollment not found")

        return db_enrollment

    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 10) -> list[Enrollment]:
        return session.query(Enrollment).offset(skip).limit(limit).all()

    @staticmethod
    def create(session: Session, enrollment: EnrollmentCreate) -> Enrollment:
        db_enrollment = session.query(Enrollment).filter(Enrollment.user_id == enrollment.user_id,
                                                         Enrollment.course_id == enrollment.course_id).first()

        if db_enrollment:
            raise HTTPException(status_code=409,
                                detail=f"Enrollment already exists with the user_id: {enrollment.user_id} and course_id: {enrollment.course_id}")

        db_enrollment_create = Enrollment(**enrollment.dict())

        try:
            session.add(db_enrollment_create)

            session.commit()

            session.refresh(db_enrollment_create)

        except IntegrityError as e:
            session.rollback()

            raise HTTPException(status_code=409, detail=str(e))

        return db_enrollment_create

    @staticmethod
    def delete(session: Session, user_id: int, course_id: int) -> Enrollment:
        db_enrollment = session.query(Enrollment).filter(Enrollment.user_id == user_id,
                                                         Enrollment.course_id == course_id).first()

        if not db_enrollment:
            raise HTTPException(status_code=409,
                                detail=f"Enrollment doesn't exist with the user_id: {user_id} and course_id: {course_id}")

        try:
            session.delete(db_enrollment)

            session.commit()

        except IntegrityError as e:
            session.rollback()

            raise HTTPException(status_code=409, detail=str(e))

        return db_enrollment
