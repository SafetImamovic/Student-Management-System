from app.controllers.base_controller import BaseController
from app.database.models.users import User
from app.database.schemas.users import (
    User as UserSchema,
    UserCreate as UserCreateSchema
)

from app.controllers.user_types_controller import UserTypeController


class UserController(BaseController):
    def get_count(self) -> int:
        """
        This method returns the number of users in the database
        :return:
        """

        return self.session.query(User).count()

    def get_by_id(self, user_id: int) -> UserSchema:
        """
        This method queries the models for the User with the given user_id
        and returns the User with the given user_id
        :param user_id:
        :return User:
        """

        return self.session.query(User).filter(User.user_id == user_id).first()

    def get_by_email(self, email: str) -> UserSchema:
        """
        This function queries the models for the User with the given email
        and returns the User with the given email
        :param email:
        :return User:
        """

        return self.session.query(User).filter(User.email == email).first()

    def get_all(self, user_type_id: int = None, skip: int = 0, limit: int = 10) -> list[UserSchema]:
        """
        This method queries the models for Users with the given skip and limit boundaries
        and returns a list of Users
        :param skip:
        :param limit:
        :param user_type_id:
        :return:
        """

        if user_type_id is not None:
            return (
                self.session.query(User)
                .filter(User.user_type_id == user_type_id)
                .offset(skip)
                .limit(limit)
                .all()
            )

        return self.session.query(User).offset(skip).limit(limit).all()

    def create(self, user: UserCreateSchema) -> UserSchema:
        """
        This method creates a new User

        It uses a fake hashing 'algorithm', just appends "fakehashed" to the given password.

        TODO: Change the hashing
        :param user: schemas.UserCreate
        :return: User
        """
        hashed_password = user.password + "fakehashed"

        db_user = User(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            age=user.age,
            is_active=user.is_active,
            user_type_id=user.user_type_id,
            hashed_password=hashed_password
        )

        self.session.add(db_user)

        self.session.commit()

        self.session.refresh(db_user)

        return db_user

    def deactivate(self, user_id: int) -> UserSchema:

        db_user = self.session.query(User).filter(User.user_id == user_id).first()

        if db_user:
            db_user.is_active = False

            self.session.commit()

            self.session.refresh(db_user)

        return db_user

    def activate(self, user_id: int) -> UserSchema:

        db_user = self.session.query(User).filter(User.user_id == user_id).first()

        if db_user:
            db_user.is_active = True

            self.session.commit()

            self.session.refresh(db_user)

        return db_user
