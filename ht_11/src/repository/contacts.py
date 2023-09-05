from datetime import date, timedelta
import logging

# from fastapi import Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ht_11.src.database.models_ import Contact
from ht_11.src.schemas_ import ContactModel

logger = logging.getLogger(__name__)


async def get_all(limit: int, offset: int, db: Session):
    contacts: list = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def create_contact(body: ContactModel, db: Session):
    contact = Contact(**body.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.phone_number = body.phone_number
        contact.email = body.email
        contact.birth_date = body.birth_date
        contact.notes = body.notes
        db.commit()
        db.refresh(contact)
    return contact


async def remove(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search(parameter: str | int, db: Session):
    attributes: list[str] = list(vars(Contact).keys())
    result = []
    for attribute in attributes:
        try:
            query = db.query(Contact).filter(
                    getattr(Contact, attribute).ilike('%'+parameter+'%')
                    if attribute != "id"
                    else None
                ).all()
        except Exception as error:
            logger.error(f"Error during proceeding SQL-query: {str(error)}")
            continue
        if query:
            result.extend([rec for rec in query if rec not in result])
    return result


async def search_2(parameter: str | int | date, db: Session):  # limit: int, offset: int,
    filters = [
        getattr(Contact, attr).ilike(f"%{parameter}%")
        for attr in Contact.__table__.columns.keys()
    ]
    query = db.query(Contact).filter(or_(*filters))
    # query = query.limit(limit).offset(offset)
    contacts = query.all()
    return contacts


async def birthdays(db: Session):
    current_date = date.today()
    dates: list = [current_date + timedelta(days=i) for i in range(7)]
    result = []
    contacts = [
        contact
        for contact in await get_all(limit=100, offset=0, db=db)
        if contact.birth_date
    ]
    for contact in contacts:
        b_date = date(
            year=current_date.year,
            month=contact.birth_date.month,
            day=contact.birth_date.day,
        )
        if b_date in dates:
            result.append(contact)
    return result
