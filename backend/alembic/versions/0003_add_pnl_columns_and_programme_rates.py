"""add pnl billing and cash columns on commercial_scenarios, plus programme_rates table

Revision ID: 0003_add_pnl_columns_and_programme_rates
Revises: 0002_add_backlog_items
Create Date: 2026-04-22

Tab 12 P&L Cockpit (v5.7.0) needs two schema additions:
  1. Five nullable columns on commercial_scenarios for the billing and cash
     picture: billed_revenue, collected_revenue, unbilled_wip, ar_balance,
     billing_ratio. Values are derived deterministically from actual_revenue
     in the seed (M2) via programme-specific ratios.
  2. A new programme_rates table for the per-programme, per-tier, per-month
     rate snapshot that feeds pyramid economics and the Price and Mix drivers
     of the margin bridge.

All additions are backwards compatible. The five new columns are nullable so
existing rows stay valid without data migration. The new table is independent
of existing foreign keys.
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0003_add_pnl_columns_and_programme_rates"
down_revision: Union[str, None] = "0002_add_backlog_items"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Five additive nullable columns on commercial_scenarios (Tab 12 KPI Board).
    op.add_column("commercial_scenarios", sa.Column("billed_revenue", sa.Float(), nullable=True))
    op.add_column("commercial_scenarios", sa.Column("collected_revenue", sa.Float(), nullable=True))
    op.add_column("commercial_scenarios", sa.Column("unbilled_wip", sa.Float(), nullable=True))
    op.add_column("commercial_scenarios", sa.Column("ar_balance", sa.Float(), nullable=True))
    op.add_column("commercial_scenarios", sa.Column("billing_ratio", sa.Float(), nullable=True))

    # programme_rates table (Tab 12 pyramid economics and margin bridge).
    op.create_table(
        "programme_rates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("program_code", sa.String(50), nullable=False, index=True),
        sa.Column("snapshot_date", sa.Date(), nullable=False, index=True),
        sa.Column("role_tier", sa.String(20), nullable=False),
        sa.Column("planned_rate", sa.Float(), nullable=False),
        sa.Column("actual_rate", sa.Float(), nullable=True),
        sa.Column("planned_headcount", sa.Integer(), nullable=True),
        sa.Column("actual_headcount", sa.Integer(), nullable=True),
        sa.Column("tier_weight_planned", sa.Float(), nullable=True),
        sa.Column("tier_weight_actual", sa.Float(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("programme_rates")
    op.drop_column("commercial_scenarios", "billing_ratio")
    op.drop_column("commercial_scenarios", "ar_balance")
    op.drop_column("commercial_scenarios", "unbilled_wip")
    op.drop_column("commercial_scenarios", "collected_revenue")
    op.drop_column("commercial_scenarios", "billed_revenue")
