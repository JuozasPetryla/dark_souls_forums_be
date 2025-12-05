from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship
from ..base import Base
from ..enums import UserRelationStatuses, UserRelationTypes

class UserRelation(Base):
    __tablename__ = "user_relations"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(UserRelationStatuses, values_callable=lambda obj: [e.value for e in obj]), nullable=False, server_default=UserRelationStatuses.PENDING.value)
    type = Column(Enum(UserRelationTypes, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    updated_at = Column(DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())

    user_a_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_b_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user_a = relationship("User", foreign_keys=[user_a_id], back_populates="user_relations_a")
    user_b = relationship("User", foreign_keys=[user_b_id], back_populates="user_relations_b")
