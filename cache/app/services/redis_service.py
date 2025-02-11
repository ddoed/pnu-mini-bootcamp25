
from app.models.post_models import Post

POST_EXIRE = 100

'''
Type: Hashes
Key: POST#1
'''
class RedisService:
    def make_post_key(self, post_id: int) -> str:
        return f'POST#{post_id}' # POST#{post_id}
    
    # id: int = Field(primary_key=True)
    # created_at: int = Field(index=True)
    # published: bool = Field(index=True)
    # title: str
    # body: str
    async def get_post(self, redis, post_id: int) -> Post | None:
        post = await redis.hgetall(self.make_post_key(post_id))
        if post is None or len(post) < 1:
            return None
        # 캐시에서 값 가져오기
        cachedPost = Post(id=0, created_at=0, published=False, title='', body='')
        cachedPost.id = int(post.get('id', 0))
        cachedPost.created_at = int(post.get('created_at', 0))
        cachedPost.published = post.get('published', '1') == '1'
        cachedPost.title = post.get('title', '')
        cachedPost.body = post.get('body', '')
        return cachedPost
    # 캐싱하기기
    async def add_post(self, redis, post: Post):
        strKey = self.make_post_key(post.id)
        await redis.hset(strKey, "id", post.id)
        await redis.hset(strKey,"title", post.title)
        await redis.hset(strKey,"body", post.body)
        await redis.hset(strKey,"created_at", post.created_at)
        await redis.hset(strKey,"published", post.published)
        # await redis.hexpire(strKey, POST_EXIRE)

    async def delete_post(self, redis, post_id):
        strKey = self.make_post_key(post_id)
        await redis.delete(strKey)