from sqlalchemy.orm import Session
from src.models import Reporter


def create_list_reporters(db: Session, reporters: list[Reporter]):
    db.add_all(reporters)
    db.commit()


def pagination_reporters(db: Session, page: int, limit: int):
    return db.query(Reporter).offset(page * 10).limit(limit).all()
