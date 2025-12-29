from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from repositories.comment import get_comments_by_post_id, create_comment_db
from schema.comment import CreateComment, CommentDisplay
from schema.user import UserAuth
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/comment',
    tags=['comments'],
)


@router.get('/all/{post_id}', response_model=list[CommentDisplay], status_code=status.HTTP_201_CREATED)
def comments(post_id: int, db: Session = Depends(get_db)):
    return get_comments_by_post_id(db, post_id)

@router.post('', response_model=CommentDisplay)
def create(request: CreateComment, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return create_comment_db(db, request)