from pydantic import BaseModel
from datetime import datetime


class Round(BaseModel):
    id: int
    stage : str

    class Config:
        orm_mode = True