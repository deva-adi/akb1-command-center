"""Delivery-Health demo data — sprints, flow, phases, EVM, milestones.

Lives alongside app/seed/data.py but is grouped here because the volume
is large and it is only consumed by Tab 3 (Delivery Health) in Iteration
2b. Figures are shaped to match the narrative in docs/DEMO_GUIDE.md:
Phoenix compressing, Sentinel lifting on AI augmentation, Orion ingest
pipeline degrading due to bench tax, Titan Waterfall mid-flight.
"""
from __future__ import annotations

from datetime import date, timedelta
from typing import TypedDict

# ---------------------------------------------------------------------------
# Internal date helpers — defined up-front so module-level builders can use them.
# ---------------------------------------------------------------------------


def _weeks(n: int) -> timedelta:
    return timedelta(weeks=n)


def _months_after(start: date, count: int) -> list[date]:
    """Return `count` month-start dates beginning at `start`."""
    out: list[date] = []
    year, month = start.year, start.month
    for _ in range(count):
        out.append(date(year, month, 1))
        month += 1
        if month > 12:
            month = 1
            year += 1
    return out


# ---------------------------------------------------------------------------
# Sprints (Scrum projects only)
# ---------------------------------------------------------------------------


class SprintSeed(TypedDict):
    project_code: str
    sprint_number: int
    start_date: date
    end_date: date
    planned_points: int
    completed_points: int
    velocity: float
    defects_found: int
    defects_fixed: int
    rework_hours: float
    team_size: int
    ai_assisted_points: int
    iteration_type: str
    estimation_unit: str


# Each Scrum project: 6 recent sprints, 14-day cadence ending around 2026-04-06.
# PHOE-CBM: no AI, velocity compressing as rework climbs.
# PHOE-INT: light AI, steady.
# SNTL-AUTO: heavy AI, velocity uplift visible.
SPRINTS: list[SprintSeed] = [
    # PHOE-CBM — Core Banking Module (declining)
    *(
        {
            "project_code": "PHOE-CBM",
            "sprint_number": 19 + i,
            "start_date": date(2026, 1, 12) + _weeks(i * 2),
            "end_date": date(2026, 1, 25) + _weeks(i * 2),
            "planned_points": 90,
            "completed_points": [85, 82, 78, 74, 70, 68][i],
            "velocity": [85, 82, 78, 74, 70, 68][i],
            "defects_found": [8, 10, 12, 14, 15, 17][i],
            "defects_fixed": [7, 8, 9, 10, 11, 12][i],
            "rework_hours": [18.0, 22.0, 26.0, 32.0, 38.0, 45.0][i],
            "team_size": 8,
            "ai_assisted_points": 0,
            "iteration_type": "Sprint",
            "estimation_unit": "StoryPoints",
        }
        for i in range(6)
    ),
    # PHOE-INT — Integration Layer (steady with light AI)
    *(
        {
            "project_code": "PHOE-INT",
            "sprint_number": 14 + i,
            "start_date": date(2026, 1, 12) + _weeks(i * 2),
            "end_date": date(2026, 1, 25) + _weeks(i * 2),
            "planned_points": 100,
            "completed_points": [95, 97, 94, 98, 96, 99][i],
            "velocity": [95, 97, 94, 98, 96, 99][i],
            "defects_found": [5, 4, 6, 4, 5, 4][i],
            "defects_fixed": [5, 4, 6, 4, 5, 4][i],
            "rework_hours": [12.0, 10.0, 11.0, 9.0, 10.0, 8.0][i],
            "team_size": 9,
            "ai_assisted_points": [18, 22, 25, 28, 30, 32][i],
            "iteration_type": "Sprint",
            "estimation_unit": "StoryPoints",
        }
        for i in range(6)
    ),
    # SNTL-AUTO — Automation Platform (heavy AI, accelerating)
    *(
        {
            "project_code": "SNTL-AUTO",
            "sprint_number": 12 + i,
            "start_date": date(2026, 1, 12) + _weeks(i * 2),
            "end_date": date(2026, 1, 25) + _weeks(i * 2),
            "planned_points": 70,
            "completed_points": [74, 78, 82, 85, 88, 92][i],
            "velocity": [74, 78, 82, 85, 88, 92][i],
            "defects_found": [2, 2, 1, 2, 1, 1][i],
            "defects_fixed": [2, 2, 1, 2, 1, 1][i],
            "rework_hours": [6.0, 5.5, 5.0, 4.5, 4.0, 3.5][i],
            "team_size": 7,
            "ai_assisted_points": [35, 40, 44, 48, 52, 56][i],
            "iteration_type": "Sprint",
            "estimation_unit": "StoryPoints",
        }
        for i in range(6)
    ),
]


