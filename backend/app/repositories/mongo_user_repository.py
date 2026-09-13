from app.database.mongodb import get_mongo_db
from app.repositories.user_repository import UserRepository
from app.models.user import User
from typing import Optional

class MongoUserRepository:
    def __init__(self, fallback_repo: Optional[UserRepository] = None):
        self.fallback_repo = fallback_repo

    @property
    def col(self):
        db = get_mongo_db()
        return db.users if db is not None else None

    async def get_by_id(self, id: str) -> Optional[User]:
        if self.col is not None:
            try:
                doc = await self.col.find_one({"_id": id})
                if doc:
                    return User(
                        id=doc["_id"],
                        email=doc["email"],
                        username=doc["username"],
                        hashed_password=doc["hashed_password"],
                        is_active=doc.get("is_active", True),
                        is_admin=doc.get("is_admin", False),
                        avatar_url=doc.get("avatar_url")
                    )
            except Exception:
                pass
        if self.fallback_repo:
            return await self.fallback_repo.get_by_id(id)
        return None

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.get_by_username_or_email(email)

    async def get_by_username_or_email(self, identifier: str) -> Optional[User]:
        if self.col is not None:
            try:
                doc = await self.col.find_one({"$or": [{"email": identifier}, {"username": identifier}]})
                if doc:
                    return User(
                        id=doc["_id"],
                        email=doc["email"],
                        username=doc["username"],
                        hashed_password=doc["hashed_password"],
                        is_active=doc.get("is_active", True),
                        is_admin=doc.get("is_admin", False),
                        avatar_url=doc.get("avatar_url")
                    )
            except Exception:
                pass
        if self.fallback_repo:
            if hasattr(self.fallback_repo, "get_by_username_or_email"):
                return await self.fallback_repo.get_by_username_or_email(identifier)
            return await self.fallback_repo.get_by_email(identifier)
        return None

    async def create(self, user: User) -> User:
        if self.col is not None:
            try:
                is_active = getattr(user, "is_active", True)
                if is_active is None:
                    is_active = True
                is_admin = getattr(user, "is_admin", False)
                if is_admin is None:
                    is_admin = False
                doc = {
                    "_id": user_id,
                    "id": user_id,
                    "email": user.email,
                    "username": user.username,
                    "hashed_password": user.hashed_password,
                    "is_active": is_active,
                    "is_admin": is_admin,
                    "avatar_url": getattr(user, "avatar_url", None)
                }
                await self.col.insert_one(doc)
            except Exception:
                pass
        if self.fallback_repo:
            try:
                return await self.fallback_repo.create(user)
            except Exception:
                pass
        return user
