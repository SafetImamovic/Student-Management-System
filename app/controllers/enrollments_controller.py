from app.controllers.base_controller import BaseController
from app.database.models.enrollments import Enrollment
from app.database.schemas.enrollments import (
    Enrollment as EnrollmentSchema,
    EnrollmentCreate as EnrollmentCreateSchema
)


class EnrollmentController(BaseController):
    def get_count(self) -> int:
        """
        This function returns the number of enrollments in the database
        :param db:
        :return:
        """

        return self.session.query(Enrollment).count()

    def get_by_id(self, user_id: int, course_id: int):
        """
        This function returns the Enrollment based on the given user_id and course_id composite key
        :param user_id: The user id
        :param course_id: The given course_id
        :return: Enrollment based on the given user_id and course_id composite key
        """

        db_enrollment = self.session.query(Enrollment).filter(Enrollment.user_id == user_id,
                                                              Enrollment.course_id == course_id).first()

        return db_enrollment

    def get_all(self, skip: int = 0, limit: int = 10) -> list[EnrollmentSchema]:
        """
        This function queries the models for the Enrollment with the given skip and limit boundaries
        and returns a list of Enrollments
        :param db: The models session
        :param skip: The starting index of the list, 0 by default
        :param limit: The ending index (skip + limit), 10 by default
        :return: List[models.Enrollment]:
        """

        return self.session.query(Enrollment).offset(skip).limit(limit).all()

    def create(self, enrollment: EnrollmentCreateSchema) -> EnrollmentSchema:
        """
        This function creates a new Enrollment based on the given enrollment pydantic model
        :param db: The models session
        :param enrollment: The given enrollment pydantic model
        :return: Created Enrollment instance
        """

        db_enrollment = Enrollment(**enrollment.dict())

        self.session.add(db_enrollment)

        self.session.commit()

        self.session.refresh(db_enrollment)

        return db_enrollment

    def delete(self, user_id: int, course_id) -> EnrollmentSchema:
        """
        This function deletes an Enrollment based on the given user_id and course_id composite key
        :param user_id:
        :param course_id:
        :return:
        """

        db_enrollment = self.get_by_id(user_id, course_id)

        self.session.delete(db_enrollment)

        self.session.commit()

        return db_enrollment
