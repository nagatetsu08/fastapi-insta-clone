from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)

class UserDisplay(BaseModel):
    username: str
    email: EmailStr
    # DBから取り出したデータ(ORM化されたもの)をPydanticモデルに変換する
    # DBモデルとこのクラス内で定義したフィールド名：型が一致すると勝手に当てはめてくれる
    class ConfigDict:
        from_attributes = True

class CreateUser(UserBase):
    password: str = Field(..., min_length=8)

class UserAuth(BaseModel):
    id: int
    username: str
    email: str