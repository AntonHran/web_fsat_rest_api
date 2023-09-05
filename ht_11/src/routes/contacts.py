from typing import List
from datetime import date

from fastapi import Depends, HTTPException, Path, Query, APIRouter, status
from sqlalchemy.orm import Session

from ht_11.src.database.database_ import get_db
from ht_11.src.repository import contacts as repository_contacts
from ht_11.src.schemas_ import ContactModel, ContactResponse


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(
    limit: int = Query(10, le=100), offset: int = 0, db: Session = Depends(get_db)
):
    contacts = await repository_contacts.get_all(limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.create_contact(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)
):
    contact = await repository_contacts.update(contact_id, body, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove(contact_id, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/search/", response_model=List[ContactResponse])
async def search_by(parameter: str | int, db: Session = Depends(get_db)):
    contacts = await repository_contacts.search(parameter, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts


@router.get("/birthdays/", response_model=List[ContactResponse])
async def get_birthdays(db: Session = Depends(get_db)):
    contacts = await repository_contacts.birthdays(db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts
