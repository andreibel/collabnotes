from fastapi import FastAPI
from app.routes import router
app = FastAPI(title="Note Service")
app.include_router(router, prefix="/notes", tags=["Notes"])