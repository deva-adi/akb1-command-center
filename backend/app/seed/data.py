"""NovaTech Solutions demo portfolio — 5 programmes × 12 months.

Per docs/DEMO_GUIDE.md the portfolio totals ₹41M revenue across 5
programmes. Figures below are month-over-month snapshots that power the
Executive Overview (Tab 1) and Data Hub (Tab 11) out-of-the-box.
"""
from __future__ import annotations

from datetime import date
from typing import TypedDict


class ProgrammeSeed(TypedDict):
    name: str
    code: str
    client: str
    start_date: date
    end_date: date
    status: str
    bac: float
    revenue: float
    team_size: int
    offshore_ratio: float
    delivery_model: str
    currency_code: str


PROGRAMMES: list[ProgrammeSeed] = [
    {
        "name": "Phoenix Platform Modernization",
        "code": "PHOENIX",
        "client": "GlobalBank Corp",
        "start_date": date(2025, 4, 1),
        "end_date": date(2027, 3, 31),
        "status": "At Risk",
        "bac": 10_000_000,
        "revenue": 10_000_000,
        "team_size": 25,
        "offshore_ratio": 0.65,
        "delivery_model": "T&M",
        "currency_code": "INR",
    },
    {
        "name": "Atlas Cloud Migration",
        "code": "ATLAS",
        "client": "GlobalBank Corp",
        "start_date": date(2025, 6, 1),
        "end_date": date(2026, 12, 31),
        "status": "Watch",
        "bac": 8_000_000,
        "revenue": 8_000_000,
        "team_size": 18,
        "offshore_ratio": 0.55,
        "delivery_model": "Fixed Price",
        "currency_code": "INR",
    },
    {
        "name": "Sentinel Quality Engineering",
        "code": "SENTINEL",
        "client": "GlobalBank Corp",
        "start_date": date(2025, 7, 1),
        "end_date": date(2026, 9, 30),
        "status": "On Track",
        "bac": 5_000_000,
        "revenue": 5_000_000,
        "team_size": 12,
        "offshore_ratio": 0.70,
        "delivery_model": "T&M",
        "currency_code": "INR",
    },
    {
        "name": "Orion Data Platform",
        "code": "ORION",
        "client": "GlobalBank Corp",
        "start_date": date(2025, 1, 15),
        "end_date": date(2027, 6, 30),
        "status": "At Risk",
        "bac": 12_000_000,
        "revenue": 12_000_000,
        "team_size": 30,
        "offshore_ratio": 0.60,
        "delivery_model": "Hybrid",
        "currency_code": "INR",
    },
    {
        "name": "Titan Digital Commerce",
        "code": "TITAN",
        "client": "GlobalBank Corp",
        "start_date": date(2025, 9, 1),
        "end_date": date(2026, 12, 31),
        "status": "At Risk",
        "bac": 6_000_000,
        "revenue": 6_000_000,
        "team_size": 15,
        "offshore_ratio": 0.50,
        "delivery_model": "Fixed Price + Managed Services",
        "currency_code": "INR",
    },
]


class ProjectSeed(TypedDict):
    program_code: str
    name: str
    code: str
    start_date: date
    end_date: date
    bac: float
    revenue: float
    team_size: int
    tech_stack: str
    is_ai_augmented: bool
    ai_augmentation_level: str | None
    delivery_methodology: str


