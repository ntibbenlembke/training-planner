from fastapi import FastAPI
from users import router as user_router


app = FastAPI(title="Training Planner App", 
              description="API for managing training planner data")

app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Training Planner API"}