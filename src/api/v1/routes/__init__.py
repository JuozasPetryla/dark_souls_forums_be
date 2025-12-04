from fastapi import APIRouter
from src.api.v1.routes.authentication import auth_router
from src.api.v1.routes.topics import topics_router

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "pong"}

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(topics_router, prefix="/topics", tags=["topics"])