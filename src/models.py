from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime, Text
from src.database import engine, Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class FundRound(Base):
    __tablename__ = 'fund_rounds'

    fund_id = Column(Integer, ForeignKey('vc_fund.id'), primary_key=True)
    round_id = Column(Integer, ForeignKey('round.id'), primary_key=True)

    fund = relationship("Fund", foreign_keys=[fund_id])
    round = relationship("Round", foreign_keys=[round_id])


class InvestorRound(Base):
    __tablename__ = 'investor_rounds'

    investor_id = Column(Integer, ForeignKey('vc_investor.id'), primary_key=True)
    round_id = Column(Integer, ForeignKey('round.id'), primary_key=True)

    investor = relationship("Investor", foreign_keys=[investor_id])
    round = relationship("Round", foreign_keys=[round_id])


class Round(Base):
    __tablename__ = "round"
    id = Column(Integer, primary_key=True)
    stage = Column(String(200), nullable=False)

    user = relationship("User", back_populates="stage_round")
    investor = relationship("Investor", secondary="investor_rounds", back_populates='rounds')
    fund = relationship("Fund", secondary="fund_rounds", back_populates='rounds')


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
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    round_id = Column(Integer, ForeignKey("round.id"))
    stage_round = relationship("Round", back_populates="user")

    education = relationship("Education", back_populates="user")
    job = relationship("Job", back_populates="user")


class Education(Base):
    __tablename__ = "education"
    id = Column(Integer, primary_key=True)
    degree_name = Column(String(200), nullable=False)
    school_name = Column(String(200), nullable=False)
    url_school_logo = Column(String(255), nullable=False)
    linkedin_url = Column(String(255), nullable=False)
    start_year = Column(DateTime, nullable=False)
    end_year = Column(DateTime, nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="education")


class Job(Base):
    __tablename__ = "job"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    website_url = Column(String(200), nullable=False)
    url_logo = Column(String(255), nullable=False)
    amount_employees = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    industry = Column(String(255), nullable=False)
    linkedin_url = Column(String(255), nullable=False)
    current = Column(Boolean, nullable=False)
    role = Column(String(200), nullable=False)
    start_year = Column(DateTime, nullable=False)
    end_year = Column(DateTime, nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="job")


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


class Investor(Base):
    __tablename__ = "vc_investor"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    photo = Column(String(255), nullable=True)
    role = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    email = Column(String(255), nullable=True)
    twitter = Column(Text, nullable=True)
    linkedin = Column(Text, nullable=True)
    crunch_base = Column(Text, nullable=True)
    youtube = Column(Text, nullable=True)

    rounds = relationship("Round", secondary="investor_rounds", back_populates='investor')


class Fund(Base):
    __tablename__ = "vc_fund"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    photo = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    twitter = Column(String(255), nullable=True)
    linkedin = Column(String(255), nullable=True)
    crunch_base = Column(String(255), nullable=True)

    rounds = relationship("Round", secondary="fund_rounds", back_populates='fund')



Base.metadata.create_all(bind=engine)


