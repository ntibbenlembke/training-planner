from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from database.database import get_db
from database import schemas, crud

router = APIRouter()
"""
@router.post("/events", response_model=schemas.Event, status_code=status.HTTP_201_CREATED)
async def create_event(
    event: schemas.EventCreate,
    user_id: int,  # In a real app, you would get this from auth token
    db: Session = Depends(get_db)
):
    # Check if training plan exists if provided
    if event.training_plan_id:
        training_plan = crud.get_training_plan(db, event.training_plan_id)
        if not training_plan:
            raise HTTPException(
                status_code=404,
                detail=f"Training plan with id {event.training_plan_id} not found"
            )
        # Verify user owns the training plan
        if training_plan.owner_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to add events to this training plan"
            )
    
    # Create the event
    return crud.create_event(db=db, event=event, user_id=user_id)

@router.get("/events", response_model=List[schemas.Event])
async def get_events(
    user_id: int,  # In a real app, you would get this from auth token
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    events = crud.get_user_events(db, user_id=user_id, skip=skip, limit=limit)
    return events

@router.get("/events/{event_id}", response_model=schemas.Event)
async def get_event(
    event_id: int,
    user_id: int,  # In a real app, you would get this from auth token
    db: Session = Depends(get_db)
):
    event = crud.get_event(db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this event")
    return event

@router.put("/events/{event_id}", response_model=schemas.Event)
async def update_event(
    event_id: int,
    event_update: schemas.EventUpdate,
    user_id: int,  # In a real app, you would get this from auth token
    db: Session = Depends(get_db)
):
    # Check if event exists and user owns it
    db_event = crud.get_event(db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this event")
    
    # If changing training plan, verify user owns the new plan
    if event_update.training_plan_id is not None:
        if event_update.training_plan_id > 0:  # Only check if assigning to a plan (not removing)
            training_plan = crud.get_training_plan(db, event_update.training_plan_id)
            if not training_plan:
                raise HTTPException(status_code=404, detail="Training plan not found")
            if training_plan.owner_id != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="You do not have permission to add events to this training plan"
                )
    
    # Update the event
    updated_event = crud.update_event(db, event_id=event_id, event=event_update)
    return updated_event

@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    user_id: int,  # In a real app, you would get this from auth token
    db: Session = Depends(get_db)
):
    # Check if event exists and user owns it
    db_event = crud.get_event(db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")
    
    # Delete the event
    crud.delete_event(db, event_id=event_id)
    return None"""