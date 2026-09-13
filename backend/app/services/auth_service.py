from app.schemas.auth import UserRegister, UserLogin
from app.repositories.user_repository import UserRepository
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import UnauthorizedError, AppError
from app.models.user import User

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, data: UserRegister) -> User:
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise AppError(400, "Email already registered")
        
        hashed = get_password_hash(data.password)
        new_user = User(email=data.email, username=data.username, hashed_password=hashed)
        return await self.user_repo.create(new_user)

    async def authenticate(self, data: UserLogin) -> str:
        user = await self.user_repo.get_by_email(data.username) # assuming email login
        if not user or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedError("Incorrect credentials")
        
        return create_access_token(subject=user.id)
