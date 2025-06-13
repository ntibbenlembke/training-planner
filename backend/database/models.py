from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    events = relationship("Event", back_populates="user")
    training_plans = relationship("TrainingPlan", back_populates="user")

class TrainingPlanStatus(enum.Enum):
    draft = "draft"
    active = "active"
    completed = "completed"
    cancelled = "cancelled"

class TrainingPlan(Base):
    __tablename__ = "training_plans"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    status = Column(Enum(TrainingPlanStatus), default=TrainingPlanStatus.active)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="training_plans")
    events = relationship("Event", back_populates="training_plan")
    preferences = relationship("PlanPreferences", back_populates="training_plan", uselist=False)

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    user_id = Column(Integer, ForeignKey("users.id"))
    training_plan_id = Column(Integer, ForeignKey("training_plans.id"), nullable=True)  # Nullable for manual events
    event_type = Column(String, nullable=True)  # 'workout', 'prep', 'cooldown', etc.
    workout_type = Column(String, nullable=True)  # 'cycling', 'running', etc.
    difficulty_level = Column(String, nullable=True)  # 'easy', 'moderate', 'hard', 'expert'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="events")
    training_plan = relationship("TrainingPlan", back_populates="events")

class PlanPreferences(Base):
    __tablename__ = "plan_preferences"

    id = Column(Integer, primary_key=True, index=True)
    training_plan_id = Column(Integer, ForeignKey("training_plans.id"))
    frequency = Column(Integer)  # workouts per week
    time_of_day = Column(String)  # 'morning', 'afternoon', 'evening'
    duration = Column(Integer)  # workout duration in minutes
    prep_time = Column(Integer)  # prep time in minutes
    cooldown_time = Column(Integer)  # cooldown time in minutes
    workout_types = Column(JSON)  # list of workout types
    difficulty_level = Column(String)  # 'easy', 'moderate', 'hard', 'expert'
    days_of_week = Column(JSON)  # preferred days of week
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    training_plan = relationship("TrainingPlan", back_populates="preferences")
