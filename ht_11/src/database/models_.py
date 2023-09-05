from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    phone_number = Column(String, unique=True, nullable=False)
    birth_date = Column(Date, nullable=True)
    notes = Column(String, nullable=True)
