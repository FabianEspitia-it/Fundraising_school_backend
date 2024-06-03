from sqlalchemy.orm import Session, joinedload

from src.models import *
from src.vc_sheet.vc_scraper import vc_scraper_partners

import time


def create_bulk_fund(db: Session, funds: list[Fund], fund_rounds: list[list[str]], fund_countries: list[list[str]], fund_partners: list[list[str]], fund_check_size: list[list[str]], fund_sectors: list[list[str]], partner_links: list[list[str]]) -> None:
    """
    Adds multiple Fund objects and their related information to the database in bulk.

    Args:
        db (Session): Database session object.
        funds (list[Fund]): List of Fund objects to be added.
        fund_rounds (list[list[str]]): List of fund rounds for each fund.
        fund_countries (list[list[str]]): List of countries for each fund.
        fund_partners (list[list[str]]): List of partners for each fund.
        fund_check_size (list[list[str]]): List of check sizes for each fund.
        fund_sectors (list[list[str]]): List of sectors for each fund.
        partner_links (list[list[str]]): List of partner links for each fund.

    Returns:
        None
    """
    start_time = time.time()

    print("Starting to add funds...")
    db.add_all(funds)
    db.commit()
    print("Funds added and committed.")

    fund_id = 1

    print("Processing fund rounds...")
    for i in fund_rounds:
        for j in i:
            round = db.query(Round).filter(Round.stage == j).first()
            
            if not round:
                round = Round(stage=j)
                db.add(round)
                db.commit()
                db.refresh(round)
                print(f"New round created and committed: {j}")
            
            existing_association = db.query(FundRound).filter_by(fund_id=fund_id, round_id=round.id).first()
            if existing_association is None:
                db.add(FundRound(fund_id=fund_id, round_id=round.id))
                db.commit()
                print(f"FundRound association created: fund_id={fund_id}, round_id={round.id}")
        fund_id += 1

    fund_id = 1

    print("Processing fund countries...")
    for n in fund_countries:
        for m in n:
            country = db.query(Country).filter(Country.name == m).first()
            
            if not country:
                country = Country(name=m)
                db.add(country)
                db.commit()
                db.refresh(country)
                print(f"New country created and committed: {m}")
            
            existing_association = db.query(FundCountry).filter_by(fund_id=fund_id, country_id=country.id).first()
            if existing_association is None:
                db.add(FundCountry(fund_id=fund_id, country_id=country.id))
                db.commit()
                print(f"FundCountry association created: fund_id={fund_id}, country_id={country.id}")
        fund_id += 1

    fund_id = 1

    print("Processing fund partners...")
    for a in fund_partners:
        for name in a:
            partner = db.query(Partner).filter(Partner.name == name).first()
            if not partner:
                partner = Partner(name=name)
                db.add(partner)
                db.commit()
                db.refresh(partner)
                print(f"New partner created and committed: {name}")
            existing_association = db.query(FundPartner).filter_by(fund_id=fund_id, partner_id=partner.id).first()
            if existing_association is None:
                db.add(FundPartner(fund_id=fund_id, partner_id=partner.id))
                db.commit()
                print(f"FundPartner association created: fund_id={fund_id}, partner_id={partner.id}")
        fund_id += 1

    fund_id = 1

    print("Processing fund check sizes...")
    for c in fund_check_size:
        for d in c:
            check = db.query(CheckSize).filter(CheckSize.size == d).first()
            if not check:
                check = CheckSize(size=d)
                db.add(check)
                db.commit()
                db.refresh(check)
                print(f"New check size created and committed: {d}")
            existing_association = db.query(FundCheckSize).filter_by(fund_id=fund_id, check_size_id=check.id).first()
            if existing_association is None:
                db.add(FundCheckSize(fund_id=fund_id, check_size_id=check.id))
                db.commit()
                print(f"FundCheckSize association created: fund_id={fund_id}, check_size_id={check.id}")
        fund_id += 1

    fund_id = 1

    print("Processing fund sectors...")
    for e in fund_sectors:
        for f in e:
            sector = db.query(Sector).filter(Sector.name == f).first()
            if not sector:
                sector = Sector(name=f)
                db.add(sector)
                db.commit()
                db.refresh(sector)
                print(f"New sector created and committed: {f}")
            existing_association = db.query(FundSector).filter_by(fund_id=fund_id, sector_id=sector.id).first()
            if existing_association is None:
                db.add(FundSector(fund_id=fund_id, sector_id=sector.id))
                db.commit()
                print(f"FundSector association created: fund_id={fund_id}, sector_id={sector.id}")
        fund_id += 1

    fund_id = 1

    print("Updating partner links...")
    for g in partner_links:
        for h in g:
            partner = db.query(Partner).filter(Partner.id == fund_id).first()
            
            if partner:
                partner.vc_link = h
                db.commit()
                db.refresh(partner)
                print(f"Partner link updated for partner_id={fund_id}, vc_link={h}")
            
            fund_id += 1
    
    print("--- %s seconds ---" % (time.time() - start_time))

