import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.exceptions import exception_handlers
from app.database.database import init_db, async_session_maker
from app.database.seed_hairstyles import seed_database
from app.api.routes import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure dirs exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.GENERATED_DIR, exist_ok=True)
    
    # Initialize DB and seed
    await init_db()
    async with async_session_maker() as session:
        await seed_database(session)
    yield

app = FastAPI(
    title="StyleAI Backend",
    version="1.0.0",
    lifespan=lifespan,
    exception_handlers=exception_handlers, # type: ignore
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
app.mount("/generated", StaticFiles(directory=settings.GENERATED_DIR), name="generated")

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to StyleAI API"}
