from pydantic import BaseModel
from src.db.enums import UserRelationStatuses, UserRelationTypes

class UserRelationCreate(BaseModel):
    user_b_id: int
    type: UserRelationTypes

class UserRelationResponse(BaseModel):
    id: int
    user_a_id: int
    user_b_id: int
    status: UserRelationStatuses
    type: UserRelationTypes
    updated_at: str

    class Config:
        orm_mode = True
