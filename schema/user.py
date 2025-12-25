from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)

class UserDisplay(BaseModel):
    username: str
    email: EmailStr

class CreateUser(UserBase):
    password: str = Field(..., min_length=8)