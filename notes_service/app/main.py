#main note app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
app = FastAPI(title="Note Service")
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
app.include_router(router, prefix="/notes", tags=["Notes"])