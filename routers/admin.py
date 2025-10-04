from fastapi import APIRouter, Request, Form, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import Optional
import os
import uuid
from pathlib import Path

from database import get_db
from models import AdminUser, GoldRate, Store, ContactEnquiry, Guide, About, Team, Mission, Terms
from auth import authenticate_user, login_user, logout_user, get_current_user, is_authenticated
from jwt_auth import require_admin_auth

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# File upload utility function
async def save_uploaded_file(file: Optional[UploadFile], folder: str) -> Optional[str]:
    """Save uploaded file and return the file path, or None if no file uploaded"""
    if not file or not file.filename:
        return None
    
    # Create uploads directory if it doesn't exist
    upload_dir = Path("static/uploads") / folder
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = upload_dir / unique_filename
    
    # Save the file
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Return the relative path for database storage
    return f"/static/uploads/{folder}/{unique_filename}"

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
    
    # Login user and get JWT token
    access_token = login_user(request, user)
    
    # Store token in session for JavaScript access
    request.session["jwt_token"] = access_token
    
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
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    # Get stats for dashboard
    total_rates = db.query(GoldRate).count()
    total_stores = db.query(Store).count()
    total_enquiries = db.query(ContactEnquiry).count()
    total_guides = db.query(Guide).count()
    total_about = db.query(About).count()
    total_team = db.query(Team).count()
    total_missions = db.query(Mission).count()
    total_terms = db.query(Terms).count()
    latest_rate = db.query(GoldRate).order_by(desc(GoldRate.release_datetime)).first()
    
    # Get JWT token from session for frontend use
    jwt_token = request.session.get("jwt_token", "")
    
    return templates.TemplateResponse(
        "dashboard.html", 
        {
            "request": request,
            "user": current_user,
            "total_rates": total_rates,
            "total_stores": total_stores,
            "total_enquiries": total_enquiries,
            "total_guides": total_guides,
            "total_about": total_about,
            "total_team": total_team,
            "total_missions": total_missions,
            "total_terms": total_terms,
            "latest_rate": latest_rate,
            "jwt_token": jwt_token
        }
    )

