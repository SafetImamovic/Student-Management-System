from app.controllers.base_controller import BaseController
from app.database.models.courses import Course
from app.database.schemas.courses import (
    Course as CourseSchema,
    CourseCreate as CourseCreateSchema
)


class CourseController(BaseController):

    def get_count(self) -> int:
        """
        This function returns the number of courses in the database
        :return:
        """

        return self.session.query(Course).count()

    def get_by_id(self, course_id: int) -> CourseSchema:
        """
        This function queries the models for the Course with the given course_id
        and returns the Course with the given course_id
        :param course_id: Pydantic Course model
        :return: Course with the given course_id
        """

        return self.session.query(Course).filter(Course.course_id == course_id).first()

    def get_by_name(self, name: str) -> CourseSchema:
        """
        This function queries the models for the Course with the given name
        :param name: Course name
        :return: Course with given name
        """

        return self.session.query(Course).filter(Course.name == name).first()

    def get_all(self, skip: int = 0, limit: int = 10) -> list[CourseSchema]:
        """
        This function queries the models for the Course with the given skip and limit boundaries
        and returns a list of Courses
        :param skip: The starting index of the list, 0 by default
        :param limit: The ending index (skip + limit), 10 by default
        :return: List[Type[Course]]:
        """

        return self.session.query(Course).offset(skip).limit(limit).all()

    def create(self, course: CourseCreateSchema) -> CourseSchema:
        """
        This function creates a new Course based on the given course pydantic model
        :param course: Pydantic Course model
        :return: Created Course
        """

        db_course = Course(**course.dict())

        self.session.add(db_course)

        self.session.commit()

        self.session.refresh(db_course)

        return db_course

    def deactivate(self, course_id: int) -> CourseSchema:
        db_course = self.session.query(Course).filter(Course.course_id == course_id).first()

        if db_course:
            db_course.is_active = False

            self.session.commit()

            self.session.refresh(db_course)

        return db_course

    def activate(self, course_id: int) -> CourseSchema:
        db_course = self.session.query(Course).filter(Course.course_id == course_id).first()

        if db_course:
            db_course.is_active = True

            self.session.commit()

            self.session.refresh(db_course)

        return db_course
