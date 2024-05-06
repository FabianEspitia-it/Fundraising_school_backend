from pydantic import BaseModel
from datetime import datetime

class Education(BaseModel):
    id : int
    degree_name : str
    school_name : str
    url_school_logo : str
    linkedin_url : str
    start_year : datetime
    end_year : datetime
    user_id : int

    class Config:
        orm_mode = True