from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session):
    return db.query(models.User).all()

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

"""
# Event CRUD operations
def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()

def get_user_events(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Event).filter(models.Event.user_id == user_id).offset(skip).limit(limit).all()

def get_training_plan_events(db: Session, training_plan_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Event).filter(models.Event.training_plan_id == training_plan_id).offset(skip).limit(limit).all()

def create_event(db: Session, event: schemas.EventCreate, user_id: int):
    db_event = models.Event(
        **event.model_dump(),
        user_id=user_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

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
    return True """