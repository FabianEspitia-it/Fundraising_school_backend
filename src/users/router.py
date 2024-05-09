from fastapi import APIRouter, status, Depends, BackgroundTasks
from fastapi.responses import JSONResponse 

from sqlalchemy.orm import Session

from src.database import get_db

from src.users.schemas import ValidUserReq, NewUserReq
from src.users.crud import *
from src.users.linkedin_data import linkedin_data


user = APIRouter()


@user.post("/user/validate", tags=["users"])
def user_validate(valid_user_req: ValidUserReq, db: Session = Depends(get_db)) -> dict:

    response: bool = False

    if get_email(db, email = valid_user_req.email):
        response = True

    return JSONResponse(content={"response": response}, status_code=status.HTTP_200_OK)


@user.post("/user/new", tags=["users"])
def new_user(new_user: NewUserReq, background_tasks: BackgroundTasks,  db: Session = Depends(get_db)):

    background_tasks.add_task(create_user, db = db, email=new_user.email, name=new_user.name, photo_url=new_user.linkedin_picture)
    #background_tasks.add_task(linkedin_data, full_name = new_user.name)
    
    return JSONResponse(content={"response": "created"}, status_code=status.HTTP_201_CREATED)
