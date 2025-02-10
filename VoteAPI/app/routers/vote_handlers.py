from fastapi import APIRouter, Depends, HTTPException, Path
from app.services.vote_service import VoteService
from app.dependencies.redis_db import get_redis
from typing import Annotated

router = APIRouter(prefix='/v1/vote')

@router.get("/members")
def get_memners(service=Depends(VoteService)):
    members = service.members()
    return members


@router.put("/{member_id}")
async def vote(member_id: Annotated[int, Path(ge=0, le = 2)], # 범위 설정 ge: greater than, le = less than
            service=Depends(VoteService),
            redis=Depends(get_redis)):
    await service.vote(redis, member_id)
    return {}

@router.get("/")
async def get_scores(service=Depends(VoteService), redis=Depends(get_redis)):
    scores = await service.scores(redis)
    return scores

@router.get("/{member_id}")
async def get_socre(member_id: Annotated[int, Path(ge=0, le=2)],
                    service=Depends(VoteService), redis=Depends(get_redis)):
    score = await service.score_of(redis, member_id)
    return score

@router.put("/{member_id}/{phone}")
async def vote(member_id: int, phone: str, service=Depends(VoteService), redis=Depends(get_redis)):
    if member_id not in [0,1,2]:
        raise HTTPException(status_code=400, detail="0~2")
    
    if await service.phone_exists(redis, phone):
        raise HTTPException(status_code=400, detail="이미 투표 했습니다")
    
    await service.vote(redis,member_id)
    await service.set_phone(redis, phone)
    return {"message":"vote success"}