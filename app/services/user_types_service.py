from sqlalchemy.orm import Session
from app.database.models.user_types import UserType
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


class UserTypesService:
    @staticmethod
    def get_count(session: Session) -> int:
        return session.query(UserType).count()

    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 10) -> list[UserType]:
        return session.query(UserType).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(session: Session, user_type_id: int) -> UserType:
        user_type_db = (session
                        .query(UserType)
                        .filter(UserType.user_type_id == user_type_id)
                        .first())

        if not user_type_db:
            raise HTTPException(status_code=404, detail="User Type not found")

        return user_type_db

    @staticmethod
    def get_by_name(session: Session, name: str) -> UserType:
        db_user_type = session.query(UserType).filter(UserType.name == name).first()

        if not db_user_type:
            raise HTTPException(status_code=404, detail="User not found")

        return db_user_type

    @staticmethod
    def create(session: Session, user_type: UserType) -> UserType:

        db_user_type = UserType(
            **user_type.dict()
        )

        try:
            session.add(db_user_type)

            session.commit()

            session.refresh(db_user_type)
        except IntegrityError as e:
            session.rollback()

            raise HTTPException(status_code=409, detail=str(e))

        return db_user_type

    @staticmethod
    def delete(session: Session, user_type_id: int) -> UserType:
        db_user_type = session.query(UserType).filter(UserType.user_type_id == user_type_id).first()

        if not db_user_type:
            raise HTTPException(status_code=404, detail="User type not found")

        try:
            session.delete(db_user_type)

            session.commit()

        except IntegrityError:
            session.rollback()

            raise HTTPException(status_code=400,
                                detail=f"Cannot delete user type as it is referenced by other records. You can send a GET request to the relative path /users?user_type_id={user_type_id} to list all users that match the user_type_id.")

        return db_user_type
