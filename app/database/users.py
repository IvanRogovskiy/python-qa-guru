from typing import Optional, Iterable

from app.database.engine import engine
from app.models.User import User
from sqlmodel import Session, select


def get_user(user_id: int) -> Optional[User]:
    with Session(engine) as s:
        return s.get(User, user_id)


def get_users() -> Iterable[User]:
    with Session(engine) as s:
        statement = select(User)
        return s.exec(statement).all()


def create_user(user: User) -> User:
    with Session(engine) as s:
        s.add(user)
        s.commit()
        s.refresh(user)
        return user


def update_user(user_id: int, user: User) -> Optional[User]:
    with Session(engine) as s:
        db_user = s.get(User, user_id)
        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        s.add(db_user)
        s.commit()
        s.refresh(db_user)
        return db_user


def delete_user(user_id: int):
    with Session(engine) as s:
        user = s.get(User, user_id)
        s.delete(user)
        s.commit()
