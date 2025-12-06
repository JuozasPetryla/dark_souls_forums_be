import time
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pwdlib import PasswordHash
from src.core.config import settings
from sqlalchemy.orm import Session
from src.db.models import User, SteamAccount
from src.db.session import get_db_session
from datetime import datetime

password_hash = PasswordHash.recommended()
bearer_scheme = HTTPBearer()

def _hash_password(password: str) -> str:
    return password_hash.hash(password)

def _verify_password_hash(password: str, password_hashed: str) -> bool:
    return password_hash.verify(password, password_hashed)

def create_access_token(user_id: int) -> str:
    now = int(time.time())

    payload = {
        "sub": str(user_id),
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

def get_user_steam_account(db: Session, user_id: int):
    return db.query(SteamAccount).filter(SteamAccount.user_id == user_id).first()

def get_user_by_token(db: Session = Depends(get_db_session), credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_access_token(token)

    user_id = int(payload["sub"])
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Such user does not exist")

    return user

def create_user(db: Session, nickname: str, email: str, password: str):
    existing_email = get_user_by_email(db, email)
    if existing_email:
        raise HTTPException(status_code=409, detail="Email is already taken")

    existing_nickname = get_user_by_nickname(db, nickname)
    if existing_nickname:
        raise HTTPException(status_code=409, detail="Nickname is already taken")

    hashed_password = _hash_password(password)
    user = User(nickname=nickname, email=email, password_hash=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def verify_password(password: str, user: User) -> bool:
    return _verify_password_hash(password, user.password_hash)

def update_user_login_time(db: Session, user: User):
    user.last_login_at = datetime.utcnow()
    db.commit()
    db.refresh(user)

def set_steam_account(db: Session, user: User, steam_id: str):
    existing_steam_account = get_user_steam_account(db, user.id)

    if existing_steam_account:
        existing_steam_account.steam_id = steam_id
        existing_steam_account.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_steam_account)
        return existing_steam_account

    new_steam_account = SteamAccount(steam_id=steam_id, updated_at=datetime.utcnow(), user_id=user.id)
    db.add(new_steam_account)
    db.commit()
    db.refresh(new_steam_account)

    return new_steam_account