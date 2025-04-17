from pydantic import BaseModel, Field
from typing import Optional,List
from datetime import datetime


class NoteCreate(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []

class SharedUser(BaseModel):
    user_id: str
    permission: str  # "read" or "write"

class NoteOut(BaseModel):
    id: str = Field(..., alias="_id")
    title: str
    content: str
    tags: Optional[List[str]] = []
    user_id: str
    shared_with: Optional[List[SharedUser]] = []
    created_at: datetime
