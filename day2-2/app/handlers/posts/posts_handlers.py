from fastapi import APIRouter
import time

from app.models.post_models import *
from app.models.shared import *

router = APIRouter(
    prefix="/v1/posts"
)

@router.get("/")
def get_posts(dir: PageDir=PageDir.PREV, 
            post_id: int=0, 
            limit: int=30) -> PostsResp:
    nCurTimestamp = int(time.time())
    return PostsResp(
        posts=[
            Post(id=1, title="T",body="B",
                created_at=nCurTimestamp,
                published=True),
            Post(id=2, title="TT",body="B1",
                created_at=nCurTimestamp,
                published=True)
        ]
    )


@router.get("/{post_id}")
def get_post(post_id: int) -> PostsResp:
    nCurTimestamp = int(time.time())
    return PostsResp(
        posts=[
            Post(id=post_id, title="T",body="B",
                created_at=nCurTimestamp,
                published=True)
        ]
    )

@router.post("/")
def create_post(params: CreatePostReq) -> PostsResp:
    nCurTimestamp = int(time.time())
    return PostsResp(
        posts=[
            Post(id=999, title=params.title,
                body=params.body,
                created_at=nCurTimestamp,
                published=params.publish)
        ]
    )

@router.put("/{post_id}")
def update_post(post_id: int, params: UpdatePostReq) ->PostsResp:
    nCurTimestamp = int(time.time())
    return PostsResp(
        posts=[
            Post(id=post_id, title=params.title,
                body=params.body,
                created_at=nCurTimestamp,
                published=params.publish)
        ]
    )

@router.delete("/{post_id}")
def delete_post(post_id: int) -> ResultResp:
    return ResultResp(ok=True)