from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db

router = APIRouter()

class Event(BaseModel):
    id: Optional[str] = None
    title: str

@router.post("/events")
async def create_event(
    db: AsyncSession = Depends(get_db)
):
    return {"message": "Event created successfully"}

@router.get("/events")
async def get_events():
    return {"message": "Events fetched successfully"}

@router.get("/events/{id}")
async def get_event(id: str):
    return {"message": "Event fetched successfully"}

@router.put("/events/{id}")
async def update_event(id: str, event: Event):
    return {"message": "Event updated successfully"}

@router.delete("/events/{id}")
async def delete_event(id: str):
    return {"message": "Event deleted successfully"}