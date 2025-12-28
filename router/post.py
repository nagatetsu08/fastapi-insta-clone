from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from schema.post import PostDisplay, CreatePost
from db.database import get_db
from repositories.post import create_post_db, get_all_posts, delete_post_by_id
import random
import string
import shutil
from schema.user import UserAuth
from auth.oauth2 import get_current_user
from exceptions.post_exception import PostNotFoundException, UnauthorizedException
from enums.image_url_types import ImageUrlTypes

router = APIRouter(
    prefix='/post',
    tags=['posts'],
)

@router.post('', response_model=PostDisplay, status_code=status.HTTP_201_CREATED)
def create_post(request: CreatePost, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):

    # in ImageUrlTypesという感じで直接enumを使うとエラーが起きる。以下のようにやるのが正解。

    if not request.image_url_type in [item.value for item in ImageUrlTypes]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail="Parameter Image_url_type can only take 'absolute' or 'relative'"
        )

    # 同じ画像だろうが、一つの投稿として登録させる（重複チェックはさせない）
    return create_post_db(db, request)

# python3.9以降はlistをそのまま型ヒントとして使える。3.9より前はfrom typing import Listを使っていた。
@router.get('/all', response_model=list[PostDisplay])
def all_posts(db: Session = Depends(get_db)):
    return get_all_posts(db)

# Fileによって、multipart/form-dataでデータを受け取ることを示す。
# ...はpythonの「必須入力」を表す（requiredと同じ）
@router.post('/image')
def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
    
    # 保存するイメージにつけるランダムな名前（Uploadファイルの名前が被らないようにするため）
    # uuidでもいいけど、こんなやり方もあるんだ的な意味で以下のやり方を試す。

    # 1.ランダム文字列の候補たち
    letters = string.ascii_letters

    # 2.ランダム文字列生成（random.choice(letters)で1文字ランダム値がそれを6回繰り返す）
    # 例: ['a', '7', 'B', 'z', ...]
    random_list = [random.choice(letters) for i in range(6)]

    # リストを結合して1つの「文字列」にする
    # '結合文字'.join でconcatさせる
    random_str = ''.join(random_list)
    new_file = f'_{random_str}'
    
    # newfile名とオリジナルのやつの拡張子だけをとる（rsplitで分けて、後の方をとる）
    filename = new_file.join(image.filename.rsplit('.', 1))

    path = f'images/{filename}.'

    # pathにあるファイルを開いて（なければ新規作成して開く）、imageの内容をbufferで書き込む
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}

@router.get("/delete/{id}")  # ※1
def delete(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    try:
        # Repositoryの関数を呼び出す
        return delete_post_by_id(db, id, current_user.id)
        
    except PostNotFoundException as e:
        # e.message には「指定された投稿が見つかりませんでした」が入っている
        # HttpExceptionでラッピングしないと、全て500エラー扱いになる
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=e.message
        )
        
    except UnauthorizedException as e:
        # e.message には「この操作を行う権限がありません」が入っている
        # HttpExceptionでラッピングしないと、全て500エラー扱いになる
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=e.message
        )