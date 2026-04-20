from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, LargeBinary, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class DataImport(Base):
    __tablename__ = "data_imports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    import_date: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
    source: Mapped[str | None] = mapped_column(String)
    file_name: Mapped[str | None] = mapped_column(String)
    rows_imported: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str | None] = mapped_column(String)
    column_mapping: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)


class AppSetting(Base):
    __tablename__ = "app_settings"

    key: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[str | None] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp()
    )


class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    action: Mapped[str | None] = mapped_column(String)
    table_name: Mapped[str | None] = mapped_column(String)
    record_id: Mapped[int | None] = mapped_column(Integer)
    old_value: Mapped[str | None] = mapped_column(Text)
    new_value: Mapped[str | None] = mapped_column(Text)
    user_action: Mapped[str | None] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )


class CurrencyRate(Base):
    __tablename__ = "currency_rates"

    code: Mapped[str] = mapped_column(String, primary_key=True)
    symbol: Mapped[str | None] = mapped_column(String)
    rate_to_base: Mapped[float] = mapped_column(Numeric(18, 8), nullable=False)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
    source: Mapped[str] = mapped_column(String, default="manual")


class DataImportSnapshot(Base):
    __tablename__ = "data_import_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    import_timestamp: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
    source_filename: Mapped[str | None] = mapped_column(String)
    source_format: Mapped[str | None] = mapped_column(String)
    row_count: Mapped[int | None] = mapped_column(Integer)
    affected_tables: Mapped[str | None] = mapped_column(Text)
    pre_import_state: Mapped[bytes | None] = mapped_column(LargeBinary)
    status: Mapped[str | None] = mapped_column(String)
    rollback_timestamp: Mapped[datetime | None] = mapped_column(DateTime)


class SchemaVersion(Base):
    __tablename__ = "schema_version"

    version: Mapped[str] = mapped_column(String, primary_key=True)
    applied_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
    applied_by: Mapped[str | None] = mapped_column(String)
