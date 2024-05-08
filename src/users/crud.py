from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import src.models as models

from src.users.schemas import NewUserReq



def get_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, email: str, name: str, photo_url: str):
    db_user = models.User(email=email, 
                          name= name, 
                          photo_url = photo_url,
                          linkedin_url = "wait3",
                          seeking_capital = True,
                          created_at = func.now(),
                          updated_at = func.now() 
                          )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


