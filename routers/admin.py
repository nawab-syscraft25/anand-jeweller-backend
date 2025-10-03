from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import Optional

from database import get_db
from models import AdminUser, GoldRate, Store, ContactEnquiry, Guide
from auth import authenticate_user, login_user, logout_user, get_current_user, is_authenticated

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Login page
@router.get("/admin/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if is_authenticated(request):
        return RedirectResponse(url="/admin", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request})

# Login form handler
@router.post("/admin/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse(
            "login.html", 
            {
                "request": request, 
                "error": "Invalid username or password"
            }
        )
    
    login_user(request, user)
    return RedirectResponse(url="/admin", status_code=302)

# Logout
@router.get("/admin/logout")
async def logout(request: Request):
    logout_user(request)
    return RedirectResponse(url="/admin/login", status_code=302)

# Dashboard home
@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db)
):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=302)
    
    # Get stats for dashboard
    total_rates = db.query(GoldRate).count()
    total_stores = db.query(Store).count()
    total_enquiries = db.query(ContactEnquiry).count()
    total_guides = db.query(Guide).count()
    latest_rates = db.query(GoldRate).order_by(desc(GoldRate.release_datetime)).limit(5).all()
    
    current_user = get_current_user(request, db)
    
    return templates.TemplateResponse(
        "dashboard.html", 
        {
            "request": request,
            "user": current_user,
            "total_rates": total_rates,
            "total_stores": total_stores,
            "total_enquiries": total_enquiries,
            "total_guides": total_guides,
            "latest_rates": latest_rates
        }
    )

# List all gold rates
@router.get("/admin/gold-rates", response_class=HTMLResponse)
async def list_gold_rates(
    request: Request,
    db: Session = Depends(get_db)
):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=302)
    
    gold_rates = db.query(GoldRate).order_by(desc(GoldRate.release_datetime)).all()
    current_user = get_current_user(request, db)
    
    return templates.TemplateResponse(
        "gold_rates/list.html",
        {
            "request": request,
            "user": current_user,
            "gold_rates": gold_rates
        }
    )

# Add gold rate form
@router.get("/admin/gold-rates/add", response_class=HTMLResponse)
async def add_gold_rate_form(
    request: Request,
    db: Session = Depends(get_db)
):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=302)
    
    current_user = get_current_user(request, db)
    
    return templates.TemplateResponse(
        "gold_rates/add.html",
        {
            "request": request,
            "user": current_user
        }
    )

# Add gold rate handler
@router.post("/admin/gold-rates/add")
async def add_gold_rate(
    request: Request,
    purity: str = Form(...),
    new_rate_per_gram: float = Form(...),
    old_rate_per_gram: float = Form(...),
    release_datetime: str = Form(...),
    db: Session = Depends(get_db)
):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=302)
    
    try:
        # Parse datetime
        release_dt = datetime.fromisoformat(release_datetime.replace('T', ' '))
        
        # Check for duplicates
        existing = db.query(GoldRate).filter(
            GoldRate.purity == purity,
            GoldRate.release_datetime == release_dt
        ).first()
        
        if existing:
            current_user = get_current_user(request, db)
            return templates.TemplateResponse(
                "gold_rates/add.html",
                {
                    "request": request,
                    "user": current_user,
                    "error": f"A rate for {purity} already exists for this date and time"
                }
            )
        
        # Create new gold rate
        gold_rate = GoldRate(
            purity=purity,
            new_rate_per_gram=new_rate_per_gram,
            old_rate_per_gram=old_rate_per_gram,
            release_datetime=release_dt
        )
        
        db.add(gold_rate)
        db.commit()
        
        return RedirectResponse(url="/admin/gold-rates", status_code=302)
        
    except Exception as e:
        current_user = get_current_user(request, db)
        return templates.TemplateResponse(
            "gold_rates/add.html",
            {
                "request": request,
                "user": current_user,
                "error": f"Error adding gold rate: {str(e)}"
            }
        )

# Edit gold rate form
@router.get("/admin/gold-rates/edit/{rate_id}", response_class=HTMLResponse)
async def edit_gold_rate_form(
    request: Request,
    rate_id: int,
    db: Session = Depends(get_db)
):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=302)
    
    gold_rate = db.query(GoldRate).filter(GoldRate.id == rate_id).first()
    if not gold_rate:
        raise HTTPException(status_code=404, detail="Gold rate not found")
    
    current_user = get_current_user(request, db)
    
    return templates.TemplateResponse(
        "gold_rates/edit.html",
        {
            "request": request,
            "user": current_user,
            "gold_rate": gold_rate
        }
    )

# Edit gold rate handler
@router.post("/admin/gold-rates/edit/{rate_id}")
async def edit_gold_rate(
    request: Request,
    rate_id: int,
    purity: str = Form(...),
    new_rate_per_gram: float = Form(...),
    old_rate_per_gram: float = Form(...),
    release_datetime: str = Form(...),
    db: Session = Depends(get_db)
):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=302)
    
    try:
        gold_rate = db.query(GoldRate).filter(GoldRate.id == rate_id).first()
        if not gold_rate:
            raise HTTPException(status_code=404, detail="Gold rate not found")
        
        # Parse datetime
        release_dt = datetime.fromisoformat(release_datetime.replace('T', ' '))
        
        # Check for duplicates (excluding current record)
        existing = db.query(GoldRate).filter(
            GoldRate.purity == purity,
            GoldRate.release_datetime == release_dt,
            GoldRate.id != rate_id
        ).first()
        
        if existing:
            current_user = get_current_user(request, db)
            return templates.TemplateResponse(
                "gold_rates/edit.html",
                {
                    "request": request,
                    "user": current_user,
                    "gold_rate": gold_rate,
                    "error": f"A rate for {purity} already exists for this date and time"
                }
            )
        
        # Update gold rate
        gold_rate.purity = purity
        gold_rate.new_rate_per_gram = new_rate_per_gram
        gold_rate.old_rate_per_gram = old_rate_per_gram
        gold_rate.release_datetime = release_dt
        
        db.commit()
        
        return RedirectResponse(url="/admin/gold-rates", status_code=302)
        
    except Exception as e:
        current_user = get_current_user(request, db)
        gold_rate = db.query(GoldRate).filter(GoldRate.id == rate_id).first()
        return templates.TemplateResponse(
            "gold_rates/edit.html",
            {
                "request": request,
                "user": current_user,
                "gold_rate": gold_rate,
                "error": f"Error updating gold rate: {str(e)}"
            }
        )

# Delete gold rate
@router.get("/admin/gold-rates/delete/{rate_id}")
async def delete_gold_rate(
    request: Request,
    rate_id: int,
    db: Session = Depends(get_db)
):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=302)
    
    gold_rate = db.query(GoldRate).filter(GoldRate.id == rate_id).first()
    if not gold_rate:
        raise HTTPException(status_code=404, detail="Gold rate not found")
    
    db.delete(gold_rate)
    db.commit()
    
    return RedirectResponse(url="/admin/gold-rates", status_code=302)