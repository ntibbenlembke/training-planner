from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

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
        orm_mode = True

class User(UserInDB):
    pass

# Training Plan schemas
class TrainingPlanBase(BaseModel):
    title: str
    description: Optional[str] = None

class TrainingPlanCreate(TrainingPlanBase):
    pass

class TrainingPlanUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TrainingPlanInDB(TrainingPlanBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class TrainingPlan(TrainingPlanInDB):
    pass 