PROJECTS: list[ProjectSeed] = [
    {
        "program_code": "PHOENIX",
        "name": "Core Banking Module",
        "code": "PHOE-CBM",
        "start_date": date(2025, 4, 15),
        "end_date": date(2026, 9, 30),
        "bac": 4_200_000,
        "revenue": 4_200_000,
        "team_size": 8,
        "tech_stack": "Java, Spring Boot, PostgreSQL, Kubernetes",
        "is_ai_augmented": False,
        "ai_augmentation_level": None,
        "delivery_methodology": "Scrum",
    },
    {
        "program_code": "PHOENIX",
        "name": "Integration Layer",
        "code": "PHOE-INT",
        "start_date": date(2025, 5, 1),
        "end_date": date(2026, 12, 31),
        "bac": 3_200_000,
        "revenue": 3_200_000,
        "team_size": 9,
        "tech_stack": "Kafka, Camel, OpenAPI",
        "is_ai_augmented": True,
        "ai_augmentation_level": "Light",
        "delivery_methodology": "Scrum",
    },
    {
        "program_code": "ATLAS",
        "name": "Lift & Shift Workstream",
        "code": "ATLS-LNS",
        "start_date": date(2025, 6, 15),
        "end_date": date(2026, 9, 30),
        "bac": 3_500_000,
        "revenue": 3_500_000,
        "team_size": 10,
        "tech_stack": "AWS, Terraform, Ansible",
        "is_ai_augmented": True,
        "ai_augmentation_level": "Medium",
        "delivery_methodology": "Kanban",
    },
    {
        "program_code": "SENTINEL",
        "name": "Automation Platform",
        "code": "SNTL-AUTO",
        "start_date": date(2025, 7, 15),
        "end_date": date(2026, 6, 30),
        "bac": 2_800_000,
        "revenue": 2_800_000,
        "team_size": 7,
        "tech_stack": "Playwright, Python, GitHub Actions",
        "is_ai_augmented": True,
        "ai_augmentation_level": "Heavy",
        "delivery_methodology": "Scrum",
    },
    {
        "program_code": "ORION",
        "name": "Ingestion Pipeline",
        "code": "ORN-INGEST",
        "start_date": date(2025, 2, 1),
        "end_date": date(2026, 10, 31),
        "bac": 5_500_000,
        "revenue": 5_500_000,
        "team_size": 14,
        "tech_stack": "Airflow, Snowflake, dbt",
        "is_ai_augmented": False,
        "ai_augmentation_level": None,
        "delivery_methodology": "Kanban",
    },
    {
        "program_code": "TITAN",
        "name": "Storefront Rebuild",
        "code": "TTN-STORE",
        "start_date": date(2025, 9, 15),
        "end_date": date(2026, 9, 30),
        "bac": 3_200_000,
        "revenue": 3_200_000,
        "team_size": 9,
        "tech_stack": "Next.js, GraphQL, Shopify",
        "is_ai_augmented": True,
        "ai_augmentation_level": "Medium",
        "delivery_methodology": "Waterfall",
    },
]


class KpiDefinitionSeed(TypedDict):
    name: str
    code: str
    formula: str
    description: str
    unit: str
    green_threshold: float
    amber_threshold: float
    red_threshold: float
    weight: float
    category: str
    is_higher_better: bool


KPI_DEFINITIONS: list[KpiDefinitionSeed] = [
    {
        "name": "Cost Performance Index",
        "code": "CPI",
        "formula": "EV / AC",
        "description": "Earned Value / Actual Cost",
        "unit": "ratio",
        "green_threshold": 1.00,
        "amber_threshold": 0.90,
        "red_threshold": 0.80,
        "weight": 1.2,
        "category": "Delivery",
        "is_higher_better": True,
    },
    {
        "name": "Schedule Performance Index",
        "code": "SPI",
        "formula": "EV / PV",
        "description": "Earned Value / Planned Value",
        "unit": "ratio",
        "green_threshold": 1.00,
        "amber_threshold": 0.90,
        "red_threshold": 0.80,
        "weight": 1.2,
        "category": "Delivery",
        "is_higher_better": True,
    },
    {
        "name": "On-Time Delivery Rate",
        "code": "OTD",
        "formula": "on_time_items / total_items",
        "description": "Milestones completed on or before planned date",
        "unit": "pct",
        "green_threshold": 0.95,
        "amber_threshold": 0.85,
        "red_threshold": 0.75,
        "weight": 1.0,
        "category": "Delivery",
        "is_higher_better": True,
    },
    {
        "name": "Defect Density",
        "code": "DEFECT_DENSITY",
        "formula": "defects / kloc",
        "description": "Defects per thousand lines of code",
        "unit": "defects/kloc",
        "green_threshold": 1.00,
        "amber_threshold": 2.50,
        "red_threshold": 4.00,
        "weight": 1.0,
        "category": "Quality",
        "is_higher_better": False,
    },
    {
        "name": "Blended Portfolio Margin",
        "code": "MARGIN",
        "formula": "(revenue - cost) / revenue",
        "description": "Portfolio blended gross margin",
        "unit": "pct",
        "green_threshold": 0.22,
        "amber_threshold": 0.15,
        "red_threshold": 0.08,
        "weight": 1.5,
        "category": "Commercial",
        "is_higher_better": True,
    },
    {
        "name": "Utilization",
        "code": "UTIL",
        "formula": "billable_hours / available_hours",
        "description": "Billable hours against available capacity",
        "unit": "pct",
        "green_threshold": 0.85,
        "amber_threshold": 0.75,
        "red_threshold": 0.65,
        "weight": 1.0,
        "category": "People",
        "is_higher_better": True,
    },
]


