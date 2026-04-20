"""initial schema — 42 tables from ARCHITECTURE.md §5

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-04-20
"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op
from sqlalchemy.orm import configure_mappers

from app.models import Base

revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    configure_mappers()
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
