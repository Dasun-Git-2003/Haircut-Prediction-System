from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class MongoDBManager:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

mongodb = MongoDBManager()

async def connect_to_mongo():
    try:
        logger.info("Connecting to MongoDB Atlas...")
        mongodb.client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=8000,
            uuidRepresentation="standard"
        )
        mongodb.db = mongodb.client[settings.MONGODB_DB_NAME]
        # Quick ping to verify credentials and network access
        await mongodb.db.command("ping")
        logger.info(f"Successfully connected to MongoDB Atlas database: {settings.MONGODB_DB_NAME}")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB Atlas: {e}")
        # Keep client instantiated or fallback
        mongodb.db = None

async def close_mongo_connection():
    if mongodb.client:
        logger.info("Closing MongoDB connection...")
        mongodb.client.close()
        logger.info("MongoDB connection closed.")

def get_mongo_db() -> AsyncIOMotorDatabase:
    return mongodb.db
