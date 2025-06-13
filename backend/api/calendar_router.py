from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from database.database import get_db
from database import schemas, crud
from datetime import datetime

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
    db: Session = Depends(get_db)
):
    events = crud.get_events_by_date(db, start_date=start_date, end_date=end_date)
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