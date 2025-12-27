from pydantic import BaseModel, Field
from datetime import datetime

class PostBase(BaseModel):
    image_url: str
    image_url_type: str
    caption: str
    creator_id: int

# For PostDisplay(リレーション用)
class UserForDisplay(BaseModel):
    username: str
    # DBモデルをこの型に突っ込んだときに、同名かつ同型の定義にマッピングしてくれる
    # このクラスはリレーションで使うのだが、このようなリレーション先でもちゃんとマッピングするようにConfigDictをかく
    class ConfigDict:
        from_attributes = True

class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    user: UserForDisplay
    # DBモデルをこの型に突っ込んだときに、同名かつ同型の定義にマッピングしてくれる
    class ConfigDict:
        from_attributes = True

class CreatePost(PostBase):
    pass