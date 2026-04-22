"""Bharat Digital Spine programme — Indian-themed demo seed (added v5.6).

New programme added to exercise every tab end-to-end with fresh data.
Two projects:
  BHARAT-UPI       — UPI 2.0 Core Modernization (Waterfall, Light AI)
  BHARAT-CITIZEN   — Swayam Citizen Mobile App (Scrum, Heavy AI)

BAC: ₹12,500,000 | Status: On Track | Start: 2026-01-15 | End: 2027-12-31

The Waterfall project exercises the new phase_deliverables table. The Scrum
project exercises the full sprint → backlog-items drill with AI augmentation.
"""
from __future__ import annotations

from datetime import date, datetime

from app.seed.ai_data import (
    AiCodeMetricsSeed,
    AiOverrideLogSeed,
    AiSdlcMetricsSeed,
    AiToolAssignmentSeed,
    AiTrustScoreSeed,
    AiUsageMetricsSeed,
)
from app.seed.commercial_data import (
    BlendRuleSeed,
    ChangeRequestSeed,
    CommercialSeed,
    LossSeed,
    RateCardSeed,
    SprintVelocityDualSeed,
)
from app.seed.customer_data import CustomerSatisfactionSeed, SlaIncidentSeed
from app.seed.data import (
    CustomerActionSeed,
    CustomerExpectationSeed,
    ProgrammeSeed,
    ProjectSeed,
    RiskSeed,
)
from app.seed.delivery_data import (
    BacklogItemSeed,
    EvmSnapshotSeed,
    MilestoneSeed,
    PhaseDeliverableSeed,
    ProjectPhaseSeed,
    SprintSeed,
)

# ===========================================================================
# Programme
# ===========================================================================

BHARAT_PROGRAMME: ProgrammeSeed = {
    "name": "Bharat Digital Spine",
    "code": "BHARAT",
    "client": "Ministry of Digital Infrastructure",
    "start_date": date(2026, 1, 15),
    "end_date": date(2027, 12, 31),
    "status": "On Track",
    "bac": 12_500_000,
    "revenue": 12_500_000,
    "team_size": 28,
    "offshore_ratio": 0.65,
    "delivery_model": "Fixed Price + Managed Services",
    "currency_code": "INR",
}


# ===========================================================================
# Projects
# ===========================================================================

BHARAT_PROJECTS: list[ProjectSeed] = [
    {
        "program_code": "BHARAT",
        "name": "UPI 2.0 Core Modernization",
        "code": "BHARAT-UPI",
        "start_date": date(2026, 1, 15),
        "end_date": date(2027, 6, 30),
        "bac": 6_800_000,
        "revenue": 6_800_000,
        "team_size": 14,
        "tech_stack": "Java, Spring, Kafka, PostgreSQL, HSM integration",
        "is_ai_augmented": True,
        "ai_augmentation_level": "Light",
        "delivery_methodology": "Waterfall",
    },
    {
        "program_code": "BHARAT",
        "name": "Swayam Citizen Mobile App",
        "code": "BHARAT-CITIZEN",
        "start_date": date(2026, 2, 1),
        "end_date": date(2027, 8, 31),
        "bac": 5_700_000,
        "revenue": 5_700_000,
        "team_size": 14,
        "tech_stack": "React Native, Node.js, Redis, AWS",
        "is_ai_augmented": True,
        "ai_augmentation_level": "Heavy",
        "delivery_methodology": "Scrum",
    },
]


# ===========================================================================
# KPI snapshots (monthly, Apr 2026 – Mar 2027 — 12 points)
# Shares the global MONTH_STARTS? — no, BHARAT started later, so uses its own.
# ===========================================================================

BHARAT_MONTH_STARTS: list[date] = [
    date(2026, 2, 1),
    date(2026, 3, 1),
    date(2026, 4, 1),
    date(2026, 5, 1),
    date(2026, 6, 1),
    date(2026, 7, 1),
    date(2026, 8, 1),
    date(2026, 9, 1),
    date(2026, 10, 1),
    date(2026, 11, 1),
    date(2026, 12, 1),
    date(2027, 1, 1),
]

BHARAT_MONTHLY_KPI_VALUES: dict[tuple[str, str], list[float]] = {
    ("BHARAT", "CPI"): [1.00, 1.02, 1.03, 1.04, 1.05, 1.05, 1.06, 1.06, 1.07, 1.07, 1.08, 1.08],
    ("BHARAT", "SPI"): [1.00, 1.00, 1.01, 1.01, 1.02, 1.02, 1.03, 1.03, 1.04, 1.04, 1.04, 1.05],
    ("BHARAT", "MARGIN"): [0.22, 0.22, 0.23, 0.23, 0.23, 0.24, 0.24, 0.24, 0.25, 0.25, 0.25, 0.26],
    ("BHARAT", "UTIL"): [0.80, 0.82, 0.84, 0.85, 0.86, 0.87, 0.87, 0.88, 0.88, 0.89, 0.89, 0.90],
    ("BHARAT", "REV_REAL"): [0.95, 0.96, 0.97, 0.97, 0.98, 0.98, 0.99, 0.99, 1.00, 1.00, 1.00, 1.01],
    ("BHARAT", "TEST_COV"): [0.70, 0.72, 0.74, 0.76, 0.78, 0.79, 0.81, 0.82, 0.83, 0.84, 0.85, 0.85],
    ("BHARAT", "OTD"): [0.92, 0.93, 0.94, 0.95, 0.95, 0.96, 0.96, 0.97, 0.97, 0.97, 0.98, 0.98],
    ("BHARAT", "AI_TRUST"): [70, 72, 74, 75, 77, 78, 79, 80, 81, 82, 82, 83],
    ("BHARAT", "AI_UPLIFT"): [0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.19, 0.20, 0.21, 0.22, 0.23, 0.24],
    ("BHARAT", "ATTRITION"): [0.08, 0.08, 0.07, 0.07, 0.07, 0.06, 0.06, 0.06, 0.06, 0.05, 0.05, 0.05],
    ("BHARAT", "FORECAST_ACC"): [0.92, 0.93, 0.93, 0.94, 0.94, 0.95, 0.95, 0.96, 0.96, 0.96, 0.97, 0.97],
    ("BHARAT", "DEFECT_DENSITY"): [1.5, 1.4, 1.3, 1.2, 1.2, 1.1, 1.1, 1.0, 1.0, 0.9, 0.9, 0.9],
    ("BHARAT", "CRIT_DEFECTS"): [0.06, 0.06, 0.05, 0.05, 0.04, 0.04, 0.04, 0.03, 0.03, 0.03, 0.02, 0.02],
}


# ===========================================================================
# Risks
# ===========================================================================

