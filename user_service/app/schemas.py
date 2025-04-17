from pydantic import BaseModel, EmailStr

# --------------------------
# Registration Input Schema
# --------------------------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

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