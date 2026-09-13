from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_active_user

router = APIRouter()

@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_active_user)):
    return current_user
