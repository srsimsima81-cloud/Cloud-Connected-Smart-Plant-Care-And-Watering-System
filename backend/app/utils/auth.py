from datetime import datetime, timedelta, timezone
import bcrypt, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..config import settings
from ..db import get_db
from ..models import User

bearer = HTTPBearer()
def hash_password(password: str) -> str: return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
def verify_password(password: str, hashed: str) -> bool:
    try: return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception: return False
def create_token(user_id: int) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_exp_minutes)
    return jwt.encode({'sub': str(user_id), 'exp': exp}, settings.jwt_secret, algorithm='HS256')
def current_user(creds: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> User:
    try: payload = jwt.decode(creds.credentials, settings.jwt_secret, algorithms=['HS256']); uid = int(payload['sub'])
    except Exception: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired token')
    user = db.get(User, uid)
    if not user: raise HTTPException(status_code=401, detail='User not found')
    return user
