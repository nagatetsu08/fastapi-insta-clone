from pydantic import BaseModel, Field
from datetime import datetime

class CommentBase(BaseModel):
    text: str
    user_id: int
    post_id: int

class CreateComment(CommentBase):
    pass

class CommentDisplay(CommentBase):

    # DBモデルをこの型に突っ込んだときに、同名かつ同型の定義にマッピングしてくれる
    class ConfigDict:
        from_attributes = True