# List all gold rates
@router.get("/admin/gold-rates", response_class=HTMLResponse)
async def list_gold_rates(
    request: Request,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    gold_rates = db.query(GoldRate).order_by(desc(GoldRate.release_datetime)).all()
    jwt_token = request.session.get("jwt_token", "")
    
    return templates.TemplateResponse(
        "gold_rates/list.html",
        {
            "request": request,
            "user": current_user,
            "gold_rates": gold_rates,
            "jwt_token": jwt_token
        }
    )

# Add gold rate form
@router.get("/admin/gold-rates/add", response_class=HTMLResponse)
async def add_gold_rate_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    jwt_token = request.session.get("jwt_token", "")
    
    return templates.TemplateResponse(
        "gold_rates/add.html",
        {
            "request": request,
            "user": current_user,
            "jwt_token": jwt_token
        }
    )

# Add gold rate handler
@router.post("/admin/gold-rates/add")
async def add_gold_rate(
    request: Request,
    # 24K Gold rates
    gold_24k_new_rate: float = Form(...),
    gold_24k_exchange_rate: float = Form(...),
    gold_24k_making_charges: float = Form(...),
    # 22K Gold rates
    gold_22k_new_rate: float = Form(...),
    gold_22k_exchange_rate: float = Form(...),
    gold_22k_making_charges: float = Form(...),
    # 18K Gold rates
    gold_18k_new_rate: float = Form(...),
    gold_18k_exchange_rate: float = Form(...),
    gold_18k_making_charges: float = Form(...),
    # Common fields
    release_datetime: str = Form(...),
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=302)
    
    try:
        # Parse datetime
        release_dt = datetime.fromisoformat(release_datetime.replace('T', ' '))
        
        # Check for duplicates (by release datetime)
        existing = db.query(GoldRate).filter(
            GoldRate.release_datetime == release_dt
        ).first()
        
        if existing:
            current_user = get_current_user(request, db)
            return templates.TemplateResponse(
                "gold_rates/add.html",
                {
                    "request": request,
                    "user": current_user,
                    "error": f"A gold rate already exists for this date and time",
                    "jwt_token": request.session.get("jwt_token", "")
                }
            )
        
        # Create new consolidated gold rate
        gold_rate = GoldRate(
            gold_24k_new_rate=gold_24k_new_rate,
            gold_24k_exchange_rate=gold_24k_exchange_rate,
            gold_24k_making_charges=gold_24k_making_charges,
            gold_22k_new_rate=gold_22k_new_rate,
            gold_22k_exchange_rate=gold_22k_exchange_rate,
            gold_22k_making_charges=gold_22k_making_charges,
            gold_18k_new_rate=gold_18k_new_rate,
            gold_18k_exchange_rate=gold_18k_exchange_rate,
            gold_18k_making_charges=gold_18k_making_charges,
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
                "error": f"Error adding gold rate: {str(e)}",
                "jwt_token": request.session.get("jwt_token", "")
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
    
    jwt_token = request.session.get("jwt_token", "")
    
    return templates.TemplateResponse(
        "gold_rates/edit.html",
        {
            "request": request,
            "user": current_user,
            "gold_rate": gold_rate,
            "jwt_token": jwt_token
        }
    )

# Edit gold rate handler
@router.post("/admin/gold-rates/edit/{rate_id}")
async def edit_gold_rate(
    request: Request,
    rate_id: int,
    # 24K Gold rates
    gold_24k_new_rate: float = Form(...),
    gold_24k_exchange_rate: float = Form(...),
    gold_24k_making_charges: float = Form(...),
    # 22K Gold rates
    gold_22k_new_rate: float = Form(...),
    gold_22k_exchange_rate: float = Form(...),
    gold_22k_making_charges: float = Form(...),
    # 18K Gold rates
    gold_18k_new_rate: float = Form(...),
    gold_18k_exchange_rate: float = Form(...),
    gold_18k_making_charges: float = Form(...),
    # Common fields
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
                    "error": f"A gold rate already exists for this date and time",
                    "jwt_token": request.session.get("jwt_token", "")
                }
            )
        
        # Update consolidated gold rate
        gold_rate.gold_24k_new_rate = gold_24k_new_rate
        gold_rate.gold_24k_exchange_rate = gold_24k_exchange_rate
        gold_rate.gold_24k_making_charges = gold_24k_making_charges
        gold_rate.gold_22k_new_rate = gold_22k_new_rate
        gold_rate.gold_22k_exchange_rate = gold_22k_exchange_rate
        gold_rate.gold_22k_making_charges = gold_22k_making_charges
        gold_rate.gold_18k_new_rate = gold_18k_new_rate
        gold_rate.gold_18k_exchange_rate = gold_18k_exchange_rate
        gold_rate.gold_18k_making_charges = gold_18k_making_charges
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
                "error": f"Error updating gold rate: {str(e)}",
                "jwt_token": request.session.get("jwt_token", "")
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

# ABOUT SECTION ROUTES

# List all about entries
@router.get("/admin/about", response_class=HTMLResponse)
async def list_about(
    request: Request,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    about_entries = db.query(About).order_by(desc(About.created_at)).all()
    jwt_token = request.session.get("jwt_token", "")
    
    return templates.TemplateResponse(
        "about/list.html",
        {
            "request": request,
            "user": current_user,
            "about_entries": about_entries,
            "jwt_token": jwt_token
        }
    )

# Add about entry form
@router.get("/admin/about/add", response_class=HTMLResponse)
async def add_about_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    jwt_token = request.session.get("jwt_token", "")
    
    return templates.TemplateResponse(
        "about/add.html",
        {
            "request": request,
            "user": current_user,
            "jwt_token": jwt_token
        }
    )

# Add about entry handler
@router.post("/admin/about/add")
async def add_about(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    try:
        # Handle file upload
        image_path = await save_uploaded_file(image, "about")
        
        about_entry = About(
            title=title,
            content=content,
            image=image_path
        )
        
        db.add(about_entry)
        db.commit()
        
        return RedirectResponse(url="/admin/about", status_code=302)
        
    except Exception as e:
        return templates.TemplateResponse(
            "about/add.html",
            {
                "request": request,
                "user": current_user,
                "error": f"Error adding about entry: {str(e)}",
                "jwt_token": request.session.get("jwt_token", "")
            }
        )

# Edit about entry form
@router.get("/admin/about/edit/{about_id}", response_class=HTMLResponse)
async def edit_about_form(
    request: Request,
    about_id: int,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    about_entry = db.query(About).filter(About.id == about_id).first()
    if not about_entry:
        raise HTTPException(status_code=404, detail="About entry not found")
    
    jwt_token = request.session.get("jwt_token", "")
    
    return templates.TemplateResponse(
        "about/edit.html",
        {
            "request": request,
            "user": current_user,
            "about_entry": about_entry,
            "jwt_token": jwt_token
        }
    )

# Edit about entry handler
@router.post("/admin/about/edit/{about_id}")
async def edit_about(
    request: Request,
    about_id: int,
    title: str = Form(...),
    content: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    try:
        about_entry = db.query(About).filter(About.id == about_id).first()
        if not about_entry:
            raise HTTPException(status_code=404, detail="About entry not found")
        
        # Handle file upload - only update image if new file is uploaded
        image_path = await save_uploaded_file(image, "about")
        
        about_entry.title = title
        about_entry.content = content
        if image_path:  # Only update image if new file was uploaded
            about_entry.image = image_path
        
        db.commit()
        
        return RedirectResponse(url="/admin/about", status_code=302)
        
    except Exception as e:
        about_entry = db.query(About).filter(About.id == about_id).first()
        return templates.TemplateResponse(
            "about/edit.html",
            {
                "request": request,
                "user": current_user,
                "about_entry": about_entry,
                "error": f"Error updating about entry: {str(e)}",
                "jwt_token": request.session.get("jwt_token", "")
            }
        )

# Delete about entry
@router.get("/admin/about/delete/{about_id}")
async def delete_about(
    request: Request,
    about_id: int,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    about_entry = db.query(About).filter(About.id == about_id).first()
    if not about_entry:
        raise HTTPException(status_code=404, detail="About entry not found")
    
    db.delete(about_entry)
    db.commit()
    
    return RedirectResponse(url="/admin/about", status_code=302)

# TEAM SECTION ROUTES

# List all team members
@router.get("/admin/team", response_class=HTMLResponse)
async def list_team(
    request: Request,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    team_members = db.query(Team).order_by(desc(Team.created_at)).all()
    jwt_token = request.session.get("jwt_token", "")
    
    return templates.TemplateResponse(
        "team/list.html",
        {
            "request": request,
            "user": current_user,
            "team_members": team_members,
            "jwt_token": jwt_token
        }
    )

# Add team member form
@router.get("/admin/team/add", response_class=HTMLResponse)
async def add_team_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    jwt_token = request.session.get("jwt_token", "")
    
    return templates.TemplateResponse(
        "team/add.html",
        {
            "request": request,
            "user": current_user,
            "jwt_token": jwt_token
        }
    )

# Add team member handler
@router.post("/admin/team/add")
async def add_team(
    request: Request,
    position: str = Form(...),
    name: str = Form(...),
    content: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    try:
        # Handle file upload
        image_path = await save_uploaded_file(image, "team")
        
        team_member = Team(
            position=position,
            name=name,
            content=content,
            image=image_path
        )
        
        db.add(team_member)
        db.commit()
        
        return RedirectResponse(url="/admin/team", status_code=302)
        
    except Exception as e:
        return templates.TemplateResponse(
            "team/add.html",
            {
                "request": request,
                "user": current_user,
                "error": f"Error adding team member: {str(e)}",
                "jwt_token": request.session.get("jwt_token", "")
            }
        )

# Edit team member form
@router.get("/admin/team/edit/{team_id}", response_class=HTMLResponse)
async def edit_team_form(
    request: Request,
    team_id: int,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    team_member = db.query(Team).filter(Team.id == team_id).first()
    if not team_member:
        raise HTTPException(status_code=404, detail="Team member not found")
    
    jwt_token = request.session.get("jwt_token", "")
    
    return templates.TemplateResponse(
        "team/edit.html",
        {
            "request": request,
            "user": current_user,
            "team_member": team_member,
            "jwt_token": jwt_token
        }
    )

# Edit team member handler
@router.post("/admin/team/edit/{team_id}")
async def edit_team(
    request: Request,
    team_id: int,
    position: str = Form(...),
    name: str = Form(...),
    content: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    try:
        team_member = db.query(Team).filter(Team.id == team_id).first()
        if not team_member:
            raise HTTPException(status_code=404, detail="Team member not found")
        
        # Handle file upload - only update image if new file is uploaded
        image_path = await save_uploaded_file(image, "team")
        
        team_member.position = position
        team_member.name = name
        team_member.content = content
        if image_path:  # Only update image if new file was uploaded
            team_member.image = image_path
        
        db.commit()
        
        return RedirectResponse(url="/admin/team", status_code=302)
        
    except Exception as e:
        team_member = db.query(Team).filter(Team.id == team_id).first()
        return templates.TemplateResponse(
            "team/edit.html",
            {
                "request": request,
                "user": current_user,
                "team_member": team_member,
                "error": f"Error updating team member: {str(e)}",
                "jwt_token": request.session.get("jwt_token", "")
            }
        )

# Delete team member
@router.get("/admin/team/delete/{team_id}")
async def delete_team(
    request: Request,
    team_id: int,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    team_member = db.query(Team).filter(Team.id == team_id).first()
    if not team_member:
        raise HTTPException(status_code=404, detail="Team member not found")
    
    db.delete(team_member)
    db.commit()
    
    return RedirectResponse(url="/admin/team", status_code=302)

# MISSION SECTION ROUTES

# List all missions
@router.get("/admin/missions", response_class=HTMLResponse)
async def list_missions(
    request: Request,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    missions = db.query(Mission).order_by(desc(Mission.created_at)).all()
    jwt_token = request.session.get("jwt_token", "")
    
    return templates.TemplateResponse(
        "missions/list.html",
        {
            "request": request,
            "user": current_user,
            "missions": missions,
            "jwt_token": jwt_token
        }
    )

# Add mission form
@router.get("/admin/missions/add", response_class=HTMLResponse)
async def add_mission_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    jwt_token = request.session.get("jwt_token", "")
    
    return templates.TemplateResponse(
        "missions/add.html",
        {
            "request": request,
            "user": current_user,
            "jwt_token": jwt_token
        }
    )

# Add mission handler
@router.post("/admin/missions/add")
async def add_mission(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    try:
        # Handle file upload
        image_path = await save_uploaded_file(image, "missions")
        
        mission = Mission(
            title=title,
            content=content,
            image=image_path
        )
        
        db.add(mission)
        db.commit()
        
        return RedirectResponse(url="/admin/missions", status_code=302)
        
    except Exception as e:
        return templates.TemplateResponse(
            "missions/add.html",
            {
                "request": request,
                "user": current_user,
                "error": f"Error adding mission: {str(e)}",
                "jwt_token": request.session.get("jwt_token", "")
            }
        )

# Edit mission form
@router.get("/admin/missions/edit/{mission_id}", response_class=HTMLResponse)
async def edit_mission_form(
    request: Request,
    mission_id: int,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    jwt_token = request.session.get("jwt_token", "")
    
    return templates.TemplateResponse(
        "missions/edit.html",
        {
            "request": request,
            "user": current_user,
            "mission": mission,
            "jwt_token": jwt_token
        }
    )

# Edit mission handler
@router.post("/admin/missions/edit/{mission_id}")
async def edit_mission(
    request: Request,
    mission_id: int,
    title: str = Form(...),
    content: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    try:
        mission = db.query(Mission).filter(Mission.id == mission_id).first()
        if not mission:
            raise HTTPException(status_code=404, detail="Mission not found")
        
        # Handle file upload - only update image if new file is uploaded
        image_path = await save_uploaded_file(image, "missions")
        
        mission.title = title
        mission.content = content
        if image_path:  # Only update image if new file was uploaded
            mission.image = image_path
        
        db.commit()
        
        return RedirectResponse(url="/admin/missions", status_code=302)
        
    except Exception as e:
        mission = db.query(Mission).filter(Mission.id == mission_id).first()
        return templates.TemplateResponse(
            "missions/edit.html",
            {
                "request": request,
                "user": current_user,
                "mission": mission,
                "error": f"Error updating mission: {str(e)}",
                "jwt_token": request.session.get("jwt_token", "")
            }
        )

# Delete mission
@router.get("/admin/missions/delete/{mission_id}")
async def delete_mission(
    request: Request,
    mission_id: int,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    db.delete(mission)
    db.commit()
    
    return RedirectResponse(url="/admin/missions", status_code=302)

# TERMS SECTION ROUTES

# List all terms
@router.get("/admin/terms", response_class=HTMLResponse)
async def list_terms(
    request: Request,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    terms = db.query(Terms).order_by(desc(Terms.created_at)).all()
    jwt_token = request.session.get("jwt_token", "")
    
    return templates.TemplateResponse(
        "terms/list.html",
        {
            "request": request,
            "user": current_user,
            "terms": terms,
            "jwt_token": jwt_token
        }
    )

# Add terms form
@router.get("/admin/terms/add", response_class=HTMLResponse)
async def add_terms_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    jwt_token = request.session.get("jwt_token", "")
    
    return templates.TemplateResponse(
        "terms/add.html",
        {
            "request": request,
            "user": current_user,
            "jwt_token": jwt_token
        }
    )

# Add terms handler
@router.post("/admin/terms/add")
async def add_terms(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    try:
        # Handle file upload
        image_path = await save_uploaded_file(image, "terms")
        
        terms = Terms(
            title=title,
            content=content,
            image=image_path
        )
        
        db.add(terms)
        db.commit()
        
        return RedirectResponse(url="/admin/terms", status_code=302)
        
    except Exception as e:
        return templates.TemplateResponse(
            "terms/add.html",
            {
                "request": request,
                "user": current_user,
                "error": f"Error adding terms: {str(e)}",
                "jwt_token": request.session.get("jwt_token", "")
            }
        )

# Edit terms form
@router.get("/admin/terms/edit/{terms_id}", response_class=HTMLResponse)
async def edit_terms_form(
    request: Request,
    terms_id: int,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    terms = db.query(Terms).filter(Terms.id == terms_id).first()
    if not terms:
        raise HTTPException(status_code=404, detail="Terms not found")
    
    jwt_token = request.session.get("jwt_token", "")
    
    return templates.TemplateResponse(
        "terms/edit.html",
        {
            "request": request,
            "user": current_user,
            "terms": terms,
            "jwt_token": jwt_token
        }
    )

# Edit terms handler
@router.post("/admin/terms/edit/{terms_id}")
async def edit_terms(
    request: Request,
    terms_id: int,
    title: str = Form(...),
    content: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    try:
        terms = db.query(Terms).filter(Terms.id == terms_id).first()
        if not terms:
            raise HTTPException(status_code=404, detail="Terms not found")
        
        # Handle file upload - only update image if new file is uploaded
        image_path = await save_uploaded_file(image, "terms")
        
        terms.title = title
        terms.content = content
        if image_path:  # Only update image if new file was uploaded
            terms.image = image_path
        
        db.commit()
        
        return RedirectResponse(url="/admin/terms", status_code=302)
        
    except Exception as e:
        terms = db.query(Terms).filter(Terms.id == terms_id).first()
        return templates.TemplateResponse(
            "terms/edit.html",
            {
                "request": request,
                "user": current_user,
                "terms": terms,
                "error": f"Error updating terms: {str(e)}",
                "jwt_token": request.session.get("jwt_token", "")
            }
        )

# Delete terms
@router.get("/admin/terms/delete/{terms_id}")
async def delete_terms(
    request: Request,
    terms_id: int,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(require_admin_auth)
):
    terms = db.query(Terms).filter(Terms.id == terms_id).first()
    if not terms:
        raise HTTPException(status_code=404, detail="Terms not found")
    
    db.delete(terms)
    db.commit()
    
    return RedirectResponse(url="/admin/terms", status_code=302)