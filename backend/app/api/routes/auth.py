from fastapi import APIRouter, Depends
from app.schemas.auth import UserRegister, UserLogin, Token, UserResponse
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.core.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

from app.repositories.mongo_user_repository import MongoUserRepository

def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(MongoUserRepository(UserRepository(db)))

from fastapi.security import OAuth2PasswordRequestForm
from app.core.dependencies import get_current_active_user
from app.models.user import User

@router.post("/register", response_model=UserResponse)
async def register(data: UserRegister, service: AuthService = Depends(get_auth_service)):
    return await service.register(data)

from fastapi import Request
from app.core.exceptions import UnauthorizedError

@router.post("/login", response_model=Token)
async def login(
    request: Request,
    service: AuthService = Depends(get_auth_service)
):
    content_type = request.headers.get("content-type", "")
    username = ""
    password = ""
    
    if "application/json" in content_type:
        body = await request.json()
        username = body.get("username") or body.get("email", "")
        password = body.get("password", "")
    elif "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        form = await request.form()
        username = form.get("username") or form.get("email", "")
        password = form.get("password", "")
    else:
        # Fallback attempt json then form
        try:
            body = await request.json()
            username = body.get("username") or body.get("email", "")
            password = body.get("password", "")
        except Exception:
            form = await request.form()
            username = form.get("username") or form.get("email", "")
            password = form.get("password", "")

    if not username or not password:
        raise UnauthorizedError("Missing username/email or password")

    login_data = UserLogin(username=str(username), password=str(password))
    token = await service.authenticate(login_data)
    return Token(access_token=token, token_type="bearer")

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    return current_user
