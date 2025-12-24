from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from data_interactor import Contact, DatabaseService

router = APIRouter()
db_service = DatabaseService()

class ContactSchema(BaseModel):
    first_name: str
    last_name: str
    phone_number: str

@router.get("/contacts")
def get_contacts():
    contacts = db_service.get_all_contacts()
    return [c.contact_to_dict() for c in contacts]


@router.post("/contacts")
def create_contact(contact: ContactSchema):
    try:
        new_id = db_service.create_contact(contact)
        return {"message": "Contact created successfully", "id": new_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.put("/contacts/{contact_id}")
def update_contact(contact_id: int, contact: ContactSchema):
    success = db_service.update_contact(contact_id, contact)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact updated successfully"}


@router.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    success = db_service.delete_contact(contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}

