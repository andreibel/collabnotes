import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get connection URI and database name
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "notes_db")

# Create Motor client
client = AsyncIOMotorClient(MONGODB_URI)

# Select the database
db = client[MONGO_DB_NAME]