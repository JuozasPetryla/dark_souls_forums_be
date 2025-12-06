from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from src.db.base import Base

class FavoritePost(Base):
    __tablename__ = "favorite_posts"

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    user = relationship("User", back_populates="favorite_posts", foreign_keys=[user_id])
    post = relationship("Post", back_populates="favorites", foreign_keys=[post_id])

    __table_args__ = (UniqueConstraint("user_id", "post_id", name="uq_favorite_user_post"),)