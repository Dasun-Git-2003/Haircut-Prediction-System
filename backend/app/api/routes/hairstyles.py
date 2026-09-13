from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.dependencies import get_db, get_admin_user
from app.repositories.hairstyle_repository import HairstyleRepository
from app.services.hairstyle_service import HairstyleService
from app.schemas.hairstyle import HairstyleResponse, HairstyleCreate, HairstyleUpdate

router = APIRouter()

from app.repositories.mongo_hairstyle_repository import MongoHairstyleRepository

def get_hairstyle_service(db: AsyncSession = Depends(get_db)) -> HairstyleService:
    return HairstyleService(MongoHairstyleRepository(HairstyleRepository(db)))

@router.get("/", response_model=List[HairstyleResponse])
async def get_hairstyles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: HairstyleService = Depends(get_hairstyle_service)
):
    return await service.get_all_hairstyles(skip=skip, limit=limit)

@router.get("/{id}", response_model=HairstyleResponse)
async def get_hairstyle(
    id: str,
    service: HairstyleService = Depends(get_hairstyle_service)
):
    h = await service.get_hairstyle_by_id(id)
    if not h:
        raise HTTPException(status_code=404, detail="Hairstyle not found")
    return h

@router.post("/", response_model=HairstyleResponse, dependencies=[Depends(get_admin_user)])
async def create_hairstyle(
    data: HairstyleCreate,
    service: HairstyleService = Depends(get_hairstyle_service)
):
    return await service.create_hairstyle(data)

@router.put("/{id}", response_model=HairstyleResponse, dependencies=[Depends(get_admin_user)])
async def update_hairstyle(
    id: str,
    data: HairstyleUpdate,
    service: HairstyleService = Depends(get_hairstyle_service)
):
    updated = await service.update_hairstyle(id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Hairstyle not found")
    return updated

@router.delete("/{id}", dependencies=[Depends(get_admin_user)])
async def delete_hairstyle(
    id: str,
    service: HairstyleService = Depends(get_hairstyle_service)
):
    success = await service.delete_hairstyle(id)
    if not success:
        raise HTTPException(status_code=404, detail="Hairstyle not found")
    return {"message": "Hairstyle deleted successfully"}
