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
from models import GoldRate, AdminUser, About, Team, Mission, Terms, Store, Guide, ContactEnquiry
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

# About section models
class AboutCreate(BaseModel):
    title: str
    content: str
    image: str = None

class AboutUpdate(BaseModel):
    title: str
    content: str
    image: str = None

class AboutResponse(BaseModel):
    id: int
    title: str
    content: str
    image: str = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Team section models
class TeamCreate(BaseModel):
    position: str
    name: str
    content: str
    image: str = None

class TeamUpdate(BaseModel):
    position: str
    name: str
    content: str
    image: str = None

class TeamResponse(BaseModel):
    id: int
    position: str
    name: str
    content: str
    image: str = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Mission section models
class MissionCreate(BaseModel):
    title: str
    content: str
    image: str = None

class MissionUpdate(BaseModel):
    title: str
    content: str
    image: str = None

class MissionResponse(BaseModel):
    id: int
    title: str
    content: str
    image: str = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Terms section models
class TermsCreate(BaseModel):
    title: str
    content: str
    image: str = None

class TermsUpdate(BaseModel):
    title: str
    content: str
    image: str = None

class TermsResponse(BaseModel):
    id: int
    title: str
    content: str
    image: str = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Store section models
class StoreCreate(BaseModel):
    store_name: str
    phone_number: str = None
    store_address: str
    store_image: str = None
    timings: str

class StoreUpdate(BaseModel):
    store_name: str
    phone_number: str = None
    store_address: str
    store_image: str = None
    timings: str

class StoreResponse(BaseModel):
    id: int
    store_name: str
    phone_number: str = None
    store_address: str
    store_image: str = None
    timings: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Guide section models
class GuideCreate(BaseModel):
    title: str
    content: str
    image: str = None

class GuideUpdate(BaseModel):
    title: str
    content: str
    image: str = None

class GuideResponse(BaseModel):
    id: int
    title: str
    content: str
    image: str = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Contact Enquiry section models
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
    total_stores = db.query(Store).count()
    total_guides = db.query(Guide).count()
    total_enquiries = db.query(ContactEnquiry).count()
    total_about = db.query(About).count()
    total_team = db.query(Team).count()
    total_missions = db.query(Mission).count()
    total_terms = db.query(Terms).count()
    
    latest_rates = db.query(GoldRate).order_by(GoldRate.release_datetime.desc()).limit(5).all()
    
    # Get current rates for all purities from the latest entry
    latest_rate = db.query(GoldRate).order_by(GoldRate.release_datetime.desc()).first()
    rates_by_purity = {}
    
    if latest_rate:
        rates_by_purity = {
            "24K": {
                "selling_rate": float(latest_rate.gold_24k_new_rate),
                "exchange_rate": float(latest_rate.gold_24k_exchange_rate),
                "making_charges": float(latest_rate.gold_24k_making_charges),
                "last_updated": latest_rate.release_datetime.isoformat()
            },
            "22K": {
                "selling_rate": float(latest_rate.gold_22k_new_rate),
                "exchange_rate": float(latest_rate.gold_22k_exchange_rate),
                "making_charges": float(latest_rate.gold_22k_making_charges),
                "last_updated": latest_rate.release_datetime.isoformat()
            },
            "18K": {
                "selling_rate": float(latest_rate.gold_18k_new_rate),
                "exchange_rate": float(latest_rate.gold_18k_exchange_rate),
                "making_charges": float(latest_rate.gold_18k_making_charges),
                "last_updated": latest_rate.release_datetime.isoformat()
            }
        }
    
    return {
        "total_counts": {
            "gold_rates": total_rates,
            "stores": total_stores,
            "guides": total_guides,
            "contact_enquiries": total_enquiries,
            "about_entries": total_about,
            "team_members": total_team,
            "missions": total_missions,
            "terms": total_terms
        },
        "current_gold_rates": rates_by_purity,
        "recent_gold_updates": [
            {
                "id": rate.id,
                "24k_rate": float(rate.gold_24k_new_rate),
                "22k_rate": float(rate.gold_22k_new_rate),
                "18k_rate": float(rate.gold_18k_new_rate),
                "updated": rate.release_datetime.isoformat()
            }
            for rate in latest_rates
        ]
    }

