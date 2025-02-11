from fastapi import APIRouter, Depends, HTTPException
from app.models.parameter_models import *
from app.dependencies.jwt import *
from app.dependencies.db import get_db_session
from app.services.auth_service import AuthService

router = APIRouter(
    prefix='/auth'
)

@router.post('/token')
async def auth_login(req: AuthTokenReq,
                    db = Depends(get_db_session),
                    jwtUtil: JWTUtil = Depends(),
                    authService: AuthService = Depends()):
    user = authService.signin(db, req.login_id, req.pwd)
    if user is None:
        raise HTTPException(status_code=401,
                            detail="Unauthrized")
    user.access_token = jwtUtil.create_access_token(user.model_dump())
    
    return user

@router.post('/signup')
async def auth_signup(req: AuthSignupReq,
                    db = Depends(get_db_session),
                    jwtUtil: JWTUtil = Depends(),
                    authService: AuthService = Depends()):
    user = authService.signup(db, login_id=req.login_id,
                            pwd=req.pwd, name=req.name)
    if not user:
        raise HTTPException(status_code=500,
                            detail="Internal Server Error")
    user.access_token = jwtUtil.create_access_token(user.model_dump())
    return user