BHARAT_RISKS: list[RiskSeed] = [
    {
        "program_code": "BHARAT",
        "title": "HSM vendor certification delay",
        "description": "UPI 2.0 core requires hardware security module re-certification; vendor SLA is 10 weeks but has slipped on similar engagements.",
        "category": "Technical",
        "severity": "High",
        "probability": 0.55,
        "impact": 1_200_000,
        "mitigation_plan": "Parallel-track certification with two HSM vendors; escalate weekly to NPCI liaison.",
        "owner": "Raj Kumar",
        "status": "Open",
    },
    {
        "program_code": "BHARAT",
        "title": "RBI regulatory clarification pending",
        "description": "Swayam app's merchant QR feature awaits RBI clarification on transaction limit thresholds.",
        "category": "Regulatory",
        "severity": "High",
        "probability": 0.35,
        "impact": 900_000,
        "mitigation_plan": "Build feature behind toggle; launch only after clarification; weekly sync with ministry legal team.",
        "owner": "Priya Sharma",
        "status": "Mitigating",
    },
    {
        "program_code": "BHARAT",
        "title": "React Native performance on low-end devices",
        "description": "Swayam app must perform on sub-₹10,000 Android devices widely used in Tier 3-4 cities.",
        "category": "Technical",
        "severity": "Medium",
        "probability": 0.45,
        "impact": 450_000,
        "mitigation_plan": "Native modules for critical paths; rollout A/B on real devices in Jaipur + Lucknow test bed.",
        "owner": "Kavya Nair",
        "status": "Open",
    },
    {
        "program_code": "BHARAT",
        "title": "Citizen data localisation audit",
        "description": "Indian data-localisation laws require all PII in Indian AZs. AWS Mumbai-only architecture must be audited.",
        "category": "Compliance",
        "severity": "Medium",
        "probability": 0.30,
        "impact": 350_000,
        "mitigation_plan": "Engage legal + CERT-In accredited auditor; complete before UAT entry.",
        "owner": "Nisha Rao",
        "status": "Open",
    },
    {
        "program_code": "BHARAT",
        "title": "AI code-assistant licence renewal",
        "description": "Existing Copilot Enterprise licence expires mid-programme; Ministry procurement cycle is 90 days.",
        "category": "Commercial",
        "severity": "Low",
        "probability": 0.25,
        "impact": 120_000,
        "mitigation_plan": "Raise renewal PR 120 days ahead; budget for 3-month bridge licence if needed.",
        "owner": "Suresh Menon",
        "status": "Monitoring",
    },
    {
        "program_code": "BHARAT",
        "title": "Peak-hour load from UPI circuit breakers",
        "description": "Planned launch overlaps Diwali transaction peak; load profile may spike 10x baseline.",
        "category": "Technical",
        "severity": "High",
        "probability": 0.50,
        "impact": 800_000,
        "mitigation_plan": "Dedicated load-test environment with synthetic Diwali traffic; circuit-breaker tuning; staged rollout.",
        "owner": "Raj Kumar",
        "status": "Mitigating",
    },
    {
        "program_code": "BHARAT",
        "title": "Offshore-onshore timezone friction for go-live",
        "description": "Go-live weekend requires onshore + offshore joint command — existing ritual has 8h handoff gap.",
        "category": "Operational",
        "severity": "Low",
        "probability": 0.40,
        "impact": 100_000,
        "mitigation_plan": "Dry-run cutover 2 weeks before; follow-the-sun command rota; dedicated Slack war-room.",
        "owner": "Suresh Menon",
        "status": "Open",
    },
]


# ===========================================================================
# Sprints (Scrum project: BHARAT-CITIZEN) — 8 sprints
# ===========================================================================

BHARAT_SPRINTS: list[SprintSeed] = [
    # Header numbers below are DERIVED from BHARAT_BACKLOG_ITEMS so Adi's
    # traceability rule holds: clicking planned/completed/AI cards shows a
    # list whose story_points sum exactly equals the card value.
    {"project_code": "BHARAT-CITIZEN", "sprint_number": 1, "start_date": date(2026, 2, 2), "end_date": date(2026, 2, 15), "planned_points": 42, "completed_points": 38, "velocity": 38, "defects_found": 1, "defects_fixed": 0, "rework_hours": 4.0, "team_size": 14, "ai_assisted_points": 16, "iteration_type": "2-week", "estimation_unit": "story_points"},
    {"project_code": "BHARAT-CITIZEN", "sprint_number": 2, "start_date": date(2026, 2, 16), "end_date": date(2026, 3, 1), "planned_points": 45, "completed_points": 45, "velocity": 45, "defects_found": 0, "defects_fixed": 1, "rework_hours": 1.0, "team_size": 14, "ai_assisted_points": 21, "iteration_type": "2-week", "estimation_unit": "story_points"},
    {"project_code": "BHARAT-CITIZEN", "sprint_number": 3, "start_date": date(2026, 3, 2), "end_date": date(2026, 3, 15), "planned_points": 46, "completed_points": 46, "velocity": 46, "defects_found": 1, "defects_fixed": 1, "rework_hours": 2.0, "team_size": 14, "ai_assisted_points": 21, "iteration_type": "2-week", "estimation_unit": "story_points"},
    {"project_code": "BHARAT-CITIZEN", "sprint_number": 4, "start_date": date(2026, 3, 16), "end_date": date(2026, 3, 29), "planned_points": 48, "completed_points": 48, "velocity": 48, "defects_found": 1, "defects_fixed": 1, "rework_hours": 3.0, "team_size": 14, "ai_assisted_points": 26, "iteration_type": "2-week", "estimation_unit": "story_points"},
    {"project_code": "BHARAT-CITIZEN", "sprint_number": 5, "start_date": date(2026, 3, 30), "end_date": date(2026, 4, 12), "planned_points": 52, "completed_points": 52, "velocity": 52, "defects_found": 0, "defects_fixed": 0, "rework_hours": 0.0, "team_size": 14, "ai_assisted_points": 26, "iteration_type": "2-week", "estimation_unit": "story_points"},
    {"project_code": "BHARAT-CITIZEN", "sprint_number": 6, "start_date": date(2026, 4, 13), "end_date": date(2026, 4, 26), "planned_points": 55, "completed_points": 47, "velocity": 47, "defects_found": 5, "defects_fixed": 4, "rework_hours": 12.0, "team_size": 14, "ai_assisted_points": 21, "iteration_type": "2-week", "estimation_unit": "story_points"},
    {"project_code": "BHARAT-CITIZEN", "sprint_number": 7, "start_date": date(2026, 4, 27), "end_date": date(2026, 5, 10), "planned_points": 54, "completed_points": 54, "velocity": 54, "defects_found": 1, "defects_fixed": 1, "rework_hours": 3.0, "team_size": 14, "ai_assisted_points": 29, "iteration_type": "2-week", "estimation_unit": "story_points"},
    {"project_code": "BHARAT-CITIZEN", "sprint_number": 8, "start_date": date(2026, 5, 11), "end_date": date(2026, 5, 24), "planned_points": 56, "completed_points": 52, "velocity": 52, "defects_found": 1, "defects_fixed": 0, "rework_hours": 4.0, "team_size": 14, "ai_assisted_points": 29, "iteration_type": "2-week", "estimation_unit": "story_points"},
]


# ===========================================================================
# Backlog items (Scrum project) — spans sprints 1-8 with realistic mix
# For each sprint we want items whose story_points sum to the completed_points
# value in SPRINTS above (so the drill reconciles). Planned items include a
# few "not completed" rows with matching status.
# ===========================================================================


def _b(
    *,
    code: str,
    sprint: int,
    title: str,
    item_type: str,
    points: int,
    status: str,
    assignee: str,
    ai: bool = False,
    defects: int = 0,
    rework: float = 0.0,
    priority: str = "medium",
) -> BacklogItemSeed:
    return {
        "project_code": code,
        "sprint_number": sprint,
        "item_type": item_type,
        "title": title,
        "story_points": points,
        "status": status,
        "assignee": assignee,
        "is_ai_assisted": ai,
        "defects_raised": defects,
        "rework_hours": rework,
        "priority": priority,
    }


