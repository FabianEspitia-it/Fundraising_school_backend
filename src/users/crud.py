from sqlalchemy.orm import Session
<<<<<<< HEAD

from src.users.schemas import NewUserReq
=======
>>>>>>> e9755fee1d32a39fdada08c77f5afe7a5f10c5e7

import src.models as models


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


<<<<<<< HEAD
def create_user_principal_data(db: Session, new_user: NewUserReq) -> int:
    user = models.User(first_name = new_user.name.split()[0], email=new_user.email, photo_url=new_user.linkedin_picture)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user.id


"""
def create_user(db: Session, user: models.User) -> int:
    db.add(user)
    db.commit()
    db.refresh(user)

    return user.id
"""

def get_education_by_user_email(db: Session, email: str) -> list[models.Education]:
    return db.query(models.Education).join(models.User).filter(models.User.email == email).all()


def get_experience_by_user_email(db: Session, email: str) -> list[models.Education]:
    return db.query(models.Experience).join(models.User).filter(models.User.email == email).all()


def create_bulk_education(db: Session, education: list[models.Education]) -> None:
    db.add_all(education)
    db.commit()


def create_bulk_experience(db: Session, experiences: list[models.Experience]) -> None:
    db.add_all(experiences)
    db.commit()
=======
def create_user(db: Session, user: models.User) -> int:
    db.add(user)
    db.commit()
    db.refresh(user)

    return user.id


def get_education_by_user_email(db: Session, email: str) -> list[models.Education]:
    return db.query(models.Education).join(models.User).filter(models.User.email == email).all()


def get_experience_by_user_email(db: Session, email: str) -> list[models.Education]:
    return db.query(models.Experience).join(models.User).filter(models.User.email == email).all()


def create_bulk_education(db: Session, education: list[models.Education]) -> None:
    db.add_all(education)
    db.commit()


def create_bulk_experience(db: Session, experiences: list[models.Experience]) -> None:
    db.add_all(experiences)
    db.commit()
>>>>>>> e9755fee1d32a39fdada08c77f5afe7a5f10c5e7
