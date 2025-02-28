from app.controllers.base_controller import BaseController
from app.database.schemas.enrollments import (
    Enrollment as EnrollmentSchema,
    EnrollmentCreate as EnrollmentCreateSchema
)
from app.services.enrollments_service import EnrollmentsService
from app.services.users_service import UserService
from app.services.courses_service import CourseService


class EnrollmentController(BaseController):
    def get_count(self) -> int:
        """
        This function returns the number of enrollments in the database
        :return:
        """

        return EnrollmentsService.get_count(self.session)

    def get_by_id(self, user_id: int, course_id: int):
        """
        This function returns the Enrollment based on the given user_id and course_id composite key
        :param user_id: The user id
        :param course_id: The given course_id
        :return: Enrollment based on the given user_id and course_id composite key
        """

        return EnrollmentsService.get_by_id(self.session, user_id=user_id, course_id=course_id)

    def get_all(self, skip: int = 0, limit: int = 10) -> list[EnrollmentSchema]:
        """
        This function queries the models for the Enrollment with the given skip and limit boundaries
        and returns a list of Enrollments
        :param skip: The starting index of the list, 0 by default
        :param limit: The ending index (skip + limit), 10 by default
        :return: List[models.Enrollment]:
        """

        return EnrollmentsService.get_all(self.session, skip, limit)

    def create(self, enrollment: EnrollmentCreateSchema) -> EnrollmentSchema:
        """
        This function creates a new Enrollment based on the given enrollment pydantic model
        :param enrollment: The given enrollment pydantic model
        :return: Created Enrollment instance
        """

        UserService.get_by_id(self.session, enrollment.user_id)

        CourseService.get_by_id(self.session, enrollment.course_id)

        return EnrollmentsService.create(self.session, enrollment)

    def delete(self, user_id: int, course_id) -> EnrollmentSchema:
        """
        This function deletes an Enrollment based on the given user_id and course_id composite key
        :param user_id:
        :param course_id:
        :return:
        """

        return EnrollmentsService.delete(self.session, user_id, course_id)
