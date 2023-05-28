import uuid

from pydantic import BaseModel, EmailStr, SecretStr, validator

from database.models import User


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

    # created: datetime.datetime

    @validator('author', pre=True)
    def take_user_name(cls, value: User) -> str:
        return f"{value.first_name.title()} {value.last_name.title()}<{value.email}>"


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


class Product(BaseModel):
    id: int
    name: str
    description: str
    cost: float

    class Config:
        orm_mode = True
