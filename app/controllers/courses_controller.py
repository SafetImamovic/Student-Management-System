from app.controllers.base_controller import BaseController
from app.database.models.courses import Course
from app.database.schemas.courses import (
    Course as CourseSchema,
    CourseCreate as CourseCreateSchema
)
from app.services.courses_service import CourseService


class CourseController(BaseController):

    def get_count(self) -> int:
        """
        This function returns the number of courses in the database
        :return:
        """

        return CourseService.get_count(self.session)

    def get_by_id(self, course_id: int) -> CourseSchema:
        """
        This function queries the models for the Course with the given course_id
        and returns the Course with the given course_id
        :param course_id: Pydantic Course model
        :return: Course with the given course_id
        """

        return CourseService.get_by_id(self.session, course_id)

    def get_by_name(self, name: str) -> CourseSchema:
        """
        This function queries the models for the Course with the given name
        :param name: Course name
        :return: Course with given name
        """

        return CourseService.get_by_name(self.session, name)

    def get_all(self, skip: int = 0, limit: int = 10) -> list[CourseSchema]:
        """
        This function queries the models for the Course with the given skip and limit boundaries
        and returns a list of Courses
        :param skip: The starting index of the list, 0 by default
        :param limit: The ending index (skip + limit), 10 by default
        :return: List[Type[Course]]:
        """

        return CourseService.get_all(self.session, skip, limit)

    def create(self, course: CourseCreateSchema) -> CourseSchema:
        """
        This function creates a new Course based on the given course pydantic model
        :param course: Pydantic Course model
        :return: Created Course
        """

        return CourseService.create(self.session, course)

    def deactivate(self, course_id: int) -> CourseSchema:
        """
        This method deactivates a course based on the given course_id
        :param course_id:
        :return:
        """
        return CourseService.deactivate(self.session, course_id)

    def activate(self, course_id: int) -> CourseSchema:
        """
        This method activates a course based on the given course_id
        :param course_id:
        :return:
        """
        return CourseService.activate(self.session, course_id)
