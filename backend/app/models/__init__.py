from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from datetime import datetime
from app.database import Base


class Contact(Base):
    """Contact Master Model"""
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    designation = Column(String(255))
    company_name = Column(String(255))
    mobile = Column(String(20), unique=True, nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    website = Column(String(255))
    address = Column(Text)
    raw_text = Column(Text)
    confidence_score = Column(Float, default=0.0)
    image_path = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Config:
        from_attributes = True
