"""Velocity & Flow + Margin & EVM demo data for Tab 4 and Tab 5.

Dual velocity, blend rules, commercial scenarios (4-layer margin), loss
exposure across 7 categories, rate cards per role tier, scope-creep log.
All amounts are in each programme's native currency (INR for NovaTech).
"""
from __future__ import annotations

from datetime import date, timedelta
from typing import TypedDict


def _weeks(n: int) -> timedelta:
    return timedelta(weeks=n)


# ---------------------------------------------------------------------------
# Dual velocity (AI-augmented projects, per sprint)
# ---------------------------------------------------------------------------


class SprintVelocityDualSeed(TypedDict):
    project_code: str
    sprint_number: int
    standard_velocity: float
    ai_raw_velocity: float
    ai_rework_points: float
    ai_quality_adjusted_velocity: float
    combined_velocity: float
    merge_eligible: bool
    quality_parity_ratio: float
    snapshot_date: date


SPRINT_VELOCITY_DUAL: list[SprintVelocityDualSeed] = [
    # SNTL-AUTO — heavy AI, trust rising
    *(
        {
            "project_code": "SNTL-AUTO",
            "sprint_number": 12 + i,
            "standard_velocity": [74, 78, 82, 85, 88, 92][i],
            "ai_raw_velocity": [32, 36, 40, 44, 48, 52][i],
            "ai_rework_points": [3.0, 2.5, 2.0, 1.5, 1.0, 0.8][i],
            "ai_quality_adjusted_velocity": [
                32 - 3.0,
                36 - 2.5,
                40 - 2.0,
                44 - 1.5,
                48 - 1.0,
                52 - 0.8,
            ][i],
            "combined_velocity": [
                74 + (32 - 3.0),
                78 + (36 - 2.5),
                82 + (40 - 2.0),
                85 + (44 - 1.5),
                88 + (48 - 1.0),
                92 + (52 - 0.8),
            ][i],
            "merge_eligible": True,
            "quality_parity_ratio": [0.91, 0.93, 0.95, 0.97, 0.98, 0.98][i],
            "snapshot_date": date(2026, 1, 25) + _weeks(i * 2),
        }
        for i in range(6)
    ),
    # PHOE-INT — light AI, merge gate on/off depending on quality parity
    *(
        {
            "project_code": "PHOE-INT",
            "sprint_number": 14 + i,
            "standard_velocity": [95, 97, 94, 98, 96, 99][i],
            "ai_raw_velocity": [18, 22, 25, 28, 30, 32][i],
            "ai_rework_points": [4.0, 3.5, 3.0, 2.5, 2.0, 1.8][i],
            "ai_quality_adjusted_velocity": [
                18 - 4.0,
                22 - 3.5,
                25 - 3.0,
                28 - 2.5,
                30 - 2.0,
                32 - 1.8,
            ][i],
            "combined_velocity": [
                95 + (18 - 4.0),
                97 + (22 - 3.5),
                94 + (25 - 3.0),
                98 + (28 - 2.5),
                96 + (30 - 2.0),
                99 + (32 - 1.8),
            ][i],
            "merge_eligible": [False, False, True, True, True, True][i],
            "quality_parity_ratio": [0.78, 0.82, 0.86, 0.89, 0.92, 0.94][i],
            "snapshot_date": date(2026, 1, 25) + _weeks(i * 2),
        }
        for i in range(6)
    ),
]


# ---------------------------------------------------------------------------
# Blend rule gates (per programme)
# ---------------------------------------------------------------------------


class BlendRuleSeed(TypedDict):
    program_code: str
    gate_name: str
    gate_condition: str
    current_value: float
    threshold: float
    passed: bool
    last_evaluated: date


