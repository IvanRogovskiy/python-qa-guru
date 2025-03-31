from http import HTTPStatus

from typing import Optional, Iterable

from pydantic import ValidationError

from app.database import users

from fastapi import APIRouter, HTTPException, Query, Response, Depends

from app.models.User import User, UserCreate, UserUpdate

from fastapi_pagination import paginate, Page

user_router = APIRouter()


@user_router.post("/api/users", status_code=HTTPStatus.CREATED)
def create_user(user: User):
    try:
        UserCreate.model_validate(user.model_dump(exclude={"id"}))
    except ValidationError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"{e}")
    if users.get_user(user.id):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"User with id: {user.id} already exist")
    return users.create_user(user)


@user_router.get("/api/users/{user_id}", response_model=User)
def get_user(user_id: int) -> User:
    if user_id < 0:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    user: Optional[User] = users.get_user(user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@user_router.get("/api/users", response_model=Page[User])
def get_users() -> Iterable[User]:
    users_list = [*users.get_users()]
    return paginate(users_list)


@user_router.patch("/api/users/{user_id}")
def update_user(user_id, user: UserUpdate) -> Optional[User]:
    UserUpdate.model_validate(user)
    if not users.get_user(user_id):
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return users.update_user(user_id, user)


@user_router.delete("/api/users/{user_id}")
def delete_user(user_id: int) -> int:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    if not users.get_user(user_id):
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    users.delete_user(user_id)
    return user_id
