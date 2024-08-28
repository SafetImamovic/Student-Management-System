from sqlalchemy import text
from sqlalchemy.engine.result import Result

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.controllers.base_controller import BaseController
from app.database.initial_records import (
    default_users,
    default_courses,
    default_enrollments
)
from app.database.models.courses import Course
from app.database.models.enrollments import Enrollment
from app.database.models.user_types import UserType
from app.database.models.users import User


class UtilityController(BaseController):

    def truncate(self) -> Result:
        try:
            truncate_sql = text("truncate user_types, users, courses, enrollments;")

            result = self.session.execute(truncate_sql)

            self.session.commit()

        except IntegrityError as e:
            self.session.rollback()

            raise HTTPException(status_code=400, detail=str(e))

        return result

    def reset_auto_increment(self, table_name: str, column_name: str) -> Result:
        """
        This function resets the autoincrement sequence in a given table
        :param table_name:
        :param column_name:
        :return:
        """

        try:
            reset_sql = text(f"alter sequence {table_name}_{column_name}_seq restart with 1")

            result = self.session.execute(reset_sql)

            self.session.commit()

        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return result

    def seed_user_types(self):
        """
        This function seeds the user_types table with some initial values
        :return:
        """
        try:
            if self.session.query(UserType).count() == 0:
                self.reset_auto_increment('user_types', 'user_type_id')

                default_user_types = ['Admin', 'Student']

                for user_type in default_user_types:
                    self.session.add(UserType(name=user_type))

                self.session.commit()

        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def seed_users(self):
        """
        This function seeds the users table with some initial values
        :return:
        """

        try:
            if self.session.query(User).count() == 0:
                self.reset_auto_increment('users', 'user_id')

                for user in default_users:
                    self.session.add(User(**user))

                self.session.commit()

        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def seed_courses(self):
        """
        This function seeds the courses table with some initial values
        :return:
        """

        try:
            if self.session.query(Course).count() == 0:
                self.reset_auto_increment('courses', 'course_id')

                for course in default_courses:
                    self.session.add(Course(**course))

                self.session.commit()

        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def seed_enrollments(self):
        """
        This function seeds the enrollments table with some initial values
        :return:
        """

        try:
            if self.session.query(Enrollment).count() == 0:

                for enrollment in default_enrollments:
                    self.session.add(Enrollment(**enrollment))

                self.session.commit()

        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=str(e))


def seed(uc: UtilityController):
    uc.seed_user_types()
    uc.seed_users()
    uc.seed_courses()
    uc.seed_enrollments()
