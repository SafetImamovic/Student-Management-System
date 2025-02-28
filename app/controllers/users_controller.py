from app.controllers.base_controller import BaseController
from app.database.schemas.users import (
    User as UserSchema,
    UserCreate as UserCreateSchema
)
from app.services.user_types_service import UserTypesService
from app.services.users_service import UserService


class UserController(BaseController):
    def get_count(self) -> int:
        """
        This method returns the number of users in the database
        :return:
        """

        return UserService.get_count(self.session)

    def get_by_id(self, user_id: int) -> UserSchema:
        """
        This method queries the models for the User with the given user_id
        and returns the User with the given user_id
        :param user_id:
        :return User:
        """

        return UserService.get_by_id(self.session, user_id)

    def get_by_email(self, email: str) -> UserSchema:
        """
        This function queries the models for the User with the given email
        and returns the User with the given email
        :param email:
        :return User:
        """

        return UserService.get_by_email(self.session, email)

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
            UserTypesService.get_by_id(self.session, user_type_id)

        users = UserService.get_all(self.session, skip=skip, limit=limit, user_type_id=user_type_id)

        return users

    def create(self, user: UserCreateSchema) -> UserSchema:
        """
        This method creates a new User

        It uses a fake hashing 'algorithm', just appends "fakehashed" to the given password.

        TODO: Change the hashing
        :param user: schemas.UserCreate
        :return: User
        """

        UserTypesService.get_by_id(self.session, user.user_type_id)

        return UserService.create(self.session, user)

    def deactivate(self, user_id: int) -> UserSchema:
        """
        This method deactivates a User
        :param user_id:
        :return:
        """

        return UserService.deactivate(self.session, user_id)

    def activate(self, user_id: int) -> UserSchema:
        """
        This method activates a User
        :param user_id:
        :return:
        """

        return UserService.activate(self.session, user_id)