BHARAT_BACKLOG_ITEMS: list[BacklogItemSeed] = [
    # Sprint 1 — planned 42, completed 38 (shortfall 4 → 1 item carried_over)
    _b(code="BHARAT-CITIZEN", sprint=1, title="Citizen login via DigiLocker OAuth", item_type="story", points=8, status="completed", assignee="Kavya Nair", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=1, title="Aadhaar-linked profile screen", item_type="story", points=8, status="completed", assignee="Priya Sharma", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=1, title="UPI collect request flow", item_type="story", points=8, status="completed", assignee="Raj Kumar"),
    _b(code="BHARAT-CITIZEN", sprint=1, title="Transaction history list view", item_type="story", points=5, status="completed", assignee="Kavya Nair"),
    _b(code="BHARAT-CITIZEN", sprint=1, title="Base app scaffold + CI pipeline", item_type="task", points=5, status="completed", assignee="Meera Iyer"),
    _b(code="BHARAT-CITIZEN", sprint=1, title="Refactor auth token refresh", item_type="task", points=4, status="completed", assignee="Anand Verma"),
    _b(code="BHARAT-CITIZEN", sprint=1, title="Low-memory crash on splash", item_type="bug", points=4, status="carried_over", assignee="Kavya Nair", defects=1, rework=4.0, priority="high"),
    # Sprint 2 — planned 45, completed 42
    _b(code="BHARAT-CITIZEN", sprint=2, title="QR code scan & pay", item_type="story", points=13, status="completed", assignee="Raj Kumar", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=2, title="Merchant VPA lookup", item_type="story", points=8, status="completed", assignee="Priya Sharma"),
    _b(code="BHARAT-CITIZEN", sprint=2, title="PIN entry keyboard UI", item_type="story", points=8, status="completed", assignee="Kavya Nair", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=2, title="Biometric unlock (fingerprint)", item_type="story", points=8, status="completed", assignee="Anand Verma"),
    _b(code="BHARAT-CITIZEN", sprint=2, title="Localization pipeline (Hindi + Tamil)", item_type="task", points=5, status="completed", assignee="Meera Iyer"),
    _b(code="BHARAT-CITIZEN", sprint=2, title="Low-memory crash on splash (carry)", item_type="bug", points=3, status="completed", assignee="Kavya Nair", defects=0, rework=1.0),
    # Sprint 3 — planned 48, completed 46
    _b(code="BHARAT-CITIZEN", sprint=3, title="Beneficiary management CRUD", item_type="story", points=13, status="completed", assignee="Priya Sharma", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=3, title="Payment limit prompts + RBI compliance", item_type="story", points=8, status="completed", assignee="Raj Kumar"),
    _b(code="BHARAT-CITIZEN", sprint=3, title="Retry & timeout handling for UPI", item_type="story", points=8, status="completed", assignee="Anand Verma", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=3, title="Dashboard home screen redesign", item_type="story", points=5, status="completed", assignee="Kavya Nair"),
    _b(code="BHARAT-CITIZEN", sprint=3, title="Crashlytics + Grafana wiring", item_type="task", points=5, status="completed", assignee="Meera Iyer"),
    _b(code="BHARAT-CITIZEN", sprint=3, title="Spike: Biometric fallback to PIN", item_type="spike", points=4, status="completed", assignee="Anand Verma"),
    _b(code="BHARAT-CITIZEN", sprint=3, title="Hindi translation edge cases", item_type="bug", points=3, status="completed", assignee="Meera Iyer", defects=1, rework=2.0, priority="high"),
    # Sprint 4 — planned 50, completed 48
    _b(code="BHARAT-CITIZEN", sprint=4, title="Request money (send request)", item_type="story", points=13, status="completed", assignee="Priya Sharma", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=4, title="Transaction dispute flow", item_type="story", points=8, status="completed", assignee="Raj Kumar"),
    _b(code="BHARAT-CITIZEN", sprint=4, title="Offline mode queue + retry", item_type="story", points=8, status="completed", assignee="Anand Verma", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=4, title="Accessibility (TalkBack) pass", item_type="story", points=5, status="completed", assignee="Divya Menon"),
    _b(code="BHARAT-CITIZEN", sprint=4, title="Performance tuning — cold start", item_type="task", points=5, status="completed", assignee="Meera Iyer", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=4, title="Race condition in QR scanner", item_type="bug", points=4, status="completed", assignee="Raj Kumar", defects=1, rework=3.0, priority="high"),
    _b(code="BHARAT-CITIZEN", sprint=4, title="Spike: Tamil RTL rendering issue", item_type="spike", points=5, status="completed", assignee="Meera Iyer"),
    # Sprint 5 — planned 52, completed 52
    _b(code="BHARAT-CITIZEN", sprint=5, title="Merchant loyalty points integration", item_type="story", points=13, status="completed", assignee="Priya Sharma"),
    _b(code="BHARAT-CITIZEN", sprint=5, title="Govt benefit scheme enrolment", item_type="story", points=13, status="completed", assignee="Kavya Nair", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=5, title="Push notifications per transaction type", item_type="story", points=8, status="completed", assignee="Anand Verma"),
    _b(code="BHARAT-CITIZEN", sprint=5, title="Pay via phone number (tokenized)", item_type="story", points=8, status="completed", assignee="Raj Kumar", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=5, title="Transaction receipt PDF export", item_type="story", points=5, status="completed", assignee="Meera Iyer"),
    _b(code="BHARAT-CITIZEN", sprint=5, title="Sentry integration + crash triage", item_type="task", points=5, status="completed", assignee="Divya Menon", ai=True),
    # Sprint 6 — planned 55, completed 50 (shortfall 5 — busiest)
    _b(code="BHARAT-CITIZEN", sprint=6, title="Two-factor SMS + TOTP", item_type="story", points=13, status="completed", assignee="Anand Verma", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=6, title="Device binding & de-binding flow", item_type="story", points=13, status="completed", assignee="Priya Sharma"),
    _b(code="BHARAT-CITIZEN", sprint=6, title="Split bill / group pay", item_type="story", points=8, status="carried_over", assignee="Raj Kumar", defects=2, rework=8.0),
    _b(code="BHARAT-CITIZEN", sprint=6, title="Recurring payment setup", item_type="story", points=8, status="completed", assignee="Kavya Nair", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=6, title="Accessibility audit fixes (TalkBack)", item_type="task", points=8, status="completed", assignee="Divya Menon"),
    _b(code="BHARAT-CITIZEN", sprint=6, title="Security pen-test findings triage", item_type="bug", points=5, status="completed", assignee="Nisha Rao", defects=3, rework=4.0, priority="critical"),
    # Sprint 7 — planned 55, completed 54
    _b(code="BHARAT-CITIZEN", sprint=7, title="Merchant category code browser", item_type="story", points=13, status="completed", assignee="Priya Sharma", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=7, title="Split bill / group pay (carry)", item_type="story", points=8, status="completed", assignee="Raj Kumar"),
    _b(code="BHARAT-CITIZEN", sprint=7, title="In-app help + FAQ viewer", item_type="story", points=8, status="completed", assignee="Kavya Nair", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=7, title="Spike: Siri Shortcuts (iOS)", item_type="spike", points=5, status="completed", assignee="Anand Verma"),
    _b(code="BHARAT-CITIZEN", sprint=7, title="Beta feedback triage", item_type="task", points=8, status="completed", assignee="Divya Menon", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=7, title="Dark mode polish", item_type="story", points=8, status="completed", assignee="Meera Iyer"),
    _b(code="BHARAT-CITIZEN", sprint=7, title="P0 crash in Tamil locale (hotfix)", item_type="bug", points=4, status="completed", assignee="Kavya Nair", defects=1, rework=3.0, priority="critical"),
    # Sprint 8 — planned 58, completed 56
    _b(code="BHARAT-CITIZEN", sprint=8, title="Offline-first transaction history", item_type="story", points=13, status="completed", assignee="Priya Sharma", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=8, title="Merchant rating + review submission", item_type="story", points=13, status="completed", assignee="Raj Kumar"),
    _b(code="BHARAT-CITIZEN", sprint=8, title="Personalized offers via AI", item_type="story", points=8, status="completed", assignee="Anand Verma", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=8, title="Deep-link integration with UPI apps", item_type="story", points=8, status="completed", assignee="Kavya Nair", ai=True),
    _b(code="BHARAT-CITIZEN", sprint=8, title="Play Store beta checklist items", item_type="task", points=8, status="completed", assignee="Divya Menon"),
    _b(code="BHARAT-CITIZEN", sprint=8, title="Compatibility bug on Android 11 ≤", item_type="bug", points=4, status="carried_over", assignee="Kavya Nair", defects=1, rework=4.0, priority="high"),
    _b(code="BHARAT-CITIZEN", sprint=8, title="Spike: Tokenized card payments", item_type="spike", points=2, status="completed", assignee="Raj Kumar"),
]


# ===========================================================================
# Phases (Waterfall project: BHARAT-UPI)
# ===========================================================================