BLEND_RULES: list[BlendRuleSeed] = [
    {
        "program_code": "SENTINEL",
        "gate_name": "Quality parity",
        "gate_condition": "parity_ratio >= 0.95",
        "current_value": 0.98,
        "threshold": 0.95,
        "passed": True,
        "last_evaluated": date(2026, 4, 5),
    },
    {
        "program_code": "SENTINEL",
        "gate_name": "Rework ceiling",
        "gate_condition": "ai_rework / ai_raw <= 0.05",
        "current_value": 0.015,
        "threshold": 0.05,
        "passed": True,
        "last_evaluated": date(2026, 4, 5),
    },
    {
        "program_code": "SENTINEL",
        "gate_name": "Override rate",
        "gate_condition": "override_pct <= 15",
        "current_value": 8.0,
        "threshold": 15.0,
        "passed": True,
        "last_evaluated": date(2026, 4, 5),
    },
    {
        "program_code": "PHOENIX",
        "gate_name": "Quality parity",
        "gate_condition": "parity_ratio >= 0.95",
        "current_value": 0.94,
        "threshold": 0.95,
        "passed": False,
        "last_evaluated": date(2026, 4, 5),
    },
    {
        "program_code": "PHOENIX",
        "gate_name": "Rework ceiling",
        "gate_condition": "ai_rework / ai_raw <= 0.05",
        "current_value": 0.056,
        "threshold": 0.05,
        "passed": False,
        "last_evaluated": date(2026, 4, 5),
    },
    {
        "program_code": "ATLAS",
        "gate_name": "Quality parity",
        "gate_condition": "parity_ratio >= 0.95",
        "current_value": 0.92,
        "threshold": 0.95,
        "passed": False,
        "last_evaluated": date(2026, 4, 5),
    },
    {
        "program_code": "ATLAS",
        "gate_name": "Override rate",
        "gate_condition": "override_pct <= 15",
        "current_value": 18.0,
        "threshold": 15.0,
        "passed": False,
        "last_evaluated": date(2026, 4, 5),
    },
]


# ---------------------------------------------------------------------------
# Commercial scenarios — monthly 4-layer margin per programme
# ---------------------------------------------------------------------------


class CommercialSeed(TypedDict):
    program_code: str
    scenario_name: str
    planned_revenue: float
    actual_revenue: float
    planned_cost: float
    actual_cost: float
    gross_margin_pct: float
    contribution_margin_pct: float
    portfolio_margin_pct: float
    net_margin_pct: float
    snapshot_date: date
    notes: str | None


def _commercial_series(
    program_code: str,
    base_revenue: float,
    base_cost: float,
    *,
    margins_trend: list[tuple[float, float, float, float]],
) -> list[CommercialSeed]:
    months = [
        date(2025, 4, 1),
        date(2025, 7, 1),
        date(2025, 10, 1),
        date(2026, 1, 1),
    ]
    return [
        {
            "program_code": program_code,
            "scenario_name": "Quarterly Actuals",
            "planned_revenue": base_revenue * (1 + 0.02 * i),
            "actual_revenue": base_revenue * (1 + 0.02 * i) * (0.98 + 0.005 * i),
            "planned_cost": base_cost * (1 + 0.02 * i),
            "actual_cost": base_cost * (1 + 0.02 * i) * (1.02 + 0.01 * i),
            "gross_margin_pct": margins_trend[i][0],
            "contribution_margin_pct": margins_trend[i][1],
            "portfolio_margin_pct": margins_trend[i][2],
            "net_margin_pct": margins_trend[i][3],
            "snapshot_date": months[i],
            "notes": None,
        }
        for i in range(4)
    ]


