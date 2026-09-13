from fastapi import APIRouter
from typing import List
from app.schemas.hairstyle import HairstyleResponse

router = APIRouter()

@router.get("/", response_model=List[HairstyleResponse])
async def get_hairstyles():
    return []
