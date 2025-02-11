from dataclasses import dataclass, asdict
from enum import Enum
from sqlmodel import (
    SQLModel,
    Field
)
class RESULT_CODE(Enum):
    SUCCESS = 1
    NOT_FOUND = -2
    FAILED = -3

@dataclass
class PostReq:
    title: str
    body: str
    published: bool

class Post(SQLModel, table=True):
    id: int = Field(primary_key=True)
    created_at: int = Field(index=True)
    published: bool = Field(index=True)
    title: str
    body: str

@dataclass
class PostResp:
    posts: list[Post]
    err_str: str | None = None
