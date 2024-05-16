from sqlalchemy.orm import Session
from src.users.linkedin_scraper import linkedin_data

import src.models as models


def get_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, email: str, name: str, photo_url: str):
    user_data = linkedin_data(full_name=name)

    db_user = models.User(email=email,
                          name=name,
                          photo_url=photo_url,
                          linkedin_url=user_data["linkedin_url"],
                          followers_amount=user_data["followers_amount"],
                          location=user_data["location"]
                          )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