COMMERCIAL_SCENARIOS: list[CommercialSeed] = [
    *_commercial_series(
        "PHOENIX",
        850_000,
        620_000,
        margins_trend=[(0.27, 0.13, 0.09, 0.04), (0.25, 0.12, 0.08, 0.03), (0.22, 0.10, 0.07, 0.02), (0.18, 0.08, 0.05, 0.01)],
    ),
    *_commercial_series(
        "ATLAS",
        680_000,
        520_000,
        margins_trend=[(0.24, 0.14, 0.10, 0.06), (0.22, 0.12, 0.09, 0.05), (0.20, 0.11, 0.08, 0.04), (0.17, 0.09, 0.06, 0.03)],
    ),
    *_commercial_series(
        "SENTINEL",
        420_000,
        310_000,
        margins_trend=[(0.28, 0.18, 0.14, 0.08), (0.30, 0.19, 0.15, 0.09), (0.31, 0.20, 0.16, 0.10), (0.32, 0.21, 0.17, 0.11)],
    ),
    *_commercial_series(
        "ORION",
        1_000_000,
        780_000,
        margins_trend=[(0.22, 0.10, 0.06, 0.02), (0.19, 0.08, 0.04, 0.01), (0.15, 0.06, 0.03, 0.00), (0.10, 0.03, 0.01, -0.02)],
    ),
    *_commercial_series(
        "TITAN",
        500_000,
        380_000,
        margins_trend=[(0.25, 0.14, 0.10, 0.05), (0.22, 0.12, 0.08, 0.04), (0.19, 0.10, 0.07, 0.03), (0.17, 0.08, 0.05, 0.02)],
    ),
]


# ---------------------------------------------------------------------------
# Loss exposure — 7 categories per programme (per ARCHITECTURE.md §6)
# ---------------------------------------------------------------------------


class LossSeed(TypedDict):
    program_code: str
    snapshot_date: date
    loss_category: str
    amount: float
    percentage_of_revenue: float
    detection_method: str
    mitigation_status: str
    notes: str | None


_LOSS_CATEGORIES = [
    "Bench Tax",
    "Scope Creep",
    "Rework & Defect Leakage",
    "Estimation Miss",
    "Attrition & Knowledge Loss",
    "Rate Card Drift",
    "SLA / Penalty Exposure",
]


LOSS_EXPOSURE: list[LossSeed] = [
    # Phoenix — scope-creep driven
    {"program_code": "PHOENIX", "snapshot_date": date(2026, 3, 31), "loss_category": "Scope Creep", "amount": 1_200_000, "percentage_of_revenue": 12.0, "detection_method": "CR log vs margin impact", "mitigation_status": "In Progress", "notes": "3 CRs uncaptured"},
    {"program_code": "PHOENIX", "snapshot_date": date(2026, 3, 31), "loss_category": "Rework & Defect Leakage", "amount": 420_000, "percentage_of_revenue": 4.2, "detection_method": "Sprint rework hrs", "mitigation_status": "Monitoring", "notes": None},
    {"program_code": "PHOENIX", "snapshot_date": date(2026, 3, 31), "loss_category": "Bench Tax", "amount": 180_000, "percentage_of_revenue": 1.8, "detection_method": "Shadow allocation", "mitigation_status": "Mitigated", "notes": None},
    {"program_code": "PHOENIX", "snapshot_date": date(2026, 3, 31), "loss_category": "Estimation Miss", "amount": 150_000, "percentage_of_revenue": 1.5, "detection_method": "Plan vs actual", "mitigation_status": "Monitoring", "notes": None},
    # Orion — bench-tax driven
    {"program_code": "ORION", "snapshot_date": date(2026, 3, 31), "loss_category": "Bench Tax", "amount": 765_000, "percentage_of_revenue": 6.4, "detection_method": "Shadow allocation", "mitigation_status": "In Progress", "notes": "12 FTE bench rotation"},
    {"program_code": "ORION", "snapshot_date": date(2026, 3, 31), "loss_category": "Attrition & Knowledge Loss", "amount": 220_000, "percentage_of_revenue": 1.8, "detection_method": "Attrition KPI", "mitigation_status": "Open", "notes": None},
    {"program_code": "ORION", "snapshot_date": date(2026, 3, 31), "loss_category": "Rate Card Drift", "amount": 150_000, "percentage_of_revenue": 1.3, "detection_method": "Rate card diff", "mitigation_status": "Monitoring", "notes": None},
    {"program_code": "ORION", "snapshot_date": date(2026, 3, 31), "loss_category": "Rework & Defect Leakage", "amount": 310_000, "percentage_of_revenue": 2.6, "detection_method": "Defect density", "mitigation_status": "Monitoring", "notes": None},
    # Titan — SLA penalty exposure
    {"program_code": "TITAN", "snapshot_date": date(2026, 3, 31), "loss_category": "SLA / Penalty Exposure", "amount": 400_000, "percentage_of_revenue": 6.7, "detection_method": "SLA incidents ledger", "mitigation_status": "Open", "notes": "2 P1 breaches"},
    {"program_code": "TITAN", "snapshot_date": date(2026, 3, 31), "loss_category": "Attrition & Knowledge Loss", "amount": 120_000, "percentage_of_revenue": 2.0, "detection_method": "Attrition KPI", "mitigation_status": "Monitoring", "notes": None},
    # Atlas — rate card drift
    {"program_code": "ATLAS", "snapshot_date": date(2026, 3, 31), "loss_category": "Rate Card Drift", "amount": 280_000, "percentage_of_revenue": 3.5, "detection_method": "Rate card diff", "mitigation_status": "In Progress", "notes": None},
    {"program_code": "ATLAS", "snapshot_date": date(2026, 3, 31), "loss_category": "Bench Tax", "amount": 200_000, "percentage_of_revenue": 2.5, "detection_method": "Shadow allocation", "mitigation_status": "Monitoring", "notes": None},
    # Sentinel — cleanest profile
    {"program_code": "SENTINEL", "snapshot_date": date(2026, 3, 31), "loss_category": "Rework & Defect Leakage", "amount": 40_000, "percentage_of_revenue": 0.8, "detection_method": "Defect density", "mitigation_status": "Mitigated", "notes": None},
]


