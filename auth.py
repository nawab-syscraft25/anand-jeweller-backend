import bcrypt
from datetime import timedelta
from fastapi import Request, HTTPException, status
from sqlalchemy.orm import Session
from models import AdminUser
from database import get_db
from jwt_auth import JWTAuth, ACCESS_TOKEN_EXPIRE_MINUTES

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def authenticate_user(db: Session, username: str, password: str) -> AdminUser:
    """Authenticate user with username and password"""
    user = db.query(AdminUser).filter(AdminUser.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def get_current_user(request: Request, db: Session) -> AdminUser:
    """Get current authenticated user from session"""
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user = db.query(AdminUser).filter(AdminUser.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

def login_user(request: Request, user: AdminUser):
    """Login user by setting session and generating JWT token"""
    request.session["user_id"] = user.id
    request.session["username"] = user.username
    
    # Generate JWT token for API access
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWTAuth.create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    # Store token in session for easy access
    request.session["access_token"] = access_token
    return access_token

def logout_user(request: Request):
    """Logout user by clearing session"""
    request.session.clear()

def is_authenticated(request: Request) -> bool:
    """Check if user is authenticated"""
    return "user_id" in request.session