from db.database import Base
from sqlalchemy import Column, Integer, String

# userモデル定義（テーブル構造）
class DBUser(Base):
    # テーブル名
    __tablename__ = "users"

    # カラム定義
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)