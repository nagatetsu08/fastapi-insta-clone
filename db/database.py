from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from collections.abc import Generator

SQLALCHEMY_DATABASE_URL = 'sqlite:///./ig_api.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db() -> Generator[Session, None, None] :
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()