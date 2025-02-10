from fastapi import FastAPI
from app.routers import vote_handlers

app = FastAPI()

app.include_router(vote_handlers.router)