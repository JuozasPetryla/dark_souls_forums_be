from sqlalchemy import Column, Integer, String
from app.db.session import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

# Uncomment if you want to create tables without Alembic (for quick dev):
# Base.metadata.create_all(bind=engine)
