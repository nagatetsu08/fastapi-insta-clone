from sqlalchemy.orm.session import Session
from schema.post import CreatePost
from models.post import DbPost
from datetime import datetime
from sqlalchemy import select
from fastapi import HTTPException, status
from exceptions.post_exception import PostNotFoundException, UnauthorizedException

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

def delete_post_by_id(db: Session, id: int, user_id: int) -> bool:
    query = select(DbPost).where(DbPost.id == id)
    result = db.execute(query)
    post = result.scalars().first()

    if not post:
        raise PostNotFoundException(f"post is not found({id})")
    
    # 所持ユーザーが認証ユーザーと異なる時
    if post.creator_id != user_id:
        raise UnauthorizedException(f"this user is Unauthorized({user_id})")
    
    try:
        db.delete(post)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    return True