from sqlalchemy.orm.session import Session
from schema.post import CreatePost
from models.post import DbPost
from datetime import datetime
from sqlalchemy import select

def create_post_db(db: Session, request: CreatePost) -> DbPost:
    post_data = request.model_dump()
    post_data['timestamp'] = datetime.now()
    new_post = DbPost(**post_data)

    try:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
    except Exception as e:
        db.rollback()
        raise e

    return new_post

def get_all_posts(db: Session) -> list[DbPost]:
    query = select(DbPost)
    result = db.execute(query)
    # .scalars() を使うことで、Rowオブジェクトではなくモデル(DbPost)のリストとして取り出せる。
    # .scalars()がdb.query(旧式の書き方でモデルを返す)と同じ意味になる
    return result.scalars().all()