BHARAT_PROJECT_PHASES: list[ProjectPhaseSeed] = [
    {"project_code": "BHARAT-UPI", "phase_name": "Requirements", "phase_sequence": 1, "planned_start": date(2026, 1, 15), "planned_end": date(2026, 3, 15), "actual_start": date(2026, 1, 15), "actual_end": date(2026, 3, 10), "percent_complete": 100.0, "gate_status": "passed", "gate_approver": "S. Iyer (Ministry)", "gate_date": date(2026, 3, 12), "notes": "Early close — 5 days ahead"},
    {"project_code": "BHARAT-UPI", "phase_name": "Design", "phase_sequence": 2, "planned_start": date(2026, 3, 16), "planned_end": date(2026, 5, 31), "actual_start": date(2026, 3, 11), "actual_end": date(2026, 6, 5), "percent_complete": 100.0, "gate_status": "passed", "gate_approver": "S. Iyer (Ministry)", "gate_date": date(2026, 6, 8), "notes": "5-day slip; HSM vendor spec took longer than forecast"},
    {"project_code": "BHARAT-UPI", "phase_name": "Development", "phase_sequence": 3, "planned_start": date(2026, 6, 1), "planned_end": date(2027, 1, 31), "actual_start": date(2026, 6, 6), "actual_end": None, "percent_complete": 45.0, "gate_status": "pending", "gate_approver": None, "gate_date": None, "notes": "On track; HSM integration is the critical path"},
    {"project_code": "BHARAT-UPI", "phase_name": "Test", "phase_sequence": 4, "planned_start": date(2027, 2, 1), "planned_end": date(2027, 4, 15), "actual_start": None, "actual_end": None, "percent_complete": 0.0, "gate_status": "pending", "gate_approver": None, "gate_date": None, "notes": None},
    {"project_code": "BHARAT-UPI", "phase_name": "UAT", "phase_sequence": 5, "planned_start": date(2027, 4, 16), "planned_end": date(2027, 5, 31), "actual_start": None, "actual_end": None, "percent_complete": 0.0, "gate_status": "pending", "gate_approver": None, "gate_date": None, "notes": None},
    {"project_code": "BHARAT-UPI", "phase_name": "Deploy", "phase_sequence": 6, "planned_start": date(2027, 6, 1), "planned_end": date(2027, 6, 30), "actual_start": None, "actual_end": None, "percent_complete": 0.0, "gate_status": "pending", "gate_approver": None, "gate_date": None, "notes": None},
]


BHARAT_PHASE_DELIVERABLES: list[PhaseDeliverableSeed] = [
    # Requirements phase — all done
    {"project_code": "BHARAT-UPI", "phase_name": "Requirements", "title": "Business requirements document (NPCI compliant)", "description": "BRD mapped to NPCI UPI 2.0 specification sections", "deliverable_type": "doc", "owner": "Priya Sharma", "planned_end": date(2026, 2, 28), "actual_end": date(2026, 2, 25), "status": "Completed", "effort_days_planned": 15, "effort_days_actual": 14, "evidence_link": "confluence://BHARAT/BRD-v1", "notes": None},
    {"project_code": "BHARAT-UPI", "phase_name": "Requirements", "title": "Functional specification v1.0", "description": "Detailed UPI 2.0 flows incl. e-mandate, overdraft, invoice-in-box", "deliverable_type": "doc", "owner": "Raj Kumar", "planned_end": date(2026, 3, 5), "actual_end": date(2026, 3, 3), "status": "Completed", "effort_days_planned": 12, "effort_days_actual": 11, "evidence_link": "confluence://BHARAT/FSD-v1", "notes": None},
    {"project_code": "BHARAT-UPI", "phase_name": "Requirements", "title": "Ministry stakeholder sign-off", "description": "Written sign-off from Ministry of Digital Infrastructure", "deliverable_type": "sign-off", "owner": "S. Iyer (Ministry)", "planned_end": date(2026, 3, 15), "actual_end": date(2026, 3, 10), "status": "Completed", "effort_days_planned": 2, "effort_days_actual": 2, "evidence_link": "email://ministry/signoff-20260310", "notes": "Early sign-off"},
    {"project_code": "BHARAT-UPI", "phase_name": "Requirements", "title": "Requirements gate review", "description": "Phase-gate review with SteerCo + NPCI liaison", "deliverable_type": "review", "owner": "Suresh Menon", "planned_end": date(2026, 3, 15), "actual_end": date(2026, 3, 12), "status": "Completed", "effort_days_planned": 1, "effort_days_actual": 1, "evidence_link": "minutes://gate-req-20260312", "notes": "Passed"},

    # Design phase — all done (5 days slip)
    {"project_code": "BHARAT-UPI", "phase_name": "Design", "title": "High-level architecture (Java / Kafka / HSM)", "description": "End-to-end architecture incl. HSM integration pattern", "deliverable_type": "doc", "owner": "Raj Kumar", "planned_end": date(2026, 4, 15), "actual_end": date(2026, 4, 20), "status": "Completed", "effort_days_planned": 20, "effort_days_actual": 22, "evidence_link": "confluence://BHARAT/HLD", "notes": "HSM section delayed vendor spec"},
    {"project_code": "BHARAT-UPI", "phase_name": "Design", "title": "Data model & schema — transaction ledger", "description": "Partitioned PostgreSQL ledger with immutable audit trail", "deliverable_type": "artefact", "owner": "Meera Iyer", "planned_end": date(2026, 4, 30), "actual_end": date(2026, 5, 2), "status": "Completed", "effort_days_planned": 10, "effort_days_actual": 10, "evidence_link": "dbdiagram://bharat-upi", "notes": None},
    {"project_code": "BHARAT-UPI", "phase_name": "Design", "title": "Security design — HSM + key ceremonies", "description": "FIPS 140-3 Level 3 HSM key-management design", "deliverable_type": "doc", "owner": "Nisha Rao", "planned_end": date(2026, 5, 15), "actual_end": date(2026, 5, 28), "status": "Completed", "effort_days_planned": 12, "effort_days_actual": 14, "evidence_link": "confluence://BHARAT/SEC", "notes": "External review added 10 days"},
    {"project_code": "BHARAT-UPI", "phase_name": "Design", "title": "Performance model — 10k TPS target", "description": "Capacity plan sized for Diwali peak multiplied by 2", "deliverable_type": "doc", "owner": "Raj Kumar", "planned_end": date(2026, 5, 25), "actual_end": date(2026, 5, 30), "status": "Completed", "effort_days_planned": 8, "effort_days_actual": 9, "evidence_link": "confluence://BHARAT/PERF", "notes": None},
    {"project_code": "BHARAT-UPI", "phase_name": "Design", "title": "Design gate review", "description": "Phase gate with Ministry tech review board", "deliverable_type": "sign-off", "owner": "S. Iyer (Ministry)", "planned_end": date(2026, 5, 31), "actual_end": date(2026, 6, 8), "status": "Completed", "effort_days_planned": 1, "effort_days_actual": 1, "evidence_link": "minutes://gate-design-20260608", "notes": "Passed with 2 minor actions"},

    # Development phase — 45% complete, in flight
    {"project_code": "BHARAT-UPI", "phase_name": "Development", "title": "Transaction ledger service", "description": "Core ledger with double-entry and reconciliation", "deliverable_type": "build", "owner": "Raj Kumar", "planned_end": date(2026, 8, 31), "actual_end": date(2026, 8, 25), "status": "Completed", "effort_days_planned": 45, "effort_days_actual": 42, "evidence_link": "pr://bharat-upi/88", "notes": None},
    {"project_code": "BHARAT-UPI", "phase_name": "Development", "title": "HSM integration module", "description": "Encrypted PIN block handling + key rotation", "deliverable_type": "build", "owner": "Nisha Rao", "planned_end": date(2026, 10, 15), "actual_end": date(2026, 11, 5), "status": "Completed", "effort_days_planned": 35, "effort_days_actual": 42, "evidence_link": "pr://bharat-upi/124", "notes": "3-week slip — HSM vendor firmware update"},
    {"project_code": "BHARAT-UPI", "phase_name": "Development", "title": "Merchant gateway adapter", "description": "NPCI merchant gateway integration with retry/idempotency", "deliverable_type": "build", "owner": "Priya Sharma", "planned_end": date(2026, 11, 30), "actual_end": None, "status": "In Progress", "effort_days_planned": 30, "effort_days_actual": 22, "evidence_link": "pr://bharat-upi/156", "notes": "On track"},
    {"project_code": "BHARAT-UPI", "phase_name": "Development", "title": "E-mandate / overdraft flows", "description": "UPI 2.0-specific flows for sanctioned credit-line use", "deliverable_type": "build", "owner": "Anand Verma", "planned_end": date(2026, 12, 31), "actual_end": None, "status": "In Progress", "effort_days_planned": 28, "effort_days_actual": 10, "evidence_link": "pr://bharat-upi/170", "notes": None},
    {"project_code": "BHARAT-UPI", "phase_name": "Development", "title": "Observability + SRE runbooks", "description": "Prometheus + Grafana + alerting playbooks", "deliverable_type": "build", "owner": "Meera Iyer", "planned_end": date(2027, 1, 15), "actual_end": None, "status": "Pending", "effort_days_planned": 15, "effort_days_actual": None, "evidence_link": None, "notes": "Starts after ledger + HSM stable"},
    {"project_code": "BHARAT-UPI", "phase_name": "Development", "title": "Load & resilience hardening", "description": "Diwali-profile load testing and circuit-breaker tuning", "deliverable_type": "build", "owner": "Raj Kumar", "planned_end": date(2027, 1, 31), "actual_end": None, "status": "Blocked", "effort_days_planned": 18, "effort_days_actual": None, "evidence_link": None, "notes": "Blocked on DC-3 capacity allocation from Ministry"},

    # Test phase — pending
    {"project_code": "BHARAT-UPI", "phase_name": "Test", "title": "Test strategy + scripts", "description": "Unit / integration / performance / security / regression", "deliverable_type": "doc", "owner": "Divya Menon", "planned_end": date(2027, 2, 28), "actual_end": None, "status": "Pending", "effort_days_planned": 10, "effort_days_actual": None, "evidence_link": None, "notes": None},
    {"project_code": "BHARAT-UPI", "phase_name": "Test", "title": "Automated regression suite", "description": "Full coverage of UPI 2.0 positive + negative flows", "deliverable_type": "build", "owner": "Divya Menon", "planned_end": date(2027, 3, 31), "actual_end": None, "status": "Pending", "effort_days_planned": 30, "effort_days_actual": None, "evidence_link": None, "notes": None},
    {"project_code": "BHARAT-UPI", "phase_name": "Test", "title": "Security pen-test report", "description": "CERT-In accredited pen-test", "deliverable_type": "doc", "owner": "Nisha Rao", "planned_end": date(2027, 4, 15), "actual_end": None, "status": "Pending", "effort_days_planned": 12, "effort_days_actual": None, "evidence_link": None, "notes": None},

    # UAT phase — pending
    {"project_code": "BHARAT-UPI", "phase_name": "UAT", "title": "NPCI certification tests", "description": "Full NPCI UPI 2.0 certification run", "deliverable_type": "review", "owner": "Raj Kumar", "planned_end": date(2027, 5, 15), "actual_end": None, "status": "Pending", "effort_days_planned": 10, "effort_days_actual": None, "evidence_link": None, "notes": None},
    {"project_code": "BHARAT-UPI", "phase_name": "UAT", "title": "Ministry UAT sign-off", "description": "Formal acceptance by Ministry team", "deliverable_type": "sign-off", "owner": "S. Iyer (Ministry)", "planned_end": date(2027, 5, 31), "actual_end": None, "status": "Pending", "effort_days_planned": 2, "effort_days_actual": None, "evidence_link": None, "notes": None},

    # Deploy phase — pending
    {"project_code": "BHARAT-UPI", "phase_name": "Deploy", "title": "Production deployment runbook", "description": "Blue-green cutover with rollback across DC-1 + DC-3", "deliverable_type": "doc", "owner": "Meera Iyer", "planned_end": date(2027, 6, 15), "actual_end": None, "status": "Pending", "effort_days_planned": 6, "effort_days_actual": None, "evidence_link": None, "notes": None},
    {"project_code": "BHARAT-UPI", "phase_name": "Deploy", "title": "Go-live and hypercare", "description": "3-week hypercare post-launch with on-call rotation", "deliverable_type": "sign-off", "owner": "Suresh Menon", "planned_end": date(2027, 6, 30), "actual_end": None, "status": "Pending", "effort_days_planned": 21, "effort_days_actual": None, "evidence_link": None, "notes": None},
]


