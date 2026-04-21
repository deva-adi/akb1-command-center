"""Hercules programme demo seed data — Workload Consolidation for GlobalBank Corp.

New programme added via CSV import (I-5b) and seeded here for full drill-down
coverage across Tabs 1-11. Three projects:
  HERC-INFRA  — Infrastructure Consolidation (Scrum, 8 people, Medium AI)
  HERC-DATA   — Data Lake Migration (Scrum, 7 people, Heavy AI)
  HERC-MGT    — Service Management Platform (Kanban, 7 people, Light AI)

BAC: ₹9,500,000 | Status: On Track | Start: 2026-02-01 | End: 2027-09-30
"""
from __future__ import annotations

from datetime import date, timedelta
from typing import TypedDict

# ---------------------------------------------------------------------------
# Re-use TypedDict classes from the sibling seed modules.
# These imports allow type-checking; at runtime they resolve the same dicts.
# ---------------------------------------------------------------------------
from app.seed.data import ProgrammeSeed, ProjectSeed, RiskSeed
from app.seed.delivery_data import (
    BacklogItemSeed,
    EvmSnapshotSeed,
    FlowMetricsSeed,
    MilestoneSeed,
    SprintSeed,
    _evm_series,
)


def _weeks(n: int) -> timedelta:
    return timedelta(weeks=n)


# ===========================================================================
# Programme
# ===========================================================================

HERC_PROGRAMME: ProgrammeSeed = {
    "name": "Hercules Workload Consolidation",
    "code": "HERCULES",
    "client": "GlobalBank Corp",
    "start_date": date(2026, 2, 1),
    "end_date": date(2027, 9, 30),
    "status": "On Track",
    "bac": 9_500_000,
    "revenue": 9_500_000,
    "team_size": 22,
    "offshore_ratio": 0.60,
    "delivery_model": "Managed Services",
    "currency_code": "INR",
}


# ===========================================================================
# Projects
# ===========================================================================

HERC_PROJECTS: list[ProjectSeed] = [
    {
        "program_code": "HERCULES",
        "name": "Infrastructure Consolidation",
        "code": "HERC-INFRA",
        "start_date": date(2026, 2, 15),
        "end_date": date(2027, 3, 31),
        "bac": 3_800_000,
        "revenue": 3_800_000,
        "team_size": 8,
        "tech_stack": "AWS, Kubernetes, Terraform, Ansible",
        "is_ai_augmented": True,
        "ai_augmentation_level": "Medium",
        "delivery_methodology": "Scrum",
    },
    {
        "program_code": "HERCULES",
        "name": "Data Lake Migration",
        "code": "HERC-DATA",
        "start_date": date(2026, 3, 1),
        "end_date": date(2027, 6, 30),
        "bac": 3_500_000,
        "revenue": 3_500_000,
        "team_size": 7,
        "tech_stack": "Databricks, Snowflake, dbt, Python",
        "is_ai_augmented": True,
        "ai_augmentation_level": "Heavy",
        "delivery_methodology": "Scrum",
    },
    {
        "program_code": "HERCULES",
        "name": "Service Management Platform",
        "code": "HERC-MGT",
        "start_date": date(2026, 2, 1),
        "end_date": date(2027, 9, 30),
        "bac": 2_200_000,
        "revenue": 2_200_000,
        "team_size": 7,
        "tech_stack": "ServiceNow, Python, Jira, Grafana",
        "is_ai_augmented": True,
        "ai_augmentation_level": "Light",
        "delivery_methodology": "Kanban",
    },
]


# ===========================================================================
# Sprints
# ===========================================================================
# HERC-INFRA: 6 sprints, 14-day cadence, start 2026-03-01
# Medium AI — velocity improving sprint-over-sprint.
# HERC-DATA:  5 sprints, 14-day cadence, start 2026-04-01
# Heavy AI  — over-delivers planned capacity every sprint.

HERC_SPRINTS: list[SprintSeed] = [
    # ── HERC-INFRA ──────────────────────────────────────────────────────────
    *(
        {
            "project_code": "HERC-INFRA",
            "sprint_number": 1 + i,
            "start_date": date(2026, 3, 1) + timedelta(days=14 * i),
            "end_date": date(2026, 3, 14) + timedelta(days=14 * i),
            "planned_points": 80,
            "completed_points": [70, 73, 76, 78, 80, 82][i],
            "velocity": [70, 73, 76, 78, 80, 82][i],
            "ai_assisted_points": [16, 20, 22, 24, 26, 28][i],
            "defects_found": [5, 5, 4, 4, 3, 3][i],
            "defects_fixed": [4, 5, 4, 4, 3, 3][i],
            "rework_hours": [14.0, 13.0, 12.0, 10.0, 9.0, 8.0][i],
            "team_size": 8,
            "iteration_type": "Sprint",
            "estimation_unit": "StoryPoints",
        }
        for i in range(6)
    ),
    # ── HERC-DATA ───────────────────────────────────────────────────────────
    *(
        {
            "project_code": "HERC-DATA",
            "sprint_number": 1 + i,
            "start_date": date(2026, 4, 1) + timedelta(days=14 * i),
            "end_date": date(2026, 4, 14) + timedelta(days=14 * i),
            "planned_points": 65,
            "completed_points": [68, 72, 74, 78, 80][i],
            "velocity": [68, 72, 74, 78, 80][i],
            "ai_assisted_points": [32, 36, 38, 42, 46][i],
            "defects_found": [2, 2, 1, 2, 1][i],
            "defects_fixed": [2, 2, 1, 2, 1][i],
            "rework_hours": [5.0, 4.5, 4.0, 3.5, 3.0][i],
            "team_size": 7,
            "iteration_type": "Sprint",
            "estimation_unit": "StoryPoints",
        }
        for i in range(5)
    ),
]


# ===========================================================================
# Flow Metrics (Kanban — HERC-MGT only)
# ===========================================================================
# 10 weeks starting 2026-02-09 (first full week of programme kick-off).
# Cycle times improving as WIP discipline beds in.

HERC_FLOW_METRICS: list[FlowMetricsSeed] = [
    *(
        {
            "project_code": "HERC-MGT",
            "period_start": date(2026, 2, 9) + _weeks(i),
            "period_end": date(2026, 2, 15) + _weeks(i),
            "throughput_items": [6, 7, 8, 7, 8, 9, 8, 9, 10, 9][i],
            "wip_avg": [8.0, 8.5, 9.0, 8.5, 8.0, 8.5, 8.0, 7.5, 7.0, 7.5][i],
            "wip_limit": 12,
            "cycle_time_p50": [2.8, 2.9, 3.0, 2.8, 2.7, 2.6, 2.5, 2.4, 2.3, 2.4][i],
            "cycle_time_p85": [5.5, 5.7, 6.0, 5.5, 5.3, 5.1, 4.9, 4.7, 4.5, 4.7][i],
            "cycle_time_p95": [8.0, 8.3, 8.8, 8.0, 7.7, 7.4, 7.1, 6.8, 6.5, 6.8][i],
            "lead_time_avg": [7.5, 7.8, 8.2, 7.6, 7.3, 7.0, 6.7, 6.4, 6.1, 6.4][i],
            "blocked_time_hours": [1.5, 2.0, 2.5, 2.0, 1.5, 1.0, 1.0, 0.8, 0.5, 0.8][i],
        }
        for i in range(10)
    ),
]


