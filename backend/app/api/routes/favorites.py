from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel
import uuid

from app.core.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.models.favorite import Favorite
from app.repositories.favorite_repository import FavoriteRepository
from app.repositories.mongo_favorite_repository import MongoFavoriteRepository

router = APIRouter()

def get_favorite_repo(db: AsyncSession = Depends(get_db)) -> MongoFavoriteRepository:
    return MongoFavoriteRepository(FavoriteRepository(db))

class FavoriteCreate(BaseModel):
    hairstyle_id: str
    tryon_result_id: str | None = None

class FavoriteResponse(BaseModel):
    id: str
    user_id: str
    hairstyle_id: str
    tryon_result_id: str | None = None

@router.get("/", response_model=List[FavoriteResponse])
async def get_favorites(
    current_user: User = Depends(get_current_active_user),
    repo: MongoFavoriteRepository = Depends(get_favorite_repo)
):
    favs = await repo.get_by_user_id(current_user.id)
    return [
        FavoriteResponse(
            id=f.id,
            user_id=f.user_id,
            hairstyle_id=f.hairstyle_id,
            tryon_result_id=f.tryon_result_id
        )
        for f in favs
    ]

@router.post("/", response_model=FavoriteResponse)
async def add_favorite(
    data: FavoriteCreate,
    current_user: User = Depends(get_current_active_user),
    repo: MongoFavoriteRepository = Depends(get_favorite_repo)
):
    fav = Favorite(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        hairstyle_id=data.hairstyle_id,
        tryon_result_id=data.tryon_result_id
    )
    created = await repo.create(fav)
    return FavoriteResponse(
        id=created.id,
        user_id=created.user_id,
        hairstyle_id=created.hairstyle_id,
        tryon_result_id=created.tryon_result_id
    )

@router.delete("/{id}")
async def remove_favorite(
    id: str,
    current_user: User = Depends(get_current_active_user),
    repo: MongoFavoriteRepository = Depends(get_favorite_repo)
):
    fav = await repo.get_by_id(id)
    if not fav or fav.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Favorite not found")
        
    await repo.delete(fav)
    return {"message": "Favorite removed successfully"}
