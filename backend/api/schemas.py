import uuid

from pydantic import BaseModel, EmailStr, SecretStr, field_validator

from database.models import User


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

    # created: datetime.datetime

    @field_validator('author')
    def take_user_name(cls, value: User) -> str:
        return f"{value.first_name.title()} {value.last_name.title()}<{value.email}>"


class __BaseUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    is_superuser: bool

    class Config:
        from_attributes = True


class UserIn(__BaseUser):
    password: str

    @field_validator("password")
    def check_password_weakness(cls, values: dict) -> dict:
        return values


class UserOut(__BaseUser):
    id: str  # noqa

    @field_validator("id")
    def uuid2str(cls, value: uuid.UUID) -> str:
        return str(value)


class Credentials(BaseModel):
    email: EmailStr
    password: SecretStr


