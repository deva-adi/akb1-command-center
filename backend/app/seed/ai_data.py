"""Tab 7 AI Governance demo data — 8 tables covering the AI lifecycle.

Follows ARCHITECTURE.md §4.7: 6-factor trust composite (provenance, review,
coverage, drift, override, defect), 5-level maturity, override logging,
productivity-tax comparison (with-AI vs without-AI).
"""
from __future__ import annotations

from datetime import date, datetime
from typing import TypedDict

# ---------------------------------------------------------------------------
# AI tools
# ---------------------------------------------------------------------------


class AiToolSeed(TypedDict):
    name: str
    vendor: str
    version: str
    category: str
    license_type: str
    cost_per_seat: float
    status: str


AI_TOOLS: list[AiToolSeed] = [
    {"name": "GitHub Copilot", "vendor": "GitHub/Microsoft", "version": "4.0", "category": "Code Gen", "license_type": "Enterprise", "cost_per_seat": 19.0, "status": "Active"},
    {"name": "Claude for Devs", "vendor": "Anthropic", "version": "Sonnet 4.6", "category": "Code Gen + Review", "license_type": "Team", "cost_per_seat": 25.0, "status": "Active"},
    {"name": "Tabnine", "vendor": "Tabnine", "version": "4.9", "category": "Code Gen", "license_type": "Enterprise", "cost_per_seat": 12.0, "status": "Pilot"},
    {"name": "Snyk AI", "vendor": "Snyk", "version": "2026-03", "category": "Security Scan", "license_type": "Enterprise", "cost_per_seat": 8.0, "status": "Active"},
    {"name": "Gemini for Docs", "vendor": "Google", "version": "Pro 2.5", "category": "Documentation", "license_type": "Team", "cost_per_seat": 18.0, "status": "Active"},
]


# ---------------------------------------------------------------------------
# Tool assignments per programme
# ---------------------------------------------------------------------------


class AiToolAssignmentSeed(TypedDict):
    tool_name: str
    program_code: str
    assigned_date: date
    users_count: int
    status: str


AI_TOOL_ASSIGNMENTS: list[AiToolAssignmentSeed] = [
    # Sentinel (heavy AI)
    {"tool_name": "GitHub Copilot", "program_code": "SENTINEL", "assigned_date": date(2025, 7, 1), "users_count": 8, "status": "Active"},
    {"tool_name": "Claude for Devs", "program_code": "SENTINEL", "assigned_date": date(2025, 8, 1), "users_count": 12, "status": "Active"},
    {"tool_name": "Snyk AI", "program_code": "SENTINEL", "assigned_date": date(2025, 8, 1), "users_count": 10, "status": "Active"},
    # Atlas (medium AI)
    {"tool_name": "GitHub Copilot", "program_code": "ATLAS", "assigned_date": date(2025, 9, 1), "users_count": 10, "status": "Active"},
    {"tool_name": "Gemini for Docs", "program_code": "ATLAS", "assigned_date": date(2025, 10, 1), "users_count": 6, "status": "Active"},
    # Phoenix (light AI)
    {"tool_name": "Claude for Devs", "program_code": "PHOENIX", "assigned_date": date(2025, 11, 1), "users_count": 5, "status": "Active"},
    {"tool_name": "Tabnine", "program_code": "PHOENIX", "assigned_date": date(2026, 1, 1), "users_count": 3, "status": "Pilot"},
    # Titan (medium AI)
    {"tool_name": "GitHub Copilot", "program_code": "TITAN", "assigned_date": date(2025, 10, 1), "users_count": 6, "status": "Active"},
    {"tool_name": "Gemini for Docs", "program_code": "TITAN", "assigned_date": date(2025, 11, 1), "users_count": 4, "status": "Active"},
]


# ---------------------------------------------------------------------------
# Monthly usage metrics (prompts, acceptance rate, hours saved, cost)
# ---------------------------------------------------------------------------


class AiUsageMetricsSeed(TypedDict):
    tool_name: str
    program_code: str
    snapshot_date: date
    prompts_count: int
    suggestions_accepted: int
    suggestions_rejected: int
    time_saved_hours: float
    cost: float


def _usage_series(
    tool_name: str,
    program_code: str,
    *,
    start_month: tuple[int, int],
    months: int,
    prompts_base: int,
    acceptance_rate: float,
    hours_saved_per_prompt: float,
    monthly_cost: float,
    ramp: float = 1.05,
) -> list[AiUsageMetricsSeed]:
    rows: list[AiUsageMetricsSeed] = []
    y, m = start_month
    for i in range(months):
        prompts = int(prompts_base * (ramp**i))
        accepted = int(prompts * acceptance_rate)
        rows.append(
            {
                "tool_name": tool_name,
                "program_code": program_code,
                "snapshot_date": date(y, m, 1),
                "prompts_count": prompts,
                "suggestions_accepted": accepted,
                "suggestions_rejected": prompts - accepted,
                "time_saved_hours": accepted * hours_saved_per_prompt,
                "cost": monthly_cost,
            }
        )
        m += 1
        if m > 12:
            m = 1
            y += 1
    return rows


