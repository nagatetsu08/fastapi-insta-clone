from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi.security import OAuth2PasswordRequestForm 
from repositories.user import get_user_by_email
from utility.hashing import Hash
from auth.oauth2 import create_access_token

router = APIRouter(
    prefix='/login',
    tags=['autentication']
)

@router.post('')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestFormの仕様により、usernameとpasswordという名前でしか受け取ってくれない
    # 独自のPydanticモデルを利用する方法もあるが、今度はSwagger UIのAuthorize（鍵マークのログインボタン）」機能が使えなくなる。
    # 従って、とりあえず渡ってくる段階ではusernameというパラメータで受け取って、email変数に詰め替えて利用する。
    email = request.username
    user = get_user_by_email(db, email)

    # ユーザーが存在しなかった時
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credential"
        )
    
    # パスワード比較した結果が違うとき
    # request.passwordをhash化して、DB上のパスワード（Hash化されて保存されているもの）と比較する。
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credential"
        )
    
    # ここでusernameではなく、user.emailをトークン内に含めるようにしてやる
    access_token = create_access_token(data={"sub": user.email})

    return {
        'access_token': access_token,
        'token_type': "bearer",
        'user_id': user.id,
        'user_name': user.username
    }
