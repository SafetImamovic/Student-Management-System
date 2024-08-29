from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.controllers.base_controller import BaseController
from app.database.models.user_types import UserType
from app.database.schemas.user_types import (
    UserType as UserTypeSchema,
    UserTypeCreate as UserTypeCreateSchema
)

from app.services.user_types_service import UserTypesService


class UserTypeController(BaseController):
    def get_count(self) -> int:
        """
        This function returns the number of user_types in the database
        :return:
        """

        return UserTypesService.get_count(self.session)

    def get_by_id(self, user_type_id: int) -> UserTypeSchema:
        """
        This function queries the models for the UserType with the given user_type_id
        :param user_type_id: The user_type_id
        :return: The UserType with the given user_type_id
        """

        return UserTypesService.get_by_id(self.session, user_type_id)

    def get_by_name(self, name: str) -> UserTypeSchema:
        """
        This function queries the models for the UserType with the given name
        :param name: The user_type_name
        :return: The UserType with the given name
        """

        return UserTypesService.get_by_name(self.session, name)

    def get_all(self, skip: int = 0, limit: int = 10) -> list[UserTypeSchema]:
        """
        This function queries the models for the UserType with the given skip and limit boundaries
        and returns a list of UserTypes
        :param skip: Starting index of the list, 0 by default
        :param limit: Ending index (skip + limit), 10 by default
        :return: List[Type[models.UserType]]:
        """

        return UserTypesService.get_all(self.session, skip, limit)

    def create(self, user_type: UserTypeCreateSchema) -> UserTypeSchema:
        """
        This function creates a new UserType
        :param user_type: schemas.UserTypeCreate
        :return: The created UserType
        """

        return UserTypesService.create(self.session, user_type)

    def delete(self, user_type_id: int) -> UserTypeSchema:
        """
        This function deletes a User Type based on the given user_type_id
        :param user_type_id: The user_type_id
        :return: Deleted UserType
        """

        return UserTypesService.delete(self.session, user_type_id)
