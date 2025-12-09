from pydantic import BaseModel
from src.db.enums import UserRelationStatuses, UserRelationTypes
from datetime import datetime


class UserRelationCreate(BaseModel):
    user_b_id: int
    type: UserRelationTypes

class UserRelationResponse(BaseModel):
    id: int
    user_a_id: int
    user_b_id: int
    type: UserRelationTypes
    status: UserRelationStatuses
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
