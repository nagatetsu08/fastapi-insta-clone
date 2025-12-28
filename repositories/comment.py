from sqlalchemy.orm.session import Session
from sqlalchemy import select
from models.comment import DbComment
from schema.comment import CreateComment
from datetime import datetime

# CreateCommentの構造とDbCommentの構造を合わせないパターンも想定した実装
def create_comment_db(db: Session, request: CreateComment) -> DbComment:
    new_comment = DbComment(
        text = request.text,
        user_id = request.user_id,
        post_id = request.post_id,
        timestamp = datetime.now()
    )

    try:
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
    except Exception as e:
        db.rollback()
        raise e

    return new_comment

def get_comments_by_post_id(db: Session, post_id: int):
    
    query = select(DbComment).where(DbComment.post_id == post_id)
    result = db.execute(query)
    return result.scalars().all()