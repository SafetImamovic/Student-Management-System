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

        return self.session.query(UserType).filter(UserType.name == name).first()

    def get_all(self, skip: int = 0, limit: int = 10) -> list[UserTypeSchema]:
        """
        This function queries the models for the UserType with the given skip and limit boundaries
        and returns a list of UserTypes
        :param skip: Starting index of the list, 0 by default
        :param limit: Ending index (skip + limit), 10 by default
        :return: List[Type[models.UserType]]:
        """

        return self.session.query(UserType).offset(skip).limit(limit).all()

    def create(self, user_type: UserTypeCreateSchema) -> UserTypeSchema:
        """
        This function creates a new UserType
        :param user_type: schemas.UserTypeCreate
        :return: The created UserType
        """

        db_user_type = UserType(
            **user_type.dict()
        )

        self.session.add(db_user_type)

        self.session.commit()

        self.session.refresh(db_user_type)

        return db_user_type

    def delete(self, user_type_id: int) -> UserTypeSchema:
        """
        This function deletes a User Type based on the given user_type_id
        :param user_type_id: The user_type_id
        :return: Deleted UserType
        """

        db_user_type = self.session.query(UserType).filter(UserType.user_type_id == user_type_id).first()

        if not db_user_type:
            raise HTTPException(status_code=404, detail="User type not found")

        try:
            self.session.delete(db_user_type)
            self.session.commit()

        except IntegrityError as e:
            self.session.rollback()
            raise HTTPException(status_code=400, detail=f"Cannot delete user type as it is referenced by other records. You can send a GET request to the relative path /users?user_type_id={user_type_id} to list all users that match the user_type_id.")

        return db_user_type
