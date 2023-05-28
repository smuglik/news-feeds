import datetime
import uuid

from pydantic import BaseModel, EmailStr, SecretStr, validator

class __BasePost(BaseModel):
    title: str
    body: str
    class Config:
        orm_mode = True


class PostIn(__BasePost):
    pass


class PostOut(__BasePost):
    id: int  # noqa
    author: str
    created: datetime.datetime


class __BaseUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    is_superuser: bool
    class Config:
        orm_mode = True


class UserIn(__BaseUser):
    password: str

    @validator("password", pre=True)
    def check_password_weakness(cls, values: dict) -> dict:
        return values


class UserOut(__BaseUser):
    id: str  # noqa

    @validator("id", pre=True)
    def uuid2str(cls, value: uuid.UUID) -> str:
        return str(value)

class Credentials(BaseModel):
    email: EmailStr
    password: SecretStr

