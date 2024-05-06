from fastapi import APIRouter, status
from fastapi.responses import JSONResponse 

from schemas import ValidUserReq
from src.database import conn
from models import users

user = APIRouter()

@user.post("/user/validate", tags=["users"])
def user_validate(valid_user_req: ValidUserReq) -> dict:

    response: bool = False

    # TODO: Validate if the user exists in the database and have the necessary requested data
    user = conn.execute(users.select().where(users.c.email == valid_user_req.email)).first()

    if user:
        response = True

    return JSONResponse(content={"response": response}, status_code=status.HTTP_200_OK)


@user.get("/new/user")
def new_user(new_user: NewUserReq):
    # TODO: Insert request data in the database

    queue.enqueue(new_user.email)
    return
