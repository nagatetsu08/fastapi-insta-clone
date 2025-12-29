from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from schema.user import UserDisplay, CreateUser
from db.database import get_db
from repositories.user import cretate_user, get_user_by_email

router = APIRouter(
    prefix='/user',
    tags=['user']
)

# repository側で戻り値の型を指定しているが、ルーティングメソッド側でも必ずresponse_modelを定義すること。
# エラーになるわけではないが、どのような値を返すのかをちゃんと定義してやるのが礼儀。

@router.post('', response_model=UserDisplay, status_code=status.HTTP_201_CREATED)
def create_user(request: CreateUser, db: Session = Depends(get_db)):

    # 既存チェック(同じメールアドレスでの登録がないか)
    # 存在していたらErrorをthrowする（後は勝手にFastAPIがCatchしてエラーレスポンスに変えてくれる）
    if get_user_by_email(db, request.email):
        raise HTTPException(status_code=400, detail="This Email Address is already registered")

    return cretate_user(db, request)