from pydantic import BaseModel
from datetime import datetime

class Job(BaseModel):
    id : int
    name : str
    website_url : str
    url_logo : str
    amount_employees : int
    country : str
    industry : str
    linkedin_url : str
    current : bool
    rol : str
    start_year : datetime
    end_year : datetime

    class Config:
        orm_mode = True