from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship
from ..base import Base

class SteamAccount(Base):
    __tablename__ = "steam_accounts"

    id = Column(Integer, primary_key=True, index=True)
    steam_id = Column(String(255), nullable=False)
    updated_at = Column(DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="steam_account", foreign_keys=[user_id])