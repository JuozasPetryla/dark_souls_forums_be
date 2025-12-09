from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from .favorite_post import FavoritePost
from .comment import Comment
from src.db.base import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)

    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    view_count = Column(Integer, nullable=False, server_default="0")

    locked = Column(Boolean, nullable=False, server_default="false")

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    modified_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    modified = Column(Boolean, nullable=False, server_default="false")

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)

    author = relationship("User", back_populates="posts", foreign_keys=[author_id])
    topic = relationship("Topic", back_populates="posts", foreign_keys=[topic_id])
    favorites = relationship("FavoritePost", back_populates="post", foreign_keys=[FavoritePost.post_id], cascade="all, delete")
    comments = relationship("Comment", back_populates="post", foreign_keys=[Comment.post_id], cascade="all, delete")