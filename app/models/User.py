from typing import Optional

from pydantic import EmailStr, BaseModel, HttpUrl

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr
    name: str


class UserCreate(BaseModel):
    email: EmailStr
    name: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
