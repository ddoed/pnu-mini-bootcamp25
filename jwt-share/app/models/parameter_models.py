from pydantic import BaseModel

# Authentication
class AuthTokenReq(BaseModel):
    login_id: str
    pwd: str
    
class AuthSignupReq(BaseModel):
    login_id: str
    pwd: str
    name: str