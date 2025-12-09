from sqlalchemy.orm import Session
from src.db.session import get_db_session
from fastapi import APIRouter, Depends, Body, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional
from src.db.models import Topic, Post
import sqlalchemy as sa
import shutil
import uuid
import os

UPLOAD_DIR = "/dark_souls_forums_be/src/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

topics_router = APIRouter()

@topics_router.post("/create")
def create(title: str = Body(...), description: str = Body(...), image_link: str = Body(...), db: Session = Depends(get_db_session)):
    author_id = 1  # temporary, will change when login is implemented

    new_topic = Topic(title=title, description=description, image=image_link, author_id=author_id)

    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Topic created successfully",
            "topic_id": new_topic.id,
            "topic_title": new_topic.title,
        }
    )

@topics_router.get("/read/{topic_id}")
def read(topic_id: int, db: Session = Depends(get_db_session)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    topic.view_count += 1
    db.commit()
    db.refresh(topic)

    posts = db.query(Post).filter(Post.topic_id == topic_id).all()

    return JSONResponse(
        status_code=200,
        content=jsonable_encoder({
            "id": topic.id,
            "description": topic.description,
            "title": topic.title,
            "image": topic.image,
            "view_count": topic.view_count,
            "created_at": topic.created_at,
            "modified_at": topic.modified_at,
            "locked": topic.locked,
            "posts": posts
        })
    )

@topics_router.get("/read")
def read(db: Session = Depends(get_db_session)):
    topics = db.query(Topic).all()

    if not topics:
        raise HTTPException(status_code=404, detail="No topics found")

    return topics


@topics_router.put("/update/{topic_id}")
def update(topic_id: int, title: str = Body(...), description: str = Body(...), image_link: str = Body(...), db: Session = Depends(get_db_session)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    topic.title = title
    topic.image = image_link
    topic.description = description
    topic.modified_at = sa.text('now()')

    db.commit()
    db.refresh(topic)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Topic updated successfully",
            "topic_id": topic.id,
            "topic_title": topic.title,
        }
    )

@topics_router.delete("/delete/{topic_id}")
def delete(topic_id: int, db: Session = Depends(get_db_session)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    db.delete(topic)
    db.commit()

    return JSONResponse(
        status_code=200,
        content={
            "message": f"Topic '{topic.title}' deleted successfully"
        }
    )

@topics_router.post("/upload-image")
async def upload_image(image: UploadFile = File(...)):
    # Validate file type
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Generate unique filename
    ext = image.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # URL that frontend can use to access the image
    file_url = f"/static/uploads/{filename}"

    return {"url": file_url}