# ===========================================================================
# Backlog Items
# ===========================================================================
# Invariant per sprint:
#   sum(story_points WHERE status != 'added')              == planned_points
#   sum(story_points WHERE status IN ('completed','added')) == completed_points
#
# HERC-INFRA: ~50% AI-assisted (Medium AI)
# HERC-DATA:  ~70% AI-assisted (Heavy AI)
# ===========================================================================

# ── HERC-INFRA Sprint 1 ─────────────────────────────────────────────────────
# planned=80, completed=70, carried_over=10
# Planned stories (not added): sum=80 → 7 completed (sum=70) + 1 carried_over (sum=10)
# completed: 13+10+13+8+10+8+8 = 70 ✓  carried_over: 10 ✓  total planned: 80 ✓

# ── HERC-INFRA Sprint 2 ─────────────────────────────────────────────────────
# planned=80, completed=73, carried_over=7
# Planned stories (not added): sum=80 → 8 completed (sum=73) + 1 carried_over (sum=7)

# ── HERC-INFRA Sprint 3 ─────────────────────────────────────────────────────
# planned=80, completed=76, carried_over=4
# Planned stories (not added): sum=80 → 9 completed (sum=76) + 1 carried_over (sum=4)

# ── HERC-INFRA Sprint 4 ─────────────────────────────────────────────────────
# planned=80, completed=78, carried_over=2
# Planned stories (not added): sum=80 → 8 completed (sum=78) + 1 carried_over (sum=2)

# ── HERC-INFRA Sprint 5 ─────────────────────────────────────────────────────
# planned=80, completed=80 → all planned stories completed, sum=80

# ── HERC-INFRA Sprint 6 ─────────────────────────────────────────────────────
# planned=80, completed=82 → 7 planned completed (sum=80) + 1 added (sum=2)

# ── HERC-DATA Sprint 1 ──────────────────────────────────────────────────────
# planned=65, completed=68 → 7 planned completed (sum=65) + 1 added (sum=3)

# ── HERC-DATA Sprint 2 ──────────────────────────────────────────────────────
# planned=65, completed=72 → 7 planned completed (sum=65) + 1 added (sum=7)

# ── HERC-DATA Sprint 3 ──────────────────────────────────────────────────────
# planned=65, completed=74 → 7 planned completed (sum=65) + 1 added (sum=9)

# ── HERC-DATA Sprint 4 ──────────────────────────────────────────────────────
# planned=65, completed=78 → 7 planned completed (sum=65) + 1 added (sum=13)

# ── HERC-DATA Sprint 5 ──────────────────────────────────────────────────────
# planned=65, completed=80 → 7 planned completed (sum=65) + 1 added (sum=15)

