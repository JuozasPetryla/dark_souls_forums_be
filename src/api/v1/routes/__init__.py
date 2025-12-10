from fastapi import APIRouter
#from src.api.v1.routes.authentication import auth_router
#from src.api.v1.routes.topics import topics_router
#from src.api.v1.routes.comments import comments_router
#from src.api.v1.routes.comments_rating import comments_rating_router
from .authentication import auth_router
from .topics import topics_router
from .profiles import profiles_router
from .comments import comments_router
from .comments_rating import comments_rating_router
from .profile_relations import router as user_relations_router

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "pong"}

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(topics_router, prefix="/topics", tags=["topics"])
router.include_router(comments_router, prefix="/comments", tags=["comments"])
router.include_router(comments_rating_router, prefix="/comments_rating", tags=["comments_rating"])
router.include_router(user_relations_router, prefix="/user-relations", tags=["User Relations"]) 
router.include_router(profiles_router, prefix="/profiles", tags=["profiles"])
router.include_router(posts_router, prefix="/posts", tags=["posts"])