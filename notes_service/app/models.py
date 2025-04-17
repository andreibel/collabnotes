from app.database import db
from datetime import datetime
from bson import ObjectId



async def create_note(note_data: dict) -> dict:
    note_data["created_at"] = datetime.utcnow()
    note_data["shared_with"] = note_data.get("shared_with", [])
    result = await db["notes"].insert_one(note_data)
    note_data["_id"] = str(result.inserted_id)
    return note_data

async def get_note_by_id(note_id: str) -> dict | None:
    try:
        obj_id = ObjectId(note_id)
    except:
        return None  # Not a valid Mongo ObjectId
    
    note = await db["notes"].find_one({"_id": obj_id})
    if note:
        note["_id"] = str(note["_id"])  # Convert ObjectId to string for Pydantic
    return note