AI_USAGE_METRICS: list[AiUsageMetricsSeed] = [
    *_usage_series("Claude for Devs", "SENTINEL", start_month=(2025, 8), months=8, prompts_base=2800, acceptance_rate=0.72, hours_saved_per_prompt=0.18, monthly_cost=3000, ramp=1.05),
    *_usage_series("GitHub Copilot", "SENTINEL", start_month=(2025, 7), months=9, prompts_base=1800, acceptance_rate=0.60, hours_saved_per_prompt=0.10, monthly_cost=1200, ramp=1.05),
    *_usage_series("GitHub Copilot", "ATLAS", start_month=(2025, 9), months=7, prompts_base=2200, acceptance_rate=0.52, hours_saved_per_prompt=0.09, monthly_cost=1500, ramp=1.03),
    *_usage_series("Claude for Devs", "PHOENIX", start_month=(2025, 11), months=5, prompts_base=1400, acceptance_rate=0.48, hours_saved_per_prompt=0.08, monthly_cost=1250, ramp=1.02),
    *_usage_series("GitHub Copilot", "TITAN", start_month=(2025, 10), months=6, prompts_base=1500, acceptance_rate=0.55, hours_saved_per_prompt=0.09, monthly_cost=900, ramp=1.04),
]


# ---------------------------------------------------------------------------
# AI code metrics per sprint (lines generated/accepted, defects)
# ---------------------------------------------------------------------------


class AiCodeMetricsSeed(TypedDict):
    program_code: str
    project_code: str
    sprint_number: int
    ai_lines_generated: int
    ai_lines_accepted: int
    ai_defect_count: int
    ai_test_coverage_pct: float
    ai_review_rejection_pct: float
    human_defect_count: int
    human_test_coverage_pct: float
    human_review_rejection_pct: float
    snapshot_date: date


AI_CODE_METRICS: list[AiCodeMetricsSeed] = [
    # Sentinel (heavy AI, improving parity)
    *(
        {
            "program_code": "SENTINEL",
            "project_code": "SNTL-AUTO",
            "sprint_number": 12 + i,
            "ai_lines_generated": [4500, 4800, 5100, 5400, 5700, 6000][i],
            "ai_lines_accepted": [3800, 4100, 4400, 4700, 5000, 5400][i],
            "ai_defect_count": [5, 4, 4, 3, 3, 2][i],
            "ai_test_coverage_pct": [78, 80, 82, 83, 85, 86][i],
            "ai_review_rejection_pct": [12, 10, 8, 7, 6, 5][i],
            "human_defect_count": [4, 3, 3, 3, 2, 2][i],
            "human_test_coverage_pct": [82, 83, 84, 85, 86, 87][i],
            "human_review_rejection_pct": [5, 5, 4, 4, 4, 3][i],
            "snapshot_date": date(2026, 1, 25),
        }
        for i in range(6)
    ),
    # Phoenix integration — worse parity (merge gate initially failing)
    *(
        {
            "program_code": "PHOENIX",
            "project_code": "PHOE-INT",
            "sprint_number": 14 + i,
            "ai_lines_generated": [1800, 2200, 2500, 2800, 3000, 3200][i],
            "ai_lines_accepted": [1200, 1500, 1800, 2100, 2350, 2600][i],
            "ai_defect_count": [7, 6, 5, 4, 4, 3][i],
            "ai_test_coverage_pct": [68, 70, 72, 74, 75, 76][i],
            "ai_review_rejection_pct": [22, 20, 18, 15, 12, 10][i],
            "human_defect_count": [3, 3, 4, 3, 3, 2][i],
            "human_test_coverage_pct": [80, 81, 81, 82, 82, 82][i],
            "human_review_rejection_pct": [6, 6, 5, 5, 5, 4][i],
            "snapshot_date": date(2026, 1, 25),
        }
        for i in range(6)
    ),
]


# ---------------------------------------------------------------------------
# SDLC productivity tax — with-AI vs without-AI comparison
# ---------------------------------------------------------------------------


