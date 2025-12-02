from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from . import Post
from ..base import Base

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    image = Column(String(255), nullable=False)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    modified_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    locked = Column(Boolean, nullable=False, server_default="false")

    view_count = Column(Integer, nullable=False, server_default="0")

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    author = relationship("User", back_populates="topics_created")
    posts = relationship("Post", back_populates="topic", foreign_keys=[Post.topic_id], cascade="all, delete")