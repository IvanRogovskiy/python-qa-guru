from typing import Optional

from pydantic import EmailStr, BaseModel, HttpUrl, ConfigDict

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr
    name: str


class UserCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    email: EmailStr
    name: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
