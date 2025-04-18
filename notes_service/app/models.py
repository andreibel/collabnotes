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


async def list_notes(user_id: str):
    cors = db["notes"].find({"user_id": user_id},{"content": 0}).sort("created_at", -1)
    notes = await cors.to_list(length=100)
    for note in notes:
        note["_id"] = str(note["_id"])
    return notes



async def list_share_notes(user_id: str):
    cors = db["notes"].find({"shared_with.user_id": user_id},{"content": 0}).sort("created_at", -1)
    notes = await cors.to_list(length=100)
    for note in notes:
        note["_id"] = str(note["_id"])
    return notes
    
    
    
async def update_note(note_id: str, update_data: dict) -> dict | None:
    try:
        obj_id = ObjectId(note_id)
    except:
        return None
    
    update_fields = {key: value for key, value in update_data.items() if value is not None}
    if not update_fields:
        return None
    
    note = await db["notes"].find_one_and_update({"_id":obj_id}, {"$set":update_fields},return_document=True)
    if note:
        note["_id"] = str(note["_id"])
    return note


async def put_note(note_id:str, note:dict) -> dict | None:
    try:
        obj_id = ObjectId(note_id)
    except:
        return None
    new_note = await db["notes"].find_one_and_replace({"_id":obj_id}, note, return_document=True)
    if new_note:
        new_note["_id"] = str(new_note["_id"])
    return new_note


async def delete_note(note_id: str) -> bool:
    try:
        obj_id = ObjectId(note_id)
    except:
        return False
    res = await db["notes"].delete_one({"_id":obj_id})
    return res.deleted_count == 1

