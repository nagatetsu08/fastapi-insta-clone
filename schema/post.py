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

# For PostDisplay(リレーション用)
class CommentForDisplay(BaseModel):
    text: str
    user: UserForDisplay | None # userが削除されたりで存在しないとエラーになるので、そういう場合も許容する
    timestamp: datetime
    class ConfigDict:
        from_attributes = True

class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    user: UserForDisplay | None # userが削除されたりで存在しないとエラーになるので、そういう場合も許容する
    comments: list[CommentForDisplay]
    # DBモデルをこの型に突っ込んだときに、同名かつ同型の定義にマッピングしてくれる
    class ConfigDict:
        from_attributes = True

class CreatePost(PostBase):
    image_url_type: str = 'absolute'
    pass