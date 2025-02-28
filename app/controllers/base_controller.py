from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db


class BaseController:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
        print(f"Session: {session}")

    def __del__(self):
        print(f"__del__: {self.session}")
        self.session.close()

