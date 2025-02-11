from fastapi import FastAPI
from app.router import ws_router

app = FastAPI()
app.include_router(ws_router.router)