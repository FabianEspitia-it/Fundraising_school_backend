from sqlalchemy.orm import Session

import src.models as models



def get_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