# ---------------------------------------------------------------------------
# Rate cards (planned vs actual per role tier)
# ---------------------------------------------------------------------------


class RateCardSeed(TypedDict):
    program_code: str
    role_tier: str
    planned_rate: float
    actual_rate: float
    planned_headcount: int
    actual_headcount: int
    snapshot_date: date
    notes: str | None


RATE_CARDS: list[RateCardSeed] = [
    # Phoenix
    {"program_code": "PHOENIX", "role_tier": "Senior Architect", "planned_rate": 180.0, "actual_rate": 175.0, "planned_headcount": 3, "actual_headcount": 4, "snapshot_date": date(2026, 3, 31), "notes": "Extra architect on integration workstream"},
    {"program_code": "PHOENIX", "role_tier": "Mid Engineer", "planned_rate": 110.0, "actual_rate": 118.0, "planned_headcount": 15, "actual_headcount": 14, "snapshot_date": date(2026, 3, 31), "notes": "Upward drift"},
    {"program_code": "PHOENIX", "role_tier": "Junior Developer", "planned_rate": 70.0, "actual_rate": 72.0, "planned_headcount": 7, "actual_headcount": 7, "snapshot_date": date(2026, 3, 31), "notes": None},
    # Atlas
    {"program_code": "ATLAS", "role_tier": "Senior Architect", "planned_rate": 170.0, "actual_rate": 195.0, "planned_headcount": 2, "actual_headcount": 2, "snapshot_date": date(2026, 3, 31), "notes": "Cloud expertise premium"},
    {"program_code": "ATLAS", "role_tier": "Mid Engineer", "planned_rate": 100.0, "actual_rate": 115.0, "planned_headcount": 10, "actual_headcount": 11, "snapshot_date": date(2026, 3, 31), "notes": "Rate card drift"},
    {"program_code": "ATLAS", "role_tier": "Junior Developer", "planned_rate": 65.0, "actual_rate": 68.0, "planned_headcount": 6, "actual_headcount": 5, "snapshot_date": date(2026, 3, 31), "notes": None},
    # Orion — worst drift
    {"program_code": "ORION", "role_tier": "Senior Architect", "planned_rate": 175.0, "actual_rate": 210.0, "planned_headcount": 4, "actual_headcount": 5, "snapshot_date": date(2026, 3, 31), "notes": "20% drift"},
    {"program_code": "ORION", "role_tier": "Mid Engineer", "planned_rate": 105.0, "actual_rate": 122.0, "planned_headcount": 18, "actual_headcount": 20, "snapshot_date": date(2026, 3, 31), "notes": "Bench rotation adds cost"},
    {"program_code": "ORION", "role_tier": "Junior Developer", "planned_rate": 68.0, "actual_rate": 70.0, "planned_headcount": 8, "actual_headcount": 9, "snapshot_date": date(2026, 3, 31), "notes": None},
    # Sentinel — clean
    {"program_code": "SENTINEL", "role_tier": "Senior Architect", "planned_rate": 185.0, "actual_rate": 182.0, "planned_headcount": 2, "actual_headcount": 2, "snapshot_date": date(2026, 3, 31), "notes": "Within tolerance"},
    {"program_code": "SENTINEL", "role_tier": "Mid Engineer", "planned_rate": 115.0, "actual_rate": 116.0, "planned_headcount": 8, "actual_headcount": 8, "snapshot_date": date(2026, 3, 31), "notes": None},
    {"program_code": "SENTINEL", "role_tier": "Junior Developer", "planned_rate": 72.0, "actual_rate": 71.0, "planned_headcount": 2, "actual_headcount": 2, "snapshot_date": date(2026, 3, 31), "notes": None},
    # Titan
    {"program_code": "TITAN", "role_tier": "Senior Architect", "planned_rate": 175.0, "actual_rate": 180.0, "planned_headcount": 2, "actual_headcount": 2, "snapshot_date": date(2026, 3, 31), "notes": None},
    {"program_code": "TITAN", "role_tier": "Mid Engineer", "planned_rate": 108.0, "actual_rate": 115.0, "planned_headcount": 9, "actual_headcount": 10, "snapshot_date": date(2026, 3, 31), "notes": "Attrition replacement cost"},
    {"program_code": "TITAN", "role_tier": "Junior Developer", "planned_rate": 68.0, "actual_rate": 70.0, "planned_headcount": 4, "actual_headcount": 3, "snapshot_date": date(2026, 3, 31), "notes": None},
]


