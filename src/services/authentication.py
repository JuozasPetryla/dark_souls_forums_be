import time
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from src.core.config import settings
from sqlalchemy.orm import Session
from src.db.models import User

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password_hash(password: str, password_hashed: str) -> str:
    return password_hash.verify(password, password_hashed)

def create_access_token(user_id: int) -> str:
    now = int(time.time())

    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + (settings.JWT_EXPIRATION_MINUTES * 60),
    }

    jwt_access_token = jwt.encode(payload=payload, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_SIGNING_ALGORITHM)
    return jwt_access_token

def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(jwt=token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_SIGNING_ALGORITHM])
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_nickname(db: Session, nickname: str):
    return db.query(User).filter(User.nickname == nickname).first()

def get_user_by_token(db: Session, token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)

    user_id = int(payload["sub"])
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Such user does not exist")

    return user

def create_user(db: Session, nickname: str, email: str, password: str):
    existing_email = get_user_by_email(db, email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email is already taken")

    existing_nickname = get_user_by_nickname(db, nickname)
    if existing_nickname:
        raise HTTPException(status_code=400, detail="Nickname is already taken")

    hashed_password = hash_password(password)
    user = User(nickname=nickname, email=email, password_hash=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user