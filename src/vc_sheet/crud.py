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
    for rounds in fund_rounds:
        for round_stage in rounds:
            round = db.query(Round).filter(Round.stage == round_stage).first()
            
            if not round:
                round = Round(stage=round_stage)
                db.add(round)
                db.commit()
                db.refresh(round)
                print(f"New round created and committed: {round_stage}")
            
            existing_association = db.query(FundRound).filter_by(fund_id=fund_id, round_id=round.id).first()
            if existing_association is None:
                db.add(FundRound(fund_id=fund_id, round_id=round.id))
                db.commit()
                print(f"FundRound association created: fund_id={fund_id}, round_id={round.id}")
        fund_id += 1

    fund_id = 1

    print("Processing fund countries...")
    for countries in fund_countries:
        for country_name in countries:
            country = db.query(Country).filter(Country.name == country_name).first()
            
            if not country:
                country = Country(name=country_name)
                db.add(country)
                db.commit()
                db.refresh(country)
                print(f"New country created and committed: {country_name}")
            
            existing_association = db.query(FundCountry).filter_by(fund_id=fund_id, country_id=country.id).first()
            if existing_association is None:
                db.add(FundCountry(fund_id=fund_id, country_id=country.id))
                db.commit()
                print(f"FundCountry association created: fund_id={fund_id}, country_id={country.id}")
        fund_id += 1

    fund_id = 1

    print("Processing fund partners...")
    for partners in fund_partners:
        for partner_name in partners:
            partner = db.query(Partner).filter(Partner.name == partner_name).first()
            if not partner:
                partner = Partner(name=partner_name)
                db.add(partner)
                db.commit()
                db.refresh(partner)
                print(f"New partner created and committed: {partner_name}")
            existing_association = db.query(FundPartner).filter_by(fund_id=fund_id, partner_id=partner.id).first()
            if existing_association is None:
                db.add(FundPartner(fund_id=fund_id, partner_id=partner.id))
                db.commit()
                print(f"FundPartner association created: fund_id={fund_id}, partner_id={partner.id}")
        fund_id += 1

    fund_id = 1

    print("Processing fund check sizes...")
    for check_sizes in fund_check_size:
        for check_size in check_sizes:
            check = db.query(CheckSize).filter(CheckSize.size == check_size).first()
            if not check:
                check = CheckSize(size=check_size)
                db.add(check)
                db.commit()
                db.refresh(check)
                print(f"New check size created and committed: {check_size}")
            existing_association = db.query(FundCheckSize).filter_by(fund_id=fund_id, check_size_id=check.id).first()
            if existing_association is None:
                db.add(FundCheckSize(fund_id=fund_id, check_size_id=check.id))
                db.commit()
                print(f"FundCheckSize association created: fund_id={fund_id}, check_size_id={check.id}")
        fund_id += 1

    fund_id = 1

    print("Processing fund sectors...")
    for sectors in fund_sectors:
        for sector_name in sectors:
            sector = db.query(Sector).filter(Sector.name == sector_name).first()
            if not sector:
                sector = Sector(name=sector_name)
                db.add(sector)
                db.commit()
                db.refresh(sector)
                print(f"New sector created and committed: {sector_name}")
            existing_association = db.query(FundSector).filter_by(fund_id=fund_id, sector_id=sector.id).first()
            if existing_association is None:
                db.add(FundSector(fund_id=fund_id, sector_id=sector.id))
                db.commit()
                print(f"FundSector association created: fund_id={fund_id}, sector_id={sector.id}")
        fund_id += 1

    partner_id = 1

    print("Updating partner links...")
    for partner_links_group in partner_links:
        for partner_link in partner_links_group:

            name = partner_link.split("/who/")[1].replace("-", " ").title()
            partner = db.query(Partner).filter(Partner.name == name).first()

            if partner:
                partner.vc_link = partner_link
                db.commit()
                db.refresh(partner)
                print(f"Partner link updated for partner_id={fund_id}, vc_link={partner_link}")
            
            partner_id += 1

    
    print("--- %s seconds ---" % (time.time() - start_time))


def total_funds(db: Session):
    """
    Retrieves the total number of funds in the database.

    Args:
        db (Session): Database session object.

    Returns:
        int: Total number of funds.
    """
    return db.query(Fund).count()


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
    return db.query(Fund).options(
        joinedload(Fund.rounds),
        joinedload(Fund.partners),
        joinedload(Fund.check_size),
        joinedload(Fund.countries),
        joinedload(Fund.sectors)
    ).offset((page - 1) * 10).limit(limit).all()


