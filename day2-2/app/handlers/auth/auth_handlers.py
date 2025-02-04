from fastapi import APIRouter

from app.models.user import *
from app.models.shared import *

router = APIRouter(
    prefix="/v1/auth"
)

@router.post("/signup", status_code=201)
def signup(user: User) -> AuthResponse:
    return AuthResponse(
        jwt_token="sksksksks"
    )

@router.post("/signin", status_code=200)
def signin(user: AuthLoginReq) -> AuthResponse:
    return AuthResponse(
        jwt_token='aaaa'
    )