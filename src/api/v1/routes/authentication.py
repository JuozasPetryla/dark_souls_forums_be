from sqlalchemy.orm import Session
from src.db.session import get_db_session
from src.services.authentication import create_user, create_access_token
from fastapi import APIRouter, Depends, Body, Form, Header, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional

auth_router = APIRouter()

@auth_router.post("/register")
def register(nickname: str = Body(...), email: str = Body(...), password: str = Body(...), authorization: Optional[str] = Header(None), db: Session = Depends(get_db_session)):
    if authorization:
        raise HTTPException(status_code=401, detail="User already logged in")

    user = create_user(db, nickname, email, password)

    token = create_access_token(user.id)

    return JSONResponse(
        status_code=201,
        content={
            "id": user.id,
            "email": user.email,
            "access_token": token,
        }
    )