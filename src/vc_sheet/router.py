from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from src.database import get_db
from src.vc_sheet.crud import *
from src.vc_sheet.vc_scraper import *

vc_sheet_router = APIRouter()

# FUND ROUTES

@vc_sheet_router.get("/vc_sheet/funds", tags=["vc_sheet"])
def get_funds(db: Session = Depends(get_db), page: int = 0, limit: int = 10):
    """
    Retrieve a list of venture capital funds.

    Args:
        db (Session, optional): Database session dependency.
        page (int, optional): The page number for pagination. Defaults to 0.
        limit (int, optional): The number of records to return per page. Defaults to 10.

    Returns:
        JSONResponse: A JSON response containing the list of funds.
    """
    return get_all_funds(db=db, page=page, limit=limit)


@vc_sheet_router.get("/vc_sheet/funds/{fund_id}", tags=["vc_sheet"])
def get_fund(fund_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific venture capital fund.

    Args:
        fund_id (int): The unique identifier of the fund.
        db (Session, optional): Database session dependency.

    Returns:
        JSONResponse: A JSON response containing the fund information.

    Raises:
        HTTPException: If the fund does not exist (status code 404).
    
    """
    fund = get_fund_by_id(db=db, fund_id=fund_id)

    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")

    return fund

@vc_sheet_router.post("/vc_sheet/funds/add", tags=["vc_sheet"])
def new_fund(db: Session = Depends(get_db)) -> JSONResponse:
    """
    Scrape and add new venture capital funds to the database.

    Args:
        db (Session, optional): Database session dependency.

    Returns:
        JSONResponse: A JSON response indicating the creation status.
    """
    funds, final_fund_invest, fund_sectors, fund_countries_invest, check_size_range, partner_names, partner_links = vc_scraper_funds()

    create_bulk_fund(
        db=db, 
        funds=funds,
        fund_rounds=final_fund_invest,
        fund_countries=fund_countries_invest,
        fund_partners=partner_names,
        fund_check_size=check_size_range,
        fund_sectors=fund_sectors,
        partner_links=partner_links

    ) 

    return JSONResponse(content={"response": "created"}, status_code=status.HTTP_201_CREATED)

#PARTNER ROUTES

@vc_sheet_router.post("/vc_sheet/partners/add", tags=["vc_sheet"])
def new_partner(db: Session = Depends(get_db)) -> JSONResponse:
    """
    Add new partner information to the database.

    Args:
        db (Session, optional): Database session dependency.

    Returns:
        JSONResponse: A JSON response indicating the creation status.
    """
    add_partners_information(db=db)

    return JSONResponse(content={"response": "created"}, status_code=status.HTTP_201_CREATED)

@vc_sheet_router.get("/vc_sheet/partners/{partner_id}", tags=["vc_sheet"])
def get_partner(partner_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific partner.

    Args:
        partner_id (int): The unique identifier of the partner.
        db (Session, optional): Database session dependency.

    Returns:
        JSONResponse: A JSON response containing the partner information.

    Raises:
        HTTPException: If the partner does not exist (status code 404).
    """
    partner = get_partner_by_id(db=db, partner_id=partner_id)

    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    return partner

"""
ROUTES THAT WE DONT NEED AT THE MOMENT

@vc_sheet_router.post("/reporters/", tags=["vc_sheet"])
def new_reporter(db: Session = Depends(get_db)) -> JSONResponse:
    reporters = vc_scraper_reporters()

    create_bulk_reporters(db=db, reporters=reporters)

    return JSONResponse(content={"response": "created"}, status_code=status.HTTP_201_CREATED)


@vc_sheet_router.get("/vc_sheet/reporters", tags=["vc_sheet"])
def get_reporters(db: Session = Depends(get_db), page: int = 0, limit: int = 10):
    return pagination_reporters(db=db, page=page, limit=limit)


# Investor Routes

@vc_sheet_router.post("/investors/", tags=["vc_sheet"])
def new_investor(db: Session = Depends(get_db)) -> JSONResponse:
    investors, invest = vc_scraper_investors()

    create_bulk_investors(db=db, investors=investors, investor_rounds=invest)

    return JSONResponse(content={"response": "created"}, status_code=status.HTTP_201_CREATED)


@vc_sheet_router.get("/vc_sheet/investors", tags=["vc_sheet"])
def get_investors(db: Session = Depends(get_db), page: int = 0, limit: int = 10):
    return get_all_investors(db=db, page=page, limit=limit)

"""




