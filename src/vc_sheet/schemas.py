from pydantic import BaseModel
from typing import List


class Round(BaseModel):
    id: int
    stage: str

    class Config:
        orm_mode = True

class Partner(BaseModel):
    id: int
    name: str
    role: str
    photo: str
    email: str
    twitter: str
    linkedin: str
    crunch_base: str
    website: str
    description: str

    class Config:
        orm_mode = True

class CheckSize(BaseModel):
    id: int
    size: str

    class Config:
        orm_mode = True

class Country(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Sector(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class FundBase(BaseModel):
    id: int
    name: str 
    website: str
    description: str
    location: str
    photo: str
    twitter: str
    linkedin: str
    crunch_base: str
    contact: str




class Fund(FundBase):
    rounds: List[Round] = []
    partners: List[Partner] = []
    check_size: List[CheckSize] = []
    countries: List[Country] = []
    sectors: List[Sector] = []
    

    class Config:
        orm_mode = True