class AiSdlcMetricsSeed(TypedDict):
    program_code: str
    sprint_number: int
    estimation_accuracy_with_ai: float
    estimation_accuracy_without_ai: float
    code_review_hours_with_ai: float
    code_review_hours_without_ai: float
    planning_velocity_with_ai: float
    planning_velocity_without_ai: float
    documentation_hours_with_ai: float
    documentation_hours_without_ai: float
    snapshot_date: date


AI_SDLC_METRICS: list[AiSdlcMetricsSeed] = [
    *(
        {
            "program_code": "SENTINEL",
            "sprint_number": 12 + i,
            "estimation_accuracy_with_ai": [0.82, 0.84, 0.86, 0.88, 0.89, 0.90][i],
            "estimation_accuracy_without_ai": 0.74,
            "code_review_hours_with_ai": [24, 22, 20, 18, 17, 16][i],
            "code_review_hours_without_ai": 32,
            "planning_velocity_with_ai": [105, 110, 114, 118, 120, 124][i],
            "planning_velocity_without_ai": 95,
            "documentation_hours_with_ai": [12, 10, 9, 8, 7, 6][i],
            "documentation_hours_without_ai": 18,
            "snapshot_date": date(2026, 1, 25),
        }
        for i in range(6)
    ),
    *(
        {
            "program_code": "PHOENIX",
            "sprint_number": 14 + i,
            "estimation_accuracy_with_ai": [0.70, 0.72, 0.74, 0.76, 0.77, 0.79][i],
            "estimation_accuracy_without_ai": 0.68,
            "code_review_hours_with_ai": [30, 30, 28, 28, 26, 26][i],
            "code_review_hours_without_ai": 30,
            "planning_velocity_with_ai": [94, 96, 98, 100, 102, 104][i],
            "planning_velocity_without_ai": 92,
            "documentation_hours_with_ai": [14, 13, 12, 12, 11, 11][i],
            "documentation_hours_without_ai": 16,
            "snapshot_date": date(2026, 1, 25),
        }
        for i in range(6)
    ),
]


# ---------------------------------------------------------------------------
# Trust scores per programme (6-factor)
# ---------------------------------------------------------------------------


class AiTrustScoreSeed(TypedDict):
    tool_name: str
    program_code: str
    snapshot_date: date
    provenance_score: float
    review_status_score: float
    test_coverage_score: float
    drift_check_score: float
    override_rate_score: float
    defect_rate_score: float
    composite_score: float
    maturity_level: str


AI_TRUST_SCORES: list[AiTrustScoreSeed] = [
    # Sentinel — Maturity Level 4 (Optimising)
    {
        "tool_name": "Claude for Devs",
        "program_code": "SENTINEL",
        "snapshot_date": date(2026, 3, 31),
        "provenance_score": 95,
        "review_status_score": 92,
        "test_coverage_score": 86,
        "drift_check_score": 88,
        "override_rate_score": 92,
        "defect_rate_score": 90,
        "composite_score": 90.5,
        "maturity_level": "L4-Optimising",
    },
    # Atlas — Level 3 (Defined)
    {
        "tool_name": "GitHub Copilot",
        "program_code": "ATLAS",
        "snapshot_date": date(2026, 3, 31),
        "provenance_score": 82,
        "review_status_score": 78,
        "test_coverage_score": 78,
        "drift_check_score": 72,
        "override_rate_score": 70,
        "defect_rate_score": 78,
        "composite_score": 76.3,
        "maturity_level": "L3-Defined",
    },
    # Phoenix — Level 2 (Managed), gates failing
    {
        "tool_name": "Claude for Devs",
        "program_code": "PHOENIX",
        "snapshot_date": date(2026, 3, 31),
        "provenance_score": 70,
        "review_status_score": 68,
        "test_coverage_score": 72,
        "drift_check_score": 64,
        "override_rate_score": 58,
        "defect_rate_score": 62,
        "composite_score": 65.7,
        "maturity_level": "L2-Managed",
    },
    # Titan — Level 3
    {
        "tool_name": "GitHub Copilot",
        "program_code": "TITAN",
        "snapshot_date": date(2026, 3, 31),
        "provenance_score": 78,
        "review_status_score": 76,
        "test_coverage_score": 74,
        "drift_check_score": 68,
        "override_rate_score": 66,
        "defect_rate_score": 72,
        "composite_score": 72.3,
        "maturity_level": "L3-Defined",
    },
]


# ---------------------------------------------------------------------------
# Governance config (policies + controls)
# ---------------------------------------------------------------------------


class AiGovernanceConfigSeed(TypedDict):
    config_type: str
    name: str
    description: str
    scope: str
    enforcement_method: str
    program_code: str | None
    status: str
    compliance_pct: float
    last_audit_date: date
    review_date: date
    owner: str


