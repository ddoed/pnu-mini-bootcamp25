
from dotenv import load_dotenv
import os
from sqlmodel import (
    create_engine, Session
)

load_dotenv()
db_url = os.getenv("DB_HOST")
db_pwd = os.getenv("DB_PASS")
db_engine = create_engine(db_url,
        connect_args={"check_same_thread": False})

def get_db_session():
    with Session(db_engine) as session:
        yield session