# ===========================================================================
# EVM snapshots (monthly — 12 points, both projects)
# ===========================================================================


def _evm(project: str, snap_date: date, pv: float, ev: float, ac: float, bac: float, pct_complete: float, notes: str | None = None) -> EvmSnapshotSeed:
    return {
        "project_code": project,
        "snapshot_date": snap_date,
        "planned_value": pv,
        "earned_value": ev,
        "actual_cost": ac,
        "bac": bac,
        "percent_complete": pct_complete,
        "notes": notes,
    }


BHARAT_EVM_SNAPSHOTS: list[EvmSnapshotSeed] = [
    # BHARAT-UPI (Waterfall, BAC = 6.8M) — steady progress
    _evm("BHARAT-UPI", date(2026, 2, 28), 400_000, 380_000, 390_000, 6_800_000, 5.6, "Requirements closing"),
    _evm("BHARAT-UPI", date(2026, 3, 31), 850_000, 820_000, 830_000, 6_800_000, 12.1, None),
    _evm("BHARAT-UPI", date(2026, 4, 30), 1_350_000, 1_290_000, 1_280_000, 6_800_000, 19.0, None),
    _evm("BHARAT-UPI", date(2026, 5, 31), 1_900_000, 1_820_000, 1_780_000, 6_800_000, 26.8, "Design closing"),
    _evm("BHARAT-UPI", date(2026, 6, 30), 2_400_000, 2_350_000, 2_280_000, 6_800_000, 34.6, None),
    _evm("BHARAT-UPI", date(2026, 7, 31), 2_900_000, 2_870_000, 2_780_000, 6_800_000, 42.2, None),
    _evm("BHARAT-UPI", date(2026, 8, 31), 3_400_000, 3_390_000, 3_260_000, 6_800_000, 49.9, "Ledger service shipped"),
    _evm("BHARAT-UPI", date(2026, 9, 30), 3_850_000, 3_860_000, 3_700_000, 6_800_000, 56.8, None),
    _evm("BHARAT-UPI", date(2026, 10, 31), 4_250_000, 4_200_000, 4_080_000, 6_800_000, 61.8, None),
    _evm("BHARAT-UPI", date(2026, 11, 30), 4_650_000, 4_580_000, 4_420_000, 6_800_000, 67.4, "HSM integration slip absorbed"),
    _evm("BHARAT-UPI", date(2026, 12, 31), 5_000_000, 4_960_000, 4_780_000, 6_800_000, 72.9, None),
    _evm("BHARAT-UPI", date(2027, 1, 31), 5_350_000, 5_340_000, 5_120_000, 6_800_000, 78.5, None),

    # BHARAT-CITIZEN (Scrum, BAC = 5.7M) — healthy, AI uplift from sprint 5
    _evm("BHARAT-CITIZEN", date(2026, 2, 28), 300_000, 285_000, 290_000, 5_700_000, 5.0, "Sprint 1-2 complete"),
    _evm("BHARAT-CITIZEN", date(2026, 3, 31), 700_000, 680_000, 685_000, 5_700_000, 11.9, None),
    _evm("BHARAT-CITIZEN", date(2026, 4, 30), 1_150_000, 1_130_000, 1_110_000, 5_700_000, 19.8, None),
    _evm("BHARAT-CITIZEN", date(2026, 5, 31), 1_600_000, 1_610_000, 1_550_000, 5_700_000, 28.2, "AI uplift visible"),
    _evm("BHARAT-CITIZEN", date(2026, 6, 30), 2_050_000, 2_070_000, 1_980_000, 5_700_000, 36.3, None),
    _evm("BHARAT-CITIZEN", date(2026, 7, 31), 2_500_000, 2_530_000, 2_400_000, 5_700_000, 44.4, None),
    _evm("BHARAT-CITIZEN", date(2026, 8, 31), 2_950_000, 2_990_000, 2_820_000, 5_700_000, 52.5, None),
    _evm("BHARAT-CITIZEN", date(2026, 9, 30), 3_400_000, 3_450_000, 3_230_000, 5_700_000, 60.5, None),
    _evm("BHARAT-CITIZEN", date(2026, 10, 31), 3_850_000, 3_920_000, 3_660_000, 5_700_000, 68.8, "Beta ready"),
    _evm("BHARAT-CITIZEN", date(2026, 11, 30), 4_300_000, 4_390_000, 4_080_000, 5_700_000, 77.0, None),
    _evm("BHARAT-CITIZEN", date(2026, 12, 31), 4_700_000, 4_800_000, 4_430_000, 5_700_000, 84.2, None),
    _evm("BHARAT-CITIZEN", date(2027, 1, 31), 5_080_000, 5_190_000, 4_750_000, 5_700_000, 91.1, "Pre-launch hardening"),
]


