from pydantic import BaseModel

class CommentIQRequest(BaseModel):
    text: str
