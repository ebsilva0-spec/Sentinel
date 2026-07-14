from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql://postgres:NovaSenha%402026@localhost:5432/sentinel"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()