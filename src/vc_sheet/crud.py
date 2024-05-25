from sqlalchemy.orm import Session
from src.models import *


def create_bulk_reporters(db: Session, reporters: list[Reporter]) -> None:
    db.add_all(reporters)
    db.commit()


def pagination_reporter(db: Session, page: int, limit: int):
    return db.query(Reporter).offset(page * 10).limit(limit).all()


def create_bulk_investors(db: Session, investors: list[Investor], investor_rounds: list[list[str]]) -> None:
    db.add_all(investors)
    db.commit()

    investor_id = 1

    for i in investor_rounds:
        for j in i:
            db.add(InvestorRound(investor_id=investor_id, round_id=db.query(Round).filter(Round.stage == j).first().id))
            db.commit()
        investor_id += 1


def get_all_investors(db: Session, page: int, limit: int):
    return db.query(Investor).offset(page * 10).limit(limit).all()


def create_bulk_fund(db: Session, funds: list[Fund], fund_rounds: list[list[str]]) -> None:
    db.add_all(funds)
    db.commit()

    fund_id = 1

    for i in fund_rounds:
        for j in i:
            db.add(FundRound(fund_id=fund_id, round_id=db.query(Round).filter(Round.stage == j).first().id))
            db.commit()
        fund_id += 1


def get_all_funds(db: Session, page: int, limit: int):
    return db.query(Fund).offset(page * 10).limit(limit).all()