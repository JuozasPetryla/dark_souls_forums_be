from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session
import httpx
from src.core.config import settings
from src.db.models import Game, User
from src.services.authentication import get_user_by_id

STEAM_API_URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
STALE_HOURS = 24

SOULS_LIKE_APPIDS = {
    570940,
    1172380,
    2622380,
    1245620,
    374320,
    814380,
    335300,
    2358720,
    1627720,
    1774580,
}


def delete_user_by_id(db: Session, id: int):
    user = get_user_by_id(db, id)

    if not user:
        raise HTTPException(status_code=404, detail="Such user does not exist")

    db.delete(user)
    db.commit()

async def _get_steam_games(steam_id: str):
    params = {
        "key": settings.STEAM_API_KEY,
        "steamid": steam_id,
        "include_appinfo": True,
        "format": "json"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(STEAM_API_URL, params=params)
        resp.raise_for_status()

    data = resp.json()

    if "response" not in data or "games" not in data["response"]:
        return []

    games = data["response"]["games"]
    games = [game for game in games if game.get("appid") in SOULS_LIKE_APPIDS]

    return games

def _is_stale(games):
    if not games:
        return True
    return datetime.utcnow() - games[0].updated_at > timedelta(hours=STALE_HOURS)


async def get_or_update_games(db, user_id, steam_id):
    existing_games = db.query(Game).filter(Game.user_id == user_id).all()

    if existing_games and not _is_stale(existing_games):
        return existing_games

    steam_games = await _get_steam_games(steam_id)

    db.query(Game).filter(Game.user_id == user_id).delete()

    new_games = []
    for g in steam_games:
        game = Game(
            name=g.get("name", "Unknown"),
            hours_played=g.get("playtime_forever", 0) // 60,
            updated_at=datetime.utcnow(),
            user_id=user_id
        )
        db.add(game)
        new_games.append(game)

    db.commit()
    return new_games


def update_user_profile(db: Session, user: User, updates: dict):
    for field, value in updates.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user