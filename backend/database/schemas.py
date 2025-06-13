from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class User(UserInDB):
    pass

# Training Plan Status Enum
class TrainingPlanStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# Plan Preferences schemas
class PlanPreferencesBase(BaseModel):
    frequency: int
    time_of_day: str
    duration: int
    prep_time: int
    cooldown_time: int
    workout_types: List[str]
    difficulty_level: str
    days_of_week: List[str]

class PlanPreferencesCreate(PlanPreferencesBase):
    pass

class PlanPreferences(PlanPreferencesBase):
    id: int
    training_plan_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Training Plan schemas
class TrainingPlanBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    status: Optional[TrainingPlanStatus] = TrainingPlanStatus.ACTIVE

class TrainingPlanCreate(TrainingPlanBase):
    preferences: PlanPreferencesCreate

class TrainingPlan(TrainingPlanBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    preferences: Optional[PlanPreferences] = None

    class Config:
        from_attributes = True

# Event schemas
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    event_type: Optional[str] = None
    workout_type: Optional[str] = None
    difficulty_level: Optional[str] = None

class EventCreate(EventBase):
    training_plan_id: Optional[int] = None

class Event(EventBase):
    id: int
    user_id: int
    training_plan_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    event_type: Optional[str] = None
    workout_type: Optional[str] = None
    difficulty_level: Optional[str] = None

# Plan Generation Request schema
class PlanGenerationRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    frequency: int
    time_of_day: str
    duration: int
    prep_time: int
    cooldown_time: int
    workout_types: List[str]
    difficulty_level: str
    days_of_week: List[str]

# Plan Generation Response schema
class PlanGenerationResponse(BaseModel):
    training_plan: TrainingPlan
    events: List[Event]
    message: str

#planner schemas
class Preferences(BaseModel):
    start_date: datetime
    end_date: datetime
    frequency: int
    time_of_day: str
    duration: int
    prep_time: int
    cooldown_time: int
    workout_types: List[str]
    difficulty_level: str
    days_of_week: List[str]

class Planner(BaseModel):
    id: int
    user_id: int
    preferences: Preferences
    created_at: datetime
    updated_at: Optional[datetime] = None
    