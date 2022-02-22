from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum


db_file = "sqlite:///pythonsqlite.db"
engine = create_engine(db_file)
Base = declarative_base()


class WeekDays(enum.Enum):
    """This function represent days of the week"""
    mon = 0
    tus = 1
    wed = 2
    thu = 3
    fri = 4
    sat = 5
    sun = 6


class Restaurant(Base):
    """This class represents the restaurants"""
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(32))


class OpenHours(Base):
    """This class represents the range time of open hours of restaurants"""
    __tablename__ = 'open_hours'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    week_day_begin = Column(Integer, Enum(WeekDays, values_callable=lambda x: [str(member.value) for member in WeekDays]))
    week_day_end = Column(Integer, Enum(WeekDays, values_callable=lambda x: [str(member.value) for member in WeekDays]))
    time_begin = Column(String(32))
    time_end = Column(String(32))
    restaurant = Column(Integer, ForeignKey("restaurant.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now())


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

