from db.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# userモデル定義（テーブル構造）
class DbUser(Base):
    # テーブル名
    __tablename__ = "users"

    # カラム定義
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    posts = relationship('DbPost', back_populates='user')
    comments = relationship('DbComment', back_populates='user')