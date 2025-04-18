from app.models import create_note
from fastapi import APIRouter, HTTPException, status,Depends
from app import models,schemas, auth
from typing import List

router = APIRouter()

@router.post('/create', response_model=schemas.NoteOut, status_code=status.HTTP_201_CREATED)
async def crete_note(note_in:schemas.NoteCreate,current_user_id: str = Depends(auth.get_current_user)):
    note_data = note_in.dict()
    note_data["user_id"] =  current_user_id
    created_note = await models.create_note(note_data)
    if not created_note:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Note creation failed")

    return created_note


@router.get('/{note_id}',response_model=schemas.NoteOut,status_code=status.HTTP_200_OK)
async def get_note(note_id:str, current_user_id: str = Depends(auth.get_current_user)):
    note:dict = models.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Note not found")
    
    
    if note["user_id"] != current_user_id and not any(
        shered["user_id"] == current_user_id for shered in note.get("shared_with", [])):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denide!!!")
    
    return note 
        
@router.post("/",response_model=List[schemas.NoteSummary],status_code=status.HTTP_200_OK)
async def get_my_notes(current_user_id: str = Depends(auth.get_current_user)):
    return models.list_notes(current_user_id)


@router.post("/shared",response_model=List[schemas.NoteSummary],status_code=status.HTTP_200_OK)
async def get_shared_notes(current_user_id: str = Depends(auth.get_current_user)):
    return models.list_share_notes(current_user_id)


@router.patch("/{note_id}",response_model=schemas.NoteOut,status_code=status.HTTP_200_OK)
async def update_note(
    note_id:str,
    note_update: schemas.NoteUpdate,
    current_user_id: str = Depends(auth.get_current_user)
):
    note = await models.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Note not found")
    
    if note["user_id"] != current_user_id and not any(
        shared["user_id"] == current_user_id and shared["permission"] == "write"
        for shared in note.get("shared_with", [])
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    update = await models.update_note(note_id,note_update.dict())
    if not update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="nothing to update")
    return update

@router.put("/{note_id}",response_model=schemas.NoteOut,status_code=status.HTTP_200_OK)
async def repalace_note(
    note_id: str,
    note_replace: schemas.NoteFullUpdate,
    current_user_id: str = Depends(auth.get_current_user)
):
    note = await models.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Note not found")
    
    if note["user_id"] != current_user_id and not any(
        shared["user_id"] == current_user_id and shared["permission"] == "write"
        for shared in note.get("shared_with", [])
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    to_replace = note_replace.dict()
    to_replace["user_id"] = note["user_id"]
    to_replace["shared_with"] = note.get("shared_with", []) 
    res = models.put_note(note_id,to_replace)
    if not res:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to replace note")

@router.delete("/{note_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: str,
    current_user_id: str = Depends(auth.get_current_user)
):
    note = await models.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Note not found")
    if note["user_id"] != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="only owner can delete this note")
    
    if not  await models.delete_note(note_id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="unsucssesful delete file")





    

    