# Monthly KPI snapshot series keyed (programme_code, kpi_code) → 12 values
# Month index 0 = FY start (Apr 2025), index 11 = Mar 2026.
MONTHLY_KPI_VALUES: dict[tuple[str, str], list[float]] = {
    ("PHOENIX", "CPI"): [1.02, 1.00, 0.98, 0.96, 0.94, 0.92, 0.90, 0.89, 0.88, 0.87, 0.87, 0.87],
    ("PHOENIX", "SPI"): [1.00, 0.98, 0.97, 0.95, 0.93, 0.92, 0.90, 0.88, 0.86, 0.85, 0.85, 0.84],
    ("PHOENIX", "MARGIN"): [0.18, 0.17, 0.16, 0.15, 0.14, 0.13, 0.12, 0.11, 0.11, 0.10, 0.10, 0.09],
    ("ATLAS", "CPI"): [1.05, 1.04, 1.02, 1.00, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91],
    ("ATLAS", "SPI"): [1.00, 1.00, 0.99, 0.98, 0.97, 0.96, 0.95, 0.95, 0.94, 0.93, 0.92, 0.91],
    ("ATLAS", "MARGIN"): [0.20, 0.19, 0.18, 0.17, 0.16, 0.15, 0.15, 0.14, 0.14, 0.13, 0.13, 0.12],
    ("SENTINEL", "CPI"): [1.08, 1.09, 1.10, 1.11, 1.12, 1.12, 1.13, 1.14, 1.14, 1.15, 1.15, 1.16],
    ("SENTINEL", "SPI"): [1.01, 1.02, 1.02, 1.03, 1.04, 1.05, 1.05, 1.06, 1.06, 1.07, 1.07, 1.07],
    ("SENTINEL", "MARGIN"): [0.21, 0.21, 0.22, 0.22, 0.22, 0.22, 0.23, 0.23, 0.23, 0.23, 0.23, 0.24],
    ("ORION", "CPI"): [0.98, 0.96, 0.94, 0.92, 0.90, 0.88, 0.86, 0.85, 0.84, 0.83, 0.82, 0.81],
    ("ORION", "SPI"): [1.00, 0.99, 0.97, 0.95, 0.93, 0.91, 0.89, 0.88, 0.86, 0.85, 0.84, 0.83],
    ("ORION", "MARGIN"): [0.16, 0.15, 0.14, 0.13, 0.12, 0.11, 0.10, 0.09, 0.08, 0.07, 0.07, 0.06],
    ("TITAN", "CPI"): [1.04, 1.02, 1.00, 0.98, 0.97, 0.95, 0.94, 0.92, 0.91, 0.90, 0.89, 0.88],
    ("TITAN", "SPI"): [1.00, 0.99, 0.98, 0.96, 0.95, 0.93, 0.92, 0.91, 0.90, 0.88, 0.87, 0.86],
    ("TITAN", "MARGIN"): [0.19, 0.18, 0.18, 0.17, 0.17, 0.16, 0.16, 0.15, 0.15, 0.14, 0.14, 0.13],
}


MONTH_STARTS: list[date] = [
    date(2025, 4, 1),
    date(2025, 5, 1),
    date(2025, 6, 1),
    date(2025, 7, 1),
    date(2025, 8, 1),
    date(2025, 9, 1),
    date(2025, 10, 1),
    date(2025, 11, 1),
    date(2025, 12, 1),
    date(2026, 1, 1),
    date(2026, 2, 1),
    date(2026, 3, 1),
]


