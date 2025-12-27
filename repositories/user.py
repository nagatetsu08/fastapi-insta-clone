from sqlalchemy.orm.session import Session
from sqlalchemy import select
from schema.user import CreateUser
from models.user import DbUser
from utility.hashing import Hash
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

def cretate_user(db: Session, request:CreateUser) -> DbUser:

    # 仮にDbUserとCreateUserが見た目上で同じ構造だったとしても、
    # new_user = DbUser(request)とするとエラーにある。
    # SQLAlchemyモデル（Base）は引数にキーワード引数（key=value）を要求する。
    # Pydanticモデル（BaseModel）は見た目はキーワード引数っぽく見えるが、あくまでオブジェクトなのでSQLAlchemyモデルは受け取ってくれない。

    # AIおすすめの書き方
    # 1.Pydanticの model_dump()（旧バージョンでは .dict()）で、辞書型に変換。(辞書に変換しても、オブジェクトなのでそのまま渡せない)
    # 2.パスワードだけ上書き。
    # 3.**を使って辞書の内容を、キーワード引数（key=value）に文字列展開して渡すことができる。
    user_data = request.model_dump()
    user_data["password"] = Hash.bcrypt(user_data["password"])
    new_user = DbUser(**user_data)

    # 以下の書き方はpydanticとDBModel側でフィールド名を合わせることができないときに1個１個をDBモデル側のフィールド名に寄せる書き方
    # new_user = DbUser(
    #     username = request.username,
    #     email = request.email,
    #     password = request.password # パスワードハッシュ化必要
    # )

    # SQLArchemyでもraiseしたら勝手にExceptして例外を出してくれるが、DB関連のエラーは一律500エラーで返ってしまう
    # もう少し細分化して、何でエラーになったのかをもう少し詳しく出せるようにリポジトリクラスでもtry-exceptする。
    # ただし、詳細のメッセージ表示は呼び出し元でやるので、リポジトリクラスではロールバック及びエラーのthrow(raise)のみを実施する。
    try:
        db.add(new_user)
        db.commit()
        # 以下を実行することで、SQLAlchemyはもう一度データベースに 
        # SELECT 文を発行し、これらの最新情報を取得してオブジェクトの中身を書き換えてくれる。
        # 自動採番された値、created_atなどのSQLAlchemyデフォルト値などもまとめて取得してくれる。
        db.refresh(new_user)
    except IntegrityError as ie:
        # 重複登録などが発生した場合、500ではなく400（Bad Request）を返す
        db.rollback() # エラー時はロールバックが必要
        raise ie
    except Exception as e:
        db.rollback()
        raise e

    return new_user

def get_user_by_email(db: Session, email: str) -> DbUser | None:
    stmt = select(DbUser).where(DbUser.email == email)
    return db.execute(stmt).scalar_one_or_none()