from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.core.config import settings
from app.core.exceptions import UnauthorizedError, ForbiddenError
from app.database.database import get_async_session
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_db() -> AsyncSession:
    async for session in get_async_session():
        yield session

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise UnauthorizedError("Invalid authentication credentials")
    except JWTError:
        raise UnauthorizedError("Invalid authentication credentials")
    
    from app.database.mongodb import get_mongo_db
    mongo_db = get_mongo_db()
    if mongo_db is not None:
        try:
            doc = await mongo_db.users.find_one({"_id": user_id})
            if doc:
                is_active = doc.get("is_active")
                if is_active is None:
                    is_active = True
                is_admin = doc.get("is_admin")
                if is_admin is None:
                    is_admin = False
                return User(
                    id=doc["_id"],
                    email=doc["email"],
                    username=doc["username"],
                    hashed_password=doc["hashed_password"],
                    is_active=bool(is_active),
                    is_admin=bool(is_admin),
                    avatar_url=doc.get("avatar_url")
                )
        except Exception:
            pass

    user = await db.get(User, user_id)
    if user is None:
        raise UnauthorizedError("User not found")
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    is_active = getattr(current_user, "is_active", True)
    if not is_active:
        raise UnauthorizedError("Inactive user")
    return current_user

async def get_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    is_admin = getattr(current_user, "is_admin", False)
    if not is_admin:
        raise ForbiddenError("Not enough privileges")
    return current_user