# ---------------------------------------------------------------------------
# Flow metrics (Kanban projects — weekly rows, 12 weeks)
# ---------------------------------------------------------------------------


class FlowMetricsSeed(TypedDict):
    project_code: str
    period_start: date
    period_end: date
    throughput_items: int
    wip_avg: float
    wip_limit: int
    cycle_time_p50: float
    cycle_time_p85: float
    cycle_time_p95: float
    lead_time_avg: float
    blocked_time_hours: float


FLOW_METRICS: list[FlowMetricsSeed] = [
    # ATLS-LNS — steady Kanban workstream
    *(
        {
            "project_code": "ATLS-LNS",
            "period_start": date(2026, 1, 12) + _weeks(i),
            "period_end": date(2026, 1, 18) + _weeks(i),
            "throughput_items": [8, 9, 7, 10, 9, 8, 11, 10, 9, 11, 12, 10][i],
            "wip_avg": [12.0, 13.5, 13.0, 12.5, 12.0, 13.0, 11.5, 12.0, 12.5, 11.0, 11.5, 12.0][i],
            "wip_limit": 15,
            "cycle_time_p50": [3.0, 3.2, 3.5, 3.1, 3.0, 3.2, 2.8, 3.0, 3.1, 2.8, 2.7, 2.9][i],
            "cycle_time_p85": [6.0, 6.4, 7.0, 6.2, 5.8, 6.3, 5.5, 5.9, 6.0, 5.5, 5.3, 5.7][i],
            "cycle_time_p95": [9.0, 9.5, 10.2, 9.0, 8.5, 9.2, 8.0, 8.6, 8.8, 8.0, 7.8, 8.3][i],
            "lead_time_avg": [8.5, 9.0, 9.5, 8.8, 8.3, 9.0, 7.9, 8.4, 8.6, 7.9, 7.6, 8.1][i],
            "blocked_time_hours": [2.5, 3.0, 3.5, 2.5, 2.0, 3.0, 1.8, 2.2, 2.4, 2.0, 1.8, 2.1][i],
        }
        for i in range(12)
    ),
    # ORN-INGEST — degrading Kanban throughput (bench tax)
    *(
        {
            "project_code": "ORN-INGEST",
            "period_start": date(2026, 1, 12) + _weeks(i),
            "period_end": date(2026, 1, 18) + _weeks(i),
            "throughput_items": [10, 10, 9, 8, 8, 7, 7, 6, 6, 5, 5, 4][i],
            "wip_avg": [14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5][i],
            "wip_limit": 18,
            "cycle_time_p50": [3.5, 3.8, 4.0, 4.4, 4.8, 5.2, 5.7, 6.1, 6.6, 7.0, 7.4, 7.9][i],
            "cycle_time_p85": [7.0, 7.6, 8.2, 9.0, 9.8, 10.7, 11.5, 12.4, 13.3, 14.1, 15.0, 15.9][i],
            "cycle_time_p95": [10.5, 11.4, 12.3, 13.5, 14.7, 16.0, 17.3, 18.6, 19.9, 21.2, 22.5, 23.9][i],
            "lead_time_avg": [9.5, 10.3, 11.1, 12.2, 13.3, 14.5, 15.6, 16.8, 18.0, 19.1, 20.3, 21.5][i],
            "blocked_time_hours": [4.0, 4.5, 5.2, 6.0, 6.8, 7.8, 8.7, 9.7, 10.8, 11.8, 12.9, 14.0][i],
        }
        for i in range(12)
    ),
]


