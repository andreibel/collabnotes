from pydantic import BaseModel, EmailStr, validator, Field
import re

# --------------------------
# Registration Input Schema
# --------------------------
class UserCreate(BaseModel):
    username: str = Field(..., regex=r'^[a-zA-Z0-9_]+$', min_length=3, max_length=20)
    email: EmailStr
    password: str
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Za-z]',v) or not re.search(r'[0-9]',v):
            raise ValueError('Password must contain both letters and numbers')
        return v

# --------------------------
# Output: Returned User Info
# --------------------------
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

# --------------------------
# Login Input Schema
# --------------------------
class UserLogin(BaseModel):
    username: str
    password: str

# --------------------------
# Output: JWT Token Response
# --------------------------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"