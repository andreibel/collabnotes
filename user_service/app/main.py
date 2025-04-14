from fastapi import FastAPI
from app.database import engine, Base
from app.routes import router

app = FastAPI(title="User Service")

# Auto-create DB tables at startup (for dev/testing)
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Register routes
app.include_router(router, prefix="/api", tags=["Users"])