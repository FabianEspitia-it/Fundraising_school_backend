from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse 

from sqlalchemy.orm import Session

from src.database import SessionLocal, engine
from src import models

models.Base.metadata.create_all(bind=engine)

from src.users.schemas import ValidUserReq, User
from src.users.crud import get_email


user = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user.post("/user/validate", tags=["users"])
def user_validate(valid_user_req: ValidUserReq, db: Session = Depends(get_db)) -> dict:

    response: bool = False
    print(valid_user_req)
    if get_email(db, email = valid_user_req.email):
        response = True

    return JSONResponse(content={"response": response}, status_code=status.HTTP_200_OK)


@user.get("/new/user")
def new_user(new_user: User):
    # TODO: Insert request data in the database

    queue.enqueue(new_user.email)
    return
