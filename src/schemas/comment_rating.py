from pydantic import BaseModel
from src.db.enums.comment_rating_types import CommentRatingTypes

class CommentRatingCreate(BaseModel):
    rating: CommentRatingTypes
    comment_id: int

class CommentRatingUpdate(BaseModel):
    rating: CommentRatingTypes