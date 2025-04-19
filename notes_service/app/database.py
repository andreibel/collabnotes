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


#note scheme in the data base
"""
{
  _id: ObjectId("6610e9a8f1e3f2b7ac9d4abc"),      // Mongo’s unique ID
  title: "Project Brainstorm",                    // Note title
  content: "Here’s the full note body, which can be very large…",  
  tags: ["ideas", "team"],                        // Array of tags
  user_id: "5f53c1e4a1b2c3d4e5f67890",             // Owner’s user ID (string)
  shared_with: [                                   // Who else can see/edit
    { user_id: "8a7b6c5d4e3f2a1b0c9d8e7", permission: "read" },
    { user_id: "1234567890abcdef12345678", permission: "write" }
  ],
  is_starred: false,                               // (Optional) favorite flag
  created_at: ISODate("2025-04-17T14:00:00Z"),     // Timestamp of creation
  updated_at: ISODate("2025-04-18T09:30:00Z")      // (Optional) last modification
}
"""