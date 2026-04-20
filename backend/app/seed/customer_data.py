"""Tab 6 Customer Intelligence demo data.

Monthly customer_satisfaction snapshots (CSAT, NPS, steering meetings,
action items) and the SLA-incident ledger that feeds the escalation log.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import TypedDict


class CustomerSatisfactionSeed(TypedDict):
    program_code: str
    snapshot_date: date
    csat_score: float
    nps_score: float
    escalation_count: int
    escalation_open: int
    steering_meetings_planned: int
    steering_meetings_held: int
    action_items_open: int
    action_items_closed: int
    positive_themes: str
    concern_themes: str
    renewal_score: float | None
    notes: str | None


# 12 monthly rows per programme. Figures reflect the NovaTech narrative:
# Phoenix + Orion + Titan drifting; Sentinel strongest; Atlas in between.
def _cs_series(
    program_code: str,
    *,
    csat: list[float],
    nps: list[float],
    escalations_total: list[int],
    escalations_open: list[int],
    meetings_planned: int,
    meetings_held: list[int],
    items_open: list[int],
    items_closed: list[int],
    positive_themes: str,
    concern_themes: str,
    renewal: list[float],
) -> list[CustomerSatisfactionSeed]:
    starts = [
        date(2025, 4, 1), date(2025, 5, 1), date(2025, 6, 1), date(2025, 7, 1),
        date(2025, 8, 1), date(2025, 9, 1), date(2025, 10, 1), date(2025, 11, 1),
        date(2025, 12, 1), date(2026, 1, 1), date(2026, 2, 1), date(2026, 3, 1),
    ]
    return [
        {
            "program_code": program_code,
            "snapshot_date": starts[i],
            "csat_score": csat[i],
            "nps_score": nps[i],
            "escalation_count": escalations_total[i],
            "escalation_open": escalations_open[i],
            "steering_meetings_planned": meetings_planned,
            "steering_meetings_held": meetings_held[i],
            "action_items_open": items_open[i],
            "action_items_closed": items_closed[i],
            "positive_themes": positive_themes,
            "concern_themes": concern_themes,
            "renewal_score": renewal[i],
            "notes": None,
        }
        for i in range(12)
    ]


CUSTOMER_SATISFACTION: list[CustomerSatisfactionSeed] = [
    *_cs_series(
        "PHOENIX",
        csat=[8.2, 8.0, 7.9, 7.8, 7.6, 7.5, 7.3, 7.2, 7.0, 6.9, 6.8, 6.7],
        nps=[45, 40, 38, 35, 30, 28, 24, 20, 16, 12, 8, 5],
        escalations_total=[1, 2, 2, 3, 4, 4, 5, 6, 7, 8, 9, 10],
        escalations_open=[0, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 5],
        meetings_planned=2,
        meetings_held=[2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 1],
        items_open=[4, 5, 5, 6, 7, 8, 9, 10, 11, 11, 12, 13],
        items_closed=[2, 3, 4, 4, 5, 5, 6, 6, 7, 8, 8, 9],
        positive_themes="Domain depth; Responsive programme leadership",
        concern_themes="CR margin erosion; Integration vendor slip; SLA pressure",
        renewal=[82, 80, 77, 74, 70, 67, 62, 58, 54, 50, 46, 43],
    ),
    *_cs_series(
        "ATLAS",
        csat=[7.8, 7.8, 7.7, 7.7, 7.6, 7.6, 7.5, 7.4, 7.4, 7.3, 7.3, 7.2],
        nps=[30, 30, 28, 28, 25, 25, 22, 20, 18, 16, 15, 13],
        escalations_total=[0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4],
        escalations_open=[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
        meetings_planned=2,
        meetings_held=[2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2],
        items_open=[3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8],
        items_closed=[1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7],
        positive_themes="Cloud expertise; Migration pace",
        concern_themes="Rate drift; Bench visibility",
        renewal=[73, 72, 70, 69, 67, 65, 62, 60, 57, 54, 52, 50],
    ),
    *_cs_series(
        "SENTINEL",
        csat=[8.6, 8.7, 8.8, 8.8, 8.9, 9.0, 9.0, 9.1, 9.1, 9.2, 9.2, 9.3],
        nps=[55, 58, 60, 62, 64, 65, 67, 68, 70, 72, 74, 75],
        escalations_total=[0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        escalations_open=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        meetings_planned=2,
        meetings_held=[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        items_open=[2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 0, 0],
        items_closed=[3, 4, 5, 5, 6, 6, 7, 7, 8, 9, 9, 10],
        positive_themes="AI augmentation quality; Fast feedback loop; Transparent reporting",
        concern_themes="None material",
        renewal=[88, 89, 90, 91, 92, 92, 93, 93, 94, 94, 95, 95],
    ),
    *_cs_series(
        "ORION",
        csat=[7.9, 7.8, 7.5, 7.3, 7.0, 6.8, 6.5, 6.2, 6.0, 5.8, 5.5, 5.2],
        nps=[25, 20, 15, 10, 5, 0, -5, -10, -15, -20, -25, -30],
        escalations_total=[0, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11],
        escalations_open=[0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 5, 6],
        meetings_planned=2,
        meetings_held=[2, 2, 2, 2, 1, 2, 1, 1, 1, 2, 1, 1],
        items_open=[5, 6, 7, 8, 10, 11, 13, 14, 15, 16, 18, 20],
        items_closed=[2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8],
        positive_themes="Strong data engineers",
        concern_themes="Bench tax; Knowledge churn; Delivery slips",
        renewal=[70, 66, 62, 57, 52, 47, 42, 37, 32, 28, 23, 20],
    ),
    *_cs_series(
        "TITAN",
        csat=[8.0, 7.9, 7.8, 7.5, 7.3, 7.0, 6.9, 6.8, 6.8, 6.8, 6.8, 6.8],
        nps=[32, 30, 25, 20, 15, 10, 8, 6, 5, 5, 5, 5],
        escalations_total=[0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
        escalations_open=[0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 2, 2],
        meetings_planned=2,
        meetings_held=[2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2],
        items_open=[3, 3, 4, 5, 6, 6, 7, 7, 8, 8, 9, 9],
        items_closed=[1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7],
        positive_themes="Front-end velocity; UX polish",
        concern_themes="SLA breaches; Attrition impact",
        renewal=[75, 73, 70, 65, 60, 56, 54, 52, 50, 50, 50, 50],
    ),
]


class SlaIncidentSeed(TypedDict):
    program_code: str
    incident_id: str
    priority: str
    summary: str
    reported_at: datetime
    responded_at: datetime | None
    resolved_at: datetime | None
    response_time_minutes: float | None
    resolution_time_minutes: float | None
    sla_breached: bool
    penalty_amount: float
    root_cause: str | None


SLA_INCIDENTS: list[SlaIncidentSeed] = [
    # Titan P1 breaches (matching the narrative)
    {
        "program_code": "TITAN",
        "incident_id": "INC-2026-0412",
        "priority": "P1",
        "summary": "Checkout service 5xx surge",
        "reported_at": datetime(2026, 1, 18, 11, 45),
        "responded_at": datetime(2026, 1, 18, 12, 40),
        "resolved_at": datetime(2026, 1, 19, 9, 20),
        "response_time_minutes": 55.0,
        "resolution_time_minutes": 21 * 60 + 35,
        "sla_breached": True,
        "penalty_amount": 150_000,
        "root_cause": "Cache stampede during peak traffic",
    },
    {
        "program_code": "TITAN",
        "incident_id": "INC-2026-0587",
        "priority": "P1",
        "summary": "Payment gateway timeout",
        "reported_at": datetime(2026, 3, 4, 18, 22),
        "responded_at": datetime(2026, 3, 4, 19, 50),
        "resolved_at": datetime(2026, 3, 5, 4, 10),
        "response_time_minutes": 88.0,
        "resolution_time_minutes": 9 * 60 + 48,
        "sla_breached": True,
        "penalty_amount": 250_000,
        "root_cause": "Third-party gateway region outage; runbook missing failover step",
    },
    {
        "program_code": "TITAN",
        "incident_id": "INC-2026-0612",
        "priority": "P2",
        "summary": "Product search slow",
        "reported_at": datetime(2026, 3, 15, 10, 0),
        "responded_at": datetime(2026, 3, 15, 10, 35),
        "resolved_at": datetime(2026, 3, 15, 15, 10),
        "response_time_minutes": 35.0,
        "resolution_time_minutes": 5 * 60 + 10,
        "sla_breached": False,
        "penalty_amount": 0,
        "root_cause": "Elasticsearch index hotspot",
    },
    # Phoenix SLA breach
    {
        "program_code": "PHOENIX",
        "incident_id": "INC-2026-0104",
        "priority": "P2",
        "summary": "Core module batch job overran",
        "reported_at": datetime(2026, 2, 2, 2, 30),
        "responded_at": datetime(2026, 2, 2, 3, 15),
        "resolved_at": datetime(2026, 2, 2, 9, 45),
        "response_time_minutes": 45.0,
        "resolution_time_minutes": 7 * 60 + 15,
        "sla_breached": True,
        "penalty_amount": 40_000,
        "root_cause": "Scope CR increased batch window",
    },
    # Orion incidents
    {
        "program_code": "ORION",
        "incident_id": "INC-2026-0231",
        "priority": "P2",
        "summary": "Analytics mart refresh failed",
        "reported_at": datetime(2026, 2, 14, 6, 0),
        "responded_at": datetime(2026, 2, 14, 7, 40),
        "resolved_at": datetime(2026, 2, 14, 15, 0),
        "response_time_minutes": 100.0,
        "resolution_time_minutes": 9 * 60,
        "sla_breached": True,
        "penalty_amount": 60_000,
        "root_cause": "Bench rotation; on-call unfamiliar with pipeline",
    },
    {
        "program_code": "ORION",
        "incident_id": "INC-2026-0398",
        "priority": "P3",
        "summary": "Ingest job latency spike",
        "reported_at": datetime(2026, 3, 2, 14, 0),
        "responded_at": datetime(2026, 3, 2, 14, 55),
        "resolved_at": datetime(2026, 3, 2, 17, 30),
        "response_time_minutes": 55.0,
        "resolution_time_minutes": 3 * 60 + 30,
        "sla_breached": False,
        "penalty_amount": 0,
        "root_cause": "Upstream source throttling",
    },
    # Atlas incident
    {
        "program_code": "ATLAS",
        "incident_id": "INC-2026-0450",
        "priority": "P3",
        "summary": "Terraform plan drift",
        "reported_at": datetime(2026, 3, 10, 9, 30),
        "responded_at": datetime(2026, 3, 10, 10, 10),
        "resolved_at": datetime(2026, 3, 10, 11, 50),
        "response_time_minutes": 40.0,
        "resolution_time_minutes": 2 * 60 + 20,
        "sla_breached": False,
        "penalty_amount": 0,
        "root_cause": "Manual console change",
    },
    # Sentinel — one benign P3 to show responsiveness
    {
        "program_code": "SENTINEL",
        "incident_id": "INC-2026-0511",
        "priority": "P3",
        "summary": "Test env flaky",
        "reported_at": datetime(2026, 3, 18, 12, 0),
        "responded_at": datetime(2026, 3, 18, 12, 20),
        "resolved_at": datetime(2026, 3, 18, 13, 5),
        "response_time_minutes": 20.0,
        "resolution_time_minutes": 65.0,
        "sla_breached": False,
        "penalty_amount": 0,
        "root_cause": "Dependency version mismatch",
    },
]
