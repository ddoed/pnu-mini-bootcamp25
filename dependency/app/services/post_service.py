from dataclasses import asdict, dataclass
import time
from sqlmodel import Field, SQLModel,Session, create_engine, select

class Post(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    created_at: int | None = Field(index=True)
    published: bool = Field(index=True)
    title: str
    body: str

@dataclass
class PostReq(SQLModel):
    title: str
    body: str
    published: bool

class PostSercvice:
    def get_post(self, db: Session, post_id: int):
        pass

    def get_posts(self, db: Session, page:int=1):
        pass

    def create_post(self, db:Session, post: PostReq):
        postModel = Post()
        postModel.title = post.title
        postModel.body = post.body
        postModel.created_at = int(time.time())
        postModel.published = post.published
        db.add(postModel)
        db.commit()
        db.refresh(postModel)
        return postModel
    
    def update_post(self, db:Session, 
                    post_id: int, post: PostReq):
        pass

    def delete_post(self, db: Session, post_id: int):
        pass