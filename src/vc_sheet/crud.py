from sqlalchemy.orm import Session
from src.models import Reporter, Investor, Round, InvestorRound


def add_reporters(db: Session, reporters: list[Reporter]):
    print(len(reporters))
    db.add_all(reporters)
    db.commit()


def all_reporters(db: Session, page: int, limit: int):
    return db.query(Reporter).offset(page * 10).limit(limit).all()


def add_investors(db: Session, investors: list[Investor]):
    db.add_all(investors)
    db.commit()

    
        


def all_investors(db: Session, page:int, limit: int):
    return db.query(Investor).offset(page * 10).limit(limit).all()