# About Management Endpoints
@router.get("/about", response_model=List[AboutResponse])
async def get_all_about(
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all about entries (Admin only)"""
    about_entries = db.query(About).order_by(About.created_at.desc()).all()
    return about_entries

@router.post("/about", response_model=AboutResponse)
async def create_about(
    about_data: AboutCreate,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new about entry (Admin only)"""
    new_about = About(
        title=about_data.title,
        content=about_data.content,
        image=about_data.image
    )
    
    db.add(new_about)
    db.commit()
    db.refresh(new_about)
    
    return new_about

@router.get("/about/{about_id}", response_model=AboutResponse)
async def get_about(
    about_id: int,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get a specific about entry by ID (Admin only)"""
    about = db.query(About).filter(About.id == about_id).first()
    
    if not about:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="About entry not found"
        )
    
    return about

@router.put("/about/{about_id}", response_model=AboutResponse)
async def update_about(
    about_id: int,
    about_update: AboutUpdate,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update an about entry (Admin only)"""
    about = db.query(About).filter(About.id == about_id).first()
    
    if not about:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="About entry not found"
        )
    
    about.title = about_update.title
    about.content = about_update.content
    about.image = about_update.image
    
    db.commit()
    db.refresh(about)
    
    return about

@router.delete("/about/{about_id}")
async def delete_about(
    about_id: int,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete an about entry (Admin only)"""
    about = db.query(About).filter(About.id == about_id).first()
    
    if not about:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="About entry not found"
        )
    
    db.delete(about)
    db.commit()
    
    return {"message": "About entry deleted successfully"}

# Team Management Endpoints
@router.get("/team", response_model=List[TeamResponse])
async def get_all_team(
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all team entries (Admin only)"""
    team_entries = db.query(Team).order_by(Team.created_at.desc()).all()
    return team_entries

@router.post("/team", response_model=TeamResponse)
async def create_team(
    team_data: TeamCreate,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new team entry (Admin only)"""
    new_team = Team(
        position=team_data.position,
        name=team_data.name,
        content=team_data.content,
        image=team_data.image
    )
    
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    
    return new_team

@router.get("/team/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: int,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get a specific team entry by ID (Admin only)"""
    team = db.query(Team).filter(Team.id == team_id).first()
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team entry not found"
        )
    
    return team

@router.put("/team/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: int,
    team_update: TeamUpdate,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update a team entry (Admin only)"""
    team = db.query(Team).filter(Team.id == team_id).first()
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team entry not found"
        )
    
    team.position = team_update.position
    team.name = team_update.name
    team.content = team_update.content
    team.image = team_update.image
    
    db.commit()
    db.refresh(team)
    
    return team

@router.delete("/team/{team_id}")
async def delete_team(
    team_id: int,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a team entry (Admin only)"""
    team = db.query(Team).filter(Team.id == team_id).first()
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team entry not found"
        )
    
    db.delete(team)
    db.commit()
    
    return {"message": "Team entry deleted successfully"}

# Mission Management Endpoints
@router.get("/missions", response_model=List[MissionResponse])
async def get_all_missions(
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all mission entries (Admin only)"""
    mission_entries = db.query(Mission).order_by(Mission.created_at.desc()).all()
    return mission_entries

@router.post("/missions", response_model=MissionResponse)
async def create_mission(
    mission_data: MissionCreate,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new mission entry (Admin only)"""
    new_mission = Mission(
        title=mission_data.title,
        content=mission_data.content,
        image=mission_data.image
    )
    
    db.add(new_mission)
    db.commit()
    db.refresh(new_mission)
    
    return new_mission

@router.get("/missions/{mission_id}", response_model=MissionResponse)
async def get_mission(
    mission_id: int,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get a specific mission entry by ID (Admin only)"""
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission entry not found"
        )
    
    return mission

@router.put("/missions/{mission_id}", response_model=MissionResponse)
async def update_mission(
    mission_id: int,
    mission_update: MissionUpdate,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update a mission entry (Admin only)"""
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission entry not found"
        )
    
    mission.title = mission_update.title
    mission.content = mission_update.content
    mission.image = mission_update.image
    
    db.commit()
    db.refresh(mission)
    
    return mission

@router.delete("/missions/{mission_id}")
async def delete_mission(
    mission_id: int,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a mission entry (Admin only)"""
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission entry not found"
        )
    
    db.delete(mission)
    db.commit()
    
    return {"message": "Mission entry deleted successfully"}

# Terms Management Endpoints
@router.get("/terms", response_model=List[TermsResponse])
async def get_all_terms(
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all terms entries (Admin only)"""
    terms_entries = db.query(Terms).order_by(Terms.created_at.desc()).all()
    return terms_entries

@router.post("/terms", response_model=TermsResponse)
async def create_terms(
    terms_data: TermsCreate,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new terms entry (Admin only)"""
    new_terms = Terms(
        title=terms_data.title,
        content=terms_data.content,
        image=terms_data.image
    )
    
    db.add(new_terms)
    db.commit()
    db.refresh(new_terms)
    
    return new_terms

@router.get("/terms/{terms_id}", response_model=TermsResponse)
async def get_terms(
    terms_id: int,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get a specific terms entry by ID (Admin only)"""
    terms = db.query(Terms).filter(Terms.id == terms_id).first()
    
    if not terms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Terms entry not found"
        )
    
    return terms

@router.put("/terms/{terms_id}", response_model=TermsResponse)
async def update_terms(
    terms_id: int,
    terms_update: TermsUpdate,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update a terms entry (Admin only)"""
    terms = db.query(Terms).filter(Terms.id == terms_id).first()
    
    if not terms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Terms entry not found"
        )
    
    terms.title = terms_update.title
    terms.content = terms_update.content
    terms.image = terms_update.image
    
    db.commit()
    db.refresh(terms)
    
    return terms

@router.delete("/terms/{terms_id}")
async def delete_terms(
    terms_id: int,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a terms entry (Admin only)"""
    terms = db.query(Terms).filter(Terms.id == terms_id).first()
    
    if not terms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Terms entry not found"
        )
    
    db.delete(terms)
    db.commit()
    
    return {"message": "Terms entry deleted successfully"}

# Store Management Endpoints
@router.get("/stores", response_model=List[StoreResponse])
async def get_all_stores(
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all stores (Admin only)"""
    stores = db.query(Store).order_by(Store.created_at.desc()).all()
    return stores

@router.post("/stores", response_model=StoreResponse)
async def create_store(
    store_data: StoreCreate,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new store (Admin only)"""
    new_store = Store(
        store_name=store_data.store_name,
        phone_number=store_data.phone_number,
        store_address=store_data.store_address,
        store_image=store_data.store_image,
        timings=store_data.timings
    )
    
    db.add(new_store)
    db.commit()
    db.refresh(new_store)
    
    return new_store

@router.get("/stores/{store_id}", response_model=StoreResponse)
async def get_store(
    store_id: int,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get a specific store by ID (Admin only)"""
    store = db.query(Store).filter(Store.id == store_id).first()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )
    
    return store

@router.put("/stores/{store_id}", response_model=StoreResponse)
async def update_store(
    store_id: int,
    store_update: StoreUpdate,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update a store (Admin only)"""
    store = db.query(Store).filter(Store.id == store_id).first()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )
    
    store.store_name = store_update.store_name
    store.phone_number = store_update.phone_number
    store.store_address = store_update.store_address
    store.store_image = store_update.store_image
    store.timings = store_update.timings
    
    db.commit()
    db.refresh(store)
    
    return store

@router.delete("/stores/{store_id}")
async def delete_store(
    store_id: int,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a store (Admin only)"""
    store = db.query(Store).filter(Store.id == store_id).first()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )
    
    db.delete(store)
    db.commit()
    
    return {"message": "Store deleted successfully"}

# Guide Management Endpoints
@router.get("/guides", response_model=List[GuideResponse])
async def get_all_guides(
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all guides (Admin only)"""
    guides = db.query(Guide).order_by(Guide.created_at.desc()).all()
    return guides

@router.post("/guides", response_model=GuideResponse)
async def create_guide(
    guide_data: GuideCreate,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new guide (Admin only)"""
    new_guide = Guide(
        title=guide_data.title,
        content=guide_data.content,
        image=guide_data.image
    )
    
    db.add(new_guide)
    db.commit()
    db.refresh(new_guide)
    
    return new_guide

@router.get("/guides/{guide_id}", response_model=GuideResponse)
async def get_guide(
    guide_id: int,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get a specific guide by ID (Admin only)"""
    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guide not found"
        )
    
    return guide

@router.put("/guides/{guide_id}", response_model=GuideResponse)
async def update_guide(
    guide_id: int,
    guide_update: GuideUpdate,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update a guide (Admin only)"""
    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guide not found"
        )
    
    guide.title = guide_update.title
    guide.content = guide_update.content
    guide.image = guide_update.image
    
    db.commit()
    db.refresh(guide)
    
    return guide

@router.delete("/guides/{guide_id}")
async def delete_guide(
    guide_id: int,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a guide (Admin only)"""
    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guide not found"
        )
    
    db.delete(guide)
    db.commit()
    
    return {"message": "Guide deleted successfully"}

# Contact Enquiry Management Endpoints (Read and Delete only - creation is done via public API)
@router.get("/contact-enquiries", response_model=List[ContactEnquiryResponse])
async def get_all_contact_enquiries_admin(
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all contact enquiries (Admin only)"""
    enquiries = db.query(ContactEnquiry).order_by(ContactEnquiry.created_at.desc()).all()
    return enquiries

@router.get("/contact-enquiries/{enquiry_id}", response_model=ContactEnquiryResponse)
async def get_contact_enquiry_admin(
    enquiry_id: int,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get a specific contact enquiry by ID (Admin only)"""
    enquiry = db.query(ContactEnquiry).filter(ContactEnquiry.id == enquiry_id).first()
    
    if not enquiry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact enquiry not found"
        )
    
    return enquiry

@router.delete("/contact-enquiries/{enquiry_id}")
async def delete_contact_enquiry(
    enquiry_id: int,
    current_user: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a contact enquiry (Admin only)"""
    enquiry = db.query(ContactEnquiry).filter(ContactEnquiry.id == enquiry_id).first()
    
    if not enquiry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact enquiry not found"
        )
    
    db.delete(enquiry)
    db.commit()
    
    return {"message": "Contact enquiry deleted successfully"}