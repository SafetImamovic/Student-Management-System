from sqlalchemy.orm import Session
from sqlalchemy import text
from ..database.models import user_types, users, enrollments, courses
from ..database.initial_records import *


def reset_auto_increment(db: Session, table_name: str, column_name: str):
    """
    This function resets the autoincrement sequence in a given table
    :param db: The
    :param table_name:
    :param column_name:
    :return:
    """
    # alter sequence user_types_user_type_id_seq restart with 1;
    reset_sql = text(f"alter sequence {table_name}_{column_name}_seq restart with 1")
    db.execute(reset_sql)
    db.commit()


def seed_user_types(db: Session):
    """
    This function seeds the user_types table with some initial values
    :param db:
    :return:
    """
    if db.query(user_types.UserType).count() == 0:
        reset_auto_increment(db, 'user_types', 'user_type_id')

        default_user_types = ['Admin', 'Student']

        for user_type in default_user_types:
            db.add(user_types.UserType(name=user_type))
        db.commit()


def seed_users(db: Session):
    """
    This function seeds the users table with some initial values
    :param db:
    :return:
    """
    if db.query(users.User).count() == 0:
        reset_auto_increment(db, 'users', 'user_id')

        for user in default_users:
            db.add(users.User(**user))
        db.commit()


def seed_courses(db: Session):
    """
    This function seeds the courses table with some initial values
    :param db:
    :return:
    """
    if db.query(courses.Course).count() == 0:
        reset_auto_increment(db, 'courses', 'course_id')

        for course in default_courses:
            db.add(courses.Course(**course))
        db.commit()


def seed_enrollments(db: Session):
    """
    This function seeds the enrollments table with some initial values
    :param db:
    :return:
    """
    if db.query(enrollments.Enrollment).count() == 0:

        for enrollment in default_enrollments:
            db.add(enrollments.Enrollment(**enrollment))
        db.commit()


def seed(db: Session):
    seed_user_types(db)
    seed_users(db)
    seed_courses(db)
    seed_enrollments(db)
