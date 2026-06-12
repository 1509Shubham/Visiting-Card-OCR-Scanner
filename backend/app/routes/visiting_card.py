import logging
import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ContactResponse, OCRResponse, ContactUpdate, ContactCreate
from app.services.ocr_service import OCRService
from app.services.contact_service import ContactService
from app.utils.entity_extractor import EntityExtractor
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["visiting_card"])

UPLOAD_DIR = "backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/visiting-card/upload", response_model=dict)
async def upload_visiting_card(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and process a visiting card image"""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Save file
        file_path = os.path.join(UPLOAD_DIR, f"{datetime.now().timestamp()}_{file.filename}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"File saved: {file_path}")
        
        # Validate image
        if not OCRService.validate_image(file_path):
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Extract text using OCR
        extracted_text, confidence = OCRService.extract_text_from_image(file_path)
        
        if not extracted_text:
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="Could not extract text from image")
        
        # Extract entities
        entities = EntityExtractor.extract_all(extracted_text)
        
        # Check for duplicates
        duplicate = ContactService.check_duplicate(
            db,
            email=entities.get('email'),
            mobile=entities.get('mobile')
        )
        
        if duplicate:
            logger.warning(f"Duplicate contact detected: {duplicate.id}")
            # Convert file path to HTTP URL
            filename = os.path.basename(file_path)
            image_url = f"/uploads/{filename}"
            return {
                "status": "duplicate",
                "message": "Contact already exists",
                "existing_id": duplicate.id,
                "extracted_data": {
                    **entities,
                    "confidence_score": confidence,
                    "raw_text": extracted_text,
                    "image_path": image_url
                }
            }
        
        # Create contact
        contact_data = ContactCreate(
            name=entities.get('name', 'Unknown'),
            designation=entities.get('designation'),
            company_name=entities.get('company_name'),
            mobile=entities.get('mobile'),
            email=entities.get('email'),
            website=entities.get('website'),
            address=entities.get('address'),
            raw_text=extracted_text,
            confidence_score=confidence,
            image_path=file_path
        )
        
        contact = ContactService.create_contact(db, contact_data)
        
        # Convert file path to HTTP URL
        filename = os.path.basename(file_path)
        image_url = f"/uploads/{filename}"
        
        return {
            "status": "success",
            "message": "Contact created successfully",
            "contact_id": contact.id,
            "extracted_data": {
                "name": contact.name,
                "designation": contact.designation,
                "company_name": contact.company_name,
                "mobile": contact.mobile,
                "email": contact.email,
                "website": contact.website,
                "address": contact.address,
                "ocr_confidence": f"{confidence}%",
                "image_path": image_url
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading visiting card: {e}")
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/contacts", response_model=list[ContactResponse])
async def get_all_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all contacts with pagination"""
    try:
        contacts = ContactService.get_all_contacts(db, skip=skip, limit=limit)
        return contacts
    except Exception as e:
        logger.error(f"Error fetching contacts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/contact/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific contact by ID"""
    try:
        contact = ContactService.get_contact(db, contact_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        return contact
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching contact: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/contact/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    contact_update: ContactUpdate,
    db: Session = Depends(get_db)
):
    """Update a contact"""
    try:
        contact = ContactService.update_contact(db, contact_id, contact_update)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        return contact
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating contact: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/contact/{contact_id}")
async def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db)
):
    """Delete a contact"""
    try:
        success = ContactService.delete_contact(db, contact_id)
        if not success:
            raise HTTPException(status_code=404, detail="Contact not found")
        return {"status": "success", "message": "Contact deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting contact: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/contacts/search")
async def search_contacts(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """Search contacts by name, email, or mobile"""
    try:
        contacts = ContactService.search_contacts(db, q)
        return contacts
    except Exception as e:
        logger.error(f"Error searching contacts: {e}")
        raise HTTPException(status_code=500, detail=str(e))
