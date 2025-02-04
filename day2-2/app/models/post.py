from dataclasses import dataclass
from enum import Enum
from typing import Optional

@dataclass
class Post:
    id: int
    title: str
    body: str
    created_at: int
    published: bool

class PageDir(Enum):
    NEXT = "next"
    PREV = "prev"

@dataclass
class PostsResp:
    posts: list[Post]
    err_msg: str | None = None

@dataclass
class CreatePostReq:
    title: str
    body: str
    publish: bool = False

@dataclass
class UpdatePostReq:
    title: Optional[str] = None
    body: Optional[str] = None
    publish: Optional[bool] = False

@dataclass
class ResultResp:
    ok: bool = False
    err_msg: Optional[str] = None