# ===========================================================================
# Milestones
# ===========================================================================

BHARAT_MILESTONES: list[MilestoneSeed] = [
    {"project_code": "BHARAT-UPI", "name": "NPCI Specification Sign-off", "planned_date": date(2026, 3, 15), "actual_date": date(2026, 3, 10), "status": "Completed", "dependencies": None, "owner": "Priya Sharma", "notes": "Completed 5 days early"},
    {"project_code": "BHARAT-UPI", "name": "HSM Integration Checkpoint", "planned_date": date(2026, 10, 15), "actual_date": date(2026, 11, 5), "status": "Completed", "dependencies": None, "owner": "Nisha Rao", "notes": "21-day slip; vendor firmware issue"},
    {"project_code": "BHARAT-UPI", "name": "NPCI Certification Run", "planned_date": date(2027, 5, 15), "actual_date": None, "status": "Pending", "dependencies": "Test + UAT phases", "owner": "Raj Kumar", "notes": None},
    {"project_code": "BHARAT-UPI", "name": "Production Go-Live", "planned_date": date(2027, 6, 30), "actual_date": None, "status": "Pending", "dependencies": "NPCI Certification", "owner": "Suresh Menon", "notes": None},
    {"project_code": "BHARAT-CITIZEN", "name": "Closed Beta Release", "planned_date": date(2026, 11, 15), "actual_date": date(2026, 11, 12), "status": "Completed", "dependencies": None, "owner": "Priya Sharma", "notes": "3 days early"},
    {"project_code": "BHARAT-CITIZEN", "name": "Play Store Submission", "planned_date": date(2027, 2, 15), "actual_date": None, "status": "In Progress", "dependencies": "Security pen-test clean", "owner": "Divya Menon", "notes": None},
    {"project_code": "BHARAT-CITIZEN", "name": "Public Launch", "planned_date": date(2027, 3, 31), "actual_date": None, "status": "Pending", "dependencies": "Play Store approval", "owner": "Suresh Menon", "notes": None},
]


# ===========================================================================
# Commercial scenarios — quarterly 4-layer margin
# ===========================================================================

BHARAT_COMMERCIAL_SCENARIOS: list[CommercialSeed] = [
    {"program_code": "BHARAT", "scenario_name": "Quarterly Actuals", "planned_revenue": 2_200_000, "actual_revenue": 2_230_000, "planned_cost": 1_650_000, "actual_cost": 1_620_000, "gross_margin_pct": 0.27, "contribution_margin_pct": 0.20, "portfolio_margin_pct": 0.15, "net_margin_pct": 0.10, "snapshot_date": date(2026, 4, 1), "notes": "Strong opening quarter"},
    {"program_code": "BHARAT", "scenario_name": "Quarterly Actuals", "planned_revenue": 2_400_000, "actual_revenue": 2_440_000, "planned_cost": 1_700_000, "actual_cost": 1_680_000, "gross_margin_pct": 0.28, "contribution_margin_pct": 0.21, "portfolio_margin_pct": 0.16, "net_margin_pct": 0.11, "snapshot_date": date(2026, 7, 1), "notes": "Continued healthy trend"},
    {"program_code": "BHARAT", "scenario_name": "Quarterly Actuals", "planned_revenue": 2_600_000, "actual_revenue": 2_670_000, "planned_cost": 1_780_000, "actual_cost": 1_770_000, "gross_margin_pct": 0.30, "contribution_margin_pct": 0.22, "portfolio_margin_pct": 0.17, "net_margin_pct": 0.12, "snapshot_date": date(2026, 10, 1), "notes": "HSM vendor slip absorbed without margin hit"},
    {"program_code": "BHARAT", "scenario_name": "Quarterly Actuals", "planned_revenue": 2_800_000, "actual_revenue": 2_860_000, "planned_cost": 1_850_000, "actual_cost": 1_820_000, "gross_margin_pct": 0.31, "contribution_margin_pct": 0.23, "portfolio_margin_pct": 0.18, "net_margin_pct": 0.13, "snapshot_date": date(2027, 1, 1), "notes": "AI uplift compounding"},
]

# ===========================================================================
# Loss exposure — 4 categories
# ===========================================================================

BHARAT_LOSS_EXPOSURE: list[LossSeed] = [
    {"program_code": "BHARAT", "snapshot_date": date(2027, 1, 31), "loss_category": "Scope Creep", "amount": 180_000, "percentage_of_revenue": 1.4, "detection_method": "CR log vs margin impact", "mitigation_status": "Mitigated", "notes": "2 CRs under watch"},
    {"program_code": "BHARAT", "snapshot_date": date(2027, 1, 31), "loss_category": "Rework & Defect Leakage", "amount": 95_000, "percentage_of_revenue": 0.8, "detection_method": "Sprint rework hours", "mitigation_status": "Monitoring", "notes": "Sprint 6 outlier"},
    {"program_code": "BHARAT", "snapshot_date": date(2027, 1, 31), "loss_category": "Estimation Miss", "amount": 120_000, "percentage_of_revenue": 1.0, "detection_method": "Plan vs actual", "mitigation_status": "Monitoring", "notes": "HSM phase"},
    {"program_code": "BHARAT", "snapshot_date": date(2027, 1, 31), "loss_category": "Bench Tax", "amount": 60_000, "percentage_of_revenue": 0.5, "detection_method": "Shadow allocation", "mitigation_status": "Mitigated", "notes": "1 FTE on ramp-down"},
]

# ===========================================================================
# Rate cards
# ===========================================================================

BHARAT_RATE_CARDS: list[RateCardSeed] = [
    {"program_code": "BHARAT", "role_tier": "Senior Architect", "planned_rate": 190.0, "actual_rate": 188.0, "planned_headcount": 3, "actual_headcount": 3, "snapshot_date": date(2027, 1, 31), "notes": "Within tolerance"},
    {"program_code": "BHARAT", "role_tier": "Tech Lead", "planned_rate": 150.0, "actual_rate": 152.0, "planned_headcount": 4, "actual_headcount": 4, "snapshot_date": date(2027, 1, 31), "notes": None},
    {"program_code": "BHARAT", "role_tier": "Mid Engineer", "planned_rate": 110.0, "actual_rate": 112.0, "planned_headcount": 15, "actual_headcount": 16, "snapshot_date": date(2027, 1, 31), "notes": "+1 headcount absorbed at slight premium"},
    {"program_code": "BHARAT", "role_tier": "Junior Developer", "planned_rate": 70.0, "actual_rate": 72.0, "planned_headcount": 6, "actual_headcount": 5, "snapshot_date": date(2027, 1, 31), "notes": None},
]

# ===========================================================================
# Change requests (scope creep log)
# ===========================================================================

BHARAT_CHANGE_REQUESTS: list[ChangeRequestSeed] = [
    {"program_code": "BHARAT", "project_code": "BHARAT-UPI", "cr_date": date(2026, 7, 20), "cr_description": "Add secondary HSM vendor failover", "effort_hours": 80, "cr_value": 420_000, "processing_cost": 48_000, "status": "Approved", "margin_impact": -0.6, "is_billable": True},
    {"program_code": "BHARAT", "project_code": "BHARAT-CITIZEN", "cr_date": date(2026, 9, 5), "cr_description": "Merchant loyalty points integration", "effort_hours": 55, "cr_value": 280_000, "processing_cost": 30_000, "status": "Approved", "margin_impact": -0.4, "is_billable": True},
    {"program_code": "BHARAT", "project_code": "BHARAT-CITIZEN", "cr_date": date(2026, 11, 12), "cr_description": "Additional Indic-language translations (Telugu, Kannada, Marathi)", "effort_hours": 40, "cr_value": 200_000, "processing_cost": 24_000, "status": "Approved", "margin_impact": -0.3, "is_billable": True},
]

