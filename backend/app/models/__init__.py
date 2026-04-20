"""SQLAlchemy ORM models — 42 tables matching ARCHITECTURE.md §5."""

from app.models.ai import (
    AiCodeMetrics,
    AiGovernanceConfig,
    AiOverrideLog,
    AiSdlcMetrics,
    AiTool,
    AiToolAssignment,
    AiTrustScore,
    AiUsageMetrics,
)
from app.models.auth import User, UserRole
from app.models.base import Base
from app.models.core import (
    CommercialScenario,
    EvmSnapshot,
    Initiative,
    KpiDefinition,
    KpiSnapshot,
    Program,
    Project,
    Risk,
    RiskHistory,
    SprintData,
)
from app.models.financial import BenchTracking, LossExposure, ScopeCreepLog
from app.models.intelligence import (
    CustomerSatisfaction,
    KpiForecast,
    Milestone,
    NarrativeCache,
    RateCard,
    SlaIncident,
    UtilizationDetail,
)
from app.models.methodology import FlowMetrics, ProjectPhase
from app.models.smart_ops import ResourcePool, ScenarioExecution
from app.models.system import (
    AppSetting,
    AuditLog,
    CurrencyRate,
    DataImport,
    DataImportSnapshot,
    SchemaVersion,
)
from app.models.velocity import SprintVelocityBlendRule, SprintVelocityDual

__all__ = [
    "Base",
    # Core (10)
    "Program",
    "Project",
    "KpiDefinition",
    "KpiSnapshot",
    "Risk",
    "RiskHistory",
    "Initiative",
    "SprintData",
    "CommercialScenario",
    "EvmSnapshot",
    # Intelligence (7)
    "Milestone",
    "SlaIncident",
    "RateCard",
    "UtilizationDetail",
    "CustomerSatisfaction",
    "KpiForecast",
    "NarrativeCache",
    # AI (8)
    "AiTool",
    "AiToolAssignment",
    "AiUsageMetrics",
    "AiCodeMetrics",
    "AiSdlcMetrics",
    "AiTrustScore",
    "AiGovernanceConfig",
    "AiOverrideLog",
    # Smart Ops (2)
    "ResourcePool",
    "ScenarioExecution",
    # Financial (3)
    "BenchTracking",
    "ScopeCreepLog",
    "LossExposure",
    # Velocity (2)
    "SprintVelocityDual",
    "SprintVelocityBlendRule",
    # System (6)
    "DataImport",
    "AppSetting",
    "AuditLog",
    "CurrencyRate",
    "DataImportSnapshot",
    "SchemaVersion",
    # Methodology (2)
    "FlowMetrics",
    "ProjectPhase",
    # Auth (2)
    "User",
    "UserRole",
]

TABLE_COUNT = 42
