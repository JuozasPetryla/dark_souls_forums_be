from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from src.db.models import User
from src.db.session import get_db_session
from src.services.authentication import get_user_by_token, get_user_by_id
from src.services.profiles import delete_user_by_id
from pydantic import BaseModel

class UserView(BaseModel):
    id: int
    last_login_at: datetime
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