"""
Admin API routes with JWT authentication
"""
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, validator

from database import get_db
from models import GoldRate, AdminUser
from jwt_auth import get_current_admin_user, JWTAuth

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Pydantic models for admin operations
class GoldRateCreate(BaseModel):
    # 24K rates
    gold_24k_new_rate: float
    gold_24k_exchange_rate: float
    gold_24k_making_charges: float
    
    # 22K rates
    gold_22k_new_rate: float
    gold_22k_exchange_rate: float
    gold_22k_making_charges: float
    
    # 18K rates
    gold_18k_new_rate: float
    gold_18k_exchange_rate: float
    gold_18k_making_charges: float
    
    release_datetime: datetime

class GoldRateUpdate(BaseModel):
    # 24K rates
    gold_24k_new_rate: float
    gold_24k_exchange_rate: float
    gold_24k_making_charges: float
    
    # 22K rates
    gold_22k_new_rate: float
    gold_22k_exchange_rate: float
    gold_22k_making_charges: float
    
    # 18K rates
    gold_18k_new_rate: float
    gold_18k_exchange_rate: float
    gold_18k_making_charges: float

class GoldRateResponse(BaseModel):
    id: int
    
    # 24K rates
    gold_24k_new_rate: float
    gold_24k_exchange_rate: float
    gold_24k_making_charges: float
    
    # 22K rates
    gold_22k_new_rate: float
    gold_22k_exchange_rate: float
    gold_22k_making_charges: float
    
    # 18K rates
    gold_18k_new_rate: float
    gold_18k_exchange_rate: float
    gold_18k_making_charges: float
    
    release_datetime: datetime
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

# Admin Authentication Endpoints
@router.post("/login", response_model=TokenResponse)
async def admin_login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Admin login endpoint that returns JWT token"""
    
    # Authenticate user
    user = JWTAuth.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = JWTAuth.create_access_token(
        data={"sub": user.username, "user_id": user.id}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 30 * 60  # 30 minutes in seconds
    }

@router.get("/verify-token")
async def verify_token(current_user: AdminUser = Depends(get_current_admin_user)):
    """Verify if the current JWT token is valid"""
    return {
        "valid": True,
        "user": {
            "id": current_user.id,
            "username": current_user.username
        }
    }

# Gold Rate Management Endpoints (JWT Protected)
@router.get("/gold-rates", response_model=List[GoldRateResponse])
async def get_all_gold_rates(
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all gold rates (Admin only)"""
    rates = db.query(GoldRate).order_by(GoldRate.release_datetime.desc()).all()
    return rates

@router.post("/gold-rates", response_model=GoldRateResponse)
async def create_gold_rate(
    rate_data: GoldRateCreate,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new gold rate entry for all three purities (Admin only)"""
    
    # Create new gold rate entry with all three purities
    new_rate = GoldRate(
        # 24K rates
        gold_24k_new_rate=rate_data.gold_24k_new_rate,
        gold_24k_exchange_rate=rate_data.gold_24k_exchange_rate,
        gold_24k_making_charges=rate_data.gold_24k_making_charges,
        
        # 22K rates
        gold_22k_new_rate=rate_data.gold_22k_new_rate,
        gold_22k_exchange_rate=rate_data.gold_22k_exchange_rate,
        gold_22k_making_charges=rate_data.gold_22k_making_charges,
        
        # 18K rates
        gold_18k_new_rate=rate_data.gold_18k_new_rate,
        gold_18k_exchange_rate=rate_data.gold_18k_exchange_rate,
        gold_18k_making_charges=rate_data.gold_18k_making_charges,
        
        release_datetime=rate_data.release_datetime
    )
    
    db.add(new_rate)
    db.commit()
    db.refresh(new_rate)
    
    return new_rate

@router.get("/gold-rates/{rate_id}", response_model=GoldRateResponse)
async def get_gold_rate(
    rate_id: int,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get a specific gold rate by ID (Admin only)"""
    rate = db.query(GoldRate).filter(GoldRate.id == rate_id).first()
    
    if not rate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gold rate not found"
        )
    
    return rate

@router.put("/gold-rates/{rate_id}", response_model=GoldRateResponse)
async def update_gold_rate(
    rate_id: int,
    rate_update: GoldRateUpdate,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update a gold rate (Admin only)"""
    rate = db.query(GoldRate).filter(GoldRate.id == rate_id).first()
    
    if not rate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gold rate not found"
        )
    
    # Update all fields
    # 24K rates
    rate.gold_24k_new_rate = rate_update.gold_24k_new_rate
    rate.gold_24k_exchange_rate = rate_update.gold_24k_exchange_rate
    rate.gold_24k_making_charges = rate_update.gold_24k_making_charges
    
    # 22K rates
    rate.gold_22k_new_rate = rate_update.gold_22k_new_rate
    rate.gold_22k_exchange_rate = rate_update.gold_22k_exchange_rate
    rate.gold_22k_making_charges = rate_update.gold_22k_making_charges
    
    # 18K rates
    rate.gold_18k_new_rate = rate_update.gold_18k_new_rate
    rate.gold_18k_exchange_rate = rate_update.gold_18k_exchange_rate
    rate.gold_18k_making_charges = rate_update.gold_18k_making_charges
    
    db.commit()
    db.refresh(rate)
    
    return rate

@router.delete("/gold-rates/{rate_id}")
async def delete_gold_rate(
    rate_id: int,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a gold rate (Admin only)"""
    rate = db.query(GoldRate).filter(GoldRate.id == rate_id).first()
    
    if not rate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gold rate not found"
        )
    
    db.delete(rate)
    db.commit()
    
    return {"message": "Gold rate deleted successfully"}

# Admin Statistics Endpoints
@router.get("/statistics")
async def get_admin_statistics(
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get admin dashboard statistics"""
    
    total_rates = db.query(GoldRate).count()
    latest_rates = db.query(GoldRate).order_by(GoldRate.release_datetime.desc()).limit(5).all()
    
    # Get rates by purity
    rates_by_purity = {}
    for purity in ["24K", "22K", "18K"]:
        latest_rate = db.query(GoldRate).filter(
            GoldRate.purity == purity
        ).order_by(GoldRate.release_datetime.desc()).first()
        
        if latest_rate:
            rates_by_purity[purity] = {
                "latest_rate": latest_rate.new_rate_per_gram,
                "previous_rate": latest_rate.old_rate_per_gram,
                "change": latest_rate.new_rate_per_gram - latest_rate.old_rate_per_gram,
                "last_updated": latest_rate.release_datetime.isoformat()
            }
    
    return {
        "total_rates": total_rates,
        "rates_by_purity": rates_by_purity,
        "recent_updates": [
            {
                "id": rate.id,
                "purity": rate.purity,
                "rate": rate.new_rate_per_gram,
                "updated": rate.release_datetime.isoformat()
            }
            for rate in latest_rates
        ]
    }