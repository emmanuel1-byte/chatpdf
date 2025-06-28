from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
from beanie import init_beanie


load_dotenv()
import os

from ..utils.logger import logger


"""
Establishes a connection to the database using an asynchronous MongoDB client.

This function initializes the Beanie ODM with the specified database and document models.
Logs a message upon successful connection or logs an error if an exception occurs.

Raises:
    PyMongoError: If there is an error connecting to the MongoDB database.
    Exception: For any other exceptions that may occur during the connection process.
"""
async def connect_to_database():
    from ..modules import User, Chat

    try:
        client = AsyncIOMotorClient(os.getenv("DATABASE_URI"))
        await init_beanie(
            database=client.chatPDF, document_models=[User, Chat]
        )
        logger.info("Database connected")

    except PyMongoError as e:
        logger.error(e)
        raise

    except Exception as e:
        logger.error(e)
        raise
