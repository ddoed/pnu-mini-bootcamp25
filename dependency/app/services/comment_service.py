from dataclasses import dataclass
from fastapi import APIRouter, Depends
from sqlmodel import (
    Field, SQLModel,
    Session, create_engine, select
)

@dataclass
class CommentReq:
    

class Comment(SQLModel, table=True):
    id: int = Field(primary_key=True)
    product_id: int = Field(foreign_key=True)
    user_id: int = Field(foreign_key=True)
    content: str

# 댓글 목록 조회
@router.get("/{product_id}/comments")
def get_comments(product_id: int, db: Session = Depends(get_db)):
    


# 댓글 작성
@router.post("/{product_id}/comments")
def create_comment():
    

# 댓글 수정하기
@router.put("/{product_id}/comments/{comment_id}")
def update_comment():

# 댓글 삭제
@router.delete("/{product_id}/comments/{comment_id}")
def delete_comment():
