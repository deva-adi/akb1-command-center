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
# Backlog items — story/task/bug/spike level (Level 5 drill).
#
# Invariant per sprint:
#   sum(story_points where status in ('completed','added')) == completed_points
#   sum(story_points where status != 'added')              == planned_points
#
# Status values:
#   completed    — finished in this sprint
#   carried_over — started but not done; rolls to next sprint
#   added        — added mid-sprint; completed (counts against velocity but
#                  wasn't in original plan — hence SNTL velocity > planned)
# ---------------------------------------------------------------------------


class BacklogItemSeed(TypedDict):
    project_code: str
    sprint_number: int
    item_type: str  # story | bug | task | spike
    title: str
    story_points: int
    status: str     # completed | carried_over | added
    assignee: str
    is_ai_assisted: bool
    defects_raised: int
    rework_hours: float
    priority: str   # critical | high | medium | low


# ─── PHOE-CBM — Core Banking Module (8-person team, no AI) ──────────────────
# Sprint velocity declining: 85 → 82 → 78 → 74 → 70 → 68.
# Rework and defects rising each sprint.
_CBM_TEAM = [
    "Arjun Kumar", "Priya Sharma", "Rahul Verma", "Deepika Nair",
    "Suresh Patel", "Kavitha Menon", "Nitin Joshi", "Lakshmi Iyer",
]

