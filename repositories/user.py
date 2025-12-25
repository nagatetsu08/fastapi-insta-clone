from sqlalchemy.orm.session import Session
from sqlalchemy import select
from schema.user import CreateUser
from models.user import DBUser

def cretate_user(db: Session, request:CreateUser):

    # 仮にDBUserとCreateUserが見た目上で同じ構造だったとしても、
    # new_user = DBUser(request)とするとエラーにある。
    # SQLAlchemyモデル（Base）は引数にキーワード引数（key=value）を要求する。
    # Pydanticモデル（BaseModel）は見た目はキーワード引数っぽく見えるが、あくまでオブジェクトなのでSQLAlchemyモデルは受け取ってくれない。

    # new_user = DBUser(
    #     username = request.username,
    #     email = request.email,
    #     password = request.password # パスワードハッシュ化必要
    # )

    # AIおすすめの書き方
    # 1.Pydanticの model_dump()（旧バージョンでは .dict()）で、辞書型に変換。(辞書に変換しても、オブジェクトなのでそのまま渡せない)
    # 2.**を使って辞書の内容を、キーワード引数（key=value）に文字列展開して渡すことができる。
    new_user = DBUser(**request.model_dump())

    db.add(new_user)
    db.commit()

    # 以下を実行することで、SQLAlchemyはもう一度データベースに 
    # SELECT 文を発行し、これらの最新情報を取得してオブジェクトの中身を書き換えてくれる。
    # 自動採番された値、created_atなどのSQLAlchemyデフォルト値などもまとめて取得してくれる。
    db.refresh(new_user)

    return new_user

def get_user_by_email(db: Session, email: str) -> DBUser | None:
    stmt = select(DBUser).where(DBUser.email == email)
    return db.execute(stmt).scalar_one_or_none