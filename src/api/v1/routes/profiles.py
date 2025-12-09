from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from src.db.models import User, SteamAccount
from src.db.session import get_db_session
from src.services.authentication import get_user_by_token, get_user_by_id, set_steam_account, get_user_steam_account
from src.services.profiles import delete_user_by_id, get_or_update_games, update_user_profile
from pydantic import BaseModel

class UserView(BaseModel):
    id: int
    last_login_at: datetime | None
    nickname: str
    image: str | None
    bio: str | None
    playing_class: str | None
    origin_country: str | None
    address: str | None
    city: str | None
    discord_id: str | None
    name: str | None
    surname: str | None
    postal_code: str | None
    phone_number: str | None

    model_config = {
        "from_attributes": True
    }

class UserUpdate(BaseModel):
    nickname: str | None = None
    bio: str | None = None
    playing_class: str | None = None
    origin_country: str | None = None
    address: str | None = None
    city: str | None = None
    discord_id: str | None = None
    name: str | None = None
    surname: str | None = None
    postal_code: str | None = None
    phone_number: str | None = None

    model_config = {
        "extra": "forbid"
    }

class GameView(BaseModel):
    id: int
    name: str
    hours_played: int

    model_config = {
        "from_attributes": True
    }

profiles_router = APIRouter()

@profiles_router.delete("/delete")
def delete_my_profile(user: User = Depends(get_user_by_token), db: Session = Depends(get_db_session)):
    delete_user_by_id(db, user.id)

    return JSONResponse(status_code=200, content={
        "success": "User deleted successfully!"}
    )

@profiles_router.get("/profile/me", response_model=UserView)
def get_my_profile(user: User = Depends(get_user_by_token)):
    return UserView.from_orm(user)


@profiles_router.get("/profile/{id}", response_model=UserView)
def get_profile(id: int, db: Session = Depends(get_db_session)):
    user = get_user_by_id(db, id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserView.from_orm(user)

@profiles_router.post("/profile/steam/add")
def update_steam_id(steam_id: str = Body(...), db: Session = Depends(get_db_session), user: User = Depends(get_user_by_token)):
    steam_account = set_steam_account(db, user, steam_id)

    return JSONResponse(status_code=200, content={
            "success": "Account updated successfully!",
            "steam_id": steam_account.id
        }
    )


@profiles_router.get("/profile/me/games", response_model=list[GameView])
async def get_my_steam_games(db: Session = Depends(get_db_session), user: User = Depends(get_user_by_token)):
    steam_account = get_user_steam_account(db, user.id)
    if not steam_account:
        raise HTTPException(status_code=400, detail="Steam account not linked")

    games = await get_or_update_games(db, user.id, steam_account.steam_id)
    return games


@profiles_router.get("/profile/{id}/games", response_model=list[GameView])
async def get_steam_games(id: int, db: Session = Depends(get_db_session)):
    steam_account = get_user_steam_account(db, id)
    if not steam_account:
        raise HTTPException(status_code=400, detail="Steam account not linked")

    games = await get_or_update_games(db, id, steam_account.steam_id)
    return games


@profiles_router.patch("/profile/me", response_model=UserView)
def update_my_profile(data: UserUpdate, db: Session = Depends(get_db_session), user: User = Depends(get_user_by_token)):
    updates = data.model_dump(exclude_unset=True)

    if "nickname" in updates:
        existing = db.query(User).filter(User.nickname == updates["nickname"]).first()
        if existing and existing.id != user.id:
            raise HTTPException(status_code=409, detail="Nickname already taken")

    if "email" in updates:
        existing = db.query(User).filter(User.email == updates["email"]).first()
        if existing and existing.id != user.id:
            raise HTTPException(status_code=409, detail="Email already taken")

    updated_user = update_user_profile(db, user, updates)
    return UserView.from_orm(updated_user)

