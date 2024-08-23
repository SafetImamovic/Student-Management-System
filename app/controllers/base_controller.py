from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db


class BaseController:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def __del__(self):
        self.session.close()
