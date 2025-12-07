from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.db.session import get_db_session
from src.db.models import Comment, CommentRating
from src.schemas.comment_rating import CommentRatingCreate
import sqlalchemy as sa

comments_rating_router = APIRouter()


@comments_rating_router.post("/create")
def create(rating_data: CommentRatingCreate = Body(...), db: Session = Depends(get_db_session)):
    user_id = 1
    comment_id = 8
    new_rating = CommentRating(rating=rating_data.rating, user_id=user_id, comment_id=comment_id)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)

    return {
        "message": "Rating added successfully",
        "rating_id": new_rating.id,
        "comment_rating": new_rating.rating.value,
    }


@comments_rating_router.get("/read/{rating_id}")
def read(rating_id: int, db: Session = Depends(get_db_session)):
    comment_rating = db.query(CommentRating).filter(CommentRating.id == rating_id).first()
    if not comment_rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    return jsonable_encoder({
        "id": comment_rating.id,
        "rating": comment_rating.rating.value,
    })

@comments_rating_router.put("/update/{rating_id}")
def update(rating_id: int, rating_data: CommentRatingCreate = Body(...), db: Session = Depends(get_db_session)):
    comment_rating = db.query(CommentRating).filter(CommentRating.id == rating_id).first()
    if not comment_rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    comment_rating.rating = rating_data.rating

    db.commit()
    db.refresh(comment_rating)

    return {
        "message": "Comment rating updated successfully",
        "rating_id": comment_rating.id,
        "comment_rating": comment_rating.rating.value,
    }

@comments_rating_router.delete("/delete/{rating_id}")
def delete(rating_id: int, db: Session = Depends(get_db_session)):
    comment_rating = db.query(CommentRating).filter(CommentRating.id == rating_id).first()
    if not comment_rating:
        raise HTTPException(status_code=404, detail="Comment rating not found")

    db.delete(comment_rating)
    db.commit()

    return {
        "message": f"Comment rating '{comment_rating.rating.value}' deleted successfully"
    }
