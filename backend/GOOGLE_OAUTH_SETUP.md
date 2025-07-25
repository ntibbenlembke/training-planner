# Google OAuth Setup Guide

This guide will help you set up Google OAuth for calendar access in your training planner application.

## Prerequisites

1. Google Cloud Console account
2. Project with Google Calendar API enabled

## Step 1: Google Cloud Console Setup

### 1.1 Create OAuth 2.0 Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project or create a new one
3. Navigate to **APIs & Services** > **Credentials**
4. Click **Create Credentials** > **OAuth 2.0 Client IDs**
5. Choose **Web application** as the application type
6. Add the following to **Authorized redirect URIs**:
   ```
   http://localhost:8000/auth/google/callback
   ```
7. Save and copy your **Client ID** and **Client Secret**

### 1.2 Enable Google Calendar API

1. Go to **APIs & Services** > **Library**
2. Search for "Google Calendar API"
3. Click on it and press **Enable**

## Step 2: Environment Configuration

Create a `.env` file in the `backend/` directory with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/dbname

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# Development settings
ENVIRONMENT=development
```

## Step 3: Database Migration

The OAuth integration adds new fields to the User model. You'll need to update your database:

1. **New User fields added:**
   - `google_id` - Google user identifier
   - `google_access_token` - OAuth access token
   - `google_refresh_token` - OAuth refresh token
   - `google_token_expires_at` - Token expiration timestamp
   - `google_calendar_connected` - Boolean flag for calendar connection status

2. **Run database migration:**
   ```bash
   # If using Alembic (recommended)
   alembic revision --autogenerate -m "Add Google OAuth fields"
   alembic upgrade head
   
   # Or drop and recreate tables (development only)
   # This will lose existing data!
   python -c "from database.init_db import init_db; init_db()"
   ```

## Step 4: How to Use

### 4.1 OAuth Flow

1. **Initiate OAuth login:**
   ```
   GET /auth/google/login
   ```
   Returns: `{"authorization_url": "...", "state": "..."}`

2. **User visits authorization_url and grants permissions**

3. **Google redirects to callback URL:**
   ```
   GET /auth/google/callback?code=...&state=...
   ```
   Returns user information and authentication status

### 4.2 Calendar Integration

1. **Check calendar connection status:**
   ```
   GET /auth/user/calendar-status?user_id={user_id}
   ```

2. **Get user's Google calendars:**
   ```
   GET /calendar/google/calendars?user_id={user_id}
   ```

3. **Sync events from Google Calendar:**
   ```
   POST /calendar/sync-google-calendar?user_id={user_id}&start_date=...&end_date=...
   ```

4. **Get events with optional Google sync:**
   ```
   GET /calendar/events/{start_date}/{end_date}?user_id={user_id}&sync_google=true
   ```

## Step 5: Frontend Integration Example

```javascript
// Initiate OAuth flow
const response = await fetch('/auth/google/login');
const { authorization_url } = await response.json();

// Redirect user to Google OAuth
window.location.href = authorization_url;

// After callback, check calendar status
const statusResponse = await fetch(`/auth/user/calendar-status?user_id=${userId}`);
const { connected } = await statusResponse.json();

if (connected) {
    // Sync calendar events
    await fetch(`/calendar/sync-google-calendar?user_id=${userId}&start_date=${start}&end_date=${end}`, {
        method: 'POST'
    });
}
```

## API Endpoints Summary

### Authentication
- `GET /auth/google/login` - Initiate OAuth flow
- `GET /auth/google/callback` - Handle OAuth callback
- `GET /auth/user/calendar-status` - Check calendar connection

### Calendar Integration
- `GET /calendar/google/calendars` - List user's Google calendars
- `POST /calendar/sync-google-calendar` - Sync events from Google Calendar
- `GET /calendar/events/{start}/{end}` - Get events (with optional Google sync)

## Security Notes

1. **State Parameter**: The OAuth flow uses a secure state parameter to prevent CSRF attacks
2. **Token Storage**: OAuth tokens are securely stored in the database
3. **Token Refresh**: Expired tokens are automatically refreshed when needed
4. **Scopes**: The integration requests minimal required scopes:
   - `calendar.readonly` - Read calendar events
   - `calendar.events` - Create/modify calendar events
   - `openid`, `email`, `profile` - User identification

## Troubleshooting

### Common Issues

1. **"Invalid redirect URI"**
   - Ensure the redirect URI in Google Console matches exactly: `http://localhost:8000/auth/google/callback`

2. **"Calendar API not enabled"**
   - Enable Google Calendar API in Google Cloud Console

3. **"Invalid state parameter"**
   - This can happen if the OAuth flow times out (10 minutes). Restart the process.

4. **Token refresh failures**
   - User may need to re-authenticate if refresh token is invalid

### Debug Mode

Add logging to see OAuth flow details:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Production Considerations

1. **Use HTTPS**: Replace `http://localhost:8000` with your production HTTPS URL
2. **Token Security**: Consider encrypting stored tokens
3. **Rate Limiting**: Implement rate limiting for OAuth endpoints
4. **Error Handling**: Add comprehensive error handling and user feedback
5. **Token Cleanup**: Implement periodic cleanup of expired tokens 