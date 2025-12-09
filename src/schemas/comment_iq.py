from pydantic import BaseModel

class CommentIQRequest(BaseModel):
    prompt: str
    text: str
