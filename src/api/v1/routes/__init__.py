from fastapi import APIRouter
from src.api.v1.routes.authentication import auth_router
from src.api.v1.routes.topics import topics_router
from src.api.v1.routes.comments import comments_router
from .authentication import auth_router
from .topics import topics_router
from .profiles import profiles_router

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "pong"}

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(topics_router, prefix="/topics", tags=["topics"])
router.include_router(comments_router, prefix="/comments", tags=["comments"])
router.include_router(profiles_router, prefix="/profiles", tags=["profiles"])