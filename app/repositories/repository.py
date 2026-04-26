from sqlalchemy.orm import Session
from app.models.weather import Weather


class Repository:
    def __init__(self, db: Session):
        self.db = db

    def save_all(self, items: list[Weather]):
        self.db.add_all(items)
        self.db.commit()