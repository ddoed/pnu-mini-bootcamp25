from fastapi import FastAPI
from app.handlers.auth import auth_handlers
from app.handlers.posts import posts_handlers

app = FastAPI()

app.include_router(auth_handlers.router)
app.include_router(posts_handlers.router)