def get_fund_countries_invest(db: Session, fund_id: int) -> list[str]:
    """
    Retrieves the names of the countries where a specific fund has invested.

    Args:
        db (Session): Database session object.
        fund_id (int): ID of the fund to retrieve countries for.

    Returns:
        list[str]: List of country names.
    """
    country_names = db.query(Country.name).join(FundCountry).filter(FundCountry.fund_id == fund_id).all()
    return [country_name[0] for country_name in country_names]


def add_partners_information(db: Session):
    """
    Updates information for all partners in the database.

    Args:
        db (Session): Database session object.

    Returns:
        None
    """
    partner_id = 1

    for _ in range(2588):
        partner = db.query(Partner).filter(Partner.id == partner_id).first()

        if partner:

            try:
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
            except:
                print(f"error: {partner_id} partner")
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
    """
    Retrieves a paginated list of all investors from the database.

    Args:
        db (Session): The database session to use for the query.
        page (int): The page number to retrieve.
        limit (int): The maximum number of investors to return per page.

    Returns:
        List[Investor]: A list of Investor objects.
    """
    return db.query(Investor).offset(page * 10).limit(limit).all()


def get_fund_by_id(db: Session, fund_id: int):
    """
    Retrieves a fund by its ID, along with its related rounds, partners, check size, countries, and sectors.

    Args:
        db (Session): The database session to use for the query.
        fund_id (int): The ID of the fund to retrieve.

    Returns:
        Fund: The Fund object corresponding to the given ID, or None if not found.
    """
    return db.query(Fund).options(
        joinedload(Fund.rounds),
        joinedload(Fund.partners),
        joinedload(Fund.check_size),
        joinedload(Fund.countries),
        joinedload(Fund.sectors)
    ).filter(Fund.id == fund_id).first()


def get_partner_by_id(db: Session, partner_id: int):
    """
    Retrieves a partner by its ID, along with the funds they are associated with and the related rounds, check size, countries, and sectors for each fund.

    Args:
        db (Session): The database session to use for the query.
        partner_id (int): The ID of the partner to retrieve.

    Returns:
        Partner: The Partner object corresponding to the given ID, or None if not found.
    """
    return db.query(Partner).options(
        joinedload(Partner.funds).options(
            joinedload(Fund.rounds),
            joinedload(Fund.check_size),
            joinedload(Fund.countries),
            joinedload(Fund.sectors)
        )
    ).filter(Partner.id == partner_id).first()


def create_bulk_crm_investors(db: Session, crm_investors: list[dict]) -> None:
    """
    Adds multiple CRMInvestor objects to the database in bulk.

    Args:
        db (Session): Database session object.
        crm_investors (list[dict]): List of CRMInvestor objects to be added.

    Returns:
        None
    """

    investor_id_count = 1

    for investor in crm_investors:
        db.add(CrmInvestor(
            name=investor["name"],
            location=investor["location"],
            role=investor["role"],
            vc_link=investor["vc_link"],
            photo=investor["photo"],
            linkedin_investor=investor["investor_linkedin"],
        ))

        for sector in investor["sector_and_stage"]:
            sector = db.query(CrmSectorAndStage).filter(CrmSectorAndStage.name == sector).first()
            if not sector:
                sector = CrmSectorAndStage(name=sector)
                db.add(sector)
                db.commit()
                db.refresh(sector)
                print(f"New sector created and committed: {sector}")
            existing_association = db.query(CrmInvestorSectorAndStage).filter_by(investor_id=investor_id_count, sector_id=sector.id).first()
            if existing_association is None:
                db.add(CrmInvestorSectorAndStage(investor_id=investor["id"], sector_id=sector.id))
                db.commit()
                print(f"CrmInvestorSector association created: investor_id={investor['id']}, sector_id={sector.id}")
        
        for invest_range in investor["invest_range_final"]:
            invest_range = db.query(CrmInvestRange).filter(CrmInvestRange.size == invest_range).first()
            if not invest_range:
                invest_range = CrmInvestRange(size=invest_range)
                db.add(invest_range)
                db.commit()
                db.refresh(invest_range)
                print(f"New invest range created and committed: {invest_range}")
            existing_association = db.query(CrmInvestorInvestRange).filter_by(investor_id=investor_id_count, invest_range_id=invest_range.id).first()
            if existing_association is None:
                db.add(CrmInvestorInvestRange(investor_id=investor["id"], invest_range_id=invest_range.id))
                db.commit()
                print(f"CrmInvestorInvestRange association created: investor_id={investor['id']}, invest_range_id={invest_range.id}")

        investor_id_count += 1

    db.commit()

   


       


    



