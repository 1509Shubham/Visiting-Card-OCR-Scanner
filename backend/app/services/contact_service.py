import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import Contact
from app.schemas import ContactCreate, ContactUpdate

logger = logging.getLogger(__name__)


class ContactService:
    """Service for managing contacts"""

    @staticmethod
    def create_contact(db: Session, contact: ContactCreate) -> Contact:
        """Create a new contact"""
        try:
            db_contact = Contact(**contact.dict())
            db.add(db_contact)
            db.commit()
            db.refresh(db_contact)
            logger.info(f"Contact created: {db_contact.id}")
            return db_contact
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating contact: {e}")
            raise

    @staticmethod
    def get_contact(db: Session, contact_id: int) -> Optional[Contact]:
        """Get a contact by ID"""
        return db.query(Contact).filter(Contact.id == contact_id).first()

    @staticmethod
    def get_all_contacts(db: Session, skip: int = 0, limit: int = 100) -> List[Contact]:
        """Get all contacts with pagination"""
        return db.query(Contact).offset(skip).limit(limit).all()

    @staticmethod
    def update_contact(db: Session, contact_id: int, contact_update: ContactUpdate) -> Optional[Contact]:
        """Update a contact"""
        try:
            db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
            if not db_contact:
                return None
            
            update_data = contact_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_contact, field, value)
            
            db.commit()
            db.refresh(db_contact)
            logger.info(f"Contact updated: {contact_id}")
            return db_contact
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating contact: {e}")
            raise

    @staticmethod
    def delete_contact(db: Session, contact_id: int) -> bool:
        """Delete a contact"""
        try:
            db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
            if not db_contact:
                return False
            
            db.delete(db_contact)
            db.commit()
            logger.info(f"Contact deleted: {contact_id}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting contact: {e}")
            raise

    @staticmethod
    def check_duplicate(db: Session, email: Optional[str] = None, mobile: Optional[str] = None) -> Optional[Contact]:
        """Check for duplicate contact by email or mobile"""
        query = db.query(Contact)
        
        if email:
            result = query.filter(Contact.email == email).first()
            if result:
                return result
        
        if mobile:
            result = query.filter(Contact.mobile == mobile).first()
            if result:
                return result
        
        return None

    @staticmethod
    def search_contacts(db: Session, query_str: str) -> List[Contact]:
        """Search contacts by name, email, or mobile"""
        return db.query(Contact).filter(
            (Contact.name.ilike(f"%{query_str}%")) |
            (Contact.email.ilike(f"%{query_str}%")) |
            (Contact.mobile.ilike(f"%{query_str}%"))
        ).all()
