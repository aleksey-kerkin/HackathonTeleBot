from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
import os
from models import Vacation

DB_NAME = os.environ.get('DATABASE_URL')
engine = create_engine(DB_NAME)
Base = declarative_base()
Session = sessionmaker(bind=engine)


def create_table():
    Base.metadata.create_all(engine)


def save_vacation(chat_id, vacation):
    session = Session()
    vacation_obj = session.query(Vacation).filter_by(chat_id=chat_id).first()

    if vacation_obj:
        # Если объект уже существует, обновляем его данные
        vacation_obj.start_date = vacation['start_date']
        vacation_obj.end_date = vacation['end_date']
        vacation_obj.is_approved = vacation['is_approved']
        vacation_obj.places_to_visit = vacation.get('places_to_visit', '')
        vacation_obj.tasks = vacation.get('tasks', '')
        vacation_obj.tickets_booked = vacation['tickets_booked']
    else:
        # Если объект не найден, создаем новый
        vacation_obj = Vacation(
            chat_id=chat_id,
            start_date=vacation['start_date'],
            end_date=vacation['end_date'],
            is_approved=vacation['is_approved'],
            places_to_visit=vacation.get('places_to_visit', ''),
            tasks=vacation.get('tasks', ''),
            tickets_booked=vacation['tickets_booked']
        )
        session.add(vacation_obj)

    session.commit()
    session.close()


def get_vacations(chat_id):
    session = Session()
    vacations = session.query(Vacation).filter_by(chat_id=chat_id).all()
    session.close()
    return vacations