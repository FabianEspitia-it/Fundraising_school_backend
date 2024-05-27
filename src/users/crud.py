from sqlalchemy.orm import Session
from src.users.linkedin_scraper import linkedin_data

from src.models import User


def get_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, name: str, photo_url: str):

    db_user = User(email=email, name=name, photo_url=photo_url)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    user_data = linkedin_data(full_name=name)
    user = get_email(db, email)

    user.linkedin_url = user_data["linkedin_url"]
    user.followers_amount = user_data["followers_amount"]
    

    
    

def create_user_additional_data(db: Session, email: str, nickname: str, contact_email: str):
    user = get_email(db, email)
    user.nickname = nickname
    user.contact_email = contact_email
    db.commit()
    db.refresh(user)
