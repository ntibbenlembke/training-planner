from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import (
    calendar_router,
    user_router,
    planner_router
)
from database.init_db import init_db

async def lifespan(app: FastAPI):
     #init_db()
    yield

app = FastAPI(title="Training Planner App", 
              description="API for managing training planner data",
              lifespan=lifespan
        )

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(user_router.router, prefix="/user", tags=["user"])
app.include_router(calendar_router.router, prefix="/calendar", tags=["calendar"])
app.include_router(planner_router.router, prefix="/planner", tags=["planner"])

@app.get("/healthcheck")
async def healthcheck():
    return {"message": "Welcome to the Training Planner API"}