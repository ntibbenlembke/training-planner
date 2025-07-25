from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from database import models, crud
from config.oauth import get_oauth_config

class GoogleCalendarService:
    """Service class for Google Calendar API operations"""
    
    def __init__(self, user: models.User):
        self.user = user
        self._service = None
    
    def get_credentials(self) -> Optional[Credentials]:
        """Get valid Google credentials for the user"""
        if not self.user.google_access_token or not self.user.google_refresh_token:
            return None
        
        credentials = Credentials(
            token=self.user.google_access_token,
            refresh_token=self.user.google_refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=get_oauth_config()["web"]["client_id"],
            client_secret=get_oauth_config()["web"]["client_secret"],
            expiry=self.user.google_token_expires_at
        )
        
        # Refresh if expired
        if credentials.expired and credentials.refresh_token:
            request = GoogleRequest()
            credentials.refresh(request)
            # Note: You should update the user's tokens in the database here
        
        return credentials
    
    def get_service(self):
        """Get Google Calendar service instance"""
        if not self._service:
            credentials = self.get_credentials()
            if not credentials:
                raise ValueError("No valid Google credentials available")
            self._service = build('calendar', 'v3', credentials=credentials)
        return self._service
    
    def list_calendars(self) -> List[Dict]:
        """List all calendars for the user"""
        try:
            service = self.get_service()
            calendars_result = service.calendarList().list().execute()
            return calendars_result.get('items', [])
        except HttpError as error:
            raise Exception(f"Failed to list calendars: {error}")
    
    def get_events(self, calendar_id: str = 'primary', 
                   time_min: Optional[datetime] = None,
                   time_max: Optional[datetime] = None,
                   max_results: int = 100) -> List[Dict]:
        """Get events from a specific calendar"""
        try:
            service = self.get_service()
            
            # Format times for Google Calendar API
            time_min_str = time_min.isoformat() if time_min else None
            time_max_str = time_max.isoformat() if time_max else None
            
            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=time_min_str,
                timeMax=time_max_str,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
        except HttpError as error:
            raise Exception(f"Failed to get events: {error}")
    
    def create_event(self, calendar_id: str = 'primary', 
                    title: str = '', description: str = '',
                    start_time: datetime = None, end_time: datetime = None,
                    attendees: List[str] = None) -> Dict:
        """Create a new event in Google Calendar"""
        try:
            service = self.get_service()
            
            event_body = {
                'summary': title,
                'description': description,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': str(start_time.tzinfo) if start_time.tzinfo else 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': str(end_time.tzinfo) if end_time.tzinfo else 'UTC',
                },
            }
            
            if attendees:
                event_body['attendees'] = [{'email': email} for email in attendees]
            
            event = service.events().insert(
                calendarId=calendar_id,
                body=event_body
            ).execute()
            
            return event
        except HttpError as error:
            raise Exception(f"Failed to create event: {error}")
    
    def update_event(self, event_id: str, calendar_id: str = 'primary',
                    title: str = None, description: str = None,
                    start_time: datetime = None, end_time: datetime = None) -> Dict:
        """Update an existing event in Google Calendar"""
        try:
            service = self.get_service()
            
            # Get the existing event
            event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
            
            # Update fields if provided
            if title:
                event['summary'] = title
            if description:
                event['description'] = description
            if start_time:
                event['start'] = {
                    'dateTime': start_time.isoformat(),
                    'timeZone': str(start_time.tzinfo) if start_time.tzinfo else 'UTC',
                }
            if end_time:
                event['end'] = {
                    'dateTime': end_time.isoformat(),
                    'timeZone': str(end_time.tzinfo) if end_time.tzinfo else 'UTC',
                }
            
            updated_event = service.events().update(
                calendarId=calendar_id,
                eventId=event_id,
                body=event
            ).execute()
            
            return updated_event
        except HttpError as error:
            raise Exception(f"Failed to update event: {error}")
    
    def delete_event(self, event_id: str, calendar_id: str = 'primary'):
        """Delete an event from Google Calendar"""
        try:
            service = self.get_service()
            service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        except HttpError as error:
            raise Exception(f"Failed to delete event: {error}")


def get_google_calendar_service(db: Session, user_id: int) -> GoogleCalendarService:
    """Factory function to create GoogleCalendarService instance"""
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise ValueError("User not found")
    
    if not user.google_calendar_connected:
        raise ValueError("User has not connected Google Calendar")
    
    return GoogleCalendarService(user) 