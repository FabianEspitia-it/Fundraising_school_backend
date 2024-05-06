from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class ValidUserReq(BaseModel):
    email: str

class ValidUserRes(BaseModel):
    is_user_saved: bool
    error: str | None = None

class RoundStage(Enum):
    SERIES_A = "series a"

class NewUserRes(BaseModel):
    error: str | None = None


class User(ValidUserReq):
    id: int
    first_name : str
    last_name : str
    followers_amount : int
    linkedin_url : str
    location : str
    photo_url : str
    seeking_capital : bool
    round_id : int
    created_at : datetime
    updated_at : datetime
    deleted_at : datetime
    is_active: bool = True

    class Config:
        orm_mode = True