class RiskSeed(TypedDict):
    program_code: str
    title: str
    description: str
    category: str
    probability: float
    impact: float
    severity: str
    status: str
    owner: str
    mitigation_plan: str


RISKS: list[RiskSeed] = [
    {
        "program_code": "PHOENIX",
        "title": "Integration vendor delivery slip",
        "description": "Third-party API delivery slipping 2 weeks; impacts go-live",
        "category": "External",
        "probability": 0.70,
        "impact": 500_000,
        "severity": "High",
        "status": "Open",
        "owner": "Raj Kumar",
        "mitigation_plan": "Backup vendor identified; contract penalty invoked",
    },
    {
        "program_code": "PHOENIX",
        "title": "Uncontrolled scope creep",
        "description": "3 change requests totalling ₹1.2M without margin uplift",
        "category": "Scope",
        "probability": 0.80,
        "impact": 1_200_000,
        "severity": "High",
        "status": "Open",
        "owner": "Priya Sharma",
        "mitigation_plan": "CAB freeze; repricing underway",
    },
    {
        "program_code": "ORION",
        "title": "Bench tax erosion",
        "description": "12 FTE on bench rotation charging to programme; 7% margin erosion",
        "category": "Resource",
        "probability": 0.90,
        "impact": 765_000,
        "severity": "High",
        "status": "Open",
        "owner": "Meera Iyer",
        "mitigation_plan": "Redeployment to Atlas workstream in Q2",
    },
    {
        "program_code": "TITAN",
        "title": "P1 SLA breaches",
        "description": "2 P1 breaches in the last quarter; CSAT dropped to 6.8",
        "category": "Operations",
        "probability": 0.60,
        "impact": 400_000,
        "severity": "Medium",
        "status": "Open",
        "owner": "Nisha Rao",
        "mitigation_plan": "Runbook automation; on-call roster refresh",
    },
    {
        "program_code": "ATLAS",
        "title": "Margin cliff in Month 8",
        "description": "Forecast breakeven in Month 8 if bench allocation continues",
        "category": "Commercial",
        "probability": 0.50,
        "impact": 600_000,
        "severity": "Medium",
        "status": "Open",
        "owner": "Suresh Menon",
        "mitigation_plan": "Rebalance team mix; negotiate scope re-set",
    },
]


APP_SETTINGS_DEFAULTS: dict[str, str] = {
    "base_currency": "INR",
    "fiscal_year_start_month": "4",
    "locale": "en-IN",
    "org_name": "NovaTech Solutions",
    "industry_preset": "IT Services",
    "demo_mode": "true",
}


CURRENCY_RATES: list[tuple[str, str, float]] = [
    ("INR", "₹", 1.0),
    ("USD", "$", 83.5),
    ("GBP", "£", 105.2),
    ("EUR", "€", 89.7),
]


class CustomerExpectationSeed(TypedDict):
    program_code: str
    snapshot_date: date
    dimension: str
    expected_score: float
    delivered_score: float
    weight: float
    evidence_source: str
    owner: str
    notes: str


