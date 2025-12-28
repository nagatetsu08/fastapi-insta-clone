from db.database import Base
from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey
from sqlalchemy.orm import relationship

class DbPost(Base):
    # テーブル名
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    image_url_type = Column(String)
    caption = Column(String)
    timestamp = Column(DATETIME)
    creator_id = Column(Integer, ForeignKey('users.id')) #ForeignKeyはテーブル名で書かないとダメ。（AI曰くモデルクラス名では書けないらしい）
    user = relationship('DbUser', back_populates='posts')
    comments = relationship('DbComment', back_populates='post')