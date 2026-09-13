from fastapi import APIRouter, Depends
from app.schemas.auth import UserRegister, UserLogin, Token, UserResponse
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.core.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))

@router.post("/register", response_model=UserResponse)
async def register(data: UserRegister, service: AuthService = Depends(get_auth_service)):
    return await service.register(data)

@router.post("/login", response_model=Token)
async def login(data: UserLogin, service: AuthService = Depends(get_auth_service)):
    token = await service.authenticate(data)
    return Token(access_token=token, token_type="bearer")
