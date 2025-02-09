from dataclasses import dataclass
from fastapi import APIRouter

router = APIRouter(
    prefix="/products"
)

@dataclass
class Comment:
    id: int
    product_id: int
    user_id: int
    content: str

# 댓글 목록 조회
@router.get("/{product_id}/comments")
def get_comments():

# 댓글 작성
@router.post("/{product_id}/comments")
def create_comment()
    

# 댓글 수정하기
@router.put("/{product_id}/comments/{comment_id}")
def update_comment():

# 댓글 삭제
@router.delete("/{product_id}/comments/{comment_id}")