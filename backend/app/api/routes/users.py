from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.auth import UserResponse

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_active_user)):
    return current_user