# ---------------------------------------------------------------------------
# Project phases (Waterfall project)
# ---------------------------------------------------------------------------


class ProjectPhaseSeed(TypedDict):
    project_code: str
    phase_name: str
    phase_sequence: int
    planned_start: date
    planned_end: date
    actual_start: date | None
    actual_end: date | None
    percent_complete: float
    gate_status: str
    gate_approver: str | None
    gate_date: date | None
    notes: str | None


PROJECT_PHASES: list[ProjectPhaseSeed] = [
    {
        "project_code": "TTN-STORE",
        "phase_name": "Requirements",
        "phase_sequence": 1,
        "planned_start": date(2025, 9, 15),
        "planned_end": date(2025, 11, 15),
        "actual_start": date(2025, 9, 15),
        "actual_end": date(2025, 11, 20),
        "percent_complete": 100.0,
        "gate_status": "passed",
        "gate_approver": "J. Wilson",
        "gate_date": date(2025, 11, 22),
        "notes": "5-day slip; acceptable within tolerance",
    },
    {
        "project_code": "TTN-STORE",
        "phase_name": "Design",
        "phase_sequence": 2,
        "planned_start": date(2025, 11, 16),
        "planned_end": date(2026, 1, 15),
        "actual_start": date(2025, 11, 21),
        "actual_end": date(2026, 1, 25),
        "percent_complete": 100.0,
        "gate_status": "passed",
        "gate_approver": "J. Wilson",
        "gate_date": date(2026, 1, 27),
        "notes": "10-day slip; scope reduced on non-critical integrations",
    },
    {
        "project_code": "TTN-STORE",
        "phase_name": "Development",
        "phase_sequence": 3,
        "planned_start": date(2026, 1, 16),
        "planned_end": date(2026, 4, 30),
        "actual_start": date(2026, 1, 26),
        "actual_end": None,
        "percent_complete": 62.0,
        "gate_status": "pending",
        "gate_approver": None,
        "gate_date": None,
        "notes": "On track despite earlier slips; AI augmentation accelerating",
    },
    {
        "project_code": "TTN-STORE",
        "phase_name": "Test",
        "phase_sequence": 4,
        "planned_start": date(2026, 5, 1),
        "planned_end": date(2026, 6, 30),
        "actual_start": None,
        "actual_end": None,
        "percent_complete": 0.0,
        "gate_status": "pending",
        "gate_approver": None,
        "gate_date": None,
        "notes": None,
    },
    {
        "project_code": "TTN-STORE",
        "phase_name": "UAT",
        "phase_sequence": 5,
        "planned_start": date(2026, 7, 1),
        "planned_end": date(2026, 8, 15),
        "actual_start": None,
        "actual_end": None,
        "percent_complete": 0.0,
        "gate_status": "pending",
        "gate_approver": None,
        "gate_date": None,
        "notes": None,
    },
    {
        "project_code": "TTN-STORE",
        "phase_name": "Deploy",
        "phase_sequence": 6,
        "planned_start": date(2026, 8, 16),
        "planned_end": date(2026, 9, 30),
        "actual_start": None,
        "actual_end": None,
        "percent_complete": 0.0,
        "gate_status": "pending",
        "gate_approver": None,
        "gate_date": None,
        "notes": None,
    },
]


# ---------------------------------------------------------------------------
# EVM snapshots (all projects, monthly — 12 months)
# ---------------------------------------------------------------------------


class EvmSnapshotSeed(TypedDict):
    project_code: str
    snapshot_date: date
    planned_value: float
    earned_value: float
    actual_cost: float
    percent_complete: float
    bac: float
    notes: str | None


