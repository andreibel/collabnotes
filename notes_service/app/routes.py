#router of note app 
from app.models import create_note
from fastapi import APIRouter, HTTPException,Depends
from typing import List
from app.models import *
from app.schemas import *
from app.auth import get_current_user 


router = APIRouter()

@router.post('/', response_model=NoteOut, status_code=201)
async def crete_note(note_in:NoteCreate,current_user_id: str = Depends(get_current_user)):
    note_data = note_in.dict()
    note_data["user_id"] =  current_user_id
    created_note = await create_note(note_data)
    if not created_note:
        raise HTTPException(500,"Note creation failed")

    return created_note


@router.get('/{note_id}',response_model=NoteOut,status_code=200)
async def get_note(note_id:str, current_user_id: str = Depends(get_current_user)):
    note =  await get_note_by_id(note_id)
    if not note:
        raise HTTPException(404,"Note not found")
    if note["user_id"] != current_user_id and not any(
        shered["user_id"] == current_user_id for shered in note.get("shared_with", [])):
        raise HTTPException(403, "access denide!!!")
    
    return note 
        
@router.get("/",response_model=List[NoteSummary],status_code=200)
async def get_my_notes(current_user_id: str = Depends(get_current_user)):
    res = await list_notes(current_user_id)
    return res


@router.get("/shared",response_model=List[NoteSummary],status_code=200)
async def get_shared_notes(current_user_id: str = Depends(get_current_user)):
    res = await list_share_notes(current_user_id)
    return res


@router.patch("/{note_id}",response_model=NoteOut,status_code=200)
async def update_note(note_id:str, note_update: NoteUpdate, current_user_id: str = Depends(get_current_user)):
    note = await get_note_by_id(note_id)
    if not note:
        raise HTTPException(404,"Note not found")
    
    if note["user_id"] != current_user_id and not any(
        shared["user_id"] == current_user_id and shared["permission"] == "write"
        for shared in note.get("shared_with", [])
    ):
        raise HTTPException(403,"Access denied")
    
    update = await update_note(note_id,note_update.dict())
    if not update:
        raise HTTPException(400,"nothing to update")
    return update

@router.put("/{note_id}",response_model=NoteOut,status_code=200)
async def repalace_note(
    note_id: str, 
    note_replace: NoteFullUpdate,
    current_user_id: str = Depends(get_current_user)
):
    note = await get_note_by_id(note_id)
    if not note:
        raise HTTPException(404,"Note not found")
    
    if note["user_id"] != current_user_id and not any(
        shared["user_id"] == current_user_id and shared["permission"] == "write"
        for shared in note.get("shared_with", [])
    ):
        raise HTTPException(403, "Access denied")
    to_replace = note_replace.dict()
    to_replace["user_id"] = note["user_id"]
    to_replace["shared_with"] = note.get("shared_with", []) 
    to_replace["created_at"] = note["created_at"]
    res =  await put_note(note_id,to_replace)
    if not res:
        raise HTTPException(500, "Failed to replace note")
    return res

@router.delete("/{note_id}",status_code=204)
async def delete_note(note_id: str, current_user_id: str = Depends(get_current_user)):
    note = await get_note_by_id(note_id)
    if not note:
        raise HTTPException(404,"Note not found")
    if note["user_id"] != current_user_id:
        raise HTTPException(403,"only owner can delete this note")
    
    if not  await del_note(note_id):
        raise HTTPException(500,"unsucssesful delete file")





    

    