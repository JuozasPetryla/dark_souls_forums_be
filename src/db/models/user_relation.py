from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship
from src.db.base import Base
from src.db.enums import UserRelationStatuses, UserRelationTypes
from datetime import datetime

class UserRelation(Base):
    __tablename__ = "user_relations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    
    type = Column(
        Enum(
            UserRelationTypes,
            values_callable=lambda obj: [e.value for e in obj],
            name="userrelationtypes",
        ),
        nullable=False
    )

    status = Column(
        Enum(
            UserRelationStatuses,
            values_callable=lambda obj: [e.value for e in obj],
            name="userrelationstatuses",
        ),
        nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user_a_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_b_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user_a = relationship("User", foreign_keys=[user_a_id], back_populates="user_relations_a")
    user_b = relationship("User", foreign_keys=[user_b_id], back_populates="user_relations_b")
