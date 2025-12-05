from sqlalchemy import Column, Integer, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from ..base import Base
from ..enums import CommentRatingTypes

class CommentRating(Base):
    __tablename__ = "comment_ratings"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Enum(CommentRatingTypes, values_callable=lambda obj: [e.value for e in obj]), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=False)

    user = relationship("User", back_populates="comment_ratings", foreign_keys=[user_id])
    comment = relationship("Comment", back_populates="ratings", foreign_keys=[comment_id])

    __table_args__ = (UniqueConstraint("user_id", "comment_id", name="uq_user_comment_rating"),)