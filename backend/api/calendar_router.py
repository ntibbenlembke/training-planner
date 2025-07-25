from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from database.database import get_db
from database import schemas, crud
from datetime import datetime
from services.google_calendar import get_google_calendar_service

router = APIRouter()

@router.post("/events", response_model=schemas.Event, status_code=status.HTTP_201_CREATED)
async def create_event(
    event: schemas.EventCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    return crud.create_event(db=db, event=event, user_id=user_id)


@router.get("/events", response_model=List[schemas.Event])
async def get_all_events(
    user_id: int,
    db: Session = Depends(get_db)
):
    events = crud.get_all_events(db)
    return events


@router.get("/events/{event_id}", response_model=schemas.Event)
async def get_event(
    event_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    event = crud.get_event(db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this event")
    return event

@router.get("/events/{start_date}/{end_date}", response_model=List[schemas.Event])
async def get_events_by_date(
    start_date: datetime,
    end_date: datetime,
    user_id: int,
    sync_google: bool = False,
    db: Session = Depends(get_db)
):
    # If sync_google is True, try to sync with Google Calendar first
    if sync_google:
        try:
            await sync_google_calendar_events(user_id, start_date, end_date, db)
        except Exception as e:
            # Log the error but don't fail the request
            print(f"Google Calendar sync failed: {e}")
    
    events = crud.get_user_events_by_date(db, user_id=user_id, start_date=start_date, end_date=end_date)
    return events

@router.put("/events/{event_id}", response_model=schemas.Event)
async def update_event(
    event_id: int,
    event_update: schemas.EventUpdate,
    user_id: int,
    db: Session = Depends(get_db)
):
    db_event = crud.get_event(db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this event")
    
    updated_event = crud.update_event(db, event_id=event_id, event=event_update)
    return updated_event


@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    db_event = crud.get_event(db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")
    
    crud.delete_event(db, event_id=event_id)
    return None

@router.get("/google/calendars")
async def get_google_calendars(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get list of user's Google calendars"""
    try:
        calendar_service = get_google_calendar_service(db, user_id)
        calendars = calendar_service.list_calendars()
        return {"calendars": calendars}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get Google calendars: {str(e)}"
        )

@router.post("/sync-google-calendar")
async def sync_google_calendar(
    user_id: int,
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db)
):
    """Manually sync events from Google Calendar"""
    try:
        await sync_google_calendar_events(user_id, start_date, end_date, db)
        return {"message": "Google Calendar sync completed successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google Calendar sync failed: {str(e)}"
        )

async def sync_google_calendar_events(user_id: int, start_date: datetime, end_date: datetime, db: Session):
    """Helper function to sync events from Google Calendar to local database"""
    try:
        calendar_service = get_google_calendar_service(db, user_id)
        
        # Get events from Google Calendar
        google_events = calendar_service.get_events(
            time_min=start_date,
            time_max=end_date
        )
        
        # Convert Google events to local events and store them
        for google_event in google_events:
            # Skip if event already exists (check by Google event ID)
            # You might want to add a google_event_id field to your Event model
            
            # Parse start and end times
            start_time = None
            end_time = None
            
            if 'dateTime' in google_event['start']:
                start_time = datetime.fromisoformat(google_event['start']['dateTime'].replace('Z', '+00:00'))
            elif 'date' in google_event['start']:
                # All-day event
                start_time = datetime.fromisoformat(google_event['start']['date'] + 'T00:00:00+00:00')
            
            if 'dateTime' in google_event['end']:
                end_time = datetime.fromisoformat(google_event['end']['dateTime'].replace('Z', '+00:00'))
            elif 'date' in google_event['end']:
                # All-day event
                end_time = datetime.fromisoformat(google_event['end']['date'] + 'T23:59:59+00:00')
            
            if start_time and end_time:
                # Create event in local database
                event_create = schemas.EventCreate(
                    title=google_event.get('summary', 'Untitled'),
                    description=google_event.get('description', ''),
                    start_time=start_time,
                    end_time=end_time,
                    event_type='imported'
                )
                
                # Check if event already exists to avoid duplicates
                existing_events = crud.get_user_events_by_date(db, user_id, start_time, end_time)
                duplicate = any(
                    event.title == event_create.title and 
                    event.start_time == event_create.start_time
                    for event in existing_events
                )
                
                if not duplicate:
                    crud.create_event(db=db, event=event_create, user_id=user_id)
        
    except Exception as e:
        raise Exception(f"Failed to sync Google Calendar events: {str(e)}")