def get_all_funds(db: Session, page: int, limit: int):
    """
    Retrieves all funds from the database with pagination.

    Args:
        db (Session): Database session object.
        page (int): Page number for pagination.
        limit (int): Number of records per page.

    Returns:
        list[Fund]: List of Fund objects.
    """
    return db.query(Fund).offset(page * 10).limit(limit).all()

def add_partners_information(db: Session):
    """
    Updates information for all partners in the database.

    Args:
        db (Session): Database session object.

    Returns:
        None
    """
    partner_id = 1

    for n in range(2587):
        partner = db.query(Partner).filter(Partner.id == partner_id).first()

        partner_dict = vc_scraper_partners(partner.vc_link)

        partner.linkedin = partner_dict["linkedin"]
        partner.twitter = partner_dict["twitter"]
        partner.email = partner_dict["email"]
        partner.description = partner_dict["description"]
        partner.photo = partner_dict["photo"]
        partner.role = partner_dict["role"]
        partner.crunch_base = partner_dict["crunch_base"]
        partner.website = partner_dict["website"]
        db.commit()
        db.refresh(partner)
        print(f"added: {partner_id} partner")
        partner_id += 1

def get_all_partners(db: Session, page: int, limit: int):
    """
    Retrieves all partners from the database with pagination.

    Args:
        db (Session): Database session object.
        page (int): Page number for pagination.
        limit (int): Number of records per page.

    Returns:
        list[Partner]: List of Partner objects.
    """
    return db.query(Partner).offset(page * 10).limit(limit).all()


def create_bulk_reporters(db: Session, reporters: list[Reporter]) -> None:
    """
    Adds multiple Reporter objects to the database in bulk.

    Args:
        db (Session): Database session object.
        reporters (list[Reporter]): List of Reporter objects to be added.

    Returns:
        None
    """
    db.add_all(reporters)
    db.commit()

def get_all_reporters(db: Session, page: int, limit: int):
    """
    Retrieves all reporters from the database with pagination.

    Args:
        db (Session): Database session object.
        page (int): Page number for pagination.
        limit (int): Number of records per page.

    Returns:
        list[Reporter]: List of Reporter objects.
    """
    return db.query(Reporter).offset(page * 10).limit(limit).all()

def create_bulk_investors(db: Session, investors: list[Investor], investor_rounds: list[list[str]]) -> None:
    """
    Adds multiple Investor objects and their related rounds to the database in bulk.

    Args:
        db (Session): Database session object.
        investors (list[Investor]): List of Investor objects to be added.
        investor_rounds (list[list[str]]): List of investment rounds for each investor.

    Returns:
        None
    """
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


def get_fund_by_id(db: Session, fund_id: int):
    return db.query(Fund).options(
        joinedload(Fund.rounds),
        joinedload(Fund.partners),
        joinedload(Fund.check_size),
        joinedload(Fund.countries),
        joinedload(Fund.sectors)
    ).filter(Fund.id == fund_id).first()


def get_partner_by_id(db: Session, partner_id: int):
    return db.query(Partner).options(
        joinedload(Partner.funds).options(
            joinedload(Fund.rounds),
            joinedload(Fund.check_size),
            joinedload(Fund.countries),
            joinedload(Fund.sectors)
        )
    ).filter(Partner.id == partner_id).first()

       


    



