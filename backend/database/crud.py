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
    
    user_data = user.dict(exclude_unset=True)
    
    # If updating password, hash it
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

# Training Plan CRUD operations
def get_training_plan(db: Session, plan_id: int):
    return db.query(models.TrainingPlan).filter(models.TrainingPlan.id == plan_id).first()

def get_user_training_plans(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.TrainingPlan).filter(models.TrainingPlan.owner_id == user_id).offset(skip).limit(limit).all()

def create_training_plan(db: Session, plan: schemas.TrainingPlanCreate, user_id: int):
    db_plan = models.TrainingPlan(**plan.dict(), owner_id=user_id)
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def update_training_plan(db: Session, plan_id: int, plan: schemas.TrainingPlanUpdate):
    db_plan = get_training_plan(db, plan_id)
    if not db_plan:
        return None
    
    plan_data = plan.dict(exclude_unset=True)
    
    for key, value in plan_data.items():
        setattr(db_plan, key, value)
    
    db.commit()
    db.refresh(db_plan)
    return db_plan

def delete_training_plan(db: Session, plan_id: int):
    db_plan = get_training_plan(db, plan_id)
    if not db_plan:
        return False
    db.delete(db_plan)
    db.commit()
    return True 