# ---------------------------------------------------------------------------
# Change requests (scope creep log)
# ---------------------------------------------------------------------------


class ChangeRequestSeed(TypedDict):
    program_code: str
    project_code: str | None
    cr_date: date
    cr_description: str
    effort_hours: float
    cr_value: float
    processing_cost: float
    status: str
    margin_impact: float
    is_billable: bool


CHANGE_REQUESTS: list[ChangeRequestSeed] = [
    {"program_code": "PHOENIX", "project_code": "PHOE-CBM", "cr_date": date(2026, 2, 15), "cr_description": "Additional reporting module", "effort_hours": 75, "cr_value": 375_000, "processing_cost": 45_000, "status": "Approved", "margin_impact": -2.1, "is_billable": True},
    {"program_code": "PHOENIX", "project_code": "PHOE-INT", "cr_date": date(2026, 2, 28), "cr_description": "Multi-region event bus", "effort_hours": 120, "cr_value": 600_000, "processing_cost": 60_000, "status": "Approved", "margin_impact": -1.4, "is_billable": True},
    {"program_code": "PHOENIX", "project_code": "PHOE-CBM", "cr_date": date(2026, 3, 5), "cr_description": "Regulatory reporting adapter", "effort_hours": 40, "cr_value": 200_000, "processing_cost": 20_000, "status": "Pending", "margin_impact": -0.8, "is_billable": True},
    {"program_code": "ORION", "project_code": "ORN-INGEST", "cr_date": date(2026, 2, 10), "cr_description": "Extra data domain onboarded", "effort_hours": 200, "cr_value": 0, "processing_cost": 85_000, "status": "Approved", "margin_impact": -4.5, "is_billable": False},
    {"program_code": "ATLAS", "project_code": "ATLS-LNS", "cr_date": date(2026, 3, 1), "cr_description": "DR site scope added", "effort_hours": 60, "cr_value": 280_000, "processing_cost": 35_000, "status": "Approved", "margin_impact": -1.2, "is_billable": True},
    {"program_code": "TITAN", "project_code": "TTN-STORE", "cr_date": date(2026, 3, 20), "cr_description": "Personalisation engine scope expansion", "effort_hours": 90, "cr_value": 450_000, "processing_cost": 55_000, "status": "In Review", "margin_impact": -1.8, "is_billable": True},
]


