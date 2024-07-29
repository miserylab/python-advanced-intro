import os

from sqlalchemy.orm import Session
from sqlmodel import SQLModel, create_engine, Session, text

engine = create_engine(os.getenv("DATABASE_ENGINE"), pool_size=int(os.getenv("DATABASE_POOL_SIZE", 10)))


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def check_availability() -> bool:
    try:
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
    except Exception as e:
        print(e)
        return False
    return True
