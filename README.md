# Instagram Clone API

Instagram風のSNS バックエンドAPIです。FastAPI + SQLAlchemy で構築されており、ユーザー管理・投稿・コメント・画像アップロード・JWT認証の機能を提供します。

本APIはUdemy講座「Complete FastAPI masterclass from scratch」をベースに、個人学習として実装および一部改修を行ったものです。サンプルコードの写経ではなく、構成や実装の意図を理解しながら実装しています。


https://www.udemy.com/course/completefastapi/

## 技術スタック

| カテゴリ           | 技術                       |
|--------------------|----------------------------|
| フレームワーク     | FastAPI                    |
| 言語               | Python 3.11                |
| ORM                | SQLAlchemy                 |
| データベース       | SQLite                     |
| マイグレーション   | Alembic                    |
| 認証               | JWT (python-jose) / OAuth2 |
| パスワードハッシュ | passlib + bcrypt           |
| サーバー           | Uvicorn                    |

## プロジェクト構成

```
insta_clone/
├── main.py                  # アプリケーションエントリーポイント
├── alembic.ini              # Alembicマイグレーション設定
├── requirement.txt          # 依存パッケージ一覧
├── ig_api.db                # SQLiteデータベースファイル
├── auth/
│   └── oauth2.py            # JWT トークン生成・検証
├── db/
│   └── database.py          # DB接続・セッション管理
├── enums/
│   └── image_url_types.py   # 画像URL種別 (absolute/relative)
├── exceptions/
│   └── post_exception.py    # 投稿関連カスタム例外
├── images/                  # アップロード画像の保存先
├── migrations/              # Alembicマイグレーションファイル
├── models/                  # SQLAlchemy モデル定義
│   ├── user.py              # ユーザーモデル
│   ├── post.py              # 投稿モデル
│   └── comment.py           # コメントモデル
├── repositories/            # データベース操作層
│   ├── user.py
│   ├── post.py
│   └── comment.py
├── router/                  # APIエンドポイント定義
│   ├── auth.py              # ログイン (POST /login)
│   ├── user.py              # ユーザー登録 (POST /user)
│   ├── post.py              # 投稿CRUD・画像アップロード
│   └── comment.py           # コメント取得・作成
├── schema/                  # Pydantic リクエスト/レスポンススキーマ
│   ├── user.py
│   ├── post.py
│   └── comment.py
└── utility/
    └── hashing.py           # パスワードハッシュユーティリティ
```

## API エンドポイント

| メソッド | パス                     | 説明                       | 認証 |
|----------|--------------------------|----------------------------|------|
| POST     | `/user`                  | ユーザー登録               | 不要 |
| POST     | `/login`                 | ログイン (JWTトークン取得) | 不要 |
| POST     | `/post`                  | 投稿作成                   | 必要 |
| GET      | `/post/all`              | 全投稿取得                 | 不要 |
| POST     | `/post/image`            | 画像アップロード           | 必要 |
| GET      | `/post/delete/{id}`      | 投稿削除                   | 必要 |
| GET      | `/comment/all/{post_id}` | 投稿のコメント一覧取得     | 不要 |
| POST     | `/comment`               | コメント作成               | 必要 |

## セットアップ

### 1. 仮想環境の作成と有効化

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. 依存パッケージのインストール

```bash
pip install -r requirement.txt
```

### 3. 環境変数の設定

プロジェクトルートに `.env` ファイルを作成し、以下の値を設定してください。

```env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. サーバーの起動

```bash
uvicorn main:app --reload
```

起動後、以下のURLでAPIドキュメント (Swagger UI) にアクセスできます。

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## CORS 設定

デフォルトでは `http://localhost:3000` からのアクセスを許可しています。本番環境では [main.py](main.py) の `origins` リストを適切に変更してください。
