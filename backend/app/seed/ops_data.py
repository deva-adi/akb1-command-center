"""Tab 8 (Smart Ops) + Tab 9 (Risk & Audit) demo data.

Smart Ops: the 8 proactive-detection scenarios from ARCHITECTURE.md §11
(each scenario execution = one triggered alert). Resource pool provides
the bench ledger used by the Smart Ops narrative.

Risk & Audit: audit_log entries show representative admin and data
changes across the portfolio.
"""
from __future__ import annotations

from datetime import datetime
from typing import TypedDict


class ScenarioExecutionSeed(TypedDict):
    scenario_name: str
    execution_date: datetime
    triggered_by: str
    status: str
    details: str
    financial_impact: float
    outcome_notes: str | None


# ARCHITECTURE.md §11 Smart Ops scenarios:
# 1 Bench Tax rising, 2 Margin Cliff projected, 3 Scope Creep unbilled,
# 4 Rate Card Drift, 5 Attrition Wave, 6 SLA Breach pattern, 7 Customer
# Satisfaction Drift, 8 AI Trust Regression.
SCENARIO_EXECUTIONS: list[ScenarioExecutionSeed] = [
    {
        "scenario_name": "Bench Tax Rising",
        "execution_date": datetime(2026, 3, 31, 9, 15),
        "triggered_by": "Monthly batch",
        "status": "Active",
        "details": '{"program":"ORION","bench_fte":12,"shadow_cost":765000,"trend":"up"}',
        "financial_impact": 765_000,
        "outcome_notes": "Redeploy plan drafted; 4 FTE to Atlas in Q2",
    },
    {
        "scenario_name": "Margin Cliff Projected",
        "execution_date": datetime(2026, 3, 29, 11, 30),
        "triggered_by": "Forecast pipeline",
        "status": "Active",
        "details": '{"program":"ATLAS","breakeven_month":8,"confidence":0.78}',
        "financial_impact": 600_000,
        "outcome_notes": "CAB reviewing team mix rebalance",
    },
    {
        "scenario_name": "Scope Creep Unbilled",
        "execution_date": datetime(2026, 3, 20, 16, 0),
        "triggered_by": "CR log scan",
        "status": "Active",
        "details": '{"program":"PHOENIX","open_crs":3,"total_value":1200000}',
        "financial_impact": 1_200_000,
        "outcome_notes": "Repricing in flight",
    },
    {
        "scenario_name": "Rate Card Drift",
        "execution_date": datetime(2026, 3, 25, 14, 45),
        "triggered_by": "Rate card diff",
        "status": "Mitigating",
        "details": '{"program":"ORION","drift_pct":0.20,"tier":"Senior Architect"}',
        "financial_impact": 150_000,
        "outcome_notes": "Refresh scheduled with procurement",
    },
    {
        "scenario_name": "Attrition Wave",
        "execution_date": datetime(2026, 3, 15, 10, 0),
        "triggered_by": "HRIS feed",
        "status": "Active",
        "details": '{"program":"TITAN","rolling_12m_attrition":0.27,"threshold":0.15}',
        "financial_impact": 220_000,
        "outcome_notes": "Backfill + retention bonus approved",
    },
    {
        "scenario_name": "SLA Breach Pattern",
        "execution_date": datetime(2026, 3, 10, 18, 30),
        "triggered_by": "Incident ledger",
        "status": "Active",
        "details": '{"program":"TITAN","p1_breaches_90d":2,"penalty_ytd":400000}',
        "financial_impact": 400_000,
        "outcome_notes": "On-call roster refresh + runbook overhaul",
    },
    {
        "scenario_name": "Customer Satisfaction Drift",
        "execution_date": datetime(2026, 4, 1, 8, 0),
        "triggered_by": "Monthly survey",
        "status": "Monitoring",
        "details": '{"program":"ORION","csat_delta":-2.7,"nps_delta":-55}',
        "financial_impact": 0,
        "outcome_notes": "Voice-of-customer review set for next steering",
    },
    {
        "scenario_name": "AI Trust Regression",
        "execution_date": datetime(2026, 3, 30, 15, 15),
        "triggered_by": "Trust score batch",
        "status": "Active",
        "details": '{"program":"PHOENIX","composite_delta":-8,"failing_gates":["parity","rework"]}',
        "financial_impact": 0,
        "outcome_notes": "Model prompt refresh scheduled",
    },
]


class ResourcePoolSeed(TypedDict):
    name: str
    role: str
    role_tier: str
    skill_set: str
    current_program_code: str | None
    current_project_code: str | None
    utilization_pct: float
    bench_days: int
    loaded_cost_annual: float
    status: str


RESOURCE_POOL: list[ResourcePoolSeed] = [
    {"name": "Priya Sharma", "role": "Senior Engineer", "role_tier": "Senior", "skill_set": "Java, Spring, AWS", "current_program_code": "PHOENIX", "current_project_code": "PHOE-CBM", "utilization_pct": 82, "bench_days": 0, "loaded_cost_annual": 780_000, "status": "Active"},
    {"name": "Raj Kumar", "role": "Tech Lead", "role_tier": "Senior", "skill_set": "Kafka, Integration, Architecture", "current_program_code": "PHOENIX", "current_project_code": "PHOE-INT", "utilization_pct": 90, "bench_days": 0, "loaded_cost_annual": 920_000, "status": "Active"},
    {"name": "Meera Iyer", "role": "Data Engineer", "role_tier": "Senior", "skill_set": "Airflow, dbt, Snowflake", "current_program_code": "ORION", "current_project_code": "ORN-INGEST", "utilization_pct": 62, "bench_days": 35, "loaded_cost_annual": 840_000, "status": "Active"},
    {"name": "Suresh Menon", "role": "Engineering Manager", "role_tier": "Senior", "skill_set": "AI tooling, Delivery", "current_program_code": "SENTINEL", "current_project_code": "SNTL-AUTO", "utilization_pct": 95, "bench_days": 0, "loaded_cost_annual": 1_100_000, "status": "Active"},
    {"name": "Nisha Rao", "role": "SRE Lead", "role_tier": "Senior", "skill_set": "Kubernetes, SLOs, Incident Mgmt", "current_program_code": "TITAN", "current_project_code": "TTN-STORE", "utilization_pct": 88, "bench_days": 0, "loaded_cost_annual": 960_000, "status": "Active"},
    {"name": "Anand Verma", "role": "Mid Engineer", "role_tier": "Mid", "skill_set": "Python, Airflow, Data Modelling", "current_program_code": "ORION", "current_project_code": "ORN-INGEST", "utilization_pct": 55, "bench_days": 42, "loaded_cost_annual": 560_000, "status": "Active"},
    {"name": "Kavya Nair", "role": "Mid Engineer", "role_tier": "Mid", "skill_set": "React, GraphQL, Shopify", "current_program_code": "TITAN", "current_project_code": "TTN-STORE", "utilization_pct": 85, "bench_days": 0, "loaded_cost_annual": 620_000, "status": "Active"},
    {"name": "Divya Menon", "role": "QA Lead", "role_tier": "Senior", "skill_set": "Playwright, Python, Test Architecture", "current_program_code": "SENTINEL", "current_project_code": "SNTL-AUTO", "utilization_pct": 92, "bench_days": 0, "loaded_cost_annual": 780_000, "status": "Active"},
    {"name": "Vikram Rao", "role": "Junior Developer", "role_tier": "Junior", "skill_set": "Java, Spring Boot", "current_program_code": None, "current_project_code": None, "utilization_pct": 0, "bench_days": 28, "loaded_cost_annual": 420_000, "status": "Bench"},
    {"name": "Ananya Desai", "role": "Junior Developer", "role_tier": "Junior", "skill_set": "Python, Data", "current_program_code": None, "current_project_code": None, "utilization_pct": 0, "bench_days": 14, "loaded_cost_annual": 400_000, "status": "Bench"},
]


class AuditLogSeed(TypedDict):
    action: str
    table_name: str
    record_id: int
    old_value: str | None
    new_value: str | None
    user_action: str
    timestamp: datetime


AUDIT_LOG: list[AuditLogSeed] = [
    {"action": "UPDATE", "table_name": "programs", "record_id": 1, "old_value": '{"status":"Active"}', "new_value": '{"status":"At Risk"}', "user_action": "Status downgrade on integration vendor slip", "timestamp": datetime(2026, 3, 2, 10, 15)},
    {"action": "INSERT", "table_name": "scope_creep_log", "record_id": 1, "old_value": None, "new_value": '{"program":"PHOENIX","cr_value":375000}', "user_action": "CR logged by Priya Sharma", "timestamp": datetime(2026, 2, 15, 14, 10)},
    {"action": "UPDATE", "table_name": "customer_satisfaction", "record_id": 10, "old_value": '{"csat":7.2}', "new_value": '{"csat":6.7}', "user_action": "Monthly survey ingest", "timestamp": datetime(2026, 3, 31, 23, 30)},
    {"action": "INSERT", "table_name": "ai_override_log", "record_id": 3, "old_value": None, "new_value": '{"tool":"Claude for Devs","type":"Rejected suggestion"}', "user_action": "Override captured by Raj Kumar", "timestamp": datetime(2026, 3, 22, 16, 45)},
    {"action": "UPDATE", "table_name": "rate_cards", "record_id": 7, "old_value": '{"actual_rate":195}', "new_value": '{"actual_rate":210}', "user_action": "Quarterly rate refresh", "timestamp": datetime(2026, 3, 25, 11, 0)},
    {"action": "INSERT", "table_name": "sla_incidents", "record_id": 2, "old_value": None, "new_value": '{"incident":"INC-2026-0587","priority":"P1"}', "user_action": "PagerDuty → audit sink", "timestamp": datetime(2026, 3, 4, 19, 52)},
    {"action": "UPDATE", "table_name": "kpi_definitions", "record_id": 5, "old_value": '{"weight":1.5}', "new_value": '{"weight":1.8}', "user_action": "KPI Studio weight edit", "timestamp": datetime(2026, 3, 28, 9, 40)},
    {"action": "DELETE", "table_name": "change_requests", "record_id": 99, "old_value": '{"description":"Abandoned CR"}', "new_value": None, "user_action": "CAB rollback", "timestamp": datetime(2026, 3, 15, 12, 20)},
]
