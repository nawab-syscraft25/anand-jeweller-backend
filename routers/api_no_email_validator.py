"""
Alternative API implementation without email-validator dependency
Use this if you prefer not to install pydantic[email]
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, validator
import re

from database import get_db
from models import GoldRate, Store, ContactEnquiry

router = APIRouter()

# Email validation regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# Pydantic models for request/response (without EmailStr)
class ContactEnquiryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Customer's full name")
    phone_number: str = Field(..., min_length=10, max_length=15, description="Phone number with country code")
    email: str = Field(..., min_length=5, max_length=100, description="Valid email address")
    preferred_store: str = Field(..., min_length=5, max_length=200, description="Name of preferred store")
    preferred_date_time: str = Field(..., min_length=10, max_length=100, description="Preferred appointment date and time")
    
    @validator('email')
    def validate_email(cls, v):
        if not EMAIL_REGEX.match(v):
            raise ValueError('Invalid email format')
        return v
    
    @validator('phone_number')
    def validate_phone(cls, v):
        # Remove spaces and special characters for validation
        clean_phone = re.sub(r'[^\d+]', '', v)
        if not re.match(r'^\+?[\d]{10,15}$', clean_phone):
            raise ValueError('Invalid phone number format')
        return v

class ContactEnquiryResponse(BaseModel):
    id: int
    name: str
    phone_number: str
    email: str
    preferred_store: str
    preferred_date_time: str
    created_at: datetime

    class Config:
        from_attributes = True

class StoreResponse(BaseModel):
    id: int
    store_name: str
    store_address: str
    store_image: Optional[str]
    timings: str
    created_at: datetime

    class Config:
        from_attributes = True

# Store Management APIs
@router.get("/api/stores", response_model=List[StoreResponse])
async def get_all_stores(db: Session = Depends(get_db)):
    """Get all store locations"""
    stores = db.query(Store).order_by(Store.created_at.desc()).all()
    return stores

@router.get("/api/stores/{store_id}", response_model=StoreResponse)
async def get_store_by_id(store_id: int, db: Session = Depends(get_db)):
    """Get a specific store by ID"""
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store

# Contact Enquiry APIs
@router.post("/api/contact-enquiries", response_model=ContactEnquiryResponse)
async def create_contact_enquiry(
    enquiry: ContactEnquiryCreate,
    db: Session = Depends(get_db)
):
    """Create a new contact enquiry"""
    
    # Validate that the preferred store exists
    store_exists = db.query(Store).filter(Store.store_name == enquiry.preferred_store).first()
    if not store_exists:
        # Get all available stores for error message
        available_stores = db.query(Store).all()
        store_names = [store.store_name for store in available_stores]
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid store name. Available stores: {', '.join(store_names)}"
        )
    
    # Create new contact enquiry
    db_enquiry = ContactEnquiry(
        name=enquiry.name,
        phone_number=enquiry.phone_number,
        email=enquiry.email,
        preferred_store=enquiry.preferred_store,
        preferred_date_time=enquiry.preferred_date_time
    )
    
    db.add(db_enquiry)
    db.commit()
    db.refresh(db_enquiry)
    
    return db_enquiry

@router.get("/api/contact-enquiries", response_model=List[ContactEnquiryResponse])
async def get_all_contact_enquiries(
    limit: int = Query(50, description="Maximum number of enquiries to return"),
    db: Session = Depends(get_db)
):
    """Get all contact enquiries (limited for performance)"""
    enquiries = db.query(ContactEnquiry).order_by(
        desc(ContactEnquiry.created_at)
    ).limit(limit).all()
    return enquiries

@router.get("/api/contact-enquiries/{enquiry_id}", response_model=ContactEnquiryResponse)
async def get_contact_enquiry_by_id(enquiry_id: int, db: Session = Depends(get_db)):
    """Get a specific contact enquiry by ID"""
    enquiry = db.query(ContactEnquiry).filter(ContactEnquiry.id == enquiry_id).first()
    if not enquiry:
        raise HTTPException(status_code=404, detail="Contact enquiry not found")
    return enquiry