def _evm_series(
    project_code: str,
    bac: float,
    start: date,
    *,
    pv_curve: list[float],
    cpi_trend: list[float],
    spi_trend: list[float],
    notes_final: str,
) -> list[EvmSnapshotSeed]:
    out: list[EvmSnapshotSeed] = []
    for i, month_start in enumerate(_months_after(start, 12)):
        pv = bac * pv_curve[i]
        cpi = cpi_trend[i]
        spi = spi_trend[i]
        ev = pv * spi
        ac = ev / cpi if cpi > 0 else ev
        percent_complete = (ev / bac) * 100 if bac > 0 else 0.0
        out.append(
            {
                "project_code": project_code,
                "snapshot_date": month_start,
                "planned_value": round(pv, 2),
                "earned_value": round(ev, 2),
                "actual_cost": round(ac, 2),
                "percent_complete": round(percent_complete, 2),
                "bac": bac,
                "notes": notes_final if i == len(pv_curve) - 1 else None,
            }
        )
    return out


EVM_SNAPSHOTS: list[EvmSnapshotSeed] = [
    *_evm_series(
        "PHOE-CBM",
        4_200_000,
        date(2025, 5, 1),
        pv_curve=[0.05, 0.12, 0.20, 0.28, 0.36, 0.44, 0.52, 0.60, 0.68, 0.76, 0.84, 0.92],
        cpi_trend=[1.02, 1.00, 0.98, 0.96, 0.94, 0.92, 0.90, 0.89, 0.88, 0.87, 0.87, 0.87],
        spi_trend=[1.00, 0.98, 0.97, 0.95, 0.93, 0.92, 0.90, 0.88, 0.86, 0.85, 0.85, 0.84],
        notes_final="Rework cost escalating; recovery plan in CAB",
    ),
    *_evm_series(
        "PHOE-INT",
        3_200_000,
        date(2025, 5, 1),
        pv_curve=[0.04, 0.10, 0.17, 0.24, 0.31, 0.39, 0.47, 0.55, 0.63, 0.71, 0.79, 0.87],
        cpi_trend=[1.02, 1.01, 1.00, 0.99, 0.98, 0.97, 0.97, 0.96, 0.95, 0.95, 0.94, 0.93],
        spi_trend=[1.01, 1.00, 0.99, 0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91],
        notes_final="Within amber band; watch trend",
    ),
    *_evm_series(
        "ATLS-LNS",
        3_500_000,
        date(2025, 7, 1),
        pv_curve=[0.04, 0.10, 0.18, 0.26, 0.34, 0.42, 0.50, 0.58, 0.66, 0.74, 0.82, 0.90],
        cpi_trend=[1.05, 1.04, 1.02, 1.00, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91],
        spi_trend=[1.00, 1.00, 0.99, 0.98, 0.97, 0.96, 0.95, 0.95, 0.94, 0.93, 0.92, 0.91],
        notes_final="Margin cliff scenario active; team mix under review",
    ),
    *_evm_series(
        "SNTL-AUTO",
        2_800_000,
        date(2025, 8, 1),
        pv_curve=[0.05, 0.13, 0.22, 0.31, 0.40, 0.49, 0.58, 0.67, 0.76, 0.83, 0.90, 0.96],
        cpi_trend=[1.08, 1.09, 1.10, 1.11, 1.12, 1.12, 1.13, 1.14, 1.14, 1.15, 1.15, 1.16],
        spi_trend=[1.01, 1.02, 1.02, 1.03, 1.04, 1.05, 1.05, 1.06, 1.06, 1.07, 1.07, 1.07],
        notes_final="Best-in-class performance; AI augmentation paying off",
    ),
    *_evm_series(
        "ORN-INGEST",
        5_500_000,
        date(2025, 3, 1),
        pv_curve=[0.03, 0.09, 0.16, 0.23, 0.30, 0.38, 0.46, 0.54, 0.62, 0.70, 0.78, 0.86],
        cpi_trend=[0.98, 0.96, 0.94, 0.92, 0.90, 0.88, 0.86, 0.85, 0.84, 0.83, 0.82, 0.81],
        spi_trend=[1.00, 0.99, 0.97, 0.95, 0.93, 0.91, 0.89, 0.88, 0.86, 0.85, 0.84, 0.83],
        notes_final="Red corridor; bench rationalisation in flight",
    ),
    *_evm_series(
        "TTN-STORE",
        3_200_000,
        date(2025, 10, 1),
        pv_curve=[0.03, 0.10, 0.18, 0.26, 0.34, 0.42, 0.50, 0.58, 0.66, 0.74, 0.82, 0.90],
        cpi_trend=[1.04, 1.02, 1.00, 0.98, 0.97, 0.95, 0.94, 0.92, 0.91, 0.90, 0.89, 0.88],
        spi_trend=[1.00, 0.99, 0.98, 0.96, 0.95, 0.93, 0.92, 0.91, 0.90, 0.88, 0.87, 0.86],
        notes_final="Gate slip absorbed; dev phase 62% complete",
    ),
]


