from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime
from src.database import engine, Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    id = Column(Integrer, primary_key= True)
    email = Column(String(200), unique= True, index= True, nullable=False)
    first_name = Column(String(200), nullable=False)
    last_name = Column(String(200), nullable=True)
    followers_amount = Column(Integer, nullable=False, default=0)
    linkedin_url = Column(String, nullable=False, unique=True)
    location = Column(String, nullable=True)
    photo_url = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    round_id = relationship("round") 







