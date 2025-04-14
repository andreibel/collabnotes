from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models, schemas, auth, database

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
async def register_user(user_in: schemas.UserCreate):
    async with database.SessionLocal() as session:
        # Check if username already exists
        existing_user = await session.execute(
            select(models.User).where(models.User.username == user_in.username)
        )
        if existing_user.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # Check if email already exists
        existing_email = await session.execute(
            select(models.User).where(models.User.email == user_in.email)
        )
        if existing_email.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        hashed_pw = auth.get_password_hash(user_in.password)

        # Create and save user
        new_user = models.User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=hashed_pw
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user