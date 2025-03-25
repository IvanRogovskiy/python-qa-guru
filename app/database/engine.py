import os

from sqlmodel import Session
from sqlalchemy.orm import Session
from sqlmodel import create_engine, SQLModel, text

# pool-size - количество одновременных коннектов
engine = create_engine(os.getenv("DATABASE_ENGINE"), pool_size=int(os.getenv("POOL_SIZE", 10)))


def create_db_and_table():
    SQLModel.metadata.create_all(engine)


def check_database():
    with Session(engine) as s:
        try:
            s.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(e)
            return False