# ===========================================================================
# Dual velocity (BHARAT-CITIZEN, AI Heavy)
# ===========================================================================

BHARAT_SPRINT_VELOCITY_DUAL: list[SprintVelocityDualSeed] = [
    {"project_code": "BHARAT-CITIZEN", "sprint_number": i + 1, "standard_velocity": v[0], "ai_raw_velocity": v[1], "ai_rework_points": v[2], "ai_quality_adjusted_velocity": v[1] - v[2], "combined_velocity": v[0] + (v[1] - v[2]), "merge_eligible": v[3], "quality_parity_ratio": v[4], "snapshot_date": date(2026, 2, 2)}
    for i, v in enumerate([
        (28, 10, 2.0, True, 0.93),
        (29, 13, 1.8, True, 0.94),
        (30, 16, 1.5, True, 0.95),
        (30, 18, 1.2, True, 0.96),
        (31, 21, 1.0, True, 0.97),
        (30, 20, 1.4, True, 0.95),
        (32, 22, 0.9, True, 0.97),
        (33, 25, 0.8, True, 0.98),
    ])
]

# ===========================================================================
# Blend rules
# ===========================================================================

BHARAT_BLEND_RULES: list[BlendRuleSeed] = [
    {"program_code": "BHARAT", "gate_name": "Quality parity", "gate_condition": "parity_ratio >= 0.95", "current_value": 0.97, "threshold": 0.95, "passed": True, "last_evaluated": date(2027, 1, 25)},
    {"program_code": "BHARAT", "gate_name": "Rework ceiling", "gate_condition": "ai_rework / ai_raw <= 0.05", "current_value": 0.035, "threshold": 0.05, "passed": True, "last_evaluated": date(2027, 1, 25)},
    {"program_code": "BHARAT", "gate_name": "Override rate", "gate_condition": "override_pct <= 15", "current_value": 9.0, "threshold": 15.0, "passed": True, "last_evaluated": date(2027, 1, 25)},
]

# ===========================================================================
# Customer satisfaction (monthly, 6 months visible)
# ===========================================================================

def _bharat_cs(snap_date: date, csat: float, nps: float, esc_total: int, esc_open: int, held: int, open_ai: int, closed: int, renewal: float) -> CustomerSatisfactionSeed:
    return {
        "program_code": "BHARAT",
        "snapshot_date": snap_date,
        "csat_score": csat,
        "nps_score": nps,
        "escalation_count": esc_total,
        "escalation_open": esc_open,
        "steering_meetings_planned": 2,
        "steering_meetings_held": held,
        "action_items_open": open_ai,
        "action_items_closed": closed,
        "positive_themes": "Ministry alignment; AI uplift in Swayam; Clean audit trail",
        "concern_themes": "HSM vendor firmware delay; DC-3 capacity not yet allocated",
        "renewal_score": renewal,
        "notes": None,
    }


BHARAT_CUSTOMER_SATISFACTION: list[CustomerSatisfactionSeed] = [
    _bharat_cs(date(2026, 8, 1), 8.4, 48, 1, 0, 2, 3, 2, 85),
    _bharat_cs(date(2026, 9, 1), 8.5, 50, 1, 0, 2, 3, 3, 86),
    _bharat_cs(date(2026, 10, 1), 8.5, 52, 2, 1, 2, 4, 3, 86),
    _bharat_cs(date(2026, 11, 1), 8.6, 55, 2, 1, 2, 4, 4, 87),
    _bharat_cs(date(2026, 12, 1), 8.7, 58, 2, 0, 2, 3, 5, 88),
    _bharat_cs(date(2027, 1, 1), 8.8, 60, 3, 1, 2, 4, 5, 89),
]

# ===========================================================================
# Customer expectations — 7 dimensions
# ===========================================================================

BHARAT_CUSTOMER_EXPECTATIONS: list[CustomerExpectationSeed] = [
    {"program_code": "BHARAT", "snapshot_date": date(2027, 1, 31), "dimension": "timeline", "expected_score": 9.0, "delivered_score": 8.5, "weight": 1.2, "evidence_source": "Ministry review", "owner": "Suresh Menon", "notes": "HSM slip absorbed without programme impact"},
    {"program_code": "BHARAT", "snapshot_date": date(2027, 1, 31), "dimension": "quality", "expected_score": 9.0, "delivered_score": 8.8, "weight": 1.1, "evidence_source": "Pen-test + audit", "owner": "Nisha Rao", "notes": "Strong audit readiness"},
    {"program_code": "BHARAT", "snapshot_date": date(2027, 1, 31), "dimension": "communication", "expected_score": 8.5, "delivered_score": 8.7, "weight": 1.0, "evidence_source": "Steering committee", "owner": "Suresh Menon", "notes": "Exceeding baseline — weekly joint stand-ups"},
    {"program_code": "BHARAT", "snapshot_date": date(2027, 1, 31), "dimension": "innovation", "expected_score": 7.5, "delivered_score": 9.0, "weight": 0.9, "evidence_source": "Ministry QBR", "owner": "Suresh Menon", "notes": "AI augmentation highlighted as exemplar"},
    {"program_code": "BHARAT", "snapshot_date": date(2027, 1, 31), "dimension": "cost", "expected_score": 8.5, "delivered_score": 8.6, "weight": 1.1, "evidence_source": "Monthly financial review", "owner": "Priya Sharma", "notes": "Within plan"},
    {"program_code": "BHARAT", "snapshot_date": date(2027, 1, 31), "dimension": "responsiveness", "expected_score": 9.0, "delivered_score": 8.5, "weight": 1.0, "evidence_source": "Ticket response metrics", "owner": "Raj Kumar", "notes": None},
    {"program_code": "BHARAT", "snapshot_date": date(2027, 1, 31), "dimension": "stability", "expected_score": 8.0, "delivered_score": 8.3, "weight": 0.9, "evidence_source": "Resource pool", "owner": "Suresh Menon", "notes": "Low attrition"},
]

# ===========================================================================
# Customer actions
# ===========================================================================

BHARAT_CUSTOMER_ACTIONS: list[CustomerActionSeed] = [
    {"program_code": "BHARAT", "meeting_date": date(2026, 11, 20), "description": "Finalise DC-3 capacity allocation with Ministry", "owner": "Suresh Menon", "due_date": date(2026, 12, 20), "status": "In Progress", "priority": "P1", "escalated": True},
    {"program_code": "BHARAT", "meeting_date": date(2026, 12, 5), "description": "Submit CERT-In pen-test scoping document", "owner": "Nisha Rao", "due_date": date(2026, 12, 31), "status": "Closed", "priority": "P2", "escalated": False},
    {"program_code": "BHARAT", "meeting_date": date(2026, 12, 18), "description": "Pre-launch marketing coordination with Ministry PR team", "owner": "Priya Sharma", "due_date": date(2027, 1, 31), "status": "Open", "priority": "P2", "escalated": False},
    {"program_code": "BHARAT", "meeting_date": date(2027, 1, 8), "description": "NPCI certification test environment setup", "owner": "Raj Kumar", "due_date": date(2027, 2, 15), "status": "In Progress", "priority": "P1", "escalated": False},
    {"program_code": "BHARAT", "meeting_date": date(2027, 1, 15), "description": "Play Store beta cohort expansion (Tier 3-4 cities)", "owner": "Divya Menon", "due_date": date(2027, 2, 10), "status": "Open", "priority": "P2", "escalated": False},
    {"program_code": "BHARAT", "meeting_date": date(2027, 1, 22), "description": "Publish updated resource-ramp schedule for Q2", "owner": "Suresh Menon", "due_date": date(2027, 2, 5), "status": "Open", "priority": "P3", "escalated": False},
]

# ===========================================================================
# SLA incidents (small volume — programme is healthy)
# ===========================================================================

