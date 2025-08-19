# Google OAuth Frontend Integration Guide

This guide explains how to set up and use Google OAuth for calendar access in the frontend of the Training Planner application.

## Setup Overview

1. **OAuth Flow**: The application uses the OAuth 2.0 Authorization Code flow with PKCE to authenticate users with Google and gain access to their calendar data.

2. **Components Created**:
   - `AuthContext` - React context for user authentication state
   - `AuthCallback` - Component to handle OAuth callback
   - `LoginPage` - Enhanced with proper OAuth flow

## Configuration Steps

### 1. Google Cloud Console Setup

Ensure your backend is configured with the Google OAuth credentials as described in `backend/GOOGLE_OAUTH_SETUP.md`.

### 2. Environment Setup

Create a `.env` file in the frontend directory:

```
VITE_API_URL=http://localhost:8000
```

### 3. Auth Callback Configuration

Ensure the redirect URL is registered in your Google Cloud Console:
- `http://localhost:5173/auth-callback`

## OAuth Flow Explanation

The OAuth flow implemented follows these steps:

1. **Initiate Login**: User clicks "Login with Google" button on the `LoginPage`
2. **Request Auth URL**: Frontend calls backend endpoint `/auth/google/login` to get authorization URL
3. **Redirect to Google**: User is redirected to Google's consent screen
4. **Google Callback**: After user consent, Google redirects to our `AuthCallback` page with a code and state parameter
5. **Token Exchange**: The callback component sends the code to our backend, which exchanges it for access and refresh tokens
6. **User Creation/Update**: Backend creates or updates user with Google credentials and returns user data
7. **Session Storage**: Frontend stores user data in AuthContext and localStorage
8. **Redirect**: User is redirected to the Calendar page

## Usage Example

```jsx
import { useAuth } from '../context/AuthContext';

function CalendarComponent() {
  const { user, isAuthenticated, checkCalendarStatus } = useAuth();
  
  useEffect(() => {
    if (isAuthenticated && user) {
      // Check if calendar is connected
      checkCalendarStatus(user.id).then(connected => {
        if (connected) {
          // Fetch calendar events
        }
      });
    }
  }, [isAuthenticated, user]);
  
  // Component code
}
```

## Security Considerations

1. **State Parameter**: The OAuth flow uses a secure state parameter to prevent CSRF attacks
2. **Token Storage**: OAuth tokens are stored only on the server, not in the browser
3. **HTTPS in Production**: Always use HTTPS in production environments
4. **Minimal Scopes**: Request only the necessary Google Calendar scopes

## Troubleshooting

### Common Issues

1. **"Redirect URI mismatch"**:
   - Ensure the exact redirect URI is registered in Google Cloud Console
   - For local development: `http://localhost:5173/auth-callback`

2. **"Consent screen error"**:
   - Verify your OAuth consent screen is properly configured
   - Add necessary scopes

3. **Silent failures**:
   - Check browser console for errors
   - Verify backend logs for token exchange issues