AI_GOVERNANCE_CONFIG: list[AiGovernanceConfigSeed] = [
    {"config_type": "policy", "name": "AI-generated code must be human-reviewed", "description": "Every AI-generated PR requires at least one human reviewer signed off before merge.", "scope": "Global", "enforcement_method": "Branch protection rule", "program_code": None, "status": "Active", "compliance_pct": 98.0, "last_audit_date": date(2026, 3, 1), "review_date": date(2026, 9, 1), "owner": "CTO Office"},
    {"config_type": "policy", "name": "AI provenance tagging required", "description": "Every AI-generated artifact tagged with tool name + prompt hash in commit trailer.", "scope": "Global", "enforcement_method": "Pre-commit hook", "program_code": None, "status": "Active", "compliance_pct": 94.0, "last_audit_date": date(2026, 3, 15), "review_date": date(2026, 9, 15), "owner": "CTO Office"},
    {"config_type": "control", "name": "AI code coverage ≥ 80%", "description": "AI-generated modules must meet 80% unit test coverage before merge.", "scope": "Programme", "enforcement_method": "CI gate", "program_code": "SENTINEL", "status": "Active", "compliance_pct": 96.0, "last_audit_date": date(2026, 3, 20), "review_date": date(2026, 6, 20), "owner": "Suresh Menon"},
    {"config_type": "control", "name": "AI code coverage ≥ 80%", "description": "Same control on Phoenix — currently below target.", "scope": "Programme", "enforcement_method": "CI gate", "program_code": "PHOENIX", "status": "Active", "compliance_pct": 72.0, "last_audit_date": date(2026, 3, 25), "review_date": date(2026, 6, 25), "owner": "Priya Sharma"},
    {"config_type": "control", "name": "Override requires justification", "description": "Any human override of an AI suggestion requires a typed rationale captured in the override log.", "scope": "Global", "enforcement_method": "IDE plugin + server log", "program_code": None, "status": "Active", "compliance_pct": 88.0, "last_audit_date": date(2026, 3, 10), "review_date": date(2026, 9, 10), "owner": "CTO Office"},
    {"config_type": "control", "name": "Weekly drift check on prompt templates", "description": "Prompts used by AI tools scanned weekly for drift vs approved library.", "scope": "Global", "enforcement_method": "Scheduled scan", "program_code": None, "status": "Active", "compliance_pct": 100.0, "last_audit_date": date(2026, 4, 1), "review_date": date(2026, 10, 1), "owner": "Platform Team"},
]


# ---------------------------------------------------------------------------
# Override log (recent overrides of AI suggestions)
# ---------------------------------------------------------------------------


class AiOverrideLogSeed(TypedDict):
    tool_name: str
    program_code: str
    project_code: str | None
    override_date: datetime
    override_type: str
    reason: str
    outcome: str
    approver: str


AI_OVERRIDE_LOG: list[AiOverrideLogSeed] = [
    {"tool_name": "Claude for Devs", "program_code": "SENTINEL", "project_code": "SNTL-AUTO", "override_date": datetime(2026, 3, 12, 14, 30), "override_type": "Rejected suggestion", "reason": "Suggestion missed the retry-on-429 edge case", "outcome": "Manual implementation shipped; post-hoc test added to regression suite", "approver": "Suresh Menon"},
    {"tool_name": "GitHub Copilot", "program_code": "ATLAS", "project_code": "ATLS-LNS", "override_date": datetime(2026, 3, 18, 10, 5), "override_type": "Modified suggestion", "reason": "Terraform module suggestion used non-approved provider version", "outcome": "Suggestion accepted after version pin", "approver": "Suresh Menon"},
    {"tool_name": "Claude for Devs", "program_code": "PHOENIX", "project_code": "PHOE-INT", "override_date": datetime(2026, 3, 22, 16, 45), "override_type": "Rejected suggestion", "reason": "Proposed race-condition-susceptible ordering", "outcome": "Raised as pattern alert; prompt template updated", "approver": "Raj Kumar"},
    {"tool_name": "GitHub Copilot", "program_code": "PHOENIX", "project_code": "PHOE-CBM", "override_date": datetime(2026, 3, 28, 11, 20), "override_type": "Escalated", "reason": "AI generated a regulatory-risk query without review", "outcome": "Blocked; mandatory review added to CI", "approver": "Priya Sharma"},
    {"tool_name": "Snyk AI", "program_code": "SENTINEL", "project_code": "SNTL-AUTO", "override_date": datetime(2026, 3, 30, 9, 0), "override_type": "False positive", "reason": "CVE flagged on a dev-only dependency", "outcome": "Whitelisted with documented rationale", "approver": "Suresh Menon"},
]
