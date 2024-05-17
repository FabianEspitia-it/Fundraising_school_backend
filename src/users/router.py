from fastapi import APIRouter, status, Depends, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse

from src.database import get_db
from src.users.linkedin_scraper import user_scraper

from src.users.schemas import NewUserReq
from src.users.crud import *

from src.utils.validations import check_email

user = APIRouter()


@user.get("/user/{email}", tags=["users"])
def user_validate(email: str, db: Session = Depends(get_db)) -> JSONResponse:
    if not check_email(email):
        raise HTTPException(status_code=400, detail="Invalid Email")

    user_record = get_user_by_email(db, email=email)
    if not user_record:
        raise HTTPException(status_code=404, detail="Not Found")

    return user_record


@user.get("/user/education/{email}", tags=["users"])
def user_validate(email: str, db: Session = Depends(get_db)):
    if not check_email(email):
        raise HTTPException(status_code=400, detail="Invalid Email")

    user_education = get_education_by_user_email(db, email=email)
    if not user_education:
        raise HTTPException(status_code=404, detail="Not Found")

    return user_education


@user.get("/user/experience/{email}", tags=["users"])
def user_validate(email: str, db: Session = Depends(get_db)):
    if not check_email(email):
        raise HTTPException(status_code=400, detail="Invalid Email")

    user_experience = get_experience_by_user_email(db, email=email)
    if not user_experience:
        raise HTTPException(status_code=404, detail="Not Found")

    return user_experience


@user.post("/user/new", tags=["users"])
def user_new(new_user: NewUserReq, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if not check_email(new_user.email):
        raise HTTPException(status_code=400, detail="Invalid Email")

    if get_user_by_email(db=db, email=new_user.email):
        raise HTTPException(status_code=400, detail="Email registered")

    background_tasks.add_task(user_scraper, db=db, req=new_user)

    return JSONResponse(content={"response": "created"}, status_code=status.HTTP_201_CREATED)
