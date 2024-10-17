from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Vacation(Base):
    __tablename__ = 'vacation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, unique=True, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    is_approved = Column(Boolean, default=False)
    places_to_visit = Column(String)
    tasks = Column(String)
    tickets_booked = Column(Boolean, default=False)

