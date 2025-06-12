from fastapi import FastAPI
from api import (
    calendar_router,
    user_router
)
from database.init_db import init_db

async def lifespan(app: FastAPI):
     #init_db()
    yield

app = FastAPI(title="Training Planner App", 
              description="API for managing training planner data",
              lifespan=lifespan
        )

app.include_router(user_router.router, prefix="/user", tags=["user"])
app.include_router(calendar_router.router, prefix="/calendar", tags=["calendar"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Training Planner API"}