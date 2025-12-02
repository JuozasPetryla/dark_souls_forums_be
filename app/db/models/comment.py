from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..base import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    modified_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    modified = Column(Boolean, nullable=False, server_default="false")

    author_iq = Column(Integer, nullable=True)
    author_ip_address = Column(String(255), nullable=False)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    author = relationship("User", back_populates="comments", foreign_keys=[author_id])
    post = relationship("Post", back_populates="comments", foreign_keys=[post_id])
    ratings = relationship("CommentRating", back_populates="comment", foreign_keys=["CommentRating.comment_id"])