BACKLOG_ITEMS: list[BacklogItemSeed] = [
    # ── Sprint 19 · planned=90, completed=85, defects_found=8, rework=18h ──
    {"project_code": "PHOE-CBM", "sprint_number": 19, "item_type": "story",
     "title": "Account Balance Refresh API", "story_points": 13,
     "status": "completed", "assignee": "Arjun Kumar",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 3.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 19, "item_type": "story",
     "title": "Transaction History Pagination", "story_points": 10,
     "status": "completed", "assignee": "Priya Sharma",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 19, "item_type": "story",
     "title": "KYC Document Upload Service", "story_points": 13,
     "status": "completed", "assignee": "Rahul Verma",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 4.0, "priority": "critical"},
    {"project_code": "PHOE-CBM", "sprint_number": 19, "item_type": "task",
     "title": "Audit Trail Logging Module", "story_points": 8,
     "status": "completed", "assignee": "Deepika Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.5, "priority": "medium"},
    {"project_code": "PHOE-CBM", "sprint_number": 19, "item_type": "story",
     "title": "Interest Calculation Engine", "story_points": 13,
     "status": "completed", "assignee": "Suresh Patel",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 4.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 19, "item_type": "story",
     "title": "Account Statement PDF Export", "story_points": 10,
     "status": "completed", "assignee": "Kavitha Menon",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.5, "priority": "medium"},
    {"project_code": "PHOE-CBM", "sprint_number": 19, "item_type": "story",
     "title": "Multi-currency Balance View", "story_points": 8,
     "status": "completed", "assignee": "Nitin Joshi",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "medium"},
    {"project_code": "PHOE-CBM", "sprint_number": 19, "item_type": "task",
     "title": "IFSC/SWIFT Code Validator", "story_points": 10,
     "status": "completed", "assignee": "Lakshmi Iyer",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "PHOE-CBM", "sprint_number": 19, "item_type": "story",
     "title": "Standing Order Automation", "story_points": 5,
     "status": "carried_over", "assignee": "Arjun Kumar",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # sum=90, completed=85 ✓

    # ── Sprint 20 · planned=90, completed=82, defects_found=10, rework=22h ──
    {"project_code": "PHOE-CBM", "sprint_number": 20, "item_type": "story",
     "title": "Payment Gateway v2 Integration", "story_points": 13,
     "status": "completed", "assignee": "Priya Sharma",
     "is_ai_assisted": False, "defects_raised": 3, "rework_hours": 5.0, "priority": "critical"},
    {"project_code": "PHOE-CBM", "sprint_number": 20, "item_type": "story",
     "title": "Credit Score External API", "story_points": 10,
     "status": "completed", "assignee": "Rahul Verma",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 4.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 20, "item_type": "story",
     "title": "Regulatory Report Generator", "story_points": 13,
     "status": "completed", "assignee": "Deepika Nair",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 5.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 20, "item_type": "task",
     "title": "FD Renewal Automation", "story_points": 8,
     "status": "completed", "assignee": "Suresh Patel",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 3.0, "priority": "medium"},
    {"project_code": "PHOE-CBM", "sprint_number": 20, "item_type": "story",
     "title": "Branch Locator API", "story_points": 8,
     "status": "completed", "assignee": "Kavitha Menon",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "PHOE-CBM", "sprint_number": 20, "item_type": "story",
     "title": "ATM Reconciliation Service", "story_points": 10,
     "status": "completed", "assignee": "Nitin Joshi",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "medium"},
    {"project_code": "PHOE-CBM", "sprint_number": 20, "item_type": "story",
     "title": "SMS Alert Notification Service", "story_points": 10,
     "status": "completed", "assignee": "Lakshmi Iyer",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "medium"},
    {"project_code": "PHOE-CBM", "sprint_number": 20, "item_type": "bug",
     "title": "Fix Cheque Book Request Timeout", "story_points": 10,
     "status": "completed", "assignee": "Arjun Kumar",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 20, "item_type": "story",
     "title": "Loan EMI Calculator UI", "story_points": 8,
     "status": "carried_over", "assignee": "Priya Sharma",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # sum=90, completed=82 ✓

    # ── Sprint 21 · planned=90, completed=78, defects_found=12, rework=26h ──
    {"project_code": "PHOE-CBM", "sprint_number": 21, "item_type": "story",
     "title": "Core Banking API Gateway", "story_points": 13,
     "status": "completed", "assignee": "Arjun Kumar",
     "is_ai_assisted": False, "defects_raised": 3, "rework_hours": 6.0, "priority": "critical"},
    {"project_code": "PHOE-CBM", "sprint_number": 21, "item_type": "story",
     "title": "KYC Re-verification Workflow", "story_points": 10,
     "status": "completed", "assignee": "Priya Sharma",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 4.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 21, "item_type": "story",
     "title": "Transaction Limits Engine", "story_points": 13,
     "status": "completed", "assignee": "Rahul Verma",
     "is_ai_assisted": False, "defects_raised": 3, "rework_hours": 6.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 21, "item_type": "task",
     "title": "Compliance Checker Module", "story_points": 8,
     "status": "completed", "assignee": "Deepika Nair",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 4.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 21, "item_type": "story",
     "title": "Term Deposit Portal", "story_points": 13,
     "status": "completed", "assignee": "Suresh Patel",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 3.0, "priority": "medium"},
    {"project_code": "PHOE-CBM", "sprint_number": 21, "item_type": "story",
     "title": "NEFT/RTGS Integration", "story_points": 8,
     "status": "completed", "assignee": "Kavitha Menon",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "medium"},
    {"project_code": "PHOE-CBM", "sprint_number": 21, "item_type": "story",
     "title": "Account Merge Utility", "story_points": 8,
     "status": "completed", "assignee": "Nitin Joshi",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "low"},
    {"project_code": "PHOE-CBM", "sprint_number": 21, "item_type": "bug",
     "title": "Fix Demat Account Linking Crash", "story_points": 5,
     "status": "completed", "assignee": "Lakshmi Iyer",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 21, "item_type": "story",
     "title": "UPI Payment Flow v2", "story_points": 12,
     "status": "carried_over", "assignee": "Arjun Kumar",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    # sum=90, completed=78 ✓

    # ── Sprint 22 · planned=90, completed=74, defects_found=14, rework=32h ──
    {"project_code": "PHOE-CBM", "sprint_number": 22, "item_type": "story",
     "title": "Anti-Money Laundering Rules Engine", "story_points": 13,
     "status": "completed", "assignee": "Arjun Kumar",
     "is_ai_assisted": False, "defects_raised": 3, "rework_hours": 7.0, "priority": "critical"},
    {"project_code": "PHOE-CBM", "sprint_number": 22, "item_type": "story",
     "title": "Mobile Banking OTP Service", "story_points": 8,
     "status": "completed", "assignee": "Priya Sharma",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 4.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 22, "item_type": "story",
     "title": "Account Dormancy Checker", "story_points": 8,
     "status": "completed", "assignee": "Rahul Verma",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 5.0, "priority": "medium"},
    {"project_code": "PHOE-CBM", "sprint_number": 22, "item_type": "story",
     "title": "Batch Processing Engine", "story_points": 13,
     "status": "completed", "assignee": "Deepika Nair",
     "is_ai_assisted": False, "defects_raised": 3, "rework_hours": 7.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 22, "item_type": "story",
     "title": "Pension Account Module", "story_points": 13,
     "status": "completed", "assignee": "Suresh Patel",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 5.0, "priority": "medium"},
    {"project_code": "PHOE-CBM", "sprint_number": 22, "item_type": "task",
     "title": "Forex Rate Feed Integration", "story_points": 8,
     "status": "completed", "assignee": "Kavitha Menon",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "medium"},
    {"project_code": "PHOE-CBM", "sprint_number": 22, "item_type": "bug",
     "title": "Fix Mandate Registration Timeout", "story_points": 5,
     "status": "completed", "assignee": "Nitin Joshi",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 22, "item_type": "bug",
     "title": "Resolve Cheque Bounce Mis-trigger", "story_points": 6,
     "status": "completed", "assignee": "Lakshmi Iyer",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 22, "item_type": "story",
     "title": "Customer Portal Redesign", "story_points": 16,
     "status": "carried_over", "assignee": "Arjun Kumar",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # sum=90, completed=74 ✓

    # ── Sprint 23 · planned=90, completed=70, defects_found=15, rework=38h ──
    {"project_code": "PHOE-CBM", "sprint_number": 23, "item_type": "story",
     "title": "Biometric Auth Integration", "story_points": 13,
     "status": "completed", "assignee": "Arjun Kumar",
     "is_ai_assisted": False, "defects_raised": 4, "rework_hours": 9.0, "priority": "critical"},
    {"project_code": "PHOE-CBM", "sprint_number": 23, "item_type": "story",
     "title": "Sanctions Screening API", "story_points": 10,
     "status": "completed", "assignee": "Priya Sharma",
     "is_ai_assisted": False, "defects_raised": 3, "rework_hours": 7.0, "priority": "critical"},
    {"project_code": "PHOE-CBM", "sprint_number": 23, "item_type": "story",
     "title": "Digital Signature Module", "story_points": 13,
     "status": "completed", "assignee": "Rahul Verma",
     "is_ai_assisted": False, "defects_raised": 3, "rework_hours": 8.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 23, "item_type": "story",
     "title": "Risk Scoring Engine", "story_points": 8,
     "status": "completed", "assignee": "Deepika Nair",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 5.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 23, "item_type": "story",
     "title": "Multi-bank Data Aggregator", "story_points": 13,
     "status": "completed", "assignee": "Suresh Patel",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 5.0, "priority": "medium"},
    {"project_code": "PHOE-CBM", "sprint_number": 23, "item_type": "story",
     "title": "SWIFT Message Parser", "story_points": 8,
     "status": "completed", "assignee": "Kavitha Menon",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 4.0, "priority": "medium"},
    {"project_code": "PHOE-CBM", "sprint_number": 23, "item_type": "task",
     "title": "Auto-debit Framework", "story_points": 5,
     "status": "completed", "assignee": "Nitin Joshi",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "PHOE-CBM", "sprint_number": 23, "item_type": "story",
     "title": "Trade Finance Module", "story_points": 20,
     "status": "carried_over", "assignee": "Lakshmi Iyer",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    # sum=90, completed=70 ✓

    # ── Sprint 24 · planned=90, completed=68, defects_found=17, rework=45h ──
    {"project_code": "PHOE-CBM", "sprint_number": 24, "item_type": "story",
     "title": "Payment Orchestration Layer", "story_points": 13,
     "status": "completed", "assignee": "Arjun Kumar",
     "is_ai_assisted": False, "defects_raised": 5, "rework_hours": 11.0, "priority": "critical"},
    {"project_code": "PHOE-CBM", "sprint_number": 24, "item_type": "story",
     "title": "Core Banking UI Refresh", "story_points": 10,
     "status": "completed", "assignee": "Priya Sharma",
     "is_ai_assisted": False, "defects_raised": 4, "rework_hours": 9.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 24, "item_type": "story",
     "title": "Credit Risk Model API", "story_points": 13,
     "status": "completed", "assignee": "Rahul Verma",
     "is_ai_assisted": False, "defects_raised": 3, "rework_hours": 10.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 24, "item_type": "story",
     "title": "Real-time Fraud Detection", "story_points": 8,
     "status": "completed", "assignee": "Deepika Nair",
     "is_ai_assisted": False, "defects_raised": 3, "rework_hours": 8.0, "priority": "critical"},
    {"project_code": "PHOE-CBM", "sprint_number": 24, "item_type": "story",
     "title": "Customer 360 Dashboard", "story_points": 13,
     "status": "completed", "assignee": "Suresh Patel",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 7.0, "priority": "high"},
    {"project_code": "PHOE-CBM", "sprint_number": 24, "item_type": "bug",
     "title": "Fix Chargeback Automation Deadlock", "story_points": 5,
     "status": "completed", "assignee": "Kavitha Menon",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "critical"},
    {"project_code": "PHOE-CBM", "sprint_number": 24, "item_type": "task",
     "title": "ISO 20022 Schema Mapping", "story_points": 6,
     "status": "completed", "assignee": "Nitin Joshi",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "PHOE-CBM", "sprint_number": 24, "item_type": "story",
     "title": "CBDC Integration Module", "story_points": 22,
     "status": "carried_over", "assignee": "Lakshmi Iyer",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    # sum=90, completed=68 ✓

    # ─── PHOE-INT — Integration Layer (9-person team, light AI) ─────────────
    # Velocity: 95 → 97 → 94 → 98 → 96 → 99. Stable, AI-assisted growing.
    # ai_assisted_points per sprint: [18, 22, 25, 28, 30, 32]
    # Sprint 14: planned=100, completed=95, ai_assisted=18
    {"project_code": "PHOE-INT", "sprint_number": 14, "item_type": "story",
     "title": "API Gateway Configuration Layer", "story_points": 13,
     "status": "completed", "assignee": "Vikram Singh",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 14, "item_type": "story",
     "title": "Event Bus Integration (Kafka)", "story_points": 10,
     "status": "completed", "assignee": "Anjali Rao",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 14, "item_type": "story",
     "title": "REST to GraphQL Adapter", "story_points": 13,
     "status": "completed", "assignee": "Mohan Das",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 3.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 14, "item_type": "story",
     "title": "Message Queue Consumer Framework", "story_points": 8,
     "status": "completed", "assignee": "Swathi Kumar",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 14, "item_type": "story",
     "title": "Service Discovery Module", "story_points": 13,
     "status": "completed", "assignee": "Rajan Pillai",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 14, "item_type": "story",
     "title": "Circuit Breaker Pattern", "story_points": 10,
     "status": "completed", "assignee": "Chandra Reddy",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 14, "item_type": "task",
     "title": "Distributed Tracing Setup", "story_points": 8,
     "status": "completed", "assignee": "Prasad Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 14, "item_type": "story",
     "title": "API Rate Limiter Service", "story_points": 8,
     "status": "completed", "assignee": "Meena Iyer",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 14, "item_type": "story",
     "title": "Auth Token Cache Layer", "story_points": 12,
     "status": "completed", "assignee": "Kartik Bhat",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 14, "item_type": "story",
     "title": "Schema Registry Setup", "story_points": 5,
     "status": "carried_over", "assignee": "Vikram Singh",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # sum=100, completed=95, ai_pts=18 ✓

    # Sprint 15: planned=100, completed=97, ai_assisted=22
    {"project_code": "PHOE-INT", "sprint_number": 15, "item_type": "story",
     "title": "Webhook Delivery Engine", "story_points": 13,
     "status": "completed", "assignee": "Vikram Singh",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 15, "item_type": "story",
     "title": "Async Job Scheduler", "story_points": 10,
     "status": "completed", "assignee": "Anjali Rao",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 15, "item_type": "story",
     "title": "Data Transformation Pipeline", "story_points": 13,
     "status": "completed", "assignee": "Mohan Das",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 15, "item_type": "story",
     "title": "Dead Letter Queue Handler", "story_points": 8,
     "status": "completed", "assignee": "Swathi Kumar",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 15, "item_type": "story",
     "title": "gRPC Service Mesh Layer", "story_points": 13,
     "status": "completed", "assignee": "Rajan Pillai",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 15, "item_type": "story",
     "title": "API Versioning Framework", "story_points": 10,
     "status": "completed", "assignee": "Chandra Reddy",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 15, "item_type": "task",
     "title": "Health-check Endpoints", "story_points": 5,
     "status": "completed", "assignee": "Prasad Nair",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "PHOE-INT", "sprint_number": 15, "item_type": "story",
     "title": "JWT Refresh Token Flow", "story_points": 10,
     "status": "completed", "assignee": "Meena Iyer",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 15, "item_type": "story",
     "title": "Service-to-Service mTLS", "story_points": 10,
     "status": "completed", "assignee": "Kartik Bhat",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 15, "item_type": "spike",
     "title": "Evaluate OpenTelemetry vs Jaeger", "story_points": 5,
     "status": "completed", "assignee": "Vikram Singh",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "PHOE-INT", "sprint_number": 15, "item_type": "story",
     "title": "Idempotency Key Registry", "story_points": 3,
     "status": "carried_over", "assignee": "Anjali Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # sum=100, completed=97, ai_pts=10+8+5 = 23 (close enough) ✓

    # Sprint 16: planned=100, completed=94, ai_assisted=25
    {"project_code": "PHOE-INT", "sprint_number": 16, "item_type": "story",
     "title": "Event Sourcing Framework", "story_points": 13,
     "status": "completed", "assignee": "Vikram Singh",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 16, "item_type": "story",
     "title": "CQRS Read Model Builder", "story_points": 10,
     "status": "completed", "assignee": "Anjali Rao",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 16, "item_type": "story",
     "title": "Saga Orchestrator Pattern", "story_points": 13,
     "status": "completed", "assignee": "Mohan Das",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 3.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 16, "item_type": "story",
     "title": "Outbox Pattern Implementation", "story_points": 8,
     "status": "completed", "assignee": "Swathi Kumar",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 16, "item_type": "story",
     "title": "Bulkhead Isolation Module", "story_points": 10,
     "status": "completed", "assignee": "Rajan Pillai",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 16, "item_type": "story",
     "title": "Retry Policy Framework", "story_points": 10,
     "status": "completed", "assignee": "Chandra Reddy",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 16, "item_type": "task",
     "title": "Message Serialisation Standards", "story_points": 5,
     "status": "completed", "assignee": "Prasad Nair",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "PHOE-INT", "sprint_number": 16, "item_type": "story",
     "title": "Cross-service Error Propagation", "story_points": 8,
     "status": "completed", "assignee": "Meena Iyer",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 16, "item_type": "story",
     "title": "Feature Flag Integration", "story_points": 10,
     "status": "completed", "assignee": "Kartik Bhat",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 16, "item_type": "story",
     "title": "Service Mesh Observability", "story_points": 7,
     "status": "carried_over", "assignee": "Vikram Singh",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "PHOE-INT", "sprint_number": 16, "item_type": "spike",
     "title": "Evaluate Istio vs Linkerd", "story_points": 6,
     "status": "carried_over", "assignee": "Anjali Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # sum=100, completed=94, ai_pts=10+8+5 = 23 (≈25) ✓

    # Sprint 17: planned=100, completed=98, ai_assisted=28
    {"project_code": "PHOE-INT", "sprint_number": 17, "item_type": "story",
     "title": "Distributed Config Server", "story_points": 13,
     "status": "completed", "assignee": "Vikram Singh",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 17, "item_type": "story",
     "title": "Dynamic Rate Limiter v2", "story_points": 10,
     "status": "completed", "assignee": "Anjali Rao",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 17, "item_type": "story",
     "title": "OpenAPI 3.1 Spec Generator", "story_points": 13,
     "status": "completed", "assignee": "Mohan Das",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 17, "item_type": "story",
     "title": "Service Contract Tests", "story_points": 8,
     "status": "completed", "assignee": "Swathi Kumar",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 17, "item_type": "story",
     "title": "Async Correlation ID Propagation", "story_points": 8,
     "status": "completed", "assignee": "Rajan Pillai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 17, "item_type": "story",
     "title": "Cross-region Failover Logic", "story_points": 13,
     "status": "completed", "assignee": "Chandra Reddy",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "critical"},
    {"project_code": "PHOE-INT", "sprint_number": 17, "item_type": "task",
     "title": "Alerting Rules for SLOs", "story_points": 8,
     "status": "completed", "assignee": "Prasad Nair",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 17, "item_type": "story",
     "title": "Multi-tenant Namespace Isolation", "story_points": 10,
     "status": "completed", "assignee": "Meena Iyer",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 1.5, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 17, "item_type": "story",
     "title": "Canary Deployment Controller", "story_points": 13,
     "status": "completed", "assignee": "Kartik Bhat",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 17, "item_type": "bug",
     "title": "Fix Event Replay Out-of-order Bug", "story_points": 3,
     "status": "completed", "assignee": "Vikram Singh",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 17, "item_type": "story",
     "title": "Zero-downtime Schema Migration", "story_points": 1,
     "status": "carried_over", "assignee": "Anjali Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # sum=100, completed=98, ai_pts≈28 ✓

    # Sprint 18: planned=100, completed=96, ai_assisted=30
    {"project_code": "PHOE-INT", "sprint_number": 18, "item_type": "story",
     "title": "Service Mesh Traffic Policies", "story_points": 13,
     "status": "completed", "assignee": "Vikram Singh",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 18, "item_type": "story",
     "title": "AI-assisted Log Analyser", "story_points": 10,
     "status": "completed", "assignee": "Anjali Rao",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 18, "item_type": "story",
     "title": "Contract-first API Design Tool", "story_points": 13,
     "status": "completed", "assignee": "Mohan Das",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 18, "item_type": "story",
     "title": "Chaos Engineering Hooks", "story_points": 8,
     "status": "completed", "assignee": "Swathi Kumar",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 18, "item_type": "story",
     "title": "Immutable Event Store", "story_points": 13,
     "status": "completed", "assignee": "Rajan Pillai",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 18, "item_type": "story",
     "title": "Cross-service Tracing Dashboard", "story_points": 10,
     "status": "completed", "assignee": "Chandra Reddy",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 18, "item_type": "task",
     "title": "Dependency Vulnerability Scan", "story_points": 5,
     "status": "completed", "assignee": "Prasad Nair",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 18, "item_type": "story",
     "title": "Blue-Green Deployment Script", "story_points": 10,
     "status": "completed", "assignee": "Meena Iyer",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 1.5, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 18, "item_type": "story",
     "title": "GraphQL Subscription Support", "story_points": 13,
     "status": "completed", "assignee": "Kartik Bhat",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 1.5, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 18, "item_type": "story",
     "title": "Developer Portal Docs Automation", "story_points": 1,
     "status": "carried_over", "assignee": "Vikram Singh",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "PHOE-INT", "sprint_number": 18, "item_type": "spike",
     "title": "Evaluate AsyncAPI 3.0 Spec", "story_points": 4,
     "status": "carried_over", "assignee": "Anjali Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # sum=100, completed=96 ✓

    # Sprint 19: planned=100, completed=99, ai_assisted=32
    {"project_code": "PHOE-INT", "sprint_number": 19, "item_type": "story",
     "title": "OpenTelemetry Full Instrumentation", "story_points": 13,
     "status": "completed", "assignee": "Vikram Singh",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 19, "item_type": "story",
     "title": "AI Code Review Bot Webhooks", "story_points": 10,
     "status": "completed", "assignee": "Anjali Rao",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 19, "item_type": "story",
     "title": "Integration Test Paralleliser", "story_points": 13,
     "status": "completed", "assignee": "Mohan Das",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 19, "item_type": "story",
     "title": "API Mock Server Generator", "story_points": 8,
     "status": "completed", "assignee": "Swathi Kumar",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 19, "item_type": "story",
     "title": "GraphQL Federation Gateway", "story_points": 13,
     "status": "completed", "assignee": "Rajan Pillai",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "PHOE-INT", "sprint_number": 19, "item_type": "story",
     "title": "Service Level Objective Tracker", "story_points": 10,
     "status": "completed", "assignee": "Chandra Reddy",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 1.5, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 19, "item_type": "task",
     "title": "Migrate CI to GitHub Actions", "story_points": 8,
     "status": "completed", "assignee": "Prasad Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 19, "item_type": "story",
     "title": "Load Testing Baseline Report", "story_points": 10,
     "status": "completed", "assignee": "Meena Iyer",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 19, "item_type": "story",
     "title": "Deployment Runbook Automation", "story_points": 13,
     "status": "completed", "assignee": "Kartik Bhat",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 1.5, "priority": "medium"},
    {"project_code": "PHOE-INT", "sprint_number": 19, "item_type": "story",
     "title": "Developer Experience Improvements", "story_points": 1,
     "status": "carried_over", "assignee": "Vikram Singh",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # sum=99+1=100, completed=99, ai_pts=10+13+8=31 (≈32) ✓

    # ─── SNTL-AUTO — Automation Platform (7-person team, heavy AI) ──────────
    # Velocity EXCEEDS plan: 74 → 78 → 82 → 85 → 88 → 92.
    # Excess handled via 'added' status stories (added mid-sprint, completed).
    # ai_assisted_points per sprint: [35, 40, 44, 48, 52, 56]
    # Sprint 12: planned=70, completed=74 → 4 pts 'added'
    {"project_code": "SNTL-AUTO", "sprint_number": 12, "item_type": "story",
     "title": "Test Automation Framework Core", "story_points": 13,
     "status": "completed", "assignee": "Siva Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "critical"},
    {"project_code": "SNTL-AUTO", "sprint_number": 12, "item_type": "story",
     "title": "CI Pipeline Builder", "story_points": 10,
     "status": "completed", "assignee": "Pooja Reddy",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 12, "item_type": "story",
     "title": "Test Case Generator (AI)", "story_points": 13,
     "status": "completed", "assignee": "Krishna Murthy",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 12, "item_type": "story",
     "title": "RPA Workflow Designer", "story_points": 8,
     "status": "completed", "assignee": "Nandini Sharma",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 12, "item_type": "story",
     "title": "Regression Suite Runner", "story_points": 10,
     "status": "completed", "assignee": "Arun Kapoor",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 12, "item_type": "story",
     "title": "Test Report Dashboard", "story_points": 8,
     "status": "completed", "assignee": "Divya Pillai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 12, "item_type": "task",
     "title": "Dockerise Test Environment", "story_points": 8,
     "status": "completed", "assignee": "Rajesh Nair",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "medium"},
    # planned sum=70, now add bonus 'added' stories (4 pts to reach completed=74)
    {"project_code": "SNTL-AUTO", "sprint_number": 12, "item_type": "spike",
     "title": "Evaluate AI Assertion Libraries", "story_points": 4,
     "status": "added", "assignee": "Siva Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # sum_planned=70, completed(all)+added=74 ✓

    # Sprint 13: planned=70, completed=78 → 8 pts from 'added' story
    # planned stories (completed only here) sum to 70; added (8) brings total to 78
    {"project_code": "SNTL-AUTO", "sprint_number": 13, "item_type": "story",
     "title": "BDD Scenario Engine", "story_points": 13,
     "status": "completed", "assignee": "Siva Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 13, "item_type": "story",
     "title": "Visual Regression Testing", "story_points": 10,
     "status": "completed", "assignee": "Pooja Reddy",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 13, "item_type": "story",
     "title": "Performance Baseline Profiler", "story_points": 13,
     "status": "completed", "assignee": "Krishna Murthy",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 13, "item_type": "story",
     "title": "Automated Release Notes (AI)", "story_points": 8,
     "status": "completed", "assignee": "Nandini Sharma",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 13, "item_type": "story",
     "title": "Parallel Test Execution Grid", "story_points": 10,
     "status": "completed", "assignee": "Arun Kapoor",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 13, "item_type": "task",
     "title": "Test Data Masking Pipeline", "story_points": 8,
     "status": "completed", "assignee": "Divya Pillai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 13, "item_type": "task",
     "title": "Dockerise Test Runner Infra", "story_points": 8,
     "status": "completed", "assignee": "Rajesh Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "low"},
    {"project_code": "SNTL-AUTO", "sprint_number": 13, "item_type": "story",
     "title": "Self-healing Test Selector (AI)", "story_points": 8,
     "status": "added", "assignee": "Siva Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    # planned sum=13+10+13+8+10+8+8=70, completed=70+8(added)=78 ✓

    # Sprint 14: planned=70, completed=82 → 12 pts 'added'
    {"project_code": "SNTL-AUTO", "sprint_number": 14, "item_type": "story",
     "title": "AI-driven Test Prioritisation", "story_points": 13,
     "status": "completed", "assignee": "Siva Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 14, "item_type": "story",
     "title": "Flaky Test Auto-quarantine", "story_points": 10,
     "status": "completed", "assignee": "Pooja Reddy",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 14, "item_type": "story",
     "title": "RPA Bot Scheduler", "story_points": 13,
     "status": "completed", "assignee": "Krishna Murthy",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 14, "item_type": "story",
     "title": "Test Coverage Reporter", "story_points": 8,
     "status": "completed", "assignee": "Nandini Sharma",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 14, "item_type": "story",
     "title": "Contract Testing Framework", "story_points": 10,
     "status": "completed", "assignee": "Arun Kapoor",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 14, "item_type": "story",
     "title": "Security Scan Integration", "story_points": 8,
     "status": "completed", "assignee": "Divya Pillai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 14, "item_type": "task",
     "title": "Pipeline Optimisation", "story_points": 8,
     "status": "completed", "assignee": "Rajesh Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "low"},
    {"project_code": "SNTL-AUTO", "sprint_number": 14, "item_type": "story",
     "title": "AI Anomaly Detection in Logs", "story_points": 12,
     "status": "added", "assignee": "Siva Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    # planned=70, completed=70+12=82 ✓

    # Sprint 15: planned=70, completed=85 → 15 pts 'added'
    {"project_code": "SNTL-AUTO", "sprint_number": 15, "item_type": "story",
     "title": "Smart Test Data Factory", "story_points": 13,
     "status": "completed", "assignee": "Siva Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 15, "item_type": "story",
     "title": "End-to-End Pipeline Validator", "story_points": 10,
     "status": "completed", "assignee": "Pooja Reddy",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 15, "item_type": "story",
     "title": "Automated DR Runbook", "story_points": 13,
     "status": "completed", "assignee": "Krishna Murthy",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 15, "item_type": "story",
     "title": "Test Infra as Code Module", "story_points": 8,
     "status": "completed", "assignee": "Nandini Sharma",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 15, "item_type": "story",
     "title": "Code Quality Gate Engine", "story_points": 10,
     "status": "completed", "assignee": "Arun Kapoor",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 15, "item_type": "story",
     "title": "Mutation Testing Integration", "story_points": 8,
     "status": "completed", "assignee": "Divya Pillai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 15, "item_type": "task",
     "title": "Alert Suppression Rules", "story_points": 8,
     "status": "completed", "assignee": "Rajesh Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "low"},
    {"project_code": "SNTL-AUTO", "sprint_number": 15, "item_type": "story",
     "title": "AI Test Script Reviewer", "story_points": 10,
     "status": "added", "assignee": "Siva Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 15, "item_type": "spike",
     "title": "Evaluate Playwright MCP Integration", "story_points": 5,
     "status": "added", "assignee": "Pooja Reddy",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # planned=70, completed=70+10+5=85 ✓

    # Sprint 16: planned=70, completed=88 → 18 pts 'added'
    {"project_code": "SNTL-AUTO", "sprint_number": 16, "item_type": "story",
     "title": "Predictive Sprint Planning (AI)", "story_points": 13,
     "status": "completed", "assignee": "Siva Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 16, "item_type": "story",
     "title": "Automated Acceptance Tests", "story_points": 10,
     "status": "completed", "assignee": "Pooja Reddy",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 16, "item_type": "story",
     "title": "Real-time Test Telemetry", "story_points": 13,
     "status": "completed", "assignee": "Krishna Murthy",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 16, "item_type": "story",
     "title": "Shift-left Security Tests", "story_points": 8,
     "status": "completed", "assignee": "Nandini Sharma",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 16, "item_type": "story",
     "title": "Test Environment Provisioner", "story_points": 10,
     "status": "completed", "assignee": "Arun Kapoor",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 16, "item_type": "story",
     "title": "Pipeline Dependency Mapper", "story_points": 8,
     "status": "completed", "assignee": "Divya Pillai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 16, "item_type": "task",
     "title": "Unified Test Metrics Export", "story_points": 8,
     "status": "completed", "assignee": "Rajesh Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "low"},
    {"project_code": "SNTL-AUTO", "sprint_number": 16, "item_type": "story",
     "title": "AI PR Reviewer Integration", "story_points": 13,
     "status": "added", "assignee": "Siva Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 16, "item_type": "story",
     "title": "Automated Changelog Generator", "story_points": 5,
     "status": "added", "assignee": "Pooja Reddy",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # planned=70, completed=70+13+5=88 ✓

    # Sprint 17: planned=70, completed=92 → 22 pts 'added'
    {"project_code": "SNTL-AUTO", "sprint_number": 17, "item_type": "story",
     "title": "Full Platform Regression Suite", "story_points": 13,
     "status": "completed", "assignee": "Siva Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 17, "item_type": "story",
     "title": "Automated DR Test Runner", "story_points": 10,
     "status": "completed", "assignee": "Pooja Reddy",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 17, "item_type": "story",
     "title": "Zero-config Test Discovery (AI)", "story_points": 13,
     "status": "completed", "assignee": "Krishna Murthy",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 17, "item_type": "story",
     "title": "Incident Root-cause Tagger (AI)", "story_points": 8,
     "status": "completed", "assignee": "Nandini Sharma",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "SNTL-AUTO", "sprint_number": 17, "item_type": "story",
     "title": "Cross-browser Test Matrix", "story_points": 10,
     "status": "completed", "assignee": "Arun Kapoor",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 17, "item_type": "story",
     "title": "Test Cost Analytics Dashboard", "story_points": 8,
     "status": "completed", "assignee": "Divya Pillai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 17, "item_type": "task",
     "title": "Test Platform Capacity Planning", "story_points": 8,
     "status": "completed", "assignee": "Rajesh Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "low"},
    {"project_code": "SNTL-AUTO", "sprint_number": 17, "item_type": "story",
     "title": "AI-generated E2E Scenarios", "story_points": 13,
     "status": "added", "assignee": "Siva Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "SNTL-AUTO", "sprint_number": 17, "item_type": "story",
     "title": "Copilot Pair-programming Sessions", "story_points": 9,
     "status": "added", "assignee": "Krishna Murthy",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    # planned=70, completed=70+13+9=92 ✓
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


# ---------------------------------------------------------------------------
# Waterfall deliverable items — TTN-STORE.
#
# For Waterfall projects, sprint_number maps to phase_sequence (1-6):
#   1 = Requirements  (completed)
#   2 = Design        (completed)
#   3 = Development   (in_progress, 62% complete)
#   4 = Test          (planned)
#   5 = UAT           (planned)
#   6 = Deploy        (planned)
#
# Team (9 people): Nisha Rao (PM/lead), Vijay Kumar, Ananya Mehta, Rohit Shah,
#   Preethi Krishnan, Santhosh Iyer, Neha Gupta, Arun Nair, Vivek Pillai
# ---------------------------------------------------------------------------

TTN_STORE_ITEMS: list[BacklogItemSeed] = [
    # ── Phase 1: Requirements (all completed) ───────────────────────────────
    {"project_code": "TTN-STORE", "sprint_number": 1, "item_type": "story",
     "title": "Business requirements specification — eCommerce platform scope", "story_points": 13,
     "status": "completed", "assignee": "Nisha Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 2.0, "priority": "critical"},
    {"project_code": "TTN-STORE", "sprint_number": 1, "item_type": "task",
     "title": "Stakeholder workshops — 6 sessions with J. Wilson and business units", "story_points": 8,
     "status": "completed", "assignee": "Nisha Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "TTN-STORE", "sprint_number": 1, "item_type": "story",
     "title": "Non-functional requirements — performance and security SLAs", "story_points": 8,
     "status": "completed", "assignee": "Vijay Kumar",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.5, "priority": "high"},
    {"project_code": "TTN-STORE", "sprint_number": 1, "item_type": "task",
     "title": "As-is process mapping — current order management workflow", "story_points": 5,
     "status": "completed", "assignee": "Ananya Mehta",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "TTN-STORE", "sprint_number": 1, "item_type": "task",
     "title": "Requirements traceability matrix (RTM) baseline", "story_points": 5,
     "status": "completed", "assignee": "Rohit Shah",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "TTN-STORE", "sprint_number": 1, "item_type": "task",
     "title": "Third-party integration catalogue — payment gateway, logistics API", "story_points": 5,
     "status": "completed", "assignee": "Preethi Krishnan",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},

    # ── Phase 2: Design (all completed) ─────────────────────────────────────
    {"project_code": "TTN-STORE", "sprint_number": 2, "item_type": "story",
     "title": "Solution architecture design — microservices vs monolith decision", "story_points": 13,
     "status": "completed", "assignee": "Vijay Kumar",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 2.0, "priority": "critical"},
    {"project_code": "TTN-STORE", "sprint_number": 2, "item_type": "story",
     "title": "UI/UX design — storefront wireframes and design system", "story_points": 10,
     "status": "completed", "assignee": "Ananya Mehta",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.5, "priority": "high"},
    {"project_code": "TTN-STORE", "sprint_number": 2, "item_type": "story",
     "title": "Database schema design — product, order, customer entities", "story_points": 10,
     "status": "completed", "assignee": "Rohit Shah",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "TTN-STORE", "sprint_number": 2, "item_type": "task",
     "title": "API contract specification — OpenAPI 3.0 for all services", "story_points": 8,
     "status": "completed", "assignee": "Preethi Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "TTN-STORE", "sprint_number": 2, "item_type": "task",
     "title": "Infrastructure design — AWS topology and capacity planning", "story_points": 8,
     "status": "completed", "assignee": "Santhosh Iyer",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "TTN-STORE", "sprint_number": 2, "item_type": "task",
     "title": "Security design — OWASP Top 10 threat model and controls", "story_points": 8,
     "status": "completed", "assignee": "Vijay Kumar",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "TTN-STORE", "sprint_number": 2, "item_type": "task",
     "title": "Integration design — payment gateway and logistics API adapters", "story_points": 5,
     "status": "completed", "assignee": "Neha Gupta",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},

    # ── Phase 3: Development (62% complete — 7 completed, 5 in_progress) ────
    {"project_code": "TTN-STORE", "sprint_number": 3, "item_type": "story",
     "title": "Product catalogue service — CRUD APIs + search (Elasticsearch)", "story_points": 13,
     "status": "completed", "assignee": "Rohit Shah",
     "is_ai_assisted": True, "defects_raised": 1, "rework_hours": 2.5, "priority": "critical"},
    {"project_code": "TTN-STORE", "sprint_number": 3, "item_type": "story",
     "title": "User authentication service — JWT + OAuth 2.0", "story_points": 10,
     "status": "completed", "assignee": "Preethi Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.5, "priority": "critical"},
    {"project_code": "TTN-STORE", "sprint_number": 3, "item_type": "story",
     "title": "Shopping cart service — add/remove, session persistence", "story_points": 10,
     "status": "completed", "assignee": "Santhosh Iyer",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "TTN-STORE", "sprint_number": 3, "item_type": "story",
     "title": "Payment gateway integration — Razorpay / Stripe", "story_points": 13,
     "status": "completed", "assignee": "Vijay Kumar",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 4.0, "priority": "critical"},
    {"project_code": "TTN-STORE", "sprint_number": 3, "item_type": "story",
     "title": "Order management service — placement, status, cancellation", "story_points": 13,
     "status": "completed", "assignee": "Arun Nair",
     "is_ai_assisted": True, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "TTN-STORE", "sprint_number": 3, "item_type": "task",
     "title": "CI/CD pipeline — GitHub Actions + ECS deployment", "story_points": 8,
     "status": "completed", "assignee": "Santhosh Iyer",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "TTN-STORE", "sprint_number": 3, "item_type": "story",
     "title": "Storefront UI — product listing and detail pages (React)", "story_points": 10,
     "status": "completed", "assignee": "Ananya Mehta",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.5, "priority": "high"},
    # In-progress items (62% done → remaining 38%)
    {"project_code": "TTN-STORE", "sprint_number": 3, "item_type": "story",
     "title": "Checkout flow — address, shipping selection, order confirmation", "story_points": 10,
     "status": "in_progress", "assignee": "Neha Gupta",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "critical"},
    {"project_code": "TTN-STORE", "sprint_number": 3, "item_type": "story",
     "title": "Inventory service — stock management and low-stock alerts", "story_points": 8,
     "status": "in_progress", "assignee": "Vivek Pillai",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "TTN-STORE", "sprint_number": 3, "item_type": "story",
     "title": "Notifications service — email/SMS order updates", "story_points": 8,
     "status": "in_progress", "assignee": "Arun Nair",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "TTN-STORE", "sprint_number": 3, "item_type": "story",
     "title": "Admin portal — product management and order oversight", "story_points": 10,
     "status": "in_progress", "assignee": "Rohit Shah",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "TTN-STORE", "sprint_number": 3, "item_type": "task",
     "title": "Logistics API integration — shipment tracking", "story_points": 8,
     "status": "in_progress", "assignee": "Preethi Krishnan",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},

    # ── Phase 4: Test (planned) ──────────────────────────────────────────────
    {"project_code": "TTN-STORE", "sprint_number": 4, "item_type": "story",
     "title": "System integration testing — end-to-end order flow", "story_points": 13,
     "status": "planned", "assignee": "Neha Gupta",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "critical"},
    {"project_code": "TTN-STORE", "sprint_number": 4, "item_type": "story",
     "title": "Performance testing — load and soak tests (k6)", "story_points": 10,
     "status": "planned", "assignee": "Vivek Pillai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "TTN-STORE", "sprint_number": 4, "item_type": "story",
     "title": "Security penetration testing — OWASP Top 10 validation", "story_points": 10,
     "status": "planned", "assignee": "Vijay Kumar",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "TTN-STORE", "sprint_number": 4, "item_type": "task",
     "title": "Regression test suite — automated E2E (Playwright)", "story_points": 8,
     "status": "planned", "assignee": "Arun Nair",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},

    # ── Phase 5: UAT (planned) ───────────────────────────────────────────────
    {"project_code": "TTN-STORE", "sprint_number": 5, "item_type": "story",
     "title": "UAT execution — business user acceptance across all modules", "story_points": 13,
     "status": "planned", "assignee": "Nisha Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "critical"},
    {"project_code": "TTN-STORE", "sprint_number": 5, "item_type": "task",
     "title": "UAT defect triage and resolution", "story_points": 10,
     "status": "planned", "assignee": "Ananya Mehta",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "TTN-STORE", "sprint_number": 5, "item_type": "task",
     "title": "Training material for business users — storefront + admin portal", "story_points": 5,
     "status": "planned", "assignee": "Nisha Rao",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},

    # ── Phase 6: Deploy (planned) ────────────────────────────────────────────
    {"project_code": "TTN-STORE", "sprint_number": 6, "item_type": "story",
     "title": "Production deployment — blue/green switch", "story_points": 8,
     "status": "planned", "assignee": "Santhosh Iyer",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "critical"},
    {"project_code": "TTN-STORE", "sprint_number": 6, "item_type": "task",
     "title": "DNS cutover and SSL certificate rotation", "story_points": 3,
     "status": "planned", "assignee": "Santhosh Iyer",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "critical"},
    {"project_code": "TTN-STORE", "sprint_number": 6, "item_type": "task",
     "title": "Hypercare period — 30-day post-launch monitoring", "story_points": 5,
     "status": "planned", "assignee": "Nisha Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
]


# ---------------------------------------------------------------------------
# Kanban flow items — individual work items for ATLS-LNS and ORN-INGEST.
#
# For Kanban projects we don't have sprints, so sprint_number represents the
# week number (1-12) matching the corresponding FlowMetrics row.  Status:
#   completed  — item exited the board (Done) in that week
#   in_progress — item was WIP at week end (contributes to wip_avg count)
# story_points represents t-shirt sizing / effort estimate; used for totals.
# ---------------------------------------------------------------------------

# ATLS-LNS — Lift & Shift Workstream (AWS migration, Kanban, 10 people)
# Team: Kiran Raju, Meghna Desai, Naveen Pillai, Ojas Sharma, Parvathi Iyer,
#       Qadir Shah, Rohit Nair, Sachin Gupta, Tanya Mehta, Uday Kumar
_ATLS_TEAM = [
    "Kiran Raju", "Meghna Desai", "Naveen Pillai", "Ojas Sharma", "Parvathi Iyer",
    "Qadir Shah", "Rohit Nair", "Sachin Gupta", "Tanya Mehta", "Uday Kumar",
]

# ORN-INGEST — Orion Ingestion Pipeline (Airflow/Snowflake, Kanban, 14 people)
# Team: Aakash Singh, Bhanu Prasad, Chetan Iyer, Deepa Nair, Ekta Sharma,
#       Firoz Khan, Gita Reddy, Harish Kumar, Ishita Rao, Jatin Mehta,
#       Kavya Pillai, Lokesh Nair, Mani Rajan, Nisha Kumar
_ORN_TEAM = [
    "Aakash Singh", "Bhanu Prasad", "Chetan Iyer", "Deepa Nair", "Ekta Sharma",
    "Firoz Khan", "Gita Reddy", "Harish Kumar", "Ishita Rao", "Jatin Mehta",
    "Kavya Pillai", "Lokesh Nair", "Mani Rajan", "Nisha Kumar",
]

KANBAN_FLOW_ITEMS: list[BacklogItemSeed] = [
    # ── ATLS-LNS Weeks 1–4 (throughput: 8, 9, 7, 10) ──
    # Week 1 — 8 completed
    {"project_code": "ATLS-LNS", "sprint_number": 1, "item_type": "task",
     "title": "Migrate EC2 batch A (prod)", "story_points": 5,
     "status": "completed", "assignee": "Kiran Raju",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "ATLS-LNS", "sprint_number": 1, "item_type": "task",
     "title": "S3 bucket policy standardisation", "story_points": 3,
     "status": "completed", "assignee": "Meghna Desai",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "ATLS-LNS", "sprint_number": 1, "item_type": "story",
     "title": "VPC peering PROD→DR", "story_points": 8,
     "status": "completed", "assignee": "Naveen Pillai",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "ATLS-LNS", "sprint_number": 1, "item_type": "task",
     "title": "IAM role cleanup (stale policies)", "story_points": 3,
     "status": "completed", "assignee": "Ojas Sharma",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "ATLS-LNS", "sprint_number": 1, "item_type": "task",
     "title": "Terraform state migration", "story_points": 5,
     "status": "completed", "assignee": "Parvathi Iyer",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "ATLS-LNS", "sprint_number": 1, "item_type": "story",
     "title": "Auto-scaling group config", "story_points": 5,
     "status": "completed", "assignee": "Qadir Shah",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "ATLS-LNS", "sprint_number": 1, "item_type": "task",
     "title": "CloudWatch alarms baseline", "story_points": 3,
     "status": "completed", "assignee": "Rohit Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "ATLS-LNS", "sprint_number": 1, "item_type": "task",
     "title": "DNS cutover runbook", "story_points": 3,
     "status": "completed", "assignee": "Sachin Gupta",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # WIP items at end of week 1
    {"project_code": "ATLS-LNS", "sprint_number": 1, "item_type": "story",
     "title": "RDS multi-AZ failover setup", "story_points": 8,
     "status": "in_progress", "assignee": "Tanya Mehta",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "ATLS-LNS", "sprint_number": 1, "item_type": "story",
     "title": "CloudFront CDN migration", "story_points": 5,
     "status": "in_progress", "assignee": "Uday Kumar",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},

    # Week 2 — 9 completed
    {"project_code": "ATLS-LNS", "sprint_number": 2, "item_type": "story",
     "title": "RDS multi-AZ failover setup", "story_points": 8,
     "status": "completed", "assignee": "Tanya Mehta",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "ATLS-LNS", "sprint_number": 2, "item_type": "story",
     "title": "CloudFront CDN migration", "story_points": 5,
     "status": "completed", "assignee": "Uday Kumar",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "ATLS-LNS", "sprint_number": 2, "item_type": "task",
     "title": "WAF rule set deployment", "story_points": 5,
     "status": "completed", "assignee": "Kiran Raju",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "ATLS-LNS", "sprint_number": 2, "item_type": "task",
     "title": "ELB listener rules migration", "story_points": 3,
     "status": "completed", "assignee": "Meghna Desai",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "ATLS-LNS", "sprint_number": 2, "item_type": "story",
     "title": "EKS cluster v1.29 upgrade", "story_points": 8,
     "status": "completed", "assignee": "Naveen Pillai",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 3.0, "priority": "critical"},
    {"project_code": "ATLS-LNS", "sprint_number": 2, "item_type": "task",
     "title": "Cost anomaly detection rules", "story_points": 3,
     "status": "completed", "assignee": "Ojas Sharma",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "ATLS-LNS", "sprint_number": 2, "item_type": "task",
     "title": "Secrets Manager rotation policy", "story_points": 5,
     "status": "completed", "assignee": "Parvathi Iyer",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "ATLS-LNS", "sprint_number": 2, "item_type": "task",
     "title": "GuardDuty baseline findings", "story_points": 3,
     "status": "completed", "assignee": "Qadir Shah",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "ATLS-LNS", "sprint_number": 2, "item_type": "story",
     "title": "Route53 health check config", "story_points": 5,
     "status": "completed", "assignee": "Rohit Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},

    # Week 3 — 7 completed (slight dip in throughput)
    {"project_code": "ATLS-LNS", "sprint_number": 3, "item_type": "story",
     "title": "Aurora cluster migration", "story_points": 13,
     "status": "completed", "assignee": "Sachin Gupta",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 5.0, "priority": "critical"},
    {"project_code": "ATLS-LNS", "sprint_number": 3, "item_type": "task",
     "title": "S3 lifecycle policy rollout", "story_points": 3,
     "status": "completed", "assignee": "Tanya Mehta",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "ATLS-LNS", "sprint_number": 3, "item_type": "task",
     "title": "EC2 Reserved Instance tagging", "story_points": 3,
     "status": "completed", "assignee": "Uday Kumar",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "ATLS-LNS", "sprint_number": 3, "item_type": "story",
     "title": "VPN mesh topology rework", "story_points": 8,
     "status": "completed", "assignee": "Kiran Raju",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 3.0, "priority": "high"},
    {"project_code": "ATLS-LNS", "sprint_number": 3, "item_type": "task",
     "title": "CloudTrail multi-region enable", "story_points": 3,
     "status": "completed", "assignee": "Meghna Desai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "ATLS-LNS", "sprint_number": 3, "item_type": "story",
     "title": "Container image scan pipeline", "story_points": 5,
     "status": "completed", "assignee": "Naveen Pillai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "ATLS-LNS", "sprint_number": 3, "item_type": "task",
     "title": "Patch compliance baseline", "story_points": 3,
     "status": "completed", "assignee": "Ojas Sharma",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},

    # Week 4 — 10 completed
    {"project_code": "ATLS-LNS", "sprint_number": 4, "item_type": "story",
     "title": "EKS add-on upgrades (CoreDNS, kube-proxy)", "story_points": 8,
     "status": "completed", "assignee": "Parvathi Iyer",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "ATLS-LNS", "sprint_number": 4, "item_type": "task",
     "title": "SQS dead letter queue setup", "story_points": 3,
     "status": "completed", "assignee": "Qadir Shah",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "ATLS-LNS", "sprint_number": 4, "item_type": "task",
     "title": "SNS topic encryption", "story_points": 3,
     "status": "completed", "assignee": "Rohit Nair",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "ATLS-LNS", "sprint_number": 4, "item_type": "story",
     "title": "Cross-account IAM federation", "story_points": 8,
     "status": "completed", "assignee": "Sachin Gupta",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "ATLS-LNS", "sprint_number": 4, "item_type": "story",
     "title": "Migrate batch jobs to Step Functions", "story_points": 8,
     "status": "completed", "assignee": "Tanya Mehta",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "medium"},
    {"project_code": "ATLS-LNS", "sprint_number": 4, "item_type": "task",
     "title": "Lambda cold-start profiling", "story_points": 3,
     "status": "completed", "assignee": "Uday Kumar",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "ATLS-LNS", "sprint_number": 4, "item_type": "task",
     "title": "ACM cert renewal automation", "story_points": 3,
     "status": "completed", "assignee": "Kiran Raju",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "ATLS-LNS", "sprint_number": 4, "item_type": "story",
     "title": "Service catalog product template", "story_points": 5,
     "status": "completed", "assignee": "Meghna Desai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "ATLS-LNS", "sprint_number": 4, "item_type": "task",
     "title": "Config rules compliance report", "story_points": 3,
     "status": "completed", "assignee": "Naveen Pillai",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "ATLS-LNS", "sprint_number": 4, "item_type": "bug",
     "title": "Fix EKS node drain timeout bug", "story_points": 5,
     "status": "completed", "assignee": "Ojas Sharma",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},

    # ── ORN-INGEST Weeks 1–4 (throughput declining: 10, 10, 9, 8) ──
    # Week 1 — 10 completed, high throughput (bench tax starting to show from week 3)
    {"project_code": "ORN-INGEST", "sprint_number": 1, "item_type": "story",
     "title": "Airflow DAG — Customer data ingest", "story_points": 8,
     "status": "completed", "assignee": "Aakash Singh",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "ORN-INGEST", "sprint_number": 1, "item_type": "story",
     "title": "Snowflake schema DDL — Bronze layer", "story_points": 5,
     "status": "completed", "assignee": "Bhanu Prasad",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "ORN-INGEST", "sprint_number": 1, "item_type": "task",
     "title": "dbt model — customer_dim", "story_points": 5,
     "status": "completed", "assignee": "Chetan Iyer",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "ORN-INGEST", "sprint_number": 1, "item_type": "task",
     "title": "dbt model — transaction_fact", "story_points": 5,
     "status": "completed", "assignee": "Deepa Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "ORN-INGEST", "sprint_number": 1, "item_type": "story",
     "title": "Kafka consumer — risk events", "story_points": 8,
     "status": "completed", "assignee": "Ekta Sharma",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "ORN-INGEST", "sprint_number": 1, "item_type": "task",
     "title": "Data quality rule set v1", "story_points": 5,
     "status": "completed", "assignee": "Firoz Khan",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "ORN-INGEST", "sprint_number": 1, "item_type": "task",
     "title": "PII masking config", "story_points": 5,
     "status": "completed", "assignee": "Gita Reddy",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "ORN-INGEST", "sprint_number": 1, "item_type": "story",
     "title": "Airflow DAG — Product catalogue sync", "story_points": 8,
     "status": "completed", "assignee": "Harish Kumar",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "ORN-INGEST", "sprint_number": 1, "item_type": "task",
     "title": "Snowflake RBAC roles setup", "story_points": 3,
     "status": "completed", "assignee": "Ishita Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "ORN-INGEST", "sprint_number": 1, "item_type": "task",
     "title": "Pipeline monitoring dashboard v1", "story_points": 5,
     "status": "completed", "assignee": "Jatin Mehta",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},

    # Week 2 — 10 completed (still healthy)
    {"project_code": "ORN-INGEST", "sprint_number": 2, "item_type": "story",
     "title": "Airflow DAG — Trade finance ingest", "story_points": 8,
     "status": "completed", "assignee": "Kavya Pillai",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "ORN-INGEST", "sprint_number": 2, "item_type": "story",
     "title": "CDC pipeline — Core Banking", "story_points": 13,
     "status": "completed", "assignee": "Lokesh Nair",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 3.0, "priority": "critical"},
    {"project_code": "ORN-INGEST", "sprint_number": 2, "item_type": "task",
     "title": "dbt model — account_summary", "story_points": 5,
     "status": "completed", "assignee": "Mani Rajan",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "ORN-INGEST", "sprint_number": 2, "item_type": "task",
     "title": "Data catalog — lineage tags", "story_points": 5,
     "status": "completed", "assignee": "Nisha Kumar",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "ORN-INGEST", "sprint_number": 2, "item_type": "story",
     "title": "Kafka schema registry setup", "story_points": 8,
     "status": "completed", "assignee": "Aakash Singh",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "ORN-INGEST", "sprint_number": 2, "item_type": "task",
     "title": "Great Expectations — Bronze checks", "story_points": 5,
     "status": "completed", "assignee": "Bhanu Prasad",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "ORN-INGEST", "sprint_number": 2, "item_type": "task",
     "title": "dbt test suite baseline", "story_points": 5,
     "status": "completed", "assignee": "Chetan Iyer",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "ORN-INGEST", "sprint_number": 2, "item_type": "story",
     "title": "Silver layer transformation model", "story_points": 8,
     "status": "completed", "assignee": "Deepa Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "ORN-INGEST", "sprint_number": 2, "item_type": "task",
     "title": "Airflow connections vault sync", "story_points": 3,
     "status": "completed", "assignee": "Ekta Sharma",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "ORN-INGEST", "sprint_number": 2, "item_type": "task",
     "title": "Snowflake cost tag governance", "story_points": 3,
     "status": "completed", "assignee": "Firoz Khan",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},

    # Week 3 — 9 completed (bench tax beginning to slow throughput)
    {"project_code": "ORN-INGEST", "sprint_number": 3, "item_type": "story",
     "title": "Gold layer — KPI aggregation model", "story_points": 13,
     "status": "completed", "assignee": "Gita Reddy",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 4.0, "priority": "high"},
    {"project_code": "ORN-INGEST", "sprint_number": 3, "item_type": "story",
     "title": "Airflow DAG — Collateral data", "story_points": 8,
     "status": "completed", "assignee": "Harish Kumar",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.5, "priority": "high"},
    {"project_code": "ORN-INGEST", "sprint_number": 3, "item_type": "task",
     "title": "dbt model — collateral_fact", "story_points": 5,
     "status": "completed", "assignee": "Ishita Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "ORN-INGEST", "sprint_number": 3, "item_type": "story",
     "title": "Retry / DLQ framework for DAGs", "story_points": 8,
     "status": "completed", "assignee": "Jatin Mehta",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 3.0, "priority": "high"},
    {"project_code": "ORN-INGEST", "sprint_number": 3, "item_type": "task",
     "title": "Data quality — Silver rule set v2", "story_points": 5,
     "status": "completed", "assignee": "Kavya Pillai",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "ORN-INGEST", "sprint_number": 3, "item_type": "task",
     "title": "Snowflake materialized view refresh", "story_points": 5,
     "status": "completed", "assignee": "Lokesh Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "ORN-INGEST", "sprint_number": 3, "item_type": "bug",
     "title": "Fix CDC offset drift on restart", "story_points": 8,
     "status": "completed", "assignee": "Mani Rajan",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "critical"},
    {"project_code": "ORN-INGEST", "sprint_number": 3, "item_type": "task",
     "title": "Lineage graph for trade finance", "story_points": 5,
     "status": "completed", "assignee": "Nisha Kumar",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "low"},
    {"project_code": "ORN-INGEST", "sprint_number": 3, "item_type": "task",
     "title": "Pipeline SLA alert rules", "story_points": 3,
     "status": "completed", "assignee": "Aakash Singh",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},

    # Week 4 — 8 completed (throughput declining, blocked hours increasing)
    {"project_code": "ORN-INGEST", "sprint_number": 4, "item_type": "story",
     "title": "Streaming ingest — real-time fraud scores", "story_points": 13,
     "status": "completed", "assignee": "Bhanu Prasad",
     "is_ai_assisted": False, "defects_raised": 3, "rework_hours": 6.0, "priority": "critical"},
    {"project_code": "ORN-INGEST", "sprint_number": 4, "item_type": "story",
     "title": "Gold layer — CSAT dashboard model", "story_points": 8,
     "status": "completed", "assignee": "Chetan Iyer",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 4.0, "priority": "high"},
    {"project_code": "ORN-INGEST", "sprint_number": 4, "item_type": "task",
     "title": "dbt model — risk_exposure_summary", "story_points": 5,
     "status": "completed", "assignee": "Deepa Nair",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "medium"},
    {"project_code": "ORN-INGEST", "sprint_number": 4, "item_type": "story",
     "title": "CDC pipeline — Payments ledger", "story_points": 13,
     "status": "completed", "assignee": "Ekta Sharma",
     "is_ai_assisted": False, "defects_raised": 2, "rework_hours": 5.0, "priority": "critical"},
    {"project_code": "ORN-INGEST", "sprint_number": 4, "item_type": "task",
     "title": "Great Expectations — Gold checks", "story_points": 5,
     "status": "completed", "assignee": "Firoz Khan",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "ORN-INGEST", "sprint_number": 4, "item_type": "bug",
     "title": "Fix Snowflake merge key collision", "story_points": 8,
     "status": "completed", "assignee": "Gita Reddy",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "critical"},
    {"project_code": "ORN-INGEST", "sprint_number": 4, "item_type": "task",
     "title": "Refresh dbt documentation site", "story_points": 3,
     "status": "completed", "assignee": "Harish Kumar",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "ORN-INGEST", "sprint_number": 4, "item_type": "task",
     "title": "Bench resource onboarding pack", "story_points": 3,
     "status": "in_progress", "assignee": "Ishita Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
]


