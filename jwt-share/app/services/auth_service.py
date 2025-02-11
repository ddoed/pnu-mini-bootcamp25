import bcrypt
import time

from sqlmodel import Session, select
from app.models.user_models import User

class AuthService:
    def get_password_hash(self, pwd: str):
        pwd_data = pwd.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password=pwd_data, salt=salt)
    
    def verity_pwd(self, pwd: str, hashed_pwd: str):
        pwd_data = pwd.encode('utf-8')
        return bcrypt.checkpw(password=pwd_data, hashed_password=hashed_pwd)
    
    def get_user_by_name(self, db: Session, login_id: str) -> User | None:
        stmt = select(User).where(User.login_id==login_id)
        results = db.exec(stmt)
        for user in results:
            return user
        return None
    
    def signin(self, db: Session, login_id: str, pwd: str) -> User | None:
        user = self.get_user_by_name(db, login_id=login_id)
        if not user:
            return None
        
        if not self.verity_pwd(pwd=pwd, hashed_pwd=user.pwd):
            return None
        
        return user
    
    def signup(self, db: Session, login_id: str, pwd: str, name: str) -> User | None:
        hashed_pwd = self.get_password_hash(pwd)
        user = User(login_id=login_id, pwd=hashed_pwd, name=name)
        user.created_at = int(time.time())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
if __name__ == '__main__':
    authService = AuthService()
    pwdHash = authService.get_password_hash('1234')
    print(pwdHash)
    
    print(authService.verity_pwd('1234', pwdHash))