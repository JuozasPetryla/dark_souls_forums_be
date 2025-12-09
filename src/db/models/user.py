from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship

from .game import Game
from .topic import Topic
from .user_relation import UserRelation
from .steam_account import SteamAccount
from .post import Post
from .favorite_post import FavoritePost
from .comment import Comment
from .comment_rating import CommentRating
from src.db.base import Base
from src.db.enums import UserRoles

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    modified_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    last_login_at = Column(DateTime, nullable=True)

    nickname = Column(String(255), nullable=False, unique=True)
    image = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    playing_class = Column(String(255), nullable=True)
    origin_country = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    discord_id = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    surname = Column(String(255), nullable=True)
    postal_code = Column(String(255), nullable=True)
    phone_number = Column(String(255), nullable=True)

    notifications_on = Column(Boolean, nullable=False, server_default="true")
    profile_visibility_on = Column(Boolean, nullable=False, server_default="true")
    auto_friend_request_accept_on = Column(Boolean, nullable=False, server_default="false")
    disable_friend_requests_on = Column(Boolean, nullable=False, server_default="false")

    role = Column(Enum(UserRoles, values_callable=lambda obj: [e.value for e in obj]), nullable=False, server_default=UserRoles.USER.value)

    games = relationship("Game", back_populates="user", foreign_keys=[Game.user_id], cascade="all, delete")
    topics_created = relationship("Topic", back_populates="author", foreign_keys=[Topic.author_id], cascade="all, delete")
    user_relations_a = relationship("UserRelation", back_populates="user_a", foreign_keys=[UserRelation.user_a_id], cascade="all, delete")
    user_relations_b = relationship("UserRelation", back_populates="user_b", foreign_keys=[UserRelation.user_b_id], cascade="all, delete")
    steam_account = relationship("SteamAccount", back_populates="user", uselist=False, foreign_keys=[SteamAccount.user_id], cascade="all, delete")
    posts = relationship("Post", back_populates="author", foreign_keys=[Post.author_id], cascade="all, delete")
    favorite_posts = relationship("FavoritePost", back_populates="user", foreign_keys=[FavoritePost.user_id], cascade="all, delete")
    comments = relationship("Comment", back_populates="author", foreign_keys=[Comment.author_id], cascade="all, delete")
    comment_ratings = relationship("CommentRating", back_populates="user", foreign_keys=[CommentRating.user_id], cascade="all, delete")