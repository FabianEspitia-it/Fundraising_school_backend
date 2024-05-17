from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime, Text
from src.database import engine, Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Round(Base):
    __tablename__ = "round"
    id = Column(Integer, primary_key=True)
    stage = Column(String(200), nullable=False)

    user = relationship("User", back_populates="stage_round")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String(200), unique=True, index=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    followers_amount = Column(Integer, nullable=False, default=0)
    linkedin_url = Column(String(255), nullable=False, unique=True)
    location = Column(String(255), nullable=True)
    seeking_capital = Column(Boolean, nullable=True)
    photo_url = Column(String(255), nullable=False, unique=True)
    industry = Column(String(255), nullable=True, unique=False)
    summary = Column(Text, nullable=True, unique=False)
    headline = Column(Text, nullable=True, unique=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    round_id = Column(Integer, ForeignKey("round.id"))
    stage_round = relationship("Round", back_populates="user")

    education = relationship("Education", back_populates="user")
    experience = relationship("Experience", back_populates="user")


class Education(Base):
    __tablename__ = "education"
    id = Column(Integer, primary_key=True)
    degree_name = Column(String(200), nullable=True)
    grade = Column(String(200), nullable=True)
    school_name = Column(String(200), nullable=False)
    linkedin_url = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="education")


class Experience(Base):
    __tablename__ = "experience"
    id = Column(Integer, primary_key=True)
    company = Column(String(200), nullable=False)
    location = Column(String(255), nullable=True)
    linkedin_url = Column(String(255), nullable=False)
    role = Column(String(200), nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    description = Column(Text, nullable=True)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="experience")


# VC MODELS

class Reporter(Base):
    __tablename__ = "vc_reporter"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    photo = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    email = Column(String(200), nullable=True)
    twitter = Column(String(255), nullable=True)
    linkedin = Column(String(255), nullable=True)
    channel_url = Column(String(255), nullable=True)
    channel_image = Column(String(255), nullable=True)
    location = Column(String(50), nullable=True)
    company = Column(String(50), nullable=True)




Base.metadata.create_all(bind=engine)


