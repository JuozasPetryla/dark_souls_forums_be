from sqlalchemy.orm import Session
from src.db.session import get_db_session
from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.db.models import Post, User, Topic, Comment, FavoritePost
from src.services.authentication import get_user_by_token
from src.services.posts import generate_and_save_post_summary
import sqlalchemy as sa

posts_router = APIRouter()


@posts_router.get("/read/{post_id}")
def read_post(post_id: int, db: Session = Depends(get_db_session)):
    """Peržiūrėti įrašą - View a post by ID"""
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Increment view count
    post.view_count += 1
    db.commit()
    db.refresh(post)
    
    # Get author information
    author = db.query(User).filter(User.id == post.author_id).first()
    
    # Get topic information
    topic = db.query(Topic).filter(Topic.id == post.topic_id).first()
    
    # Get comments for this post
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "summary": post.summary,
            "view_count": post.view_count,
            "locked": post.locked,
            "created_at": post.created_at,
            "modified_at": post.modified_at,
            "modified": post.modified,
            "author": {
                "id": author.id,
                "nickname": author.nickname,
                "image": author.image
            },
            "topic": {
                "id": topic.id,
                "title": topic.title,
                "image": topic.image
            },
            "comments": comments
        })
    )


@posts_router.get("/read")
def read_all_posts(db: Session = Depends(get_db_session)):
    """Get all posts"""
    posts = db.query(Post).all()
    
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found")
    
    result = []
    for post in posts:
        author = db.query(User).filter(User.id == post.author_id).first()
        topic = db.query(Topic).filter(Topic.id == post.topic_id).first()
        
        result.append({
            "id": post.id,
            "title": post.title,
            "summary": post.summary,
            "view_count": post.view_count,
            "created_at": post.created_at,
            "modified_at": post.modified_at,
            "author": {
                "id": author.id,
                "nickname": author.nickname,
                "image": author.image
            },
            "topic": {
                "id": topic.id,
                "title": topic.title
            }
        })
    
    return JSONResponse(content=jsonable_encoder(result))


@posts_router.post("/generate-summary/{post_id}")
async def generate_summary(
    post_id: int,
    db: Session = Depends(get_db_session),
    user: User = Depends(get_user_by_token),
):
    """Sugeneruoti įrašo santrauką naudojant AI - Generate post summary using AI"""
    
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if user is the author of the post
    if post.author_id != user.id:
        raise HTTPException(status_code=403, detail="You can only generate summary for your own posts")
    
    try:
        summary = await generate_and_save_post_summary(db, post_id, post.content, post.title)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Summary generated successfully",
                "post_id": post_id,
                "summary": summary
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")


@posts_router.post("/create")
def create_post(
    title: str = Body(...),
    content: str = Body(...),
    summary: str = Body(None),
    topic_id: int = Body(...),
    db: Session = Depends(get_db_session),
    user: User = Depends(get_user_by_token),
):
    """Pridėti įrašą - Create a new post"""
    
    # Verify that topic exists
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Check if topic is locked
    if topic.locked:
        raise HTTPException(status_code=403, detail="Cannot create post in a locked topic")
    
    new_post = Post(
        title=title,
        content=content,
        summary=summary,
        topic_id=topic_id,
        author_id=user.id
    )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return JSONResponse(
        status_code=201,
        content={
            "message": "Post created successfully",
            "post_id": new_post.id,
            "title": new_post.title,
            "author_id": new_post.author_id,
            "author_nickname": user.nickname,
            "topic_id": new_post.topic_id
        }
    )


@posts_router.put("/update/{post_id}")
def update_post(
    post_id: int,
    title: str = Body(...),
    content: str = Body(...),
    summary: str = Body(None),
    db: Session = Depends(get_db_session),
    user: User = Depends(get_user_by_token),
):
    """Redaguoti įrašą - Update an existing post"""
    
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if user is the author of the post
    if post.author_id != user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own posts")
    
    # Check if post is locked
    if post.locked:
        raise HTTPException(status_code=403, detail="Cannot edit a locked post")
    
    # Update post fields
    post.title = title
    post.content = content
    post.summary = summary
    post.modified = True
    post.modified_at = sa.text('now()')
    
    db.commit()
    db.refresh(post)
    
    return JSONResponse(
        status_code=200,
        content={
            "message": "Post updated successfully",
            "post_id": post.id,
            "title": post.title,
            "modified_at": post.modified_at
        }
    )


@posts_router.delete("/delete/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db_session),
    user: User = Depends(get_user_by_token),
):
    """Trinti įrašą - Delete a post"""
    
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if user is the author of the post
    if post.author_id != user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own posts")
    
    post_title = post.title
    
    db.delete(post)
    db.commit()
    
    return JSONResponse(
        status_code=200,
        content={
            "message": f"Post '{post_title}' deleted successfully"
        }
    )


@posts_router.post("/favorite/{post_id}")
def add_to_favorites(
    post_id: int,
    db: Session = Depends(get_db_session),
    user: User = Depends(get_user_by_token),
):
    """Pridėti į mėgstamus įrašus - Add a post to favorites"""

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing = db.query(FavoritePost).filter(
        FavoritePost.user_id == user.id,
        FavoritePost.post_id == post_id,
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Post already in favorites")

    favorite = FavoritePost(user_id=user.id, post_id=post_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Post added to favorites",
            "favorite_id": favorite.id,
            "post_id": post_id,
            "user_id": user.id,
        },
    )


@posts_router.delete("/favorite/{post_id}")
def remove_from_favorites(
    post_id: int,
    db: Session = Depends(get_db_session),
    user: User = Depends(get_user_by_token),
):
    """Išimti iš mėgstamų įrašų - Remove a post from favorites"""

    favorite = db.query(FavoritePost).filter(
        FavoritePost.user_id == user.id,
        FavoritePost.post_id == post_id,
    ).first()

    if not favorite:
        raise HTTPException(status_code=404, detail="Post is not in favorites")

    db.delete(favorite)
    db.commit()

    return JSONResponse(
        status_code=200,
        content={
            "message": "Post removed from favorites",
            "post_id": post_id,
            "user_id": user.id,
        },
    )


@posts_router.get("/favorite")
def list_my_favorites(
    db: Session = Depends(get_db_session),
    user: User = Depends(get_user_by_token),
):
    """Peržiūrėti mėgstamus įrašus - List current user's favorite posts"""

    favorites = db.query(FavoritePost).filter(FavoritePost.user_id == user.id).all()

    if not favorites:
        raise HTTPException(status_code=404, detail="No favorite posts found")

    result = []
    for fav in favorites:
        post = db.query(Post).filter(Post.id == fav.post_id).first()
        if not post:
            # Skip dangling favorites if post was deleted
            continue
        author = db.query(User).filter(User.id == post.author_id).first()
        topic = db.query(Topic).filter(Topic.id == post.topic_id).first()

        result.append({
            "favorite_id": fav.id,
            "added_at": fav.created_at,
            "post": {
                "id": post.id,
                "title": post.title,
                "summary": post.summary,
                "view_count": post.view_count,
                "created_at": post.created_at,
                "modified_at": post.modified_at,
                "author": {
                    "id": author.id if author else None,
                    "nickname": author.nickname if author else None,
                    "image": author.image if author else None,
                },
                "topic": {
                    "id": topic.id if topic else None,
                    "title": topic.title if topic else None,
                },
            },
        })

    if not result:
        raise HTTPException(status_code=404, detail="No favorite posts found")

    return JSONResponse(content=jsonable_encoder(result))