BHARAT_SLA_INCIDENTS: list[SlaIncidentSeed] = [
    {"program_code": "BHARAT", "incident_id": "BHR-INC-001", "priority": "P2", "summary": "Swayam beta crash on Android 9 devices", "reported_at": datetime(2026, 11, 15, 14, 20), "responded_at": datetime(2026, 11, 15, 14, 45), "resolved_at": datetime(2026, 11, 16, 10, 30), "response_time_minutes": 25.0, "resolution_time_minutes": 20 * 60 + 10, "sla_breached": False, "penalty_amount": 0, "root_cause": "Missing null check in biometric fallback path"},
    {"program_code": "BHARAT", "incident_id": "BHR-INC-002", "priority": "P3", "summary": "Hindi translation glitch on checkout screen", "reported_at": datetime(2026, 12, 8, 10, 0), "responded_at": datetime(2026, 12, 8, 11, 45), "resolved_at": datetime(2026, 12, 9, 15, 30), "response_time_minutes": 105.0, "resolution_time_minutes": 29 * 60 + 30, "sla_breached": False, "penalty_amount": 0, "root_cause": "Fallback translation key missing"},
    {"program_code": "BHARAT", "incident_id": "BHR-INC-003", "priority": "P1", "summary": "UPI ledger service timeout during load test", "reported_at": datetime(2027, 1, 18, 16, 30), "responded_at": datetime(2027, 1, 18, 16, 48), "resolved_at": datetime(2027, 1, 19, 2, 15), "response_time_minutes": 18.0, "resolution_time_minutes": 9 * 60 + 45, "sla_breached": False, "penalty_amount": 0, "root_cause": "Connection pool undersized for Diwali-profile; retuned"},
]

# ===========================================================================
# AI tool assignments, usage, trust, overrides, SDLC, code metrics
# ===========================================================================

BHARAT_AI_TOOL_ASSIGNMENTS: list[AiToolAssignmentSeed] = [
    {"tool_name": "Claude for Devs", "program_code": "BHARAT", "assigned_date": date(2026, 2, 1), "users_count": 18, "status": "Active"},
    {"tool_name": "GitHub Copilot", "program_code": "BHARAT", "assigned_date": date(2026, 2, 1), "users_count": 22, "status": "Active"},
    {"tool_name": "Snyk AI", "program_code": "BHARAT", "assigned_date": date(2026, 4, 1), "users_count": 14, "status": "Active"},
]


def _bharat_usage(tool: str, start: tuple[int, int], months: int, base: int, accept: float, hrs: float, cost: float) -> list[AiUsageMetricsSeed]:
    rows: list[AiUsageMetricsSeed] = []
    y, m = start
    for i in range(months):
        prompts = int(base * (1.05 ** i))
        accepted = int(prompts * accept)
        rows.append({
            "tool_name": tool,
            "program_code": "BHARAT",
            "snapshot_date": date(y, m, 1),
            "prompts_count": prompts,
            "suggestions_accepted": accepted,
            "suggestions_rejected": prompts - accepted,
            "time_saved_hours": accepted * hrs,
            "cost": cost,
        })
        m += 1
        if m > 12:
            m = 1
            y += 1
    return rows


BHARAT_AI_USAGE_METRICS: list[AiUsageMetricsSeed] = [
    *_bharat_usage("Claude for Devs", (2026, 3), 11, 2400, 0.68, 0.16, 3200),
    *_bharat_usage("GitHub Copilot", (2026, 3), 11, 2800, 0.58, 0.11, 2600),
    *_bharat_usage("Snyk AI", (2026, 5), 9, 350, 0.82, 0.20, 1800),
]

BHARAT_AI_TRUST_SCORES: list[AiTrustScoreSeed] = [
    {"tool_name": "Claude for Devs", "program_code": "BHARAT", "snapshot_date": date(2027, 1, 31), "provenance_score": 90, "review_status_score": 88, "test_coverage_score": 84, "drift_check_score": 85, "override_rate_score": 86, "defect_rate_score": 85, "composite_score": 86.3, "maturity_level": "L4-Optimising"},
    {"tool_name": "GitHub Copilot", "program_code": "BHARAT", "snapshot_date": date(2027, 1, 31), "provenance_score": 85, "review_status_score": 82, "test_coverage_score": 80, "drift_check_score": 78, "override_rate_score": 80, "defect_rate_score": 82, "composite_score": 81.2, "maturity_level": "L3-Defined"},
    {"tool_name": "Snyk AI", "program_code": "BHARAT", "snapshot_date": date(2027, 1, 31), "provenance_score": 92, "review_status_score": 88, "test_coverage_score": 86, "drift_check_score": 90, "override_rate_score": 88, "defect_rate_score": 90, "composite_score": 89.0, "maturity_level": "L4-Optimising"},
]

BHARAT_AI_OVERRIDE_LOG: list[AiOverrideLogSeed] = [
    {"tool_name": "Claude for Devs", "program_code": "BHARAT", "project_code": "BHARAT-CITIZEN", "override_date": datetime(2026, 10, 5, 11, 20), "override_type": "Rejected suggestion", "reason": "Suggestion used deprecated React Native API", "outcome": "Manual implementation; prompt template updated", "approver": "Priya Sharma"},
    {"tool_name": "GitHub Copilot", "program_code": "BHARAT", "project_code": "BHARAT-UPI", "override_date": datetime(2026, 11, 14, 15, 45), "override_type": "Modified suggestion", "reason": "HSM key handling needed additional safety wrapping", "outcome": "Accepted with wrapper", "approver": "Nisha Rao"},
    {"tool_name": "Claude for Devs", "program_code": "BHARAT", "project_code": "BHARAT-CITIZEN", "override_date": datetime(2026, 12, 2, 9, 30), "override_type": "Rejected suggestion", "reason": "Proposed component broke accessibility (TalkBack)", "outcome": "Manual fix; regression test added", "approver": "Divya Menon"},
    {"tool_name": "Snyk AI", "program_code": "BHARAT", "project_code": "BHARAT-UPI", "override_date": datetime(2027, 1, 10, 14, 0), "override_type": "False positive", "reason": "CVE reported on dev-only dependency (junit)", "outcome": "Whitelisted with rationale", "approver": "Nisha Rao"},
    {"tool_name": "GitHub Copilot", "program_code": "BHARAT", "project_code": "BHARAT-CITIZEN", "override_date": datetime(2027, 1, 18, 16, 25), "override_type": "Escalated", "reason": "Suggestion introduced PII logging", "outcome": "Blocked; mandatory privacy review added to CI", "approver": "Suresh Menon"},
]

BHARAT_AI_SDLC_METRICS: list[AiSdlcMetricsSeed] = [
    {"program_code": "BHARAT", "sprint_number": i + 1, "estimation_accuracy_with_ai": [0.72, 0.75, 0.78, 0.80, 0.82, 0.84, 0.86, 0.87][i], "estimation_accuracy_without_ai": 0.70, "code_review_hours_with_ai": [28, 26, 24, 22, 20, 19, 18, 17][i], "code_review_hours_without_ai": 30, "planning_velocity_with_ai": [90, 94, 98, 102, 104, 106, 108, 110][i], "planning_velocity_without_ai": 84, "documentation_hours_with_ai": [15, 14, 12, 11, 10, 9, 8, 8][i], "documentation_hours_without_ai": 18, "snapshot_date": date(2026, 2, 2)}
    for i in range(8)
]

BHARAT_AI_CODE_METRICS: list[AiCodeMetricsSeed] = [
    {"program_code": "BHARAT", "project_code": "BHARAT-CITIZEN", "sprint_number": i + 1, "ai_lines_generated": [3200, 3500, 3800, 4000, 4200, 4400, 4500, 4700][i], "ai_lines_accepted": [2400, 2700, 3000, 3300, 3500, 3700, 3900, 4100][i], "ai_defect_count": [6, 5, 5, 4, 3, 3, 2, 2][i], "ai_test_coverage_pct": [74, 76, 78, 80, 82, 83, 84, 85][i], "ai_review_rejection_pct": [18, 16, 14, 12, 11, 10, 9, 8][i], "human_defect_count": [4, 4, 3, 3, 3, 2, 2, 2][i], "human_test_coverage_pct": [82, 83, 83, 84, 84, 85, 85, 86][i], "human_review_rejection_pct": [6, 5, 5, 5, 4, 4, 4, 3][i], "snapshot_date": date(2026, 2, 2)}
    for i in range(8)
]