HERC_BACKLOG_ITEMS: list[BacklogItemSeed] = [

    # =========================================================================
    # HERC-INFRA — Infrastructure Consolidation
    # ~50% AI-assisted (Medium AI)
    # Team: Gaurav Mehta, Preethi Iyer, Ashwin Kumar, Madhuri Singh,
    #       Tarun Nair, Pallavi Joshi, Rishi Patel, Sunita Rao
    # =========================================================================

    # ── Sprint 1 · planned=80, completed=70 ──────────────────────────────────
    # Completed (7 stories): 13+10+13+8+10+8+8 = 70
    # Carried over (1 story): 10
    # Total planned (not added): 70+10 = 80 ✓
    {"project_code": "HERC-INFRA", "sprint_number": 1, "item_type": "story",
     "title": "AWS Account Consolidation — Master Payer Setup", "story_points": 13,
     "status": "completed", "assignee": "Gaurav Mehta",
     "is_ai_assisted": True, "defects_raised": 1, "rework_hours": 2.5, "priority": "critical"},
    {"project_code": "HERC-INFRA", "sprint_number": 1, "item_type": "story",
     "title": "Terraform State Backend Migration to S3", "story_points": 10,
     "status": "completed", "assignee": "Preethi Iyer",
     "is_ai_assisted": True, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 1, "item_type": "story",
     "title": "VPN Mesh Topology Design and Implementation", "story_points": 13,
     "status": "completed", "assignee": "Ashwin Kumar",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 3.0, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 1, "item_type": "task",
     "title": "IAM Role Baseline Policy Standards", "story_points": 8,
     "status": "completed", "assignee": "Madhuri Singh",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.5, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 1, "item_type": "story",
     "title": "CloudWatch Dashboard — Infrastructure Overview", "story_points": 10,
     "status": "completed", "assignee": "Tarun Nair",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 1, "item_type": "task",
     "title": "Kubernetes Namespace Segregation Policy", "story_points": 8,
     "status": "completed", "assignee": "Pallavi Joshi",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 1, "item_type": "story",
     "title": "Container Image Scanning Pipeline (ECR + Trivy)", "story_points": 8,
     "status": "completed", "assignee": "Rishi Patel",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 1, "item_type": "story",
     "title": "Network Segmentation — Spoke VPC Peering", "story_points": 10,
     "status": "carried_over", "assignee": "Sunita Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # planned sum = 13+10+13+8+10+8+8+10 = 80 ✓
    # completed sum = 13+10+13+8+10+8+8 = 70 ✓

    # ── Sprint 2 · planned=80, completed=73 ──────────────────────────────────
    # Completed (8 stories): 13+10+8+10+8+8+8+6 = 71... need sum=73
    # Completed: 13+10+8+10+8+10+8+6 = 73 ✓
    # Carried over (1 story): 7
    # Total planned: 73+7 = 80 ✓
    {"project_code": "HERC-INFRA", "sprint_number": 2, "item_type": "story",
     "title": "Kubernetes Cluster Migration — Wave 1 (Dev/Test)", "story_points": 13,
     "status": "completed", "assignee": "Gaurav Mehta",
     "is_ai_assisted": True, "defects_raised": 1, "rework_hours": 2.5, "priority": "critical"},
    {"project_code": "HERC-INFRA", "sprint_number": 2, "item_type": "story",
     "title": "Ansible Playbooks for OS Hardening", "story_points": 10,
     "status": "completed", "assignee": "Preethi Iyer",
     "is_ai_assisted": True, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 2, "item_type": "task",
     "title": "Security Hub Integration — Finding Aggregation", "story_points": 8,
     "status": "completed", "assignee": "Ashwin Kumar",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 2, "item_type": "story",
     "title": "Cost Optimisation Engine — Reserved Instance Analysis", "story_points": 10,
     "status": "completed", "assignee": "Madhuri Singh",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.5, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 2, "item_type": "story",
     "title": "Auto-scaling Policy — EKS Node Groups", "story_points": 8,
     "status": "completed", "assignee": "Tarun Nair",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 2, "item_type": "task",
     "title": "Terraform Module Library — Reusable VPC Patterns", "story_points": 10,
     "status": "completed", "assignee": "Pallavi Joshi",
     "is_ai_assisted": True, "defects_raised": 1, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 2, "item_type": "story",
     "title": "DR Failover Testing — Runbook Automation", "story_points": 8,
     "status": "completed", "assignee": "Rishi Patel",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.5, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 2, "item_type": "story",
     "title": "Transit Gateway Route Table Configuration", "story_points": 6,
     "status": "completed", "assignee": "Sunita Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "low"},
    {"project_code": "HERC-INFRA", "sprint_number": 2, "item_type": "spike",
     "title": "Evaluate Spot Instance Fleet for Batch Workloads", "story_points": 7,
     "status": "carried_over", "assignee": "Gaurav Mehta",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # planned sum = 13+10+8+10+8+10+8+6+7 = 80 ✓
    # completed sum = 13+10+8+10+8+10+8+6 = 73 ✓

    # ── Sprint 3 · planned=80, completed=76 ──────────────────────────────────
    # Completed (9 stories): 13+8+10+8+8+10+8+8+3 = 76 ✓
    # Carried over (1 story): 4
    # Total planned: 76+4 = 80 ✓
    {"project_code": "HERC-INFRA", "sprint_number": 3, "item_type": "story",
     "title": "Kubernetes Cluster Migration — Wave 2 (Staging)", "story_points": 13,
     "status": "completed", "assignee": "Gaurav Mehta",
     "is_ai_assisted": True, "defects_raised": 1, "rework_hours": 2.0, "priority": "critical"},
    {"project_code": "HERC-INFRA", "sprint_number": 3, "item_type": "task",
     "title": "IAM Policy Standardisation Across All Accounts", "story_points": 8,
     "status": "completed", "assignee": "Madhuri Singh",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.5, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 3, "item_type": "story",
     "title": "Cost Optimisation Engine — Savings Plan Modelling", "story_points": 10,
     "status": "completed", "assignee": "Preethi Iyer",
     "is_ai_assisted": True, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 3, "item_type": "story",
     "title": "CloudTrail Centralisation and SIEM Integration", "story_points": 8,
     "status": "completed", "assignee": "Ashwin Kumar",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 3, "item_type": "story",
     "title": "EKS Managed Node Group Rolling Upgrade", "story_points": 8,
     "status": "completed", "assignee": "Tarun Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 3, "item_type": "task",
     "title": "S3 Lifecycle Policy and Intelligent-Tiering", "story_points": 10,
     "status": "completed", "assignee": "Pallavi Joshi",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 3, "item_type": "story",
     "title": "Container Image Scanning — CI Gate Enforcement", "story_points": 8,
     "status": "completed", "assignee": "Rishi Patel",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 3, "item_type": "story",
     "title": "Grafana Dashboard — Multi-account Cost View", "story_points": 8,
     "status": "completed", "assignee": "Sunita Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "low"},
    {"project_code": "HERC-INFRA", "sprint_number": 3, "item_type": "story",
     "title": "Bastion Host Replacement with AWS SSM Session Manager", "story_points": 3,
     "status": "completed", "assignee": "Gaurav Mehta",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "HERC-INFRA", "sprint_number": 3, "item_type": "spike",
     "title": "Evaluate AWS Config Conformance Packs for Compliance", "story_points": 4,
     "status": "carried_over", "assignee": "Madhuri Singh",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # planned sum = 13+8+10+8+8+10+8+8+3+4 = 80 ✓
    # completed sum = 13+8+10+8+8+10+8+8+3 = 76 ✓

    # ── Sprint 4 · planned=80, completed=78 ──────────────────────────────────
    # Completed (8 stories): 13+10+13+8+10+8+8+8 = 78 ✓
    # Carried over (1 story): 2
    # Total planned: 78+2 = 80 ✓
    {"project_code": "HERC-INFRA", "sprint_number": 4, "item_type": "story",
     "title": "Kubernetes Cluster Migration — Wave 3 (Production)", "story_points": 13,
     "status": "completed", "assignee": "Gaurav Mehta",
     "is_ai_assisted": True, "defects_raised": 1, "rework_hours": 2.0, "priority": "critical"},
    {"project_code": "HERC-INFRA", "sprint_number": 4, "item_type": "story",
     "title": "Terraform Remote State Locking — DynamoDB Integration", "story_points": 10,
     "status": "completed", "assignee": "Preethi Iyer",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.5, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 4, "item_type": "story",
     "title": "Multi-region Failover Routing — Route 53 Health Checks", "story_points": 13,
     "status": "completed", "assignee": "Ashwin Kumar",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 4, "item_type": "task",
     "title": "Security Hub — Custom Insights for Consolidated Findings", "story_points": 8,
     "status": "completed", "assignee": "Madhuri Singh",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 4, "item_type": "story",
     "title": "Cost Anomaly Detection — SNS Alert Integration", "story_points": 10,
     "status": "completed", "assignee": "Tarun Nair",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 4, "item_type": "task",
     "title": "Kubernetes RBAC Audit and Remediation", "story_points": 8,
     "status": "completed", "assignee": "Pallavi Joshi",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 4, "item_type": "story",
     "title": "Auto-scaling — Predictive Scaling Policies (EKS + EC2)", "story_points": 8,
     "status": "completed", "assignee": "Rishi Patel",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 4, "item_type": "story",
     "title": "Centralised Secrets Manager Rotation Policies", "story_points": 8,
     "status": "completed", "assignee": "Sunita Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "low"},
    {"project_code": "HERC-INFRA", "sprint_number": 4, "item_type": "spike",
     "title": "Evaluate EKS Karpenter for Node Provisioning", "story_points": 2,
     "status": "carried_over", "assignee": "Gaurav Mehta",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # planned sum = 13+10+13+8+10+8+8+8+2 = 80 ✓
    # completed sum = 13+10+13+8+10+8+8+8 = 78 ✓

    # ── Sprint 5 · planned=80, completed=80 ──────────────────────────────────
    # All 8 stories completed: 13+10+13+8+10+8+10+8 = 80 ✓
    {"project_code": "HERC-INFRA", "sprint_number": 5, "item_type": "story",
     "title": "Kubernetes Cluster Migration — Smoke Test and Cutover", "story_points": 13,
     "status": "completed", "assignee": "Gaurav Mehta",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.5, "priority": "critical"},
    {"project_code": "HERC-INFRA", "sprint_number": 5, "item_type": "story",
     "title": "AWS Config Rules — Compliance-as-Code Baseline", "story_points": 10,
     "status": "completed", "assignee": "Preethi Iyer",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.5, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 5, "item_type": "story",
     "title": "Centralised Log Aggregation — OpenSearch Cluster", "story_points": 13,
     "status": "completed", "assignee": "Ashwin Kumar",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 5, "item_type": "task",
     "title": "IAM Access Analyser — Unused Access Remediation", "story_points": 8,
     "status": "completed", "assignee": "Madhuri Singh",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 5, "item_type": "story",
     "title": "Network ACL Review and Tightening", "story_points": 10,
     "status": "completed", "assignee": "Tarun Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 5, "item_type": "task",
     "title": "Terraform CI/CD Pipeline — Plan/Apply Gating", "story_points": 8,
     "status": "completed", "assignee": "Pallavi Joshi",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 5, "item_type": "story",
     "title": "EKS Pod Security Standards Enforcement", "story_points": 10,
     "status": "completed", "assignee": "Rishi Patel",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 5, "item_type": "story",
     "title": "Cost Dashboard — Chargeback Report by Business Unit", "story_points": 8,
     "status": "completed", "assignee": "Sunita Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "low"},
    # planned sum = 13+10+13+8+10+8+10+8 = 80 ✓
    # completed sum = 80 ✓

    # ── Sprint 6 · planned=80, completed=82 ──────────────────────────────────
    # 7 planned stories completed (sum=80) + 1 added story (sum=2) = 82
    {"project_code": "HERC-INFRA", "sprint_number": 6, "item_type": "story",
     "title": "Multi-account Inventory — AWS Resource Explorer", "story_points": 13,
     "status": "completed", "assignee": "Gaurav Mehta",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.5, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 6, "item_type": "story",
     "title": "Kubernetes HPA Tuning — Custom Metrics (KEDA)", "story_points": 13,
     "status": "completed", "assignee": "Preethi Iyer",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 6, "item_type": "story",
     "title": "Security Posture Report — Executive Dashboard", "story_points": 10,
     "status": "completed", "assignee": "Ashwin Kumar",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 6, "item_type": "task",
     "title": "DR Runbook Testing — Full Failover Simulation", "story_points": 13,
     "status": "completed", "assignee": "Madhuri Singh",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "HERC-INFRA", "sprint_number": 6, "item_type": "story",
     "title": "Spot Instance Fleet — Batch Job Scheduler", "story_points": 10,
     "status": "completed", "assignee": "Tarun Nair",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 6, "item_type": "task",
     "title": "Terraform Drift Detection — Weekly Audit Pipeline", "story_points": 8,
     "status": "completed", "assignee": "Pallavi Joshi",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 6, "item_type": "story",
     "title": "Consolidation Health Check — Final Sign-off Report", "story_points": 13,
     "status": "completed", "assignee": "Rishi Patel",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-INFRA", "sprint_number": 6, "item_type": "spike",
     "title": "Quick-win: Add EBS Snapshot Lifecycle for DR Cost Saving", "story_points": 2,
     "status": "added", "assignee": "Sunita Rao",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # planned sum (not added) = 13+13+10+13+10+8+13 = 80 ✓
    # completed sum = 13+13+10+13+10+8+13+2(added) = 82 ✓

    # =========================================================================
    # HERC-DATA — Data Lake Migration
    # ~70% AI-assisted (Heavy AI)
    # Team: Aditi Sharma, Brijesh Kumar, Chitra Nair, Dinesh Menon,
    #       Esha Pillai, Farhan Ahmad, Geetha Reddy
    # =========================================================================

    # ── Sprint 1 · planned=65, completed=68 ──────────────────────────────────
    # 7 planned completed (sum=65) + 1 added (sum=3) = 68
    # Planned (completed): 13+10+8+10+8+8+8 = 65 ✓
    {"project_code": "HERC-DATA", "sprint_number": 1, "item_type": "story",
     "title": "Snowflake Schema Design — Bronze Layer DDL", "story_points": 13,
     "status": "completed", "assignee": "Aditi Sharma",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "critical"},
    {"project_code": "HERC-DATA", "sprint_number": 1, "item_type": "story",
     "title": "Databricks Cluster Setup — Job Cluster Profiles", "story_points": 10,
     "status": "completed", "assignee": "Brijesh Kumar",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-DATA", "sprint_number": 1, "item_type": "task",
     "title": "dbt Project Scaffolding and Profile Configuration", "story_points": 8,
     "status": "completed", "assignee": "Chitra Nair",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-DATA", "sprint_number": 1, "item_type": "story",
     "title": "Data Quality Framework — Great Expectations Setup", "story_points": 10,
     "status": "completed", "assignee": "Dinesh Menon",
     "is_ai_assisted": True, "defects_raised": 1, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "HERC-DATA", "sprint_number": 1, "item_type": "story",
     "title": "PII Masking Framework — Pre-ingestion Tokenisation", "story_points": 8,
     "status": "completed", "assignee": "Esha Pillai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-DATA", "sprint_number": 1, "item_type": "task",
     "title": "Data Catalog Integration — Apache Atlas Connector", "story_points": 8,
     "status": "completed", "assignee": "Farhan Ahmad",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "HERC-DATA", "sprint_number": 1, "item_type": "story",
     "title": "Historical Data Backfill Feasibility Analysis", "story_points": 8,
     "status": "completed", "assignee": "Geetha Reddy",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-DATA", "sprint_number": 1, "item_type": "spike",
     "title": "Automate Snowflake Role Hierarchy via dbt Macros", "story_points": 3,
     "status": "added", "assignee": "Aditi Sharma",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # planned sum (not added) = 13+10+8+10+8+8+8 = 65 ✓
    # completed sum = 65+3(added) = 68 ✓

    # ── Sprint 2 · planned=65, completed=72 ──────────────────────────────────
    # 7 planned completed (sum=65) + 1 added (sum=7) = 72
    # Planned (completed): 13+10+8+10+8+8+8 = 65 ✓
    {"project_code": "HERC-DATA", "sprint_number": 2, "item_type": "story",
     "title": "Bronze Layer Ingestion — CDC Pipeline via Debezium", "story_points": 13,
     "status": "completed", "assignee": "Aditi Sharma",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "critical"},
    {"project_code": "HERC-DATA", "sprint_number": 2, "item_type": "story",
     "title": "dbt Transformation Models — Silver Layer Core", "story_points": 10,
     "status": "completed", "assignee": "Brijesh Kumar",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-DATA", "sprint_number": 2, "item_type": "task",
     "title": "Data Lineage Tracking — Column-level in Snowflake", "story_points": 8,
     "status": "completed", "assignee": "Chitra Nair",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-DATA", "sprint_number": 2, "item_type": "story",
     "title": "Great Expectations Suites — Source System Rules", "story_points": 10,
     "status": "completed", "assignee": "Dinesh Menon",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-DATA", "sprint_number": 2, "item_type": "story",
     "title": "ML Feature Store Foundation — Databricks Feature Store", "story_points": 8,
     "status": "completed", "assignee": "Esha Pillai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-DATA", "sprint_number": 2, "item_type": "task",
     "title": "Databricks Workflow Orchestration — DAG Templates", "story_points": 8,
     "status": "completed", "assignee": "Farhan Ahmad",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "HERC-DATA", "sprint_number": 2, "item_type": "story",
     "title": "Snowflake External Tables — S3 Partitioned Data", "story_points": 8,
     "status": "completed", "assignee": "Geetha Reddy",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-DATA", "sprint_number": 2, "item_type": "story",
     "title": "AI-generated dbt Source Documentation and Tests", "story_points": 7,
     "status": "added", "assignee": "Brijesh Kumar",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # planned sum (not added) = 13+10+8+10+8+8+8 = 65 ✓
    # completed sum = 65+7(added) = 72 ✓

    # ── Sprint 3 · planned=65, completed=74 ──────────────────────────────────
    # 7 planned completed (sum=65) + 1 added (sum=9) = 74
    # Planned (completed): 13+10+8+10+8+8+8 = 65 ✓
    {"project_code": "HERC-DATA", "sprint_number": 3, "item_type": "story",
     "title": "Silver Layer — dbt Transformations for Core Entities", "story_points": 13,
     "status": "completed", "assignee": "Aditi Sharma",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "critical"},
    {"project_code": "HERC-DATA", "sprint_number": 3, "item_type": "story",
     "title": "Historical Data Backfill — Batch Pipeline Wave 1", "story_points": 10,
     "status": "completed", "assignee": "Brijesh Kumar",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-DATA", "sprint_number": 3, "item_type": "task",
     "title": "PII Masking — Dynamic Data Masking Policies in Snowflake", "story_points": 8,
     "status": "completed", "assignee": "Chitra Nair",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-DATA", "sprint_number": 3, "item_type": "story",
     "title": "Data Quality Alerting — Slack/PagerDuty Integration", "story_points": 10,
     "status": "completed", "assignee": "Dinesh Menon",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "HERC-DATA", "sprint_number": 3, "item_type": "story",
     "title": "ML Feature Store — Feature Registration Workflow", "story_points": 8,
     "status": "completed", "assignee": "Esha Pillai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-DATA", "sprint_number": 3, "item_type": "task",
     "title": "Databricks Unity Catalog — Governance Setup", "story_points": 8,
     "status": "completed", "assignee": "Farhan Ahmad",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-DATA", "sprint_number": 3, "item_type": "story",
     "title": "Snowflake Resource Monitor — Cost Governance", "story_points": 8,
     "status": "completed", "assignee": "Geetha Reddy",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-DATA", "sprint_number": 3, "item_type": "story",
     "title": "AI Auto-generated Data Contract Stubs (schema + SLA)", "story_points": 9,
     "status": "added", "assignee": "Aditi Sharma",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    # planned sum (not added) = 13+10+8+10+8+8+8 = 65 ✓
    # completed sum = 65+9(added) = 74 ✓

    # ── Sprint 4 · planned=65, completed=78 ──────────────────────────────────
    # 7 planned completed (sum=65) + 1 added (sum=13) = 78
    # Planned (completed): 13+10+8+10+8+8+8 = 65 ✓
    {"project_code": "HERC-DATA", "sprint_number": 4, "item_type": "story",
     "title": "Gold Layer — dbt Aggregations for Reporting Views", "story_points": 13,
     "status": "completed", "assignee": "Aditi Sharma",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "critical"},
    {"project_code": "HERC-DATA", "sprint_number": 4, "item_type": "story",
     "title": "Historical Backfill — Wave 2 (5-year Data Range)", "story_points": 10,
     "status": "completed", "assignee": "Brijesh Kumar",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-DATA", "sprint_number": 4, "item_type": "task",
     "title": "dbt Incremental Model Optimisation — Late-arriving Records", "story_points": 8,
     "status": "completed", "assignee": "Chitra Nair",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-DATA", "sprint_number": 4, "item_type": "story",
     "title": "Data Lineage Dashboard — Atlan Integration", "story_points": 10,
     "status": "completed", "assignee": "Dinesh Menon",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-DATA", "sprint_number": 4, "item_type": "story",
     "title": "Databricks AutoML — Baseline Churn Model", "story_points": 8,
     "status": "completed", "assignee": "Esha Pillai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "HERC-DATA", "sprint_number": 4, "item_type": "task",
     "title": "CDC Pipeline SLA Monitoring — Prometheus Metrics", "story_points": 8,
     "status": "completed", "assignee": "Farhan Ahmad",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 1.0, "priority": "medium"},
    {"project_code": "HERC-DATA", "sprint_number": 4, "item_type": "story",
     "title": "Snowflake Query Performance Optimisation — Clustering Keys", "story_points": 8,
     "status": "completed", "assignee": "Geetha Reddy",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-DATA", "sprint_number": 4, "item_type": "story",
     "title": "AI-powered Data Anomaly Detector — Isolation Forest Model", "story_points": 13,
     "status": "added", "assignee": "Esha Pillai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    # planned sum (not added) = 13+10+8+10+8+8+8 = 65 ✓
    # completed sum = 65+13(added) = 78 ✓

    # ── Sprint 5 · planned=65, completed=80 ──────────────────────────────────
    # 7 planned completed (sum=65) + 1 added (sum=15) = 80
    # Planned (completed): 13+10+8+10+8+8+8 = 65 ✓
    {"project_code": "HERC-DATA", "sprint_number": 5, "item_type": "story",
     "title": "End-to-End Migration Smoke Test — Bronze → Silver → Gold", "story_points": 13,
     "status": "completed", "assignee": "Aditi Sharma",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "critical"},
    {"project_code": "HERC-DATA", "sprint_number": 5, "item_type": "story",
     "title": "Regulatory Data Retention — Snowflake Time Travel Config", "story_points": 10,
     "status": "completed", "assignee": "Brijesh Kumar",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-DATA", "sprint_number": 5, "item_type": "task",
     "title": "dbt CI/CD Pipeline — PR Checks with Slim CI", "story_points": 8,
     "status": "completed", "assignee": "Chitra Nair",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-DATA", "sprint_number": 5, "item_type": "story",
     "title": "Great Expectations — Gold Layer Validation Suites", "story_points": 10,
     "status": "completed", "assignee": "Dinesh Menon",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-DATA", "sprint_number": 5, "item_type": "story",
     "title": "ML Feature Store — Serving API via Databricks Model Serving", "story_points": 8,
     "status": "completed", "assignee": "Esha Pillai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "HERC-DATA", "sprint_number": 5, "item_type": "task",
     "title": "Databricks Cost Attribution — Tags + Unity Catalog Budgets", "story_points": 8,
     "status": "completed", "assignee": "Farhan Ahmad",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-DATA", "sprint_number": 5, "item_type": "story",
     "title": "Data Lake Hand-off Documentation and Runbook", "story_points": 8,
     "status": "completed", "assignee": "Geetha Reddy",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-DATA", "sprint_number": 5, "item_type": "story",
     "title": "AI Predictive Quality Gate — Pre-load Scoring Model", "story_points": 15,
     "status": "added", "assignee": "Aditi Sharma",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    # planned sum (not added) = 13+10+8+10+8+8+8 = 65 ✓
    # completed sum = 65+15(added) = 80 ✓
]


# ===========================================================================
# Risks
# ===========================================================================

HERC_RISKS: list[RiskSeed] = [
    {
        "program_code": "HERCULES",
        "title": "Cloud Cost Overrun",
        "description": (
            "AWS multi-account consolidation may exceed BAC by 15-20% if Reserved "
            "Instance coverage remains below 60%; current RI coverage is 42%."
        ),
        "category": "Commercial",
        "probability": 0.70,
        "impact": 1_425_000,
        "severity": "High",
        "status": "Open",
        "owner": "Gaurav Mehta",
        "mitigation_plan": (
            "Activate Savings Plans for steady-state workloads; enforce tagging policy "
            "for cost anomaly detection; weekly FinOps review cadence."
        ),
    },
    {
        "program_code": "HERCULES",
        "title": "Data Migration — Silent Data Loss",
        "description": (
            "Historical backfill pipeline lacks row-count reconciliation; silent data loss "
            "from source truncation or encoding mismatches could corrupt Gold layer."
        ),
        "category": "Quality",
        "probability": 0.20,
        "impact": 2_800_000,
        "severity": "Critical",
        "status": "Open",
        "owner": "Aditi Sharma",
        "mitigation_plan": (
            "Implement Great Expectations reconciliation checkpoints at each layer boundary; "
            "dual-source row-count assertions before any cutover."
        ),
    },
    {
        "program_code": "HERCULES",
        "title": "Key Resource Attrition",
        "description": (
            "Two senior engineers (Gaurav Mehta, Aditi Sharma) hold critical knowledge; "
            "attrition would delay Wave 3 cluster migration by 6-8 weeks."
        ),
        "category": "Resource",
        "probability": 0.35,
        "impact": 475_000,
        "severity": "Medium",
        "status": "Open",
        "owner": "Hari Krishnan",
        "mitigation_plan": (
            "Cross-train two mid-level engineers; maintain architecture decision records (ADRs); "
            "retention bonus approved for critical path individuals."
        ),
    },
    {
        "program_code": "HERCULES",
        "title": "Vendor Lock-in — Databricks / Snowflake",
        "description": (
            "Deep Databricks and Snowflake coupling without abstraction layers could "
            "make future platform migration cost-prohibitive for GlobalBank Corp."
        ),
        "category": "Technical",
        "probability": 0.40,
        "impact": 600_000,
        "severity": "Medium",
        "status": "Open",
        "owner": "Aditi Sharma",
        "mitigation_plan": (
            "Design dbt models as the abstraction layer; use open formats (Delta, Iceberg) "
            "for storage; document vendor-specific features separately in ADRs."
        ),
    },
]


# ===========================================================================
# Monthly KPI Values
# ===========================================================================
# Months: 2026-02-01, 2026-03-01, 2026-04-01
# Keys: (programme_code, kpi_code) → list of values per month

HERC_MONTHLY_KPI_VALUES: dict[tuple[str, str], list[float]] = {
    # CPI — slight dip in March (infra onboarding ramp), recovering in April
    ("HERCULES", "CPI"): [1.02, 0.98, 1.05],
    # SPI — ahead of schedule (new programme energy, strong team)
    ("HERCULES", "SPI"): [1.05, 1.02, 1.08],
    # Utilisation — growing as team hits its stride
    ("HERCULES", "UTIL"): [0.72, 0.75, 0.78],
    # Gross margin — healthy; slight dip in March due to infra setup costs
    ("HERCULES", "MARGIN"): [0.38, 0.36, 0.40],
    # Attrition — zero for first two months; one departure in April
    ("HERCULES", "ATTRITION"): [0.0, 0.0, 0.05],
}

# Month start dates aligned to the KPI value lists above
HERC_MONTH_STARTS: list[date] = [
    date(2026, 2, 1),
    date(2026, 3, 1),
    date(2026, 4, 1),
]


# ===========================================================================
# Commercial Scenarios
# ===========================================================================

# Re-use the CommercialSeed TypedDict from commercial_data.py
from app.seed.commercial_data import CommercialSeed  # noqa: E402

HERC_COMMERCIAL_SCENARIOS: list[CommercialSeed] = [
    # ── Baseline Scenario ────────────────────────────────────────────────────
    # Planned revenue = 9,500,000 over the programme; quarterly snapshots.
    # Costs calibrated to 35% gross margin at plan.
    {
        "program_code": "HERCULES",
        "scenario_name": "Baseline",
        "planned_revenue": 791_667,          # ≈ 9.5M / 12 months
        "actual_revenue": 775_833,           # 98% realisation (ramp-up phase)
        "planned_cost": 514_583,             # ~35% gross margin
        "actual_cost": 527_167,             # 2.4% cost overrun (infra setup)
        "gross_margin_pct": 0.38,
        "contribution_margin_pct": 0.28,
        "portfolio_margin_pct": 0.22,
        "net_margin_pct": 0.14,
        "snapshot_date": date(2026, 2, 1),
        "notes": "Programme kick-off month; infra provisioning costs front-loaded.",
    },
    {
        "program_code": "HERCULES",
        "scenario_name": "Baseline",
        "planned_revenue": 791_667,
        "actual_revenue": 783_750,           # 99% realisation
        "planned_cost": 514_583,
        "actual_cost": 524_688,             # 2% cost overrun (March ramp)
        "gross_margin_pct": 0.36,
        "contribution_margin_pct": 0.26,
        "portfolio_margin_pct": 0.20,
        "net_margin_pct": 0.12,
        "snapshot_date": date(2026, 3, 1),
        "notes": "HERC-DATA project onboarding; additional tooling licences.",
    },
    {
        "program_code": "HERCULES",
        "scenario_name": "Baseline",
        "planned_revenue": 791_667,
        "actual_revenue": 807_500,           # 102% realisation (catch-up billing)
        "planned_cost": 514_583,
        "actual_cost": 484_750,             # below plan as team reaches steady state
        "gross_margin_pct": 0.40,
        "contribution_margin_pct": 0.30,
        "portfolio_margin_pct": 0.24,
        "net_margin_pct": 0.16,
        "snapshot_date": date(2026, 4, 1),
        "notes": "All three projects fully staffed; velocity improving across board.",
    },
    # ── Optimistic Scenario — AI Productivity Gains ──────────────────────────
    # Assumes heavy-AI (HERC-DATA) delivers 20% velocity uplift beyond plan,
    # reducing cost of delivery while maintaining revenue recognition schedule.
    {
        "program_code": "HERCULES",
        "scenario_name": "Optimistic (AI Uplift)",
        "planned_revenue": 791_667,
        "actual_revenue": 791_667,           # on-plan
        "planned_cost": 514_583,
        "actual_cost": 494_000,             # 4% cost reduction via AI efficiency
        "gross_margin_pct": 0.42,
        "contribution_margin_pct": 0.32,
        "portfolio_margin_pct": 0.26,
        "net_margin_pct": 0.18,
        "snapshot_date": date(2026, 2, 1),
        "notes": (
            "Optimistic: HERC-DATA AI over-delivery (planned_pts=65, achieved=68+) "
            "reduces senior engineer hours needed, cutting cost by ~4%."
        ),
    },
    {
        "program_code": "HERCULES",
        "scenario_name": "Optimistic (AI Uplift)",
        "planned_revenue": 791_667,
        "actual_revenue": 807_500,           # 102% — early delivery milestone
        "planned_cost": 514_583,
        "actual_cost": 488_354,             # 5% cost reduction
        "gross_margin_pct": 0.44,
        "contribution_margin_pct": 0.34,
        "portfolio_margin_pct": 0.28,
        "net_margin_pct": 0.20,
        "snapshot_date": date(2026, 3, 1),
        "notes": (
            "Optimistic: AI augmentation across HERC-INFRA and HERC-DATA "
            "enables completion of Wave 2 migration 1 sprint ahead of plan."
        ),
    },
    {
        "program_code": "HERCULES",
        "scenario_name": "Optimistic (AI Uplift)",
        "planned_revenue": 791_667,
        "actual_revenue": 823_334,           # 104% — value-add scope accepted
        "planned_cost": 514_583,
        "actual_cost": 477_292,             # 7% cost reduction
        "gross_margin_pct": 0.42,
        "contribution_margin_pct": 0.36,
        "portfolio_margin_pct": 0.30,
        "net_margin_pct": 0.22,
        "snapshot_date": date(2026, 4, 1),
        "notes": (
            "Optimistic: AI-powered predictive scaling (HERC-INFRA Sprint 4) "
            "delivers quantified cloud cost saving presented to client as value-add; "
            "client approves ₹95K incremental revenue item."
        ),
    },
]


# ===========================================================================
# EVM Snapshots (HERC-INFRA and HERC-DATA only — Kanban projects excluded)
# ===========================================================================
# 12-month window from project start, mixing actuals (months 1-2) + projections.

HERC_EVM_SNAPSHOTS: list[EvmSnapshotSeed] = [
    *_evm_series(
        "HERC-INFRA",
        3_800_000,
        date(2026, 3, 1),
        pv_curve=[0.04, 0.10, 0.18, 0.27, 0.36, 0.45, 0.54, 0.63, 0.72, 0.80, 0.87, 0.94],
        # CPI improving sprint-over-sprint as team adopts AI tooling (Medium AI)
        cpi_trend=[1.00, 1.01, 1.02, 1.03, 1.04, 1.05, 1.05, 1.06, 1.06, 1.07, 1.07, 1.08],
        # SPI slightly behind early (ramp-up), catching up by month 4
        spi_trend=[0.95, 0.97, 0.99, 1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.06, 1.07, 1.07],
        notes_final="Wave 3 migration complete; consolidation health check signed off",
    ),
    *_evm_series(
        "HERC-DATA",
        3_500_000,
        date(2026, 4, 1),
        pv_curve=[0.05, 0.13, 0.22, 0.32, 0.42, 0.52, 0.62, 0.71, 0.80, 0.87, 0.93, 0.98],
        # CPI excellent — heavy AI augmentation drives cost efficiency
        cpi_trend=[1.05, 1.07, 1.09, 1.10, 1.11, 1.12, 1.13, 1.14, 1.14, 1.15, 1.15, 1.16],
        # SPI consistently above 1.0 (Heavy AI over-delivery pattern)
        spi_trend=[1.02, 1.03, 1.04, 1.05, 1.05, 1.06, 1.06, 1.07, 1.07, 1.07, 1.08, 1.08],
        notes_final="Gold layer fully migrated; predictive quality gate operational",
    ),
]


# ===========================================================================
# Milestones (4-6 per project, all 3 HERC projects)
# ===========================================================================

HERC_MILESTONES: list[MilestoneSeed] = [
    # ── HERC-INFRA ───────────────────────────────────────────────────────────
    {
        "project_code": "HERC-INFRA",
        "name": "Account consolidation kickoff",
        "planned_date": date(2026, 2, 15),
        "actual_date": date(2026, 2, 15),
        "status": "Completed",
        "owner": "Gaurav Mehta",
        "notes": "On time; AWS master payer account activated",
    },
    {
        "project_code": "HERC-INFRA",
        "name": "Wave 1 migration complete (Dev/Test)",
        "planned_date": date(2026, 3, 28),
        "actual_date": date(2026, 3, 26),
        "status": "Completed",
        "owner": "Gaurav Mehta",
        "notes": "2 days ahead — Kubernetes cluster migration ran smoothly",
    },
    {
        "project_code": "HERC-INFRA",
        "name": "Wave 2 migration complete (Staging)",
        "planned_date": date(2026, 4, 25),
        "actual_date": date(2026, 4, 23),
        "status": "Completed",
        "owner": "Gaurav Mehta",
        "notes": "2 days ahead; AI-assisted Terraform drift detection paid off",
    },
    {
        "project_code": "HERC-INFRA",
        "name": "Wave 3 migration complete (Production)",
        "planned_date": date(2026, 5, 23),
        "actual_date": None,
        "status": "In Progress",
        "owner": "Gaurav Mehta",
        "notes": "Sprint 4 in progress; EKS prod cutover scheduled",
    },
    {
        "project_code": "HERC-INFRA",
        "name": "Security posture sign-off",
        "planned_date": date(2026, 7, 31),
        "actual_date": None,
        "status": "Pending",
        "owner": "Ashwin Kumar",
        "notes": "Contingent on Wave 3 completion",
    },
    {
        "project_code": "HERC-INFRA",
        "name": "Consolidation programme closure",
        "planned_date": date(2027, 3, 31),
        "actual_date": None,
        "status": "Pending",
        "owner": "Gaurav Mehta",
        "notes": None,
    },

    # ── HERC-DATA ────────────────────────────────────────────────────────────
    {
        "project_code": "HERC-DATA",
        "name": "Data lake architecture approved",
        "planned_date": date(2026, 3, 1),
        "actual_date": date(2026, 3, 1),
        "status": "Completed",
        "owner": "Aditi Sharma",
        "notes": "Bronze-Silver-Gold medallion design signed off by GlobalBank architects",
    },
    {
        "project_code": "HERC-DATA",
        "name": "Bronze layer live (raw ingestion)",
        "planned_date": date(2026, 4, 14),
        "actual_date": date(2026, 4, 12),
        "status": "Completed",
        "owner": "Aditi Sharma",
        "notes": "2 days ahead — AI-assisted pipeline generation (Sprint 1 over-delivery)",
    },
    {
        "project_code": "HERC-DATA",
        "name": "Silver layer live (cleansed data)",
        "planned_date": date(2026, 5, 26),
        "actual_date": date(2026, 5, 22),
        "status": "Completed",
        "owner": "Brijesh Kumar",
        "notes": "4 days ahead; dbt model count exceeded target by 18 models",
    },
    {
        "project_code": "HERC-DATA",
        "name": "Gold layer live (business metrics)",
        "planned_date": date(2026, 7, 7),
        "actual_date": None,
        "status": "In Progress",
        "owner": "Aditi Sharma",
        "notes": "Sprint 5 in flight; Great Expectations validation suites deploying",
    },
    {
        "project_code": "HERC-DATA",
        "name": "ML feature store operational",
        "planned_date": date(2026, 9, 30),
        "actual_date": None,
        "status": "Pending",
        "owner": "Aditi Sharma",
        "notes": None,
    },
    {
        "project_code": "HERC-DATA",
        "name": "Data lake handover to GlobalBank",
        "planned_date": date(2027, 6, 30),
        "actual_date": None,
        "status": "Pending",
        "owner": "Aditi Sharma",
        "notes": None,
    },

    # ── HERC-MGT ─────────────────────────────────────────────────────────────
    {
        "project_code": "HERC-MGT",
        "name": "ServiceNow baseline configured",
        "planned_date": date(2026, 2, 28),
        "actual_date": date(2026, 2, 27),
        "status": "Completed",
        "owner": "Hari Krishnan",
        "notes": "1 day ahead; ITSM workflows and SLA rules activated",
    },
    {
        "project_code": "HERC-MGT",
        "name": "Incident management live",
        "planned_date": date(2026, 3, 31),
        "actual_date": date(2026, 3, 30),
        "status": "Completed",
        "owner": "Hari Krishnan",
        "notes": "P1/P2 escalation paths validated; WIP discipline bedding in",
    },
    {
        "project_code": "HERC-MGT",
        "name": "Change management process adopted",
        "planned_date": date(2026, 5, 31),
        "actual_date": None,
        "status": "In Progress",
        "owner": "Indira Nair",
        "notes": "CAB cadence established; week 10 metrics looking strong",
    },
    {
        "project_code": "HERC-MGT",
        "name": "Grafana observability dashboards live",
        "planned_date": date(2026, 8, 31),
        "actual_date": None,
        "status": "Pending",
        "owner": "Hari Krishnan",
        "notes": None,
    },
    {
        "project_code": "HERC-MGT",
        "name": "Service management platform handover",
        "planned_date": date(2027, 9, 30),
        "actual_date": None,
        "status": "Pending",
        "owner": "Hari Krishnan",
        "notes": None,
    },
]


# ===========================================================================
# HERC-MGT Kanban Flow Items (weeks 1–10, matching HERC_FLOW_METRICS)
# ===========================================================================
# Team (7 people): Hari Krishnan, Indira Nair, Jyoti Pillai, Kishore Kumar,
#                  Lakshmi Menon, Mohan Rao, Nalini Sharma
# Throughput per HERC_FLOW_METRICS: [6, 7, 8, 7, 8, 9, 8, 9, 10, 9]

HERC_MGT_FLOW_ITEMS: list[BacklogItemSeed] = [
    # Week 1 — 6 completed, 2 WIP (wip_avg=8.0)
    {"project_code": "HERC-MGT", "sprint_number": 1, "item_type": "task",
     "title": "ServiceNow instance provisioning and baseline config", "story_points": 8,
     "status": "completed", "assignee": "Hari Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "critical"},
    {"project_code": "HERC-MGT", "sprint_number": 1, "item_type": "task",
     "title": "ITSM workflow design — incident classification matrix", "story_points": 5,
     "status": "completed", "assignee": "Indira Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-MGT", "sprint_number": 1, "item_type": "story",
     "title": "SLA rule engine — P1/P2 thresholds and escalation paths", "story_points": 8,
     "status": "completed", "assignee": "Jyoti Pillai",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "HERC-MGT", "sprint_number": 1, "item_type": "task",
     "title": "Jira–ServiceNow bi-directional sync setup", "story_points": 5,
     "status": "completed", "assignee": "Kishore Kumar",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-MGT", "sprint_number": 1, "item_type": "task",
     "title": "On-call rotation schedule and runbook template", "story_points": 3,
     "status": "completed", "assignee": "Lakshmi Menon",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "HERC-MGT", "sprint_number": 1, "item_type": "task",
     "title": "Grafana alerting integration — Slack webhook config", "story_points": 3,
     "status": "completed", "assignee": "Mohan Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "HERC-MGT", "sprint_number": 1, "item_type": "story",
     "title": "Change advisory board (CAB) cadence and templates", "story_points": 5,
     "status": "in_progress", "assignee": "Nalini Sharma",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "HERC-MGT", "sprint_number": 1, "item_type": "task",
     "title": "Asset CMDB initial data load from legacy ITSM", "story_points": 8,
     "status": "in_progress", "assignee": "Hari Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},

    # Week 2 — 7 completed, 2 WIP (wip_avg=8.5)
    {"project_code": "HERC-MGT", "sprint_number": 2, "item_type": "story",
     "title": "Change advisory board (CAB) cadence and templates", "story_points": 5,
     "status": "completed", "assignee": "Nalini Sharma",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-MGT", "sprint_number": 2, "item_type": "task",
     "title": "Asset CMDB initial data load from legacy ITSM", "story_points": 8,
     "status": "completed", "assignee": "Hari Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "HERC-MGT", "sprint_number": 2, "item_type": "story",
     "title": "Incident auto-classification model (AI) integration", "story_points": 8,
     "status": "completed", "assignee": "Indira Nair",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-MGT", "sprint_number": 2, "item_type": "task",
     "title": "Problem management workflow — root cause categories", "story_points": 5,
     "status": "completed", "assignee": "Jyoti Pillai",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-MGT", "sprint_number": 2, "item_type": "task",
     "title": "ITSM reporting dashboard — weekly SLA breach view", "story_points": 5,
     "status": "completed", "assignee": "Kishore Kumar",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "HERC-MGT", "sprint_number": 2, "item_type": "task",
     "title": "Service catalogue — 12 core IT services defined", "story_points": 3,
     "status": "completed", "assignee": "Lakshmi Menon",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "HERC-MGT", "sprint_number": 2, "item_type": "task",
     "title": "Knowledge base article template and taxonomy", "story_points": 3,
     "status": "completed", "assignee": "Mohan Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "HERC-MGT", "sprint_number": 2, "item_type": "story",
     "title": "Request fulfilment workflows — top 10 service requests", "story_points": 8,
     "status": "in_progress", "assignee": "Nalini Sharma",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "HERC-MGT", "sprint_number": 2, "item_type": "task",
     "title": "User access review — ServiceNow RBAC baseline", "story_points": 5,
     "status": "in_progress", "assignee": "Hari Krishnan",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},

    # Week 3 — 8 completed, 2 WIP (wip_avg=9.0)
    {"project_code": "HERC-MGT", "sprint_number": 3, "item_type": "story",
     "title": "Request fulfilment workflows — top 10 service requests", "story_points": 8,
     "status": "completed", "assignee": "Nalini Sharma",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 1.5, "priority": "medium"},
    {"project_code": "HERC-MGT", "sprint_number": 3, "item_type": "task",
     "title": "User access review — ServiceNow RBAC baseline", "story_points": 5,
     "status": "completed", "assignee": "Hari Krishnan",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-MGT", "sprint_number": 3, "item_type": "story",
     "title": "SLA dashboard — real-time breach tracking", "story_points": 8,
     "status": "completed", "assignee": "Indira Nair",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 1.0, "priority": "high"},
    {"project_code": "HERC-MGT", "sprint_number": 3, "item_type": "task",
     "title": "Email-to-ticket integration — SMTP relay config", "story_points": 3,
     "status": "completed", "assignee": "Jyoti Pillai",
     "is_ai_assisted": False, "defects_raised": 1, "rework_hours": 2.0, "priority": "high"},
    {"project_code": "HERC-MGT", "sprint_number": 3, "item_type": "task",
     "title": "Grafana — ServiceNow MTTR/MTTD panel", "story_points": 5,
     "status": "completed", "assignee": "Kishore Kumar",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-MGT", "sprint_number": 3, "item_type": "task",
     "title": "Knowledge base — 20 KB articles authored (AI-assisted)", "story_points": 3,
     "status": "completed", "assignee": "Lakshmi Menon",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "HERC-MGT", "sprint_number": 3, "item_type": "task",
     "title": "Capacity management — headcount and hardware inventory", "story_points": 5,
     "status": "completed", "assignee": "Mohan Rao",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-MGT", "sprint_number": 3, "item_type": "task",
     "title": "Availability management — uptime SLA targets defined", "story_points": 3,
     "status": "completed", "assignee": "Nalini Sharma",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "HERC-MGT", "sprint_number": 3, "item_type": "story",
     "title": "Automated ticket triage — AI priority scoring", "story_points": 8,
     "status": "in_progress", "assignee": "Hari Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "HERC-MGT", "sprint_number": 3, "item_type": "task",
     "title": "Disaster recovery runbook for ServiceNow instance", "story_points": 5,
     "status": "in_progress", "assignee": "Indira Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},

    # Week 4 — 7 completed, 2 WIP (wip_avg=8.5)
    {"project_code": "HERC-MGT", "sprint_number": 4, "item_type": "story",
     "title": "Automated ticket triage — AI priority scoring", "story_points": 8,
     "status": "completed", "assignee": "Hari Krishnan",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-MGT", "sprint_number": 4, "item_type": "task",
     "title": "Disaster recovery runbook for ServiceNow instance", "story_points": 5,
     "status": "completed", "assignee": "Indira Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-MGT", "sprint_number": 4, "item_type": "story",
     "title": "Change impact assessment workflow — AI risk scoring", "story_points": 8,
     "status": "completed", "assignee": "Jyoti Pillai",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.5, "priority": "high"},
    {"project_code": "HERC-MGT", "sprint_number": 4, "item_type": "task",
     "title": "Performance analytics — monthly exec report template", "story_points": 5,
     "status": "completed", "assignee": "Kishore Kumar",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
    {"project_code": "HERC-MGT", "sprint_number": 4, "item_type": "task",
     "title": "Configuration item (CI) baseline audit", "story_points": 5,
     "status": "completed", "assignee": "Lakshmi Menon",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.5, "priority": "medium"},
    {"project_code": "HERC-MGT", "sprint_number": 4, "item_type": "task",
     "title": "Knowledge base — additional 15 KB articles", "story_points": 3,
     "status": "completed", "assignee": "Mohan Rao",
     "is_ai_assisted": True, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "HERC-MGT", "sprint_number": 4, "item_type": "task",
     "title": "ServiceNow mobile app enablement for on-call team", "story_points": 3,
     "status": "completed", "assignee": "Nalini Sharma",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "low"},
    {"project_code": "HERC-MGT", "sprint_number": 4, "item_type": "story",
     "title": "Event management — Prometheus alert-to-incident pipeline", "story_points": 8,
     "status": "in_progress", "assignee": "Hari Krishnan",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "high"},
    {"project_code": "HERC-MGT", "sprint_number": 4, "item_type": "story",
     "title": "Supplier management — vendor SLA tracking in ServiceNow", "story_points": 5,
     "status": "in_progress", "assignee": "Indira Nair",
     "is_ai_assisted": False, "defects_raised": 0, "rework_hours": 0.0, "priority": "medium"},
]
