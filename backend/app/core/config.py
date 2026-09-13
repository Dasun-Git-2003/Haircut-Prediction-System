from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./styleai.db"
    MONGODB_URI: str = "mongodb+srv://Dasun:Dilshan%261231@cluster0.xcjb2dw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    MONGODB_DB_NAME: str = "styleai"
    USE_MONGODB: bool = True
    JWT_SECRET: str = "supersecret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    GENAI_PROVIDER: str = "gemini"
    GOOGLE_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    STABLE_DIFFUSION_URL: str = ""
    UPLOAD_DIR: str = "./uploads"
    GENERATED_DIR: str = "./generated"
    MAX_FILE_SIZE: int = 5242880
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080,http://localhost:5173"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
