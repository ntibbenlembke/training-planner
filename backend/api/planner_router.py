"""- GET suggestions/weekly
- GET suggestions/weekly/{date}
- GET suggestions/optimal?date=2025-06-15
- GET suggestions/optimal?duration=60&difficulty=moderate"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db
from database import schemas, crud
from typing import List

router = APIRouter()

@router.post("/create-training-plan", response_model=schemas.PlanGenerationResponse)
async def create_training_plan(
    request: schemas.PlanGenerationRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Generate a training plan with events based on user preferences.
    
    This endpoint will:
    1. Search for existing events in the specified date range
    2. Find available time slots that don't conflict with existing events
    3. Generate the requested number of workout events
    4. Create prep and cooldown events if specified
    5. Link all events to a training plan
    6. Return the created training plan and events
    """
    try:
        result = crud.create_training_plan_with_events(db, user_id, request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create training plan: {str(e)}"
        )

@router.get("/training-plans", response_model=List[schemas.TrainingPlan])
async def get_user_training_plans(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all training plans for a user."""
    training_plans = crud.get_user_training_plans(db, user_id)
    return training_plans

@router.get("/training-plans/{plan_id}", response_model=schemas.TrainingPlan)
async def get_training_plan(
    plan_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific training plan by ID."""
    plan = crud.get_training_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Training plan not found")
    if plan.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this training plan")
    return plan

@router.get("/training-plans/{plan_id}/events", response_model=List[schemas.Event])
async def get_training_plan_events(
    plan_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all events associated with a training plan."""
    plan = crud.get_training_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Training plan not found")
    if plan.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this training plan")
    
    events = crud.get_training_plan_events(db, plan_id)
    return events

@router.put("/training-plans/{plan_id}/status")
async def update_training_plan_status(
    plan_id: int,
    status: schemas.TrainingPlanStatus,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Update the status of a training plan."""
    plan = crud.get_training_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Training plan not found")
    if plan.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this training plan")
    
    updated_plan = crud.update_training_plan_status(db, plan_id, status)
    return {"message": f"Training plan status updated to {status.value}"}

@router.delete("/training-plans/{plan_id}")
async def delete_training_plan(
    plan_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete a training plan and all associated events."""
    plan = crud.get_training_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Training plan not found")
    if plan.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this training plan")
    
    success = crud.delete_training_plan(db, plan_id)
    if success:
        return {"message": "Training plan deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete training plan")
