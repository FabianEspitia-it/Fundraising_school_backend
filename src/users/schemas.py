from pydantic import BaseModel
from enum import Enum

class ValidUserReq(BaseModel):
    email: str

class ValidUserRes(BaseModel):
    is_user_saved: bool
    error: str | None = None

class RoundStage(Enum):
    SERIES_A = "series a"


class NewUserReq(BaseModel):
    email: str
    given_name: str
    family_name: str
    picture: str
    locale: str
    seeking_capital: bool = False
    round: RoundStage | None = None
    terms_and_conditions: bool = False

class NewUserRes(BaseModel):
    error: str | None = None