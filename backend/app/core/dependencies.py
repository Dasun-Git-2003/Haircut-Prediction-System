from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.core.config import settings
from app.core.exceptions import UnauthorizedError, ForbiddenError
from app.database.database import get_async_session
# Note: Models will be imported later
# from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_db() -> AsyncSession:
    async for session in get_async_session():
        yield session

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise UnauthorizedError("Invalid authentication credentials")
    except JWTError:
        raise UnauthorizedError("Invalid authentication credentials")
    
    # We will fetch user properly when user repository is set up
    # user = await db.get(User, user_id)
    # if user is None:
    #     raise UnauthorizedError("User not found")
    # return user
    return {"id": user_id, "is_active": True, "is_admin": True} # Mock for now

async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if not current_user.get("is_active"):
        raise UnauthorizedError("Inactive user")
    return current_user

async def get_admin_user(current_user: dict = Depends(get_current_active_user)):
    if not current_user.get("is_admin"):
        raise ForbiddenError("Not enough privileges")
    return current_user
