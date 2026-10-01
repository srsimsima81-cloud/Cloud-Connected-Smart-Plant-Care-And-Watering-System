from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User
from ..schemas import RegisterRequest, LoginRequest, TokenResponse
from ..utils.auth import hash_password, verify_password, create_token
router=APIRouter(prefix='/api/auth', tags=['Authentication'])
@router.post('/register', response_model=TokenResponse, status_code=201)
def register(data:RegisterRequest, db:Session=Depends(get_db)):
    if db.query(User).filter(User.email==data.email.lower()).first(): raise HTTPException(409,'Email already registered')
    u=User(name=data.name.strip(), email=data.email.lower(), password_hash=hash_password(data.password)); db.add(u); db.commit(); db.refresh(u)
    return {'token':create_token(u.user_id)}
@router.post('/login', response_model=TokenResponse)
def login(data:LoginRequest, db:Session=Depends(get_db)):
    u=db.query(User).filter(User.email==data.email.lower()).first()
    if not u or not verify_password(data.password,u.password_hash): raise HTTPException(401,'Invalid email or password')
    return {'token':create_token(u.user_id)}
