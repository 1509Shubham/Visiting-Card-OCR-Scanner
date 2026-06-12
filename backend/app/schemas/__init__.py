from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class ContactBase(BaseModel):
    name: str
    designation: Optional[str] = None
    company_name: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    raw_text: Optional[str] = None
    confidence_score: float = 0.0
    image_path: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    name: Optional[str] = None
    designation: Optional[str] = None
    company_name: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    confidence_score: Optional[float] = None


class ContactResponse(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OCRResponse(BaseModel):
    name: str
    designation: Optional[str] = None
    company_name: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    ocr_confidence: str
    raw_text: str
    image_path: Optional[str] = None
