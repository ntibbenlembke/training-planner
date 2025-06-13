from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from . import models, schemas

# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "_hashed"
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    user_data = user.model_dump(exclude_unset=True)
    
    if "password" in user_data:
        user_data["hashed_password"] = user_data.pop("password") + "_hashed"
    
    for key, value in user_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True

# Event operations
def create_event(db: Session, event: schemas.EventCreate, user_id: int):
    db_event = models.Event(
        **event.model_dump(),
        user_id=user_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_all_events(db: Session):
    return db.query(models.Event).all()

def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_events_by_date(db: Session, start_date: datetime, end_date: datetime):
    return db.query(models.Event).filter(
        models.Event.start_time >= start_date, 
        models.Event.end_time <= end_date
    ).all()

def get_user_events_by_date(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    return db.query(models.Event).filter(
        models.Event.user_id == user_id,
        models.Event.start_time >= start_date,
        models.Event.end_time <= end_date
    ).all()

def update_event(db: Session, event_id: int, event: schemas.EventUpdate):
    db_event = get_event(db, event_id)
    if not db_event:
        return None
    
    event_data = event.model_dump(exclude_unset=True)
    
    for key, value in event_data.items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int):
    db_event = get_event(db, event_id)
    if not db_event:
        return False
    db.delete(db_event)
    db.commit()
    return True

def create_training_plan(db: Session, plan: schemas.TrainingPlanCreate, user_id: int):
    # Create the training plan
    db_plan = models.TrainingPlan(
        title=plan.title,
        description=plan.description,
        start_date=plan.start_date,
        end_date=plan.end_date,
        status=plan.status,
        user_id=user_id
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    
    # Create the preferences
    db_preferences = models.PlanPreferences(
        training_plan_id=db_plan.id,
        **plan.preferences.model_dump()
    )
    db.add(db_preferences)
    db.commit()
    db.refresh(db_preferences)
    
    return db_plan

def get_training_plan(db: Session, plan_id: int):
    return db.query(models.TrainingPlan).filter(models.TrainingPlan.id == plan_id).first()

def get_user_training_plans(db: Session, user_id: int):
    return db.query(models.TrainingPlan).filter(models.TrainingPlan.user_id == user_id).all()

def get_training_plan_events(db: Session, plan_id: int):
    return db.query(models.Event).filter(models.Event.training_plan_id == plan_id).all()

def update_training_plan_status(db: Session, plan_id: int, status: schemas.TrainingPlanStatus):
    db_plan = get_training_plan(db, plan_id)
    if not db_plan:
        return None
    
    # Convert the schema enum value to the models enum
    model_status = models.TrainingPlanStatus(status.value)
    db_plan.status = model_status
    db.commit()
    db.refresh(db_plan)
    return db_plan

def delete_training_plan(db: Session, plan_id: int):
    db_plan = get_training_plan(db, plan_id)
    if not db_plan:
        return False
    
    # Delete associated events
    db.query(models.Event).filter(models.Event.training_plan_id == plan_id).delete()
    
    # Delete associated preferences
    db.query(models.PlanPreferences).filter(models.PlanPreferences.training_plan_id == plan_id).delete()
    
    # Delete the plan
    db.delete(db_plan)
    db.commit()
    return True

# Plan generation helper functions
def find_available_time_slots(db: Session, user_id: int, start_date: datetime, end_date: datetime, 
                             duration_minutes: int, preferred_times: List[str]) -> List[dict]:
    """
    Find available time slots for a user within a date range.
    Returns a list of available slots with start and end times.
    """
    # Get existing events in the date range
    existing_events = get_user_events_by_date(db, user_id, start_date, end_date)
    
    available_slots = []
    current_date = start_date.date()
    end_date_only = end_date.date()
    
    # Time preferences mapping
    time_ranges = {
        'morning': (6, 12),
        'afternoon': (12, 18),
        'evening': (18, 22)
    }
    
    while current_date <= end_date_only:
        for time_preference in preferred_times:
            if time_preference in time_ranges:
                start_hour, end_hour = time_ranges[time_preference]
                
                # Check each hour slot in the preferred time range
                for hour in range(start_hour, end_hour):
                    # Create timezone-aware datetime objects
                    slot_start = datetime.combine(current_date, datetime.min.time().replace(hour=hour))
                    
                    # Make the datetime timezone-aware to match database datetimes
                    if slot_start.tzinfo is None:
                        slot_start = slot_start.replace(tzinfo=start_date.tzinfo or timezone.utc)
                    
                    slot_end = slot_start + timedelta(minutes=duration_minutes)
                    
                    # Check if this slot conflicts with existing events
                    conflicts = False
                    for event in existing_events:
                        if (slot_start < event.end_time and slot_end > event.start_time):
                            conflicts = True
                            break
                    
                    if not conflicts:
                        available_slots.append({
                            'start_time': slot_start,
                            'end_time': slot_end,
                            'date': current_date,
                            'time_preference': time_preference
                        })
        
        current_date += timedelta(days=1)
    
    return available_slots

def create_training_plan_with_events(db: Session, user_id: int, 
                                   request: schemas.PlanGenerationRequest) -> schemas.PlanGenerationResponse:
    """
    Generate a complete training plan with events based on user preferences.
    """
    # Create the training plan
    plan_data = schemas.TrainingPlanCreate(
        title=f"Training Plan - {request.start_date.strftime('%Y-%m-%d')}",
        description="Auto-generated training plan",
        start_date=request.start_date,
        end_date=request.end_date,
        preferences=schemas.PlanPreferencesCreate(
            frequency=request.frequency,
            time_of_day=request.time_of_day,
            duration=request.duration,
            prep_time=request.prep_time,
            cooldown_time=request.cooldown_time,
            workout_types=request.workout_types,
            difficulty_level=request.difficulty_level,
            days_of_week=request.days_of_week
        )
    )
    
    training_plan = create_training_plan(db, plan_data, user_id)
    
    # Find available time slots
    total_duration = request.prep_time + request.duration + request.cooldown_time
    available_slots = find_available_time_slots(
        db, user_id, request.start_date, request.end_date, 
        total_duration, [request.time_of_day]
    )
    
    # Filter by preferred days if specified
    if request.days_of_week:
        day_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        preferred_day_indices = [day_names.index(day.lower()) for day in request.days_of_week if day.lower() in day_names]
        available_slots = [slot for slot in available_slots if slot['start_time'].weekday() in preferred_day_indices]
    
    # Select the best slots based on frequency
    selected_slots = available_slots[:request.frequency]
    
    # Create events for each selected slot
    created_events = []
    for i, slot in enumerate(selected_slots):
        workout_type = request.workout_types[i % len(request.workout_types)]
        
        # Create prep event
        if request.prep_time > 0:
            prep_event = create_event(db, schemas.EventCreate(
                title=f"Prep - {workout_type.title()}",
                description="Preparation time",
                start_time=slot['start_time'],
                end_time=slot['start_time'] + timedelta(minutes=request.prep_time),
                event_type="prep",
                workout_type=workout_type,
                difficulty_level=request.difficulty_level,
                training_plan_id=training_plan.id
            ), user_id)
            created_events.append(prep_event)
        
        # Create main workout event
        workout_start = slot['start_time'] + timedelta(minutes=request.prep_time)
        workout_event = create_event(db, schemas.EventCreate(
            title=f"{workout_type.title()} Workout",
            description=f"{request.difficulty_level.title()} {workout_type} workout",
            start_time=workout_start,
            end_time=workout_start + timedelta(minutes=request.duration),
            event_type="workout",
            workout_type=workout_type,
            difficulty_level=request.difficulty_level,
            training_plan_id=training_plan.id
        ), user_id)
        created_events.append(workout_event)
        
        # Create cooldown event
        if request.cooldown_time > 0:
            cooldown_start = workout_start + timedelta(minutes=request.duration)
            cooldown_event = create_event(db, schemas.EventCreate(
                title=f"Cooldown - {workout_type.title()}",
                description="Cooldown time",
                start_time=cooldown_start,
                end_time=cooldown_start + timedelta(minutes=request.cooldown_time),
                event_type="cooldown",
                workout_type=workout_type,
                difficulty_level=request.difficulty_level,
                training_plan_id=training_plan.id
            ), user_id)
            created_events.append(cooldown_event)
    
    message = f"Created {len(selected_slots)} workout sessions with {len(created_events)} total events"
    
    return schemas.PlanGenerationResponse(
        training_plan=training_plan,
        events=created_events,
        message=message
    )