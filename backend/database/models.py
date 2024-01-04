import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class User(Base):
    __tablename__ = "user"  # noqa

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)  # noqa
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return self.username


class Post(Base):
    __tablename__ = "post"  # noqa

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa
    title: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column(nullable=False)
    author: Mapped["User"] = relationship(back_populates="posts")
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created: Mapped[datetime] = mapped_column(server_default=func.now())
