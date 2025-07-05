from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import json
from pydantic import BaseModel

from src.data.database import get_session
from src.data.models import User, UserReport
from src.schemas.auth import UserResponse, Token, UserReportCreate, UserReportResponse
from src.utils.supabase_auth import supabase_auth
from src.utils.supabase import supabase_config

# Simple request models for auth
class RegisterRequest(BaseModel):
    email: str
    password: str
    username: str

class LoginRequest(BaseModel):
    email: str
    password: str

router = APIRouter(prefix="/api/supabase-auth", tags=["supabase-authentication"])

@router.post("/register", response_model=UserResponse)
def register(user_data: RegisterRequest, db: Session = Depends(get_session)):
    """Register a new user using Supabase Auth."""
    if not supabase_config.use_supabase_auth_enabled():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supabase Auth is not enabled"
        )
    try:
        # Check if user already exists in local database
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        
        # Sign up with Supabase Auth
        auth_response = supabase_auth.sign_up(
            email=user_data.email,
            password=user_data.password,
            user_metadata={"username": user_data.username}
        )
        
        if existing_user:
            # Update existing user record
            existing_user.username = user_data.username
            existing_user.is_active = True
            db.commit()
            db.refresh(existing_user)
            return existing_user
        else:
            # Create new local user record for reports
            db_user = User(
                email=user_data.email,
                username=user_data.username,
                hashed_password="supabase_auth",  # Placeholder since we're using Supabase Auth
                is_active=True
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=Token)
def login(user_credentials: LoginRequest, db: Session = Depends(get_session)):
    """Login user using Supabase Auth and return access token."""
    if not supabase_config.use_supabase_auth_enabled():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supabase Auth is not enabled"
        )
    try:
        # Sign in with Supabase Auth
        auth_response = supabase_auth.sign_in(
            email=user_credentials.email,
            password=user_credentials.password
        )
        # Get local user record
        user = db.query(User).filter(User.email == user_credentials.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found in local database"
            )
        return {
            "access_token": auth_response["session"].access_token,
            "token_type": "bearer",
            "expires_in": 30
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: dict = Depends(supabase_auth.get_current_user), db: Session = Depends(get_session)):
    """Get current user information from Supabase Auth."""
    if not supabase_config.use_supabase_auth_enabled():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supabase Auth is not enabled"
        )
    # Get user from local database
    user = db.query(User).filter(User.email == current_user["email"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in local database"
        )
    return user

@router.post("/reports", response_model=UserReportResponse)
def save_user_report(
    report_data: UserReportCreate,
    current_user: dict = Depends(supabase_auth.get_current_user),
    db: Session = Depends(get_session)
):
    """Save a user report using Supabase Auth."""
    if not supabase_config.use_supabase_auth_enabled():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supabase Auth is not enabled"
        )
    # Validate that report_data is valid JSON
    try:
        json.loads(report_data.report_data)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON in report_data"
        )
    # Get user from local database
    user = db.query(User).filter(User.email == current_user["email"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in local database"
        )
    db_report = UserReport(
        user_id=user.id,
        title=report_data.title,
        description=report_data.description,
        report_data=report_data.report_data,
        report_type=report_data.report_type
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.get("/reports", response_model=list[UserReportResponse])
def get_user_reports(
    current_user: dict = Depends(supabase_auth.get_current_user),
    db: Session = Depends(get_session)
):
    """Get all reports for the current user using Supabase Auth."""
    if not supabase_config.use_supabase_auth_enabled():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supabase Auth is not enabled"
        )
    # Get user from local database
    user = db.query(User).filter(User.email == current_user["email"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in local database"
        )
    reports = db.query(UserReport).filter(UserReport.user_id == user.id).all()
    return reports

@router.get("/reports/{report_id}", response_model=UserReportResponse)
def get_user_report(
    report_id: int,
    current_user: dict = Depends(supabase_auth.get_current_user),
    db: Session = Depends(get_session)
):
    """Get a specific user report using Supabase Auth."""
    if not supabase_config.use_supabase_auth_enabled():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supabase Auth is not enabled"
        )
    # Get user from local database
    user = db.query(User).filter(User.email == current_user["email"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in local database"
        )
    report = db.query(UserReport).filter(
        UserReport.id == report_id,
        UserReport.user_id == user.id
    ).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return report

@router.delete("/reports/{report_id}")
def delete_user_report(
    report_id: int,
    current_user: dict = Depends(supabase_auth.get_current_user),
    db: Session = Depends(get_session)
):
    """Delete a user report using Supabase Auth."""
    if not supabase_config.use_supabase_auth_enabled():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supabase Auth is not enabled"
        )
    # Get user from local database
    user = db.query(User).filter(User.email == current_user["email"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in local database"
        )
    report = db.query(UserReport).filter(
        UserReport.id == report_id,
        UserReport.user_id == user.id
    ).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    db.delete(report)
    db.commit()
    return {"detail": "Report deleted"} 