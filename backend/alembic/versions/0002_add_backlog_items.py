"""add backlog_items table (story/task/bug/spike level data)

Revision ID: 0002_add_backlog_items
Revises: 0001_initial_schema
Create Date: 2026-04-21
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002_add_backlog_items"
down_revision: Union[str, None] = "0001_initial_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "backlog_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id"), nullable=True, index=True),
        sa.Column("sprint_number", sa.Integer(), nullable=True, index=True),
        sa.Column("item_type", sa.String(50), nullable=False, server_default="story"),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("story_points", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="planned"),
        sa.Column("assignee", sa.String(100), nullable=True),
        sa.Column("is_ai_assisted", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("defects_raised", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rework_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("priority", sa.String(20), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("backlog_items")
