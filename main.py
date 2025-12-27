from fastapi import FastAPI
from db.database import engine, Base
from models.user import DbUser
from router.user import router as user_router
from router.post import router as post_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(user_router)
app.include_router(post_router)


# DB migration(uvicornを起動した状態で保存すると必要ならばmigrationが勝手に動く)
Base.metadata.create_all(bind=engine)

# 第一引数（'/images'）: ブラウザからアクセスする時のURL
# 第二引数（StaticFiles(directory='images')）: サーバー上のどのフォルダを公開するか
# 第三引数（name='images'）：FastAPIの内部でこの「マウント設定」を識別するための名前
# （プログラム内でURLを逆引き（url_for）する時に使いますが、基本的には第1引数と同じにしておけばOK）
app.mount('/images', StaticFiles(directory='images'), name='images')