from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from .base import BaseModel


class Role(BaseModel):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True, nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    users = relationship(
        "User",
        back_populates="role",
    )
