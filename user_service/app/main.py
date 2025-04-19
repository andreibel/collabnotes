from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import router

app = FastAPI(title="User Service")
DEV_ORIGINS = [
    "http://localhost:8080",   # your vanilla HTML page
    "http://localhost:5173",   # vite dev server
    "http://localhost:5500"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True     # works with Authorization header
)
# Auto-create DB tables at startup (for dev/testing)
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Register routes
app.include_router(router, prefix="/api", tags=["Users"])