# Tab 10 §4.10 Expectation Framework — 7 dimensions × the most-exposed programmes.
# Gaps are computed at seed time (delivered - expected).
CUSTOMER_EXPECTATIONS: list[CustomerExpectationSeed] = [
    {
        "program_code": "PHOENIX",
        "snapshot_date": date(2026, 3, 31),
        "dimension": "timeline",
        "expected_score": 9.0,
        "delivered_score": 6.5,
        "weight": 1.2,
        "evidence_source": "Quarterly survey",
        "owner": "Priya Sharma",
        "notes": "Integration vendor slip cascades into go-live",
    },
    {
        "program_code": "PHOENIX",
        "snapshot_date": date(2026, 3, 31),
        "dimension": "cost",
        "expected_score": 8.5,
        "delivered_score": 6.0,
        "weight": 1.1,
        "evidence_source": "Steering committee",
        "owner": "Raj Kumar",
        "notes": "Scope creep consuming margin reserve",
    },
    {
        "program_code": "ORION",
        "snapshot_date": date(2026, 3, 31),
        "dimension": "quality",
        "expected_score": 8.0,
        "delivered_score": 6.8,
        "weight": 1.0,
        "evidence_source": "Escalation",
        "owner": "Meera Iyer",
        "notes": "Pipeline defect density 1.4× baseline",
    },
    {
        "program_code": "ORION",
        "snapshot_date": date(2026, 3, 31),
        "dimension": "stability",
        "expected_score": 8.0,
        "delivered_score": 5.5,
        "weight": 0.9,
        "evidence_source": "Manual",
        "owner": "Meera Iyer",
        "notes": "Bench rotation churning knowledge",
    },
    {
        "program_code": "TITAN",
        "snapshot_date": date(2026, 3, 31),
        "dimension": "responsiveness",
        "expected_score": 9.0,
        "delivered_score": 5.0,
        "weight": 1.1,
        "evidence_source": "Escalation",
        "owner": "Nisha Rao",
        "notes": "Two P1 SLA breaches last quarter",
    },
    {
        "program_code": "SENTINEL",
        "snapshot_date": date(2026, 3, 31),
        "dimension": "innovation",
        "expected_score": 7.5,
        "delivered_score": 9.0,
        "weight": 0.8,
        "evidence_source": "Quarterly survey",
        "owner": "Suresh Menon",
        "notes": "AI augmentation delivering above plan",
    },
    {
        "program_code": "ATLAS",
        "snapshot_date": date(2026, 3, 31),
        "dimension": "communication",
        "expected_score": 8.0,
        "delivered_score": 7.5,
        "weight": 1.0,
        "evidence_source": "Steering committee",
        "owner": "Suresh Menon",
        "notes": "Steering cadence held; minor delay in action-item closure",
    },
]


class CustomerActionSeed(TypedDict):
    program_code: str
    meeting_date: date
    description: str
    owner: str
    due_date: date
    status: str
    priority: str
    escalated: bool


CUSTOMER_ACTIONS: list[CustomerActionSeed] = [
    {
        "program_code": "PHOENIX",
        "meeting_date": date(2026, 3, 15),
        "description": "Reprice the 3 open change requests and re-present to CAB",
        "owner": "Priya Sharma",
        "due_date": date(2026, 4, 5),
        "status": "In Progress",
        "priority": "P1",
        "escalated": True,
    },
    {
        "program_code": "PHOENIX",
        "meeting_date": date(2026, 3, 15),
        "description": "Evaluate backup integration vendor within 2 weeks",
        "owner": "Raj Kumar",
        "due_date": date(2026, 3, 29),
        "status": "Open",
        "priority": "P1",
        "escalated": False,
    },
    {
        "program_code": "ORION",
        "meeting_date": date(2026, 3, 20),
        "description": "Redeploy 4 bench FTEs to Atlas workstream by end of Q1",
        "owner": "Meera Iyer",
        "due_date": date(2026, 3, 31),
        "status": "Open",
        "priority": "P1",
        "escalated": True,
    },
    {
        "program_code": "TITAN",
        "meeting_date": date(2026, 3, 10),
        "description": "Publish updated P1 SLA runbook and on-call roster",
        "owner": "Nisha Rao",
        "due_date": date(2026, 3, 22),
        "status": "Closed",
        "priority": "P2",
        "escalated": False,
    },
    {
        "program_code": "ATLAS",
        "meeting_date": date(2026, 3, 25),
        "description": "Rebalance team mix: +2 Senior, -2 Junior",
        "owner": "Suresh Menon",
        "due_date": date(2026, 4, 15),
        "status": "Open",
        "priority": "P2",
        "escalated": False,
    },
    {
        "program_code": "SENTINEL",
        "meeting_date": date(2026, 3, 5),
        "description": "Present AI augmentation case study at next QBR",
        "owner": "Suresh Menon",
        "due_date": date(2026, 4, 30),
        "status": "Open",
        "priority": "P3",
        "escalated": False,
    },
]
