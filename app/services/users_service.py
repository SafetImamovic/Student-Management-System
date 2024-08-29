from sqlalchemy.orm import Session
from app.database.models.users import User
from app.database.schemas.users import UserCreate
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


class UserService:
    @staticmethod
    def get_count(session: Session) -> int:
        return session.query(User).count()

    @staticmethod
    def get_by_id(session: Session, user_id: int) -> User:
        db_user = session.query(User).filter(User.user_id == user_id).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        return db_user

    @staticmethod
    def get_by_email(session: Session, email: str) -> User:
        db_user = session.query(User).filter(User.email == email).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        return db_user

    @staticmethod
    def get_all(session, user_type_id: int = None, skip: int = 0, limit: int = 10):
        if user_type_id is not None:
            return (
                session.query(User)
                .filter(User.user_type_id == user_type_id)
                .offset(skip)
                .limit(limit)
                .all()
            )

        return session.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def create(session: Session, user: UserCreate):
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

        try:
            session.add(db_user)

            session.commit()

            session.refresh(db_user)

        except IntegrityError as e:
            session.rollback()

            raise HTTPException(status_code=409, detail=str(e))

        return db_user

    @staticmethod
    def deactivate(session: Session, user_id: int):
        db_user = session.query(User).filter(User.user_id == user_id).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        if not db_user.is_active:
            raise HTTPException(status_code=409, detail="User is already not active")

        try:
            db_user.is_active = False

            session.commit()

            session.refresh(db_user)

        except IntegrityError as e:
            session.rollback()

            raise HTTPException(status_code=404, detail=str(e))

        return db_user

    @staticmethod
    def activate(session: Session, user_id: int):
        db_user = session.query(User).filter(User.user_id == user_id).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        if db_user.is_active:
            raise HTTPException(status_code=409, detail="User is already active")

        try:
            db_user.is_active = True

            session.commit()

            session.refresh(db_user)

        except IntegrityError as e:
            session.rollback()

            raise HTTPException(status_code=409, detail=str(e))

        return db_user