# ---------------------------------------------------------------------------
# Milestones (every project gets 4–6)
# ---------------------------------------------------------------------------


class MilestoneSeed(TypedDict):
    project_code: str
    name: str
    planned_date: date
    actual_date: date | None
    status: str
    owner: str | None
    notes: str | None


MILESTONES: list[MilestoneSeed] = [
    # PHOE-CBM
    {
        "project_code": "PHOE-CBM",
        "name": "Sprint 0 complete",
        "planned_date": date(2025, 5, 15),
        "actual_date": date(2025, 5, 15),
        "status": "Completed",
        "owner": "Priya Sharma",
        "notes": "On time",
    },
    {
        "project_code": "PHOE-CBM",
        "name": "Core module feature-complete",
        "planned_date": date(2025, 12, 31),
        "actual_date": date(2026, 1, 18),
        "status": "Completed",
        "owner": "Priya Sharma",
        "notes": "18-day slip; scope 93% delivered",
    },
    {
        "project_code": "PHOE-CBM",
        "name": "Integration ready",
        "planned_date": date(2026, 3, 31),
        "actual_date": None,
        "status": "Delayed",
        "owner": "Priya Sharma",
        "notes": "Vendor dependency; 3-week slip projected",
    },
    {
        "project_code": "PHOE-CBM",
        "name": "UAT sign-off",
        "planned_date": date(2026, 6, 30),
        "actual_date": None,
        "status": "At Risk",
        "owner": "Priya Sharma",
        "notes": "Contingent on integration recovery",
    },
    {
        "project_code": "PHOE-CBM",
        "name": "Go-live",
        "planned_date": date(2026, 9, 30),
        "actual_date": None,
        "status": "At Risk",
        "owner": "Priya Sharma",
        "notes": "Buffer consumed; re-baseline in progress",
    },
    # PHOE-INT
    {
        "project_code": "PHOE-INT",
        "name": "Contract signed",
        "planned_date": date(2025, 5, 1),
        "actual_date": date(2025, 5, 1),
        "status": "Completed",
        "owner": "Raj Kumar",
        "notes": None,
    },
    {
        "project_code": "PHOE-INT",
        "name": "API adapter live",
        "planned_date": date(2026, 1, 31),
        "actual_date": date(2026, 2, 10),
        "status": "Completed",
        "owner": "Raj Kumar",
        "notes": "10-day slip",
    },
    {
        "project_code": "PHOE-INT",
        "name": "Event bus integrated",
        "planned_date": date(2026, 5, 31),
        "actual_date": None,
        "status": "In Progress",
        "owner": "Raj Kumar",
        "notes": None,
    },
    {
        "project_code": "PHOE-INT",
        "name": "Production cutover",
        "planned_date": date(2026, 12, 15),
        "actual_date": None,
        "status": "Pending",
        "owner": "Raj Kumar",
        "notes": None,
    },
    # ATLS-LNS
    {
        "project_code": "ATLS-LNS",
        "name": "Cloud landing zone",
        "planned_date": date(2025, 8, 15),
        "actual_date": date(2025, 8, 20),
        "status": "Completed",
        "owner": "Suresh Menon",
        "notes": None,
    },
    {
        "project_code": "ATLS-LNS",
        "name": "Wave 1 workloads migrated",
        "planned_date": date(2026, 2, 28),
        "actual_date": date(2026, 3, 8),
        "status": "Completed",
        "owner": "Suresh Menon",
        "notes": "8-day slip",
    },
    {
        "project_code": "ATLS-LNS",
        "name": "Wave 2 migration",
        "planned_date": date(2026, 6, 30),
        "actual_date": None,
        "status": "In Progress",
        "owner": "Suresh Menon",
        "notes": None,
    },
    {
        "project_code": "ATLS-LNS",
        "name": "Decommission data centre",
        "planned_date": date(2026, 12, 15),
        "actual_date": None,
        "status": "Pending",
        "owner": "Suresh Menon",
        "notes": None,
    },
    # SNTL-AUTO
    {
        "project_code": "SNTL-AUTO",
        "name": "Pilot pipeline green",
        "planned_date": date(2025, 10, 31),
        "actual_date": date(2025, 10, 25),
        "status": "Completed",
        "owner": "Suresh Menon",
        "notes": "Ahead of plan",
    },
    {
        "project_code": "SNTL-AUTO",
        "name": "Coverage 80% achieved",
        "planned_date": date(2026, 2, 28),
        "actual_date": date(2026, 2, 22),
        "status": "Completed",
        "owner": "Suresh Menon",
        "notes": "Ahead of plan",
    },
    {
        "project_code": "SNTL-AUTO",
        "name": "AI trust audit",
        "planned_date": date(2026, 5, 15),
        "actual_date": None,
        "status": "In Progress",
        "owner": "Suresh Menon",
        "notes": None,
    },
    {
        "project_code": "SNTL-AUTO",
        "name": "Final handover",
        "planned_date": date(2026, 6, 30),
        "actual_date": None,
        "status": "Pending",
        "owner": "Suresh Menon",
        "notes": None,
    },
    # ORN-INGEST
    {
        "project_code": "ORN-INGEST",
        "name": "Raw ingest layer",
        "planned_date": date(2025, 6, 30),
        "actual_date": date(2025, 7, 12),
        "status": "Completed",
        "owner": "Meera Iyer",
        "notes": "12-day slip",
    },
    {
        "project_code": "ORN-INGEST",
        "name": "Curated layer live",
        "planned_date": date(2026, 1, 31),
        "actual_date": date(2026, 2, 28),
        "status": "Completed",
        "owner": "Meera Iyer",
        "notes": "28-day slip",
    },
    {
        "project_code": "ORN-INGEST",
        "name": "Analytics marts",
        "planned_date": date(2026, 5, 31),
        "actual_date": None,
        "status": "Delayed",
        "owner": "Meera Iyer",
        "notes": "Bench tax; redeploy plan in CAB",
    },
    {
        "project_code": "ORN-INGEST",
        "name": "Data platform GA",
        "planned_date": date(2026, 10, 31),
        "actual_date": None,
        "status": "At Risk",
        "owner": "Meera Iyer",
        "notes": None,
    },
    # TTN-STORE (Waterfall)
    {
        "project_code": "TTN-STORE",
        "name": "Requirements sign-off",
        "planned_date": date(2025, 11, 15),
        "actual_date": date(2025, 11, 20),
        "status": "Completed",
        "owner": "Nisha Rao",
        "notes": "Gate passed after 5-day slip",
    },
    {
        "project_code": "TTN-STORE",
        "name": "Design sign-off",
        "planned_date": date(2026, 1, 15),
        "actual_date": date(2026, 1, 27),
        "status": "Completed",
        "owner": "Nisha Rao",
        "notes": "Scope reduced on non-critical integrations",
    },
    {
        "project_code": "TTN-STORE",
        "name": "Development complete",
        "planned_date": date(2026, 4, 30),
        "actual_date": None,
        "status": "In Progress",
        "owner": "Nisha Rao",
        "notes": "62% complete; on track despite earlier slips",
    },
    {
        "project_code": "TTN-STORE",
        "name": "UAT exit",
        "planned_date": date(2026, 8, 15),
        "actual_date": None,
        "status": "Pending",
        "owner": "Nisha Rao",
        "notes": None,
    },
    {
        "project_code": "TTN-STORE",
        "name": "Go-live",
        "planned_date": date(2026, 9, 30),
        "actual_date": None,
        "status": "At Risk",
        "owner": "Nisha Rao",
        "notes": "P1 SLA risk window",
    },
]


