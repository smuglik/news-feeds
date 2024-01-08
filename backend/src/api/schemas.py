from datetime import datetime
import uuid

from pydantic import BaseModel, EmailStr, SecretStr, field_validator


class __BasePost(BaseModel):
    title: str
    body: str

    class Config:
        from_attributes = True


class PostIn(__BasePost):
    pass


class PostOut(__BasePost):
    id: int  # noqa
    author: str
    created: datetime


class __BaseUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    is_superuser: bool

    class Config:
        from_attributes = True


class UserIn(__BaseUser):
    password: str


class UserOut(__BaseUser):
    id: str  # noqa

    @field_validator("id")
    def uuid2str(cls, value: uuid.UUID) -> str:
        return str(value)


class Credentials(BaseModel):
    email: EmailStr
    password: SecretStr
