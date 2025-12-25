from fastapi import FastAPI
from db.database import engine, Base
from models.user import DBUser
from router.user import router as user_router


app = FastAPI()
app.include_router(user_router)

@app.get("")
def root():
    return "Hello world"


# DB migration(uvicornを起動した状態で保存すると必要ならばmigrationが勝手に動く)
Base.metadata.create_all(bind=engine)

