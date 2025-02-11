from fastapi import (
    FastAPI
)
from app.dependencies.sqlite_db import db_engine
from app.services.post_service import *
from app.routers import post_handlers

def create_db():
    SQLModel.metadata.create_all(db_engine)

app = FastAPI()
app.include_router(post_handlers.router)
create_db()



