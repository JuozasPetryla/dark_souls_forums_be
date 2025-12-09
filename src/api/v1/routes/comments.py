from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.db.session import get_db_session
from src.db.models import Comment, CommentRating
from src.schemas.comment import CommentCreate, CommentUpdate
from src.db.models import User
from src.services.authentication import get_user_by_token
import hashlib

import sqlalchemy as sa

comments_router = APIRouter()

def hash_ip(ip: str) -> str:
    return hashlib.sha256(ip.encode()).hexdigest()

@comments_router.post("/create")
def create(request: Request, comment_data: CommentCreate, db: Session = Depends(get_db_session), current_user: User = Depends(get_user_by_token)):
    
    author_id = current_user.id
    real_ip = request.client.host
    hashed_ip = hash_ip(real_ip)
    new_comment = Comment(content=comment_data.content, author_ip_address=hashed_ip, author_id=author_id, post_id=comment_data.post_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {
        "message": "Comment created successfully",
        "comment_id": new_comment.id,
        "comment_content": new_comment.content,
        "date": new_comment.created_at.strftime("%Y-%m-%d %H:%M")
    }

@comments_router.get("/read_all/{post_id}")
def read_all(post_id: int, db: Session = Depends(get_db_session), current_user: User = Depends(get_user_by_token)):
    CURRENT_USER_ID = current_user.id
    
    comments_with_ratings = (
        db.query(Comment, CommentRating)
        .outerjoin(
            CommentRating,
            sa.and_(
                Comment.id == CommentRating.comment_id,
                CommentRating.user_id == CURRENT_USER_ID
            )
        )
        .filter(Comment.post_id == post_id)
        .order_by(Comment.created_at)
        .all()
    )

    if not comments_with_ratings:
        return {"comments": []}
    
    result = []
    for comment, rating in comments_with_ratings:
        
        if rating:
            user_vote = rating.rating.value
            rating_id = rating.id
        else:
            user_vote = None
            rating_id = None
            
        result.append({
            "id": comment.id,
            "author": f"User {comment.author_id}",
            "author_id": comment.author_id,
            "date": comment.created_at.strftime("%Y-%m-%d %H:%M"),
            "text": comment.content,
            "userVote": user_vote,
            "rating_id": rating_id,
        })
    
    return {"comments": result}

@comments_router.get("/read/{comment_id}")
def read(comment_id: int, db: Session = Depends(get_db_session)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return jsonable_encoder({
        "id": comment.id,
        "content": comment.content,
        "created_at": comment.created_at,
        "modified_at": comment.modified_at,
        "modified": comment.modified,
        "author_iq": comment.author_iq,
        "author_ip_address": comment.author_ip_address,
    })

@comments_router.put("/update/{comment_id}")
def update(comment_id: int, comment_data: CommentUpdate, db: Session = Depends(get_db_session), current_user: User = Depends(get_user_by_token)):
    CURRENT_USER_ID = current_user.id
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.author_id != CURRENT_USER_ID:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    if not comment_data.content.strip():
        raise HTTPException(status_code=400, detail="Comment cannot be empty")
    comment.content = comment_data.content
    comment.modified = True
    comment.modified_at = sa.text("now()")

    db.commit()
    db.refresh(comment)

    return {
        "message": "Comment updated successfully",
        "comment_id": comment.id,
        "comment_content": comment.content,
    }

@comments_router.delete("/delete/{comment_id}")
def delete(comment_id: int, db: Session = Depends(get_db_session), current_user: User = Depends(get_user_by_token)):
    CURRENT_USER_ID = current_user.id
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != CURRENT_USER_ID:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    

    db.delete(comment)
    db.commit()

    return {
        "message": f"Comment '{comment.content}' deleted successfully"
    }
