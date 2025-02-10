from fastapi import HTTPException


MEMBERS = ['Trump', 'Biden', 'Harris']
VOTE_KEY = "vote"


class VoteService:
    def members(self):
        return MEMBERS
    
    async def vote(self, redis, member_id: int) -> bool:
        try:
            await redis.zincrby(VOTE_KEY, 1, MEMBERS[member_id])
        except TypeError as e:
            print(e)
            return False
        return True
        
    async def score(self, redis):
        scores = await redis.zrevrange(VOTE_KEY, 0, -1)
        return scores
    
    async def score_of(self, redis, member_id: int):
        score = await redis.zscore(VOTE_KEY, MEMBERS[member_id])
        return score
    
    async def phone_exists(self, redis, phone):
        return await redis.exists(f'VOTE#{phone}')
    
    async def set_phone(self, redis, phone):
        await redis.set(f'VOTE#{phone}', 1)