from fastapi import APIRouter
from src.api.v1.routes.authentication import auth_router

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "pong"}

router.include_router(auth_router, prefix="/auth", tags=["auth"])