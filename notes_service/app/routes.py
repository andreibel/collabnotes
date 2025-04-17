from app.models import create_note
from fastapi import APIRouter, HTTPException, status
from app import models,schemas


router = APIRouter()

@router.post('/create', response_model=schemas.NoteOut, status_code=status.HTTP_201_CREATED)
async def creteNote(note_in:schemas.NoteCreate):
    note_data = note_in.dict()
    
    # TODO: Replace with JWT logic to get the user
    note_data["user_id"] = "123"  # Hardcoded for now

    created_note = await models.create_note(note_data)
    
    if not created_note:
        raise HTTPException(status_code=500, detail="Note creation failed")

    return created_note


