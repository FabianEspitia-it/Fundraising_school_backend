from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from src.database import get_db
from src.vc_sheet.crud import *
from src.vc_sheet.vc_scraper import *

vc_sheet_router = APIRouter()


@vc_sheet_router.post("/reporters/", tags=["vc_sheet"])
def new_reporter(db: Session = Depends(get_db)) -> JSONResponse:
    reporters = vc_scraper_reporters()

    create_bulk_reporters(db=db, reporters=reporters)

    return JSONResponse(content={"response": "created"}, status_code=status.HTTP_201_CREATED)


@vc_sheet_router.get("/vc_sheet/reporters", tags=["vc_sheet"])
def get_reporters(db: Session = Depends(get_db), page: int = 0, limit: int = 10):
    return get_all_reporters(db=db, page=page, limit=limit)

# Investor Routes

@vc_sheet_router.post("/investors/", tags=["vc_sheet"])
def new_investor(db: Session = Depends(get_db)) -> JSONResponse:
    investors, invest = vc_scraper_investors()

    create_bulk_investors(db=db, investors= investors, investor_rounds=invest)

    return JSONResponse(content={"response": "created"}, status_code=status.HTTP_201_CREATED)


@vc_sheet_router.get("/vc_sheet/investors", tags=["vc_sheet"])
def get_investors(db: Session = Depends(get_db), page: int = 0, limit: int = 10):
    return get_all_investors(db=db, page=page, limit=limit)


@vc_sheet_router.post("/funds/", tags=["vc_sheet"])
def new_fund(db: Session = Depends(get_db)) -> JSONResponse:
    funds, fund_rounds = vc_scraper_funds()

    create_bulk_fund(db=db, funds=funds, fund_rounds=fund_rounds)

    return JSONResponse(content={"response": "created"}, status_code=status.HTTP_201_CREATED)


@vc_sheet_router.get("/vc_sheet/funds", tags=["vc_sheet"])
def get_funds(db: Session = Depends(get_db), page: int = 0, limit: int = 10):
    return get_all_funds(db=db, page=page, limit=limit)



