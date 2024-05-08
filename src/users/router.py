from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse 

from sqlalchemy.orm import Session

from src.database import get_db


from src.users.schemas import ValidUserReq, User
from src.users.crud import get_email
from src.users.linkedin_data import get_user_data


user = APIRouter()


@user.post("/user/validate", tags=["users"])
def user_validate(valid_user_req: ValidUserReq, db: Session = Depends(get_db)) -> dict:

    response: bool = False
    print(valid_user_req)
    if get_email(db, email = valid_user_req.email):
        response = True

    return JSONResponse(content={"response": response}, status_code=status.HTTP_200_OK)


@user.post("/new/user", tags=["users"])
def new_user(new_user: ValidUserReq):

    return JSONResponse(content=get_user_data(new_user.email), status_code=status.HTTP_200_OK)
