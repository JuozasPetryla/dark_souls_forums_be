from sqlalchemy.orm import Session
from src.db.session import get_db_session
from src.services.authentication import create_user, create_access_token, get_user_by_email, verify_password, update_user_login_time, get_user_by_token
from fastapi import APIRouter, Depends, Body, Form, Header, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.db.models import User

auth_router = APIRouter()

@auth_router.get("/me")
def get_me(current_user: User = Depends(get_user_by_token)):
    return {
        "id": current_user.id,
        "nickname": current_user.nickname,
        "email": current_user.email,
    }

@auth_router.post("/register")
def register(nickname: str = Body(...), email: str = Body(...), password: str = Body(...), db: Session = Depends(get_db_session)):
    user = create_user(db, nickname, email, password)

    token = create_access_token(user.id)

    update_user_login_time(db, user)

    return JSONResponse(
        status_code=201,
        content={
            "user": {
                "id": user.id,
                "email": user.email
            },
            "access_token": token,
            "success": "Successfully registered!"
        }
    )

@auth_router.post("/login")
def login(email: str = Body(...), password: str = Body(...),  db: Session = Depends(get_db_session)):
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=401, detail="User does not exist")

    if not verify_password(password, user):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token(user.id)

    update_user_login_time(db, user)

    return JSONResponse(
        status_code=200,
        content={
            "success": "Succesfully logged in!",
            "access_token": token,
        }
    )

@auth_router.post("/logout")
def logout():
    return JSONResponse(
        status_code=200,
        content={
            "success": "Successfully logged out!"
        }
    )
