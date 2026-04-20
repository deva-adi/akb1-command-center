from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, default="viewer")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    auth_provider: Mapped[str] = mapped_column(String, default="local")
    external_id: Mapped[str | None] = mapped_column(String)
    password_hash: Mapped[str | None] = mapped_column(String)
    last_login: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )


class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = (
        UniqueConstraint("user_id", "role", "scope_type", "scope_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    role: Mapped[str] = mapped_column(String, nullable=False)
    scope_type: Mapped[str | None] = mapped_column(String)
    scope_id: Mapped[int | None] = mapped_column(Integer)
    granted_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    granted_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
