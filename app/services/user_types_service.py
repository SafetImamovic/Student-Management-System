from sqlalchemy.orm import Session
from app.database.models.user_types import UserType
from fastapi import HTTPException


class UserTypesService:
    @staticmethod
    def get_count(session: Session) -> int:
        return session.query(UserType).count()

    @staticmethod
    def get_by_id(session: Session, user_type_id: int) -> UserType:
        user_type_db = (session
                        .query(UserType)
                        .filter(UserType.user_type_id == user_type_id)
                        .first())

        if not user_type_db:
            raise HTTPException(status_code=404, detail="User Type not found")

        return user_type_db
