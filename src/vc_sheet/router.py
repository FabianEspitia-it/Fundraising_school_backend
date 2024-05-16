from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from src.database import get_db
from src.vc_sheet.crud import *

vc_sheet_router = APIRouter()


@vc_sheet_router.post("/reporters/", tags=["vc_sheet"])
def new_reporter(db: Session = Depends(get_db)):
    reporters = vc_scraper_reporters()

    add_reporters(db=db, reporters=reporters)

    return JSONResponse(content={"response": "created"}, status_code=status.HTTP_201_CREATED)


@vc_sheet_router.get("/vc_sheet/reporters", tags=["vc_sheet"])
def get_reporters(db: Session = Depends(get_db), page: int = 0, limit: int = 10):
    return all_reporters(db=db, page=page, limit=limit)
