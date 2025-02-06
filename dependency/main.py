from fastapi import (FastAPI, Depends, HTTPException, Depends)

from dataclasses import dataclass, asdict
from app.services.post_service import *

@dataclass
class PostResp:
    posts: list[Post]
    err_str: str | None = None

db_file_name = "blog.db"
db_url = f"sqlite:///{db_file_name}"
db_conn_args = {"check_same_thread": False}
db_engine = create_engine(db_url,connect_args=db_conn_args)

def get_db_session():
    with Session(db_engine) as session:
        yield session

def create_db():
    SQLModel.metadata.create_all(db_engine)

app = FastAPI()

create_db()

@app.post("/posts")
def create_post(post:PostReq, db = Depends(get_db_session),
                PostSercvice: PostSercvice = Depends()):
    resp = PostSercvice.create_post(db, post)
    return resp

@app.get("/posts")
def get_posts(page:int=1, limit: int=2, db=Depends(get_db_session)) -> PostResp:
    if page < 1:
        page = 1
    if limit < 1:
        return []
    
    noffset = (page - 1) * limit
    posts = db.exec(
        select(Post).offset(noffset).limit(limit)
    ).all()
    return PostResp(posts=posts)

@app.get("/posts/{post_id}")
def get_post(post_id:int, db=Depends(get_db_session)) -> PostResp:
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostResp([post])

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db=Depends(get_db_session)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {
        'ok': True
    }

@app.put("/posts/{post_id}")
def update_post(post_id: int, reqBody: PostReq, db = Depends(get_db_session)):
    oldPost = db.get(Post, post_id)
    if not oldPost:
        raise HTTPException(status_code=404, detail="not found")
    
    dictToUpdate = asdict(reqBody)
    oldPost.sqlmodel_update(dictToUpdate)
    db.add(oldPost)
    db.commit()
    db.refresh(oldPost)
    return oldPost