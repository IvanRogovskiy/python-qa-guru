from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(..., error_msg={"value_error": "Id не может быть пустым или None."})
    email: str
    name: str