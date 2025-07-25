from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest
from googleapiclient.discovery import build
import secrets
import json
from datetime import datetime, timezone, timedelta
from typing import Optional

from database.database import get_db
from database import schemas, crud, models
from config.oauth import get_oauth_config, GOOGLE_SCOPES, GOOGLE_REDIRECT_URI

router = APIRouter(prefix="/auth", tags=["authentication"])

# In-memory store for OAuth state (in production, use Redis or similar)
oauth_states = {}

@router.get("/google/login")
async def google_login():
    """Initiate Google OAuth login flow"""
    try:
        # Create flow instance
        flow = Flow.from_client_config(
            get_oauth_config(),
            scopes=GOOGLE_SCOPES
        )
        flow.redirect_uri = GOOGLE_REDIRECT_URI
        
        # Generate a random state parameter for security
        state = secrets.token_urlsafe(32)
        oauth_states[state] = {
            "created_at": datetime.now(timezone.utc),
            "used": False
        }
        
        # Get authorization URL
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=state
        )
        
        return {"authorization_url": authorization_url, "state": state}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate OAuth flow: {str(e)}"
        )

@router.get("/google/callback")
async def google_callback(
    code: str,
    state: str,
    db: Session = Depends(get_db)
):
    """Handle Google OAuth callback"""
    try:
        # Verify state parameter
        if state not in oauth_states or oauth_states[state]["used"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired state parameter"
            )
        
        # Mark state as used
        oauth_states[state]["used"] = True
        
        # Create flow instance
        flow = Flow.from_client_config(
            get_oauth_config(),
            scopes=GOOGLE_SCOPES
        )
        flow.redirect_uri = GOOGLE_REDIRECT_URI
        
        # Fetch tokens
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # Get user info from Google
        service = build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute()
        
        # Check if user already exists
        existing_user = crud.get_user_by_email(db, email=user_info['email'])
        
        if existing_user:
            # Update existing user with OAuth tokens
            user = crud.update_user_oauth_tokens(
                db=db,
                user_id=existing_user.id,
                google_id=user_info['id'],
                access_token=credentials.token,
                refresh_token=credentials.refresh_token,
                expires_at=credentials.expiry
            )
        else:
            # Create new user
            user_create = schemas.UserCreateOAuth(
                email=user_info['email'],
                username=user_info.get('name', user_info['email'].split('@')[0]),
                google_id=user_info['id']
            )
            user = crud.create_user_oauth(
                db=db,
                user=user_create,
                access_token=credentials.token,
                refresh_token=credentials.refresh_token,
                expires_at=credentials.expiry
            )
        
        # Clean up old state entries (basic cleanup)
        cleanup_oauth_states()
        
        return {
            "message": "Authentication successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "google_calendar_connected": user.google_calendar_connected
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth callback failed: {str(e)}"
        )

@router.get("/user/calendar-status")
async def get_calendar_status(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Check if user's Google Calendar is connected and tokens are valid"""
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.google_access_token:
        return {"connected": False, "message": "Google Calendar not connected"}
    
    # Check if tokens are expired
    if user.google_token_expires_at and user.google_token_expires_at < datetime.now(timezone.utc):
        # Try to refresh tokens
        try:
            refreshed = await refresh_user_tokens(db, user)
            if refreshed:
                return {"connected": True, "message": "Google Calendar connected"}
            else:
                return {"connected": False, "message": "Tokens expired and refresh failed"}
        except Exception:
            return {"connected": False, "message": "Tokens expired and refresh failed"}
    
    return {"connected": True, "message": "Google Calendar connected"}

async def refresh_user_tokens(db: Session, user: models.User) -> bool:
    """Refresh user's Google OAuth tokens"""
    try:
        if not user.google_refresh_token:
            return False
        
        credentials = Credentials(
            token=user.google_access_token,
            refresh_token=user.google_refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=get_oauth_config()["web"]["client_id"],
            client_secret=get_oauth_config()["web"]["client_secret"]
        )
        
        # Refresh the credentials
        request = GoogleRequest()
        credentials.refresh(request)
        
        # Update user with new tokens
        crud.update_user_oauth_tokens(
            db=db,
            user_id=user.id,
            google_id=user.google_id,
            access_token=credentials.token,
            refresh_token=credentials.refresh_token,
            expires_at=credentials.expiry
        )
        
        return True
    except Exception:
        return False

def cleanup_oauth_states():
    """Clean up expired OAuth state entries"""
    current_time = datetime.now(timezone.utc)
    expired_states = [
        state for state, data in oauth_states.items()
        if (current_time - data["created_at"]).total_seconds() > 600  # 10 minutes
    ]
    for state in expired_states:
        del oauth_states[state] 