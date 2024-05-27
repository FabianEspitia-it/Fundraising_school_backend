from fastapi import APIRouter, status, Depends, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse

from src.database import get_db

from src.users.schemas import NewUserReq, AdditionalDataReq
from src.users.crud import *

from src.utils.validations import check_email

user = APIRouter()


@user.get("/user/{email}", tags=["users"])
def user_validate(email: str, db: Session = Depends(get_db)) -> JSONResponse:
    if not check_email(email):
        raise HTTPException(status_code=400, detail="Invalid Email")

    user_record = get_email(db, email=email)
    if not user_record:
        raise HTTPException(status_code=404, detail="Not Found")

    return user_record


@user.post("/user/new", tags=["users"])
def user_new(new_user: NewUserReq, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

    if not check_email(new_user.email):
        raise HTTPException(status_code=400, detail="Invalid Email")

    background_tasks.add_task(create_user, db=db, email=new_user.email, name=new_user.name,
                              photo_url=new_user.linkedin_picture)

    return JSONResponse(content={"response": "created"}, status_code=status.HTTP_201_CREATED)


@user.post("/user/new/additional", tags=["users"])
def user_additional_data(new_user_additional: AdditionalDataReq, db: Session = Depends(get_db)) -> JSONResponse:
    
    create_user_additional_data(db, new_user_additional.email, new_user_additional.nickname, new_user_additional.contact_email)

    return JSONResponse(content={"response": "created"}, status_code=status.HTTP_201_CREATED)


    

# Agregar un end point que permita agregar seeking capital: bool y las rondas en las que estan interesados, acepta Tyc