import re

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import src.models as models

from src.users.schemas import NewUserReq
from src.users.linkedin_data import linkedin_data



def get_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def check_email(person_email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, person_email)


def create_user(db: Session, email: str, name: str, photo_url: str):

    user_data = linkedin_data(full_name = name)

    db_user = models.User(email=email, 
                          name= name, 
                          photo_url = photo_url,
                          linkedin_url = user_data["linkedin_url"],
                          followers_amount = user_data["followers_amount"],
                          location = user_data["location"],
                          seeking_capital = True
                          )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


