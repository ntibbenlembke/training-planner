import os
import json
from typing import List
from pathlib import Path

# Path to credentials.json file
CREDENTIALS_FILE = Path(__file__).parent.parent / "credentials.json"

# Load credentials from file
try:
    with open(CREDENTIALS_FILE, "r") as f:
        CREDENTIALS = json.load(f)
    # Extract client ID and secret from credentials
    GOOGLE_CLIENT_ID = CREDENTIALS["web"]["client_id"]
    GOOGLE_CLIENT_SECRET = CREDENTIALS["web"]["client_secret"]
except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
    # Fall back to environment variables if file loading fails
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    print(f"Warning: Failed to load credentials from file: {e}")
    print("Falling back to environment variables.")

# Redirect URI (can be overridden by environment variable)
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:51335/")

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
    # If we've loaded credentials from file, return them directly
    if CREDENTIALS_FILE.exists():
        try:
            with open(CREDENTIALS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    # Otherwise build config from individual variables
    return {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [GOOGLE_REDIRECT_URI]
        }
    }