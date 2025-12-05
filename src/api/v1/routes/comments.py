from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.db.session import get_db_session
from src.db.models import Comment
import sqlalchemy as sa

comments_router = APIRouter()

@comments_router.post("/create")
def create(content: str = Body(...), db: Session = Depends(get_db_session)):
    author_id = 1
    post_id = 2
    #pridėti autoriaus ip
    author_ip_address = 1
    new_comment = Comment(content=content, author_ip_address=author_ip_address, author_id=author_id, post_id=post_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {
        "message": "Comment created successfully",
        "comment_id": new_comment.id,
        "comment_content": new_comment.content,
    }


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
def update(comment_id: int, content: str = Body(...), db: Session = Depends(get_db_session)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    comment.content = content
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
def delete(comment_id: int, db: Session = Depends(get_db_session)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(comment)
    db.commit()

    return {
        "message": f"Comment '{comment.content}' deleted successfully"
    }
