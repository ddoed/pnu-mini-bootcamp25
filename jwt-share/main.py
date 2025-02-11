from fastapi import FastAPI

from app.dependencies.db import create_db_and_tables
from app.routers import auth_handlers

app = FastAPI()

create_db_and_tables()

app.include_router(auth_handlers.router)
