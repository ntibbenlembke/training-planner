"""- GET suggestions/weekly
- GET suggestions/weekly/{date}
- GET suggestions/optimal?date=2025-06-15
- GET suggestions/optimal?duration=60&difficulty=moderate"""

from fastapi import APIRouter

router = APIRouter()

@router.post("/create-training-plan")
async def create_planner():
    return {"message": "Imagine this created an awesome plan"}

@router.get("/get-training-plan")
async def get_planner(date: str):
    return {"message": "Just imagine this fetched an awesome plan"}
