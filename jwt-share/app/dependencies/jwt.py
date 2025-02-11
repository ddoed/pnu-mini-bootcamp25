from jose import jwt

from datetime import datetime, timedelta, timezone

class JWTUtil:
    #  openssl rand -hex 32
    __SECRET_KEY = '139c41ea8c9c3e4543d647db3d39288496798f06408f4808155020e9bcf21cff'
    __ALGORITHM = "HS256"
    __ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def create_access_token(self, data: dict, 
                            expires_delta: timedelta | None = timedelta(minutes=__ACCESS_TOKEN_EXPIRE_MINUTES)):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({'exp': expire})
        return jwt.encode(to_encode, self.__SECRET_KEY, algorithm=self.__ALGORITHM)

    def decode_jwt(self, token) -> dict | None:
        try:
            return jwt.decode(token, self.__SECRET_KEY, algorithms=[self.__ALGORITHM])
        except Exception as e:
            print(e)
        return None

if __name__ == "__main__":
    to_encode = {
        'name': 'Linux',
        'email': 'example@example.com'
    }
    
    jwtUtil = JWTUtil()
    token = jwtUtil.create_access_token(to_encode)
    print(token)
    
    decodedDict = jwtUtil.decode_jwt(token)
    print(decodedDict)