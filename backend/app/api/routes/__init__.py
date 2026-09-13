from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .analysis import router as analysis_router
from .recommendations import router as recommendations_router
from .hairstyles import router as hairstyles_router
from .tryon import router as tryon_router
from .favorites import router as favorites_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(analysis_router, prefix="/analysis", tags=["analysis"])
api_router.include_router(recommendations_router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(hairstyles_router, prefix="/hairstyles", tags=["hairstyles"])
api_router.include_router(tryon_router, prefix="/tryon", tags=["tryon"])
api_router.include_router(tryon_router, prefix="/try-on", tags=["try-on"])
api_router.include_router(favorites_router, prefix="/favorites", tags=["favorites"])
