import os
from typing import List

# Google OAuth 2.0 settings
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback")

# Google Calendar API scopes
GOOGLE_SCOPES: List[str] = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events",
    "openid",
    "email",
    "profile"
]

# OAuth flow settings
OAUTH_STATE_EXPIRE_SECONDS = 600  # 10 minutes

def get_oauth_config():
    """Get OAuth configuration dictionary for google-auth-oauthlib"""
    return {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [GOOGLE_REDIRECT_URI]
        }
    } 