from db.database import Base
from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey
from sqlalchemy.orm import relationship

# リレーションにおいて、「多」側になるテーブル。ForeignKeyを設定する
# postを通して取得できるユーザーはあくまで、投稿をしたユーザー。
# コメントしたユーザーを取得するためにここにも必要。
class DbComment(Base):
    # テーブル名
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    timestamp = Column(DATETIME)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("DbUser", back_populates='comments') # テーブル項目としては作成されない
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship("DbPost", back_populates='comments') # テーブル項目としては作成されない
