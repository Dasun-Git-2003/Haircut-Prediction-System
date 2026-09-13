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

# Ensure uploads and generated directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.GENERATED_DIR, exist_ok=True)

from app.database.mongodb import connect_to_mongo, close_mongo_connection
from app.database.seed_hairstyles import seed_database, seed_mongo_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure dirs exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.GENERATED_DIR, exist_ok=True)
    
    # Initialize Relational DB and seed
    await init_db()
    async with async_session_maker() as session:
        await seed_database(session)
        
    # Connect and seed MongoDB Atlas
    if settings.USE_MONGODB:
        await connect_to_mongo()
        await seed_mongo_database()
        
    yield
    
    # Graceful shutdown
    if settings.USE_MONGODB:
        await close_mongo_connection()

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
