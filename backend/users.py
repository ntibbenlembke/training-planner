from fastapi import APIRouter, UploadFile, File, Body, Depends, status
from io import StringIO, BytesIO
from fastapi.responses import JSONResponse
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/profile/")
async def get_user_profile():
    return {"message": "Welcome to the user profile API"}
