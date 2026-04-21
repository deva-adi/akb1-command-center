"""Tab 10 Reports & Exports endpoints."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import (
    AiGovernanceConfig,
    AiTrustScore,
    AiUsageMetrics,
    AuditLog,
    CommercialScenario,
    CustomerAction,
    CustomerSatisfaction,
    EvmSnapshot,
    KpiDefinition,
    KpiSnapshot,
    LossExposure,
    Milestone,
    Program,
    Risk,
    ScopeCreepLog,
    SlaIncident,
    SprintData,
)
from app.services.reports import (
    build_audit_zip,
    build_csv_report,
    build_qbr_pdf,
    build_report_pdf,
)

router = APIRouter(prefix="/reports", tags=["reports"])


# ---------- helpers ----------

async def _require_programme(session: AsyncSession, program_id: int) -> Program:
    programme = await session.get(Program, program_id)
    if programme is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Programme not found"
        )
    return programme


def _format_currency(amount: float | None, symbol: str = "₹") -> str:
    if amount is None:
        return "—"
    abs_amount = abs(amount)
    if abs_amount >= 1e7:
        return f"{symbol}{amount / 1e7:.2f} Cr"
    if abs_amount >= 1e5:
        return f"{symbol}{amount / 1e5:.2f} L"
    return f"{symbol}{amount:,.0f}"


def _fmt_pct(v: float | None) -> str:
    return f"{v * 100:.1f}%" if v is not None else "—"


def _fmt_f(v: float | None, decimals: int = 2) -> str:
    return f"{v:.{decimals}f}" if v is not None else "—"


def _row_to_dict(row: object) -> dict[str, object]:
    result: dict[str, object] = {}
    for col in row.__table__.columns:  # type: ignore[attr-defined]
        value = getattr(row, col.name)
        if hasattr(value, "isoformat"):
            result[col.name] = value.isoformat()
        else:
            result[col.name] = value
    return result


async def _all_programmes(session: AsyncSession) -> list[Program]:
    return list((await session.execute(select(Program).order_by(Program.name))).scalars().all())


async def _resolve_programmes(
    session: AsyncSession,
    codes: list[str],
) -> list[Program]:
    if not codes:
        return await _all_programmes(session)
    progs = list(
        (
            await session.execute(
                select(Program).where(Program.code.in_(codes)).order_by(Program.name)
            )
        )
        .scalars()
        .all()
    )
    return progs


# ---------- context builders ----------

async def _ctx_executive_summary(
    session: AsyncSession,
    programmes: list[Program],
    prog_ids: list[int],
    cutoff: datetime,
) -> dict:
    # Latest EVM per programme
    evm_map: dict[int, EvmSnapshot] = {}
    for pid in prog_ids:
        row = (
            await session.execute(
                select(EvmSnapshot)
                .where(EvmSnapshot.program_id == pid)
                .order_by(EvmSnapshot.snapshot_date.desc())
                .limit(1)
            )
        ).scalar_one_or_none()
        if row:
            evm_map[pid] = row

    # Latest commercial per programme
    cs_map: dict[int, CommercialScenario] = {}
    for pid in prog_ids:
        row = (
            await session.execute(
                select(CommercialScenario)
                .where(CommercialScenario.program_id == pid)
                .order_by(CommercialScenario.snapshot_date.desc())
                .limit(1)
            )
        ).scalar_one_or_none()
        if row:
            cs_map[pid] = row

    # Top 10 risks
    top_risks = list(
        (
            await session.execute(
                select(Risk)
                .where(Risk.program_id.in_(prog_ids))
                .order_by(Risk.impact.desc().nulls_last())
                .limit(10)
            )
        )
        .scalars()
        .all()
    )

    prog_code_map = {p.id: p.code for p in programmes}

    port_rows = []
    csv_rows = []
    for p in programmes:
        evm = evm_map.get(p.id)
        cs = cs_map.get(p.id)
        cpi = _fmt_f(evm.cpi if evm else None)
        spi = _fmt_f(evm.spi if evm else None)
        margin = _fmt_pct(cs.net_margin_pct if cs else None)
        rev = _format_currency(p.revenue, "₹" if p.currency_code == "INR" else "$")
        port_rows.append([p.code, p.name or "—", p.status or "—", rev, cpi, spi, margin])
        csv_rows.append(
            {
                "Programme": p.code,
                "Name": p.name,
                "Status": p.status,
                "Revenue": p.revenue,
                "CPI": evm.cpi if evm else None,
                "SPI": evm.spi if evm else None,
                "Net Margin %": (cs.net_margin_pct * 100) if cs and cs.net_margin_pct else None,
            }
        )

    risk_rows = [
        [
            prog_code_map.get(r.program_id or 0, "—"),
            (r.title or "—")[:50],
            r.severity or "—",
            _format_currency(r.impact),
            r.owner or "—",
        ]
        for r in top_risks
    ]

    sections = [
        {
            "heading": "Portfolio Status",
            "type": "table",
            "data": {
                "headers": ["Code", "Name", "Status", "Revenue", "CPI", "SPI", "Net Margin"],
                "rows": port_rows,
                "col_widths": [16, 44, 18, 24, 14, 14, 22],
            },
        },
        {
            "heading": "Top Risks by Financial Impact",
            "type": "table",
            "data": {
                "headers": ["Prog", "Risk Title", "Severity", "Impact", "Owner"],
                "rows": risk_rows,
                "col_widths": [16, 60, 20, 30, 28],
            },
        },
    ]

    return {
        "title": "Executive Summary Report",
        "subtitle": f"Portfolio of {len(programmes)} programme(s) · Generated {datetime.utcnow().strftime('%Y-%m-%d')}",
        "sections": sections,
        "csv_rows": csv_rows,
        "csv_headers": ["Programme", "Name", "Status", "Revenue", "CPI", "SPI", "Net Margin %"],
    }


async def _ctx_qbr_pack(
    session: AsyncSession,
    programmes: list[Program],
    prog_ids: list[int],
    cutoff: datetime,
) -> dict:
    sections: list[dict] = []
    csv_rows: list[dict] = []

    for p in programmes:
        latest_cs = (
            await session.execute(
                select(CustomerSatisfaction)
                .where(CustomerSatisfaction.program_id == p.id)
                .order_by(CustomerSatisfaction.snapshot_date.desc())
                .limit(1)
            )
        ).scalar_one_or_none()

        latest_evm = (
            await session.execute(
                select(EvmSnapshot)
                .where(EvmSnapshot.program_id == p.id)
                .order_by(EvmSnapshot.snapshot_date.desc())
                .limit(1)
            )
        ).scalar_one_or_none()

        latest_commercial = (
            await session.execute(
                select(CommercialScenario)
                .where(CommercialScenario.program_id == p.id)
                .order_by(CommercialScenario.snapshot_date.desc())
                .limit(1)
            )
        ).scalar_one_or_none()

        top_risks = list(
            (
                await session.execute(
                    select(Risk)
                    .where(Risk.program_id == p.id)
                    .order_by(Risk.impact.desc().nulls_last())
                    .limit(5)
                )
            )
            .scalars()
            .all()
        )

        symbol = "₹" if p.currency_code == "INR" else "$"
        sections.append(
            {
                "heading": f"{p.code} — {p.name}",
                "type": "kv",
                "data": {
                    "pairs": [
                        ("Client", p.client or "—"),
                        ("Status", p.status or "—"),
                        ("Revenue", _format_currency(p.revenue, symbol)),
                        ("CPI", _fmt_f(latest_evm.cpi if latest_evm else None)),
                        ("SPI", _fmt_f(latest_evm.spi if latest_evm else None)),
                        ("Net Margin", _fmt_pct(latest_commercial.net_margin_pct if latest_commercial else None)),
                        ("CSAT", _fmt_f(latest_cs.csat_score if latest_cs else None, 1)),
                        ("NPS", _fmt_f(latest_cs.nps_score if latest_cs else None, 0)),
                        ("Renewal Probability", _fmt_pct((latest_cs.renewal_score / 100) if latest_cs and latest_cs.renewal_score else None)),
                    ]
                },
            }
        )

        if top_risks:
            sections.append(
                {
                    "heading": f"{p.code} — Top Risks",
                    "type": "table",
                    "data": {
                        "headers": ["Risk", "Severity", "Impact", "Owner"],
                        "rows": [
                            [
                                (r.title or "—")[:55],
                                r.severity or "—",
                                _format_currency(r.impact, symbol),
                                r.owner or "—",
                            ]
                            for r in top_risks
                        ],
                        "col_widths": [75, 24, 32, 33],
                    },
                }
            )

        csv_rows.append(
            {
                "Programme": p.code,
                "Name": p.name,
                "Client": p.client,
                "Status": p.status,
                "Revenue": p.revenue,
                "CPI": latest_evm.cpi if latest_evm else None,
                "SPI": latest_evm.spi if latest_evm else None,
                "Net Margin %": (latest_commercial.net_margin_pct * 100) if latest_commercial and latest_commercial.net_margin_pct else None,
                "CSAT": latest_cs.csat_score if latest_cs else None,
                "NPS": latest_cs.nps_score if latest_cs else None,
                "Renewal %": latest_cs.renewal_score if latest_cs else None,
            }
        )

    return {
        "title": "QBR Pack",
        "subtitle": f"{len(programmes)} programme(s) · {datetime.utcnow().strftime('%Y-%m-%d')}",
        "sections": sections,
        "csv_rows": csv_rows,
        "csv_headers": ["Programme", "Name", "Client", "Status", "Revenue", "CPI", "SPI", "Net Margin %", "CSAT", "NPS", "Renewal %"],
    }


async def _ctx_board_pack(
    session: AsyncSession,
    programmes: list[Program],
    prog_ids: list[int],
    cutoff: datetime,
) -> dict:
    exec_ctx = await _ctx_executive_summary(session, programmes, prog_ids, cutoff)

    # Latest CSAT per programme
    csat_rows = []
    for p in programmes:
        row = (
            await session.execute(
                select(CustomerSatisfaction)
                .where(CustomerSatisfaction.program_id == p.id)
                .order_by(CustomerSatisfaction.snapshot_date.desc())
                .limit(1)
            )
        ).scalar_one_or_none()
        if row:
            csat_rows.append(
                [
                    p.code,
                    _fmt_f(row.csat_score, 1),
                    _fmt_f(row.nps_score, 0),
                    str(row.escalation_open),
                    _fmt_pct((row.renewal_score / 100) if row.renewal_score else None),
                ]
            )

    # Open SLA breaches
    breach_rows = list(
        (
            await session.execute(
                select(SlaIncident)
                .where(
                    SlaIncident.program_id.in_(prog_ids),
                    SlaIncident.sla_breached == True,  # noqa: E712
                )
                .order_by(SlaIncident.reported_at.desc())
                .limit(15)
            )
        )
        .scalars()
        .all()
    )

    prog_code_map = {p.id: p.code for p in programmes}

    sections = exec_ctx["sections"] + [
        {
            "heading": "Customer Health",
            "type": "table",
            "data": {
                "headers": ["Prog", "CSAT", "NPS", "Open Escalations", "Renewal"],
                "rows": csat_rows,
                "col_widths": [20, 24, 24, 40, 30],
            },
        },
        {
            "heading": "SLA Breaches",
            "type": "table",
            "data": {
                "headers": ["Prog", "Priority", "Summary", "Penalty"],
                "rows": [
                    [
                        prog_code_map.get(b.program_id or 0, "—"),
                        b.priority or "—",
                        (b.summary or "—")[:50],
                        _format_currency(b.penalty_amount),
                    ]
                    for b in breach_rows
                ],
                "col_widths": [16, 20, 90, 28],
            },
        },
    ]

    return {
        "title": "Board Pack",
        "subtitle": f"{len(programmes)} programme(s) · {datetime.utcnow().strftime('%Y-%m-%d')}",
        "sections": sections,
        "csv_rows": exec_ctx["csv_rows"],
        "csv_headers": exec_ctx["csv_headers"],
    }


async def _ctx_margin_loss(
    session: AsyncSession,
    programmes: list[Program],
    prog_ids: list[int],
    cutoff: datetime,
) -> dict:
    commercial_rows = list(
        (
            await session.execute(
                select(CommercialScenario)
                .where(
                    CommercialScenario.program_id.in_(prog_ids),
                    CommercialScenario.snapshot_date >= cutoff,
                )
                .order_by(CommercialScenario.snapshot_date.desc())
                .limit(200)
            )
        )
        .scalars()
        .all()
    )

    loss_rows = list(
        (
            await session.execute(
                select(LossExposure)
                .where(
                    LossExposure.program_id.in_(prog_ids),
                    LossExposure.snapshot_date >= cutoff,
                )
                .order_by(LossExposure.amount.desc().nulls_last())
                .limit(100)
            )
        )
        .scalars()
        .all()
    )

    prog_code_map = {p.id: p.code for p in programmes}

    margin_table_rows = [
        [
            prog_code_map.get(r.program_id or 0, "—"),
            str(r.snapshot_date)[:10] if r.snapshot_date else "—",
            _fmt_pct(r.gross_margin_pct),
            _fmt_pct(r.contribution_margin_pct),
            _fmt_pct(r.portfolio_margin_pct),
            _fmt_pct(r.net_margin_pct),
        ]
        for r in commercial_rows[:50]
    ]

    loss_table_rows = [
        [
            prog_code_map.get(r.program_id or 0, "—"),
            r.loss_category or "—",
            _format_currency(r.amount),
            _fmt_pct((r.percentage_of_revenue / 100) if r.percentage_of_revenue else None),
            r.mitigation_status or "—",
        ]
        for r in loss_rows[:50]
    ]

    sections = [
        {
            "heading": "Margin Waterfall by Snapshot",
            "type": "table",
            "data": {
                "headers": ["Prog", "Date", "Gross%", "Contribution%", "Portfolio%", "Net%"],
                "rows": margin_table_rows,
                "col_widths": [16, 24, 24, 32, 32, 24],
            },
        },
        {
            "heading": "Loss Exposure by Category",
            "type": "table",
            "data": {
                "headers": ["Prog", "Category", "Amount", "% Revenue", "Mitigation"],
                "rows": loss_table_rows,
                "col_widths": [16, 40, 32, 24, 42],
            },
        },
    ]

    csv_rows = [
        {
            "Programme": prog_code_map.get(r.program_id or 0, "—"),
            "Date": str(r.snapshot_date)[:10] if r.snapshot_date else None,
            "Gross Margin %": r.gross_margin_pct,
            "Contribution Margin %": r.contribution_margin_pct,
            "Portfolio Margin %": r.portfolio_margin_pct,
            "Net Margin %": r.net_margin_pct,
        }
        for r in commercial_rows
    ]

    return {
        "title": "Margin & Loss Analysis",
        "subtitle": f"{len(programmes)} programme(s) · last {(datetime.utcnow() - cutoff).days} days",
        "sections": sections,
        "csv_rows": csv_rows,
        "csv_headers": ["Programme", "Date", "Gross Margin %", "Contribution Margin %", "Portfolio Margin %", "Net Margin %"],
    }


async def _ctx_evm_portfolio(
    session: AsyncSession,
    programmes: list[Program],
    prog_ids: list[int],
    cutoff: datetime,
) -> dict:
    evm_rows = list(
        (
            await session.execute(
                select(EvmSnapshot)
                .where(
                    EvmSnapshot.program_id.in_(prog_ids),
                    EvmSnapshot.snapshot_date >= cutoff,
                )
                .order_by(EvmSnapshot.snapshot_date.desc())
                .limit(300)
            )
        )
        .scalars()
        .all()
    )

    prog_code_map = {p.id: p.code for p in programmes}

    table_rows = [
        [
            prog_code_map.get(r.program_id or 0, "—"),
            str(r.snapshot_date)[:10],
            _fmt_f(r.cpi),
            _fmt_f(r.spi),
            _fmt_pct(r.percent_complete),
            _format_currency(r.eac),
            _format_currency(r.vac),
            _fmt_f(r.tcpi),
        ]
        for r in evm_rows[:60]
    ]

    sections = [
        {
            "heading": "EVM Snapshots",
            "type": "table",
            "data": {
                "headers": ["Prog", "Date", "CPI", "SPI", "% Complete", "EAC", "VAC", "TCPI"],
                "rows": table_rows,
                "col_widths": [16, 24, 16, 16, 22, 24, 24, 16],
            },
        }
    ]

    csv_rows = [
        {
            "Programme": prog_code_map.get(r.program_id or 0, "—"),
            "Date": str(r.snapshot_date)[:10],
            "CPI": r.cpi,
            "SPI": r.spi,
            "% Complete": r.percent_complete,
            "EAC": r.eac,
            "VAC": r.vac,
            "TCPI": r.tcpi,
        }
        for r in evm_rows
    ]

    return {
        "title": "EVM Portfolio Report",
        "subtitle": f"{len(programmes)} programme(s) · last {(datetime.utcnow() - cutoff).days} days",
        "sections": sections,
        "csv_rows": csv_rows,
        "csv_headers": ["Programme", "Date", "CPI", "SPI", "% Complete", "EAC", "VAC", "TCPI"],
    }


async def _ctx_kpi_trend(
    session: AsyncSession,
    programmes: list[Program],
    prog_ids: list[int],
    cutoff: datetime,
    kpi_codes: list[str],
) -> dict:
    # Resolve KPI IDs
    kpi_defs: list[KpiDefinition] = []
    if kpi_codes:
        kpi_defs = list(
            (
                await session.execute(
                    select(KpiDefinition).where(KpiDefinition.code.in_(kpi_codes))
                )
            )
            .scalars()
            .all()
        )
    else:
        kpi_defs = list(
            (await session.execute(select(KpiDefinition).limit(10))).scalars().all()
        )

    kpi_id_map = {k.id: k.code for k in kpi_defs}
    kpi_ids = list(kpi_id_map.keys())

    snapshots = list(
        (
            await session.execute(
                select(KpiSnapshot)
                .where(
                    KpiSnapshot.program_id.in_(prog_ids),
                    KpiSnapshot.kpi_id.in_(kpi_ids),
                    KpiSnapshot.snapshot_date >= cutoff,
                )
                .order_by(KpiSnapshot.snapshot_date.desc())
                .limit(500)
            )
        )
        .scalars()
        .all()
    )

    prog_code_map = {p.id: p.code for p in programmes}

    table_rows = [
        [
            prog_code_map.get(s.program_id or 0, "—"),
            kpi_id_map.get(s.kpi_id or 0, "—"),
            str(s.snapshot_date)[:10],
            _fmt_f(s.value),
            s.trend or "—",
        ]
        for s in snapshots[:80]
    ]

    sections = [
        {
            "heading": f"KPI Trend — {', '.join(k.code for k in kpi_defs)}",
            "type": "table",
            "data": {
                "headers": ["Prog", "KPI", "Date", "Value", "Trend"],
                "rows": table_rows,
                "col_widths": [20, 28, 24, 24, 24],
            },
        }
    ]

    csv_rows = [
        {
            "Programme": prog_code_map.get(s.program_id or 0, "—"),
            "KPI": kpi_id_map.get(s.kpi_id or 0, "—"),
            "Date": str(s.snapshot_date)[:10],
            "Value": s.value,
            "Trend": s.trend,
        }
        for s in snapshots
    ]

    return {
        "title": "KPI Trend Report",
        "subtitle": f"{len(kpi_defs)} KPI(s) · {len(programmes)} programme(s) · last {(datetime.utcnow() - cutoff).days} days",
        "sections": sections,
        "csv_rows": csv_rows,
        "csv_headers": ["Programme", "KPI", "Date", "Value", "Trend"],
    }


async def _ctx_delivery_health(
    session: AsyncSession,
    programmes: list[Program],
    prog_ids: list[int],
    cutoff: datetime,
) -> dict:
    sprints = list(
        (
            await session.execute(
                select(SprintData)
                .where(SprintData.program_id.in_(prog_ids))
                .order_by(SprintData.sprint_number.desc())
                .limit(100)
            )
        )
        .scalars()
        .all()
    )

    milestones = list(
        (
            await session.execute(
                select(Milestone)
                .where(Milestone.program_id.in_(prog_ids))
                .order_by(Milestone.planned_date.asc())
                .limit(50)
            )
        )
        .scalars()
        .all()
    )

    incidents = list(
        (
            await session.execute(
                select(SlaIncident)
                .where(SlaIncident.program_id.in_(prog_ids))
                .order_by(SlaIncident.reported_at.desc())
                .limit(30)
            )
        )
        .scalars()
        .all()
    )

    prog_code_map = {p.id: p.code for p in programmes}

    sprint_rows = [
        [
            prog_code_map.get(s.program_id or 0, "—"),
            str(s.sprint_number or "—"),
            _fmt_f(s.velocity),
            _fmt_f(s.planned_points),
            _fmt_f(s.completed_points),
            str(s.defects_found or 0),
        ]
        for s in sprints[:40]
    ]

    milestone_rows = [
        [
            prog_code_map.get(m.program_id or 0, "—"),
            (m.name or "—")[:40],
            str(m.planned_date)[:10] if m.planned_date else "—",
            str(m.actual_date)[:10] if m.actual_date else "—",
            m.status or "—",
        ]
        for m in milestones
    ]

    incident_rows = [
        [
            prog_code_map.get(i.program_id or 0, "—"),
            i.priority or "—",
            (i.summary or "—")[:45],
            "Yes" if i.sla_breached else "No",
            _format_currency(i.penalty_amount),
        ]
        for i in incidents
    ]

    sections = [
        {
            "heading": "Sprint Velocity",
            "type": "table",
            "data": {
                "headers": ["Prog", "Sprint", "Velocity", "Planned Pts", "Completed Pts", "Defects"],
                "rows": sprint_rows,
                "col_widths": [16, 18, 24, 28, 32, 22],
            },
        },
        {
            "heading": "Milestones",
            "type": "table",
            "data": {
                "headers": ["Prog", "Milestone", "Planned", "Actual", "Status"],
                "rows": milestone_rows,
                "col_widths": [16, 58, 24, 24, 22],
            },
        },
        {
            "heading": "SLA Incidents",
            "type": "table",
            "data": {
                "headers": ["Prog", "Priority", "Summary", "Breached?", "Penalty"],
                "rows": incident_rows,
                "col_widths": [16, 20, 66, 22, 24],
            },
        },
    ]

    csv_rows = [
        {
            "Programme": prog_code_map.get(s.program_id or 0, "—"),
            "Sprint": s.sprint_number,
            "Velocity": s.velocity,
            "Planned Points": s.planned_points,
            "Completed Points": s.completed_points,
            "Defects Found": s.defects_found,
        }
        for s in sprints
    ]

    return {
        "title": "Delivery Health Summary",
        "subtitle": f"{len(programmes)} programme(s) · {datetime.utcnow().strftime('%Y-%m-%d')}",
        "sections": sections,
        "csv_rows": csv_rows,
        "csv_headers": ["Programme", "Sprint", "Velocity", "Planned Points", "Completed Points", "Defects Found"],
    }


async def _ctx_risk_audit(
    session: AsyncSession,
    programmes: list[Program],
    prog_ids: list[int],
    cutoff: datetime,
) -> dict:
    risks = list(
        (
            await session.execute(
                select(Risk)
                .where(Risk.program_id.in_(prog_ids))
                .order_by(Risk.impact.desc().nulls_last())
                .limit(100)
            )
        )
        .scalars()
        .all()
    )

    audit_entries = list(
        (
            await session.execute(
                select(AuditLog)
                .where(AuditLog.timestamp >= cutoff)
                .order_by(AuditLog.timestamp.desc())
                .limit(100)
            )
        )
        .scalars()
        .all()
    )

    breaches = list(
        (
            await session.execute(
                select(SlaIncident)
                .where(
                    SlaIncident.program_id.in_(prog_ids),
                    SlaIncident.sla_breached == True,  # noqa: E712
                )
                .order_by(SlaIncident.reported_at.desc())
                .limit(50)
            )
        )
        .scalars()
        .all()
    )

    prog_code_map = {p.id: p.code for p in programmes}

    risk_rows = [
        [
            prog_code_map.get(r.program_id or 0, "—"),
            (r.title or "—")[:45],
            r.category or "—",
            r.severity or "—",
            _fmt_f(r.probability),
            _format_currency(r.impact),
            r.status or "—",
        ]
        for r in risks[:50]
    ]

    audit_rows = [
        [
            str(e.timestamp)[:16] if e.timestamp else "—",
            e.action or "—",
            e.table_name or "—",
            e.user_action or "—",
        ]
        for e in audit_entries[:50]
    ]

    breach_rows = [
        [
            prog_code_map.get(b.program_id or 0, "—"),
            b.priority or "—",
            (b.summary or "—")[:45],
            str(b.reported_at)[:10] if b.reported_at else "—",
            _format_currency(b.penalty_amount),
        ]
        for b in breaches[:30]
    ]

    sections = [
        {
            "heading": "Risk Register",
            "type": "table",
            "data": {
                "headers": ["Prog", "Title", "Category", "Severity", "Prob", "Impact", "Status"],
                "rows": risk_rows,
                "col_widths": [16, 50, 24, 20, 14, 24, 18],
            },
        },
        {
            "heading": "SLA Breaches",
            "type": "table",
            "data": {
                "headers": ["Prog", "Priority", "Summary", "Reported", "Penalty"],
                "rows": breach_rows,
                "col_widths": [16, 20, 60, 24, 24],
            },
        },
        {
            "heading": "Recent Audit Trail",
            "type": "table",
            "data": {
                "headers": ["Timestamp", "Action", "Table", "User"],
                "rows": audit_rows,
                "col_widths": [36, 40, 40, 38],
            },
        },
    ]

    csv_rows = [
        {
            "Programme": prog_code_map.get(r.program_id or 0, "—"),
            "Title": r.title,
            "Category": r.category,
            "Severity": r.severity,
            "Probability": r.probability,
            "Impact": r.impact,
            "Status": r.status,
        }
        for r in risks
    ]

    return {
        "title": "Risk & Audit Digest",
        "subtitle": f"{len(programmes)} programme(s) · last {(datetime.utcnow() - cutoff).days} days",
        "sections": sections,
        "csv_rows": csv_rows,
        "csv_headers": ["Programme", "Title", "Category", "Severity", "Probability", "Impact", "Status"],
    }


async def _ctx_ai_governance(
    session: AsyncSession,
    programmes: list[Program],
    prog_ids: list[int],
    cutoff: datetime,
) -> dict:
    trust_scores = list(
        (
            await session.execute(
                select(AiTrustScore)
                .where(AiTrustScore.program_id.in_(prog_ids))
                .order_by(AiTrustScore.snapshot_date.desc())
                .limit(100)
            )
        )
        .scalars()
        .all()
    )

    usage = list(
        (
            await session.execute(
                select(AiUsageMetrics)
                .where(
                    AiUsageMetrics.program_id.in_(prog_ids),
                    AiUsageMetrics.snapshot_date >= cutoff,
                )
                .order_by(AiUsageMetrics.snapshot_date.desc())
                .limit(100)
            )
        )
        .scalars()
        .all()
    )

    governance = list(
        (
            await session.execute(
                select(AiGovernanceConfig)
                .where(
                    AiGovernanceConfig.program_id.in_(prog_ids)
                    | (AiGovernanceConfig.program_id == None)  # noqa: E711
                )
                .order_by(AiGovernanceConfig.compliance_pct.desc().nulls_last())
                .limit(30)
            )
        )
        .scalars()
        .all()
    )

    prog_code_map = {p.id: p.code for p in programmes}

    trust_rows = [
        [
            prog_code_map.get(t.program_id or 0, "—"),
            str(t.snapshot_date)[:10] if t.snapshot_date else "—",
            _fmt_f(t.composite_score),
            t.maturity_level or "—",
            _fmt_f(t.provenance_score),
            _fmt_f(t.test_coverage_score),
            _fmt_f(t.defect_rate_score),
        ]
        for t in trust_scores[:40]
    ]

    usage_rows = [
        [
            prog_code_map.get(u.program_id or 0, "—"),
            str(u.snapshot_date)[:10] if u.snapshot_date else "—",
            str(u.prompts_count or 0),
            str(u.suggestions_accepted or 0),
            _fmt_f(u.time_saved_hours),
            _format_currency(u.cost),
        ]
        for u in usage[:30]
    ]

    gov_rows = [
        [
            (g.name or "—")[:40],
            g.config_type or "—",
            g.status or "—",
            _fmt_pct((g.compliance_pct / 100) if g.compliance_pct else None),
            g.owner or "—",
        ]
        for g in governance[:20]
    ]

    sections = [
        {
            "heading": "AI Trust Scores",
            "type": "table",
            "data": {
                "headers": ["Prog", "Date", "Composite", "Maturity", "Provenance", "Test Cov.", "Defect"],
                "rows": trust_rows,
                "col_widths": [16, 22, 22, 22, 26, 26, 20],
            },
        },
        {
            "heading": "AI Usage Metrics",
            "type": "table",
            "data": {
                "headers": ["Prog", "Date", "Prompts", "Accepted", "Hrs Saved", "Cost"],
                "rows": usage_rows,
                "col_widths": [16, 22, 22, 22, 28, 28],
            },
        },
        {
            "heading": "Governance Config Compliance",
            "type": "table",
            "data": {
                "headers": ["Config Name", "Type", "Status", "Compliance", "Owner"],
                "rows": gov_rows,
                "col_widths": [55, 24, 20, 28, 27],
            },
        },
    ]

    csv_rows = [
        {
            "Programme": prog_code_map.get(t.program_id or 0, "—"),
            "Date": str(t.snapshot_date)[:10] if t.snapshot_date else None,
            "Composite Score": t.composite_score,
            "Maturity Level": t.maturity_level,
            "Provenance Score": t.provenance_score,
            "Test Coverage Score": t.test_coverage_score,
            "Defect Rate Score": t.defect_rate_score,
        }
        for t in trust_scores
    ]

    return {
        "title": "AI Governance Report",
        "subtitle": f"{len(programmes)} programme(s) · last {(datetime.utcnow() - cutoff).days} days",
        "sections": sections,
        "csv_rows": csv_rows,
        "csv_headers": ["Programme", "Date", "Composite Score", "Maturity Level", "Provenance Score", "Test Coverage Score", "Defect Rate Score"],
    }


# ---------- existing endpoints ----------

@router.get("/qbr/{program_id}.pdf", response_class=Response)
async def qbr_pdf(
    program_id: int,
    session: AsyncSession = Depends(get_session),
) -> Response:
    programme = await _require_programme(session, program_id)

    latest_cs = (
        await session.execute(
            select(CustomerSatisfaction)
            .where(CustomerSatisfaction.program_id == program_id)
            .order_by(CustomerSatisfaction.snapshot_date.desc())
            .limit(1)
        )
    ).scalar_one_or_none()

    latest_evm = (
        await session.execute(
            select(EvmSnapshot)
            .where(EvmSnapshot.program_id == program_id)
            .order_by(EvmSnapshot.snapshot_date.desc())
            .limit(1)
        )
    ).scalar_one_or_none()

    latest_commercial = (
        await session.execute(
            select(CommercialScenario)
            .where(CommercialScenario.program_id == program_id)
            .order_by(CommercialScenario.snapshot_date.desc())
            .limit(1)
        )
    ).scalar_one_or_none()

    top_risks = (
        await session.execute(
            select(Risk)
            .where(Risk.program_id == program_id)
            .order_by(Risk.impact.desc().nulls_last())
            .limit(5)
        )
    ).scalars().all()

    open_actions = (
        await session.execute(
            select(CustomerAction)
            .where(
                CustomerAction.program_id == program_id,
                CustomerAction.status != "Closed",
            )
            .order_by(CustomerAction.due_date.asc().nulls_last())
            .limit(6)
        )
    ).scalars().all()

    commentary_parts = [
        f"{programme.name} is currently {programme.status}. ",
    ]
    if latest_cs:
        commentary_parts.append(
            f"CSAT {latest_cs.csat_score:.1f} / NPS {latest_cs.nps_score:.0f} / "
            f"Renewal probability {latest_cs.renewal_score:.0f}%. "
        )
    if latest_evm and latest_evm.cpi is not None:
        commentary_parts.append(
            f"Earned-value metrics: CPI {latest_evm.cpi:.2f}, "
            f"SPI {(latest_evm.spi or 0):.2f}. "
        )
    if latest_commercial and latest_commercial.net_margin_pct is not None:
        commentary_parts.append(
            f"Net margin {latest_commercial.net_margin_pct * 100:.1f}%."
        )

    symbol = "₹" if programme.currency_code == "INR" else "$"
    context = {
        "programme": {
            "name": programme.name,
            "code": programme.code,
            "client": programme.client or "—",
            "currency_code": programme.currency_code,
        },
        "snapshot": {
            "status": programme.status,
            "revenue": _format_currency(programme.revenue, symbol),
            "cpi": f"{latest_evm.cpi:.2f}" if latest_evm and latest_evm.cpi else "—",
            "spi": f"{latest_evm.spi:.2f}" if latest_evm and latest_evm.spi else "—",
            "margin": (
                f"{latest_commercial.net_margin_pct * 100:.1f}%"
                if latest_commercial and latest_commercial.net_margin_pct is not None
                else "—"
            ),
            "renewal_score": (
                f"{latest_cs.renewal_score:.0f}%"
                if latest_cs and latest_cs.renewal_score is not None
                else "—"
            ),
        },
        "commentary": "".join(commentary_parts),
        "top_risks": [
            {
                "title": r.title,
                "severity": r.severity or "—",
                "impact_display": _format_currency(r.impact, symbol),
                "owner": r.owner or "—",
            }
            for r in top_risks
        ],
        "open_actions": [
            {
                "description": a.description,
                "owner": a.owner or "—",
                "due_date": str(a.due_date) if a.due_date else "—",
                "priority": a.priority or "—",
            }
            for a in open_actions
        ],
    }

    pdf = build_qbr_pdf(context)
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="qbr-{programme.code.lower()}.pdf"'
            )
        },
    )


@router.get("/audit-package.zip", response_class=Response)
async def audit_package_zip(
    program_id: int | None = None,
    session: AsyncSession = Depends(get_session),
) -> Response:
    """Bundle the audit-evidence JSON dumps for the requested scope."""
    queries = {
        "audit_log": select(AuditLog).order_by(AuditLog.timestamp.desc()).limit(200),
    }
    scoped = {
        "risks": select(Risk),
        "scope_creep_log": select(ScopeCreepLog),
        "sla_incidents": select(SlaIncident),
        "kpi_snapshots": select(KpiSnapshot).limit(500),
        "customer_satisfaction": select(CustomerSatisfaction),
    }
    if program_id is not None:
        await _require_programme(session, program_id)
        scoped["risks"] = scoped["risks"].where(Risk.program_id == program_id)
        scoped["scope_creep_log"] = scoped["scope_creep_log"].where(
            ScopeCreepLog.program_id == program_id
        )
        scoped["sla_incidents"] = scoped["sla_incidents"].where(
            SlaIncident.program_id == program_id
        )
        scoped["kpi_snapshots"] = scoped["kpi_snapshots"].where(
            KpiSnapshot.program_id == program_id
        )
        scoped["customer_satisfaction"] = scoped["customer_satisfaction"].where(
            CustomerSatisfaction.program_id == program_id
        )

    bundle: dict[str, list[dict[str, object]]] = {}
    for name, stmt in {**queries, **scoped}.items():
        rows = (await session.execute(stmt)).scalars().all()
        bundle[name] = [_row_to_dict(r) for r in rows]

    zip_bytes = build_audit_zip(bundle)
    filename = (
        f"audit-{program_id}.zip" if program_id is not None else "audit-portfolio.zip"
    )
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ---------- configurable report generator ----------

class ReportRequest(BaseModel):
    report_type: Literal[
        "executive_summary",
        "qbr_pack",
        "board_pack",
        "margin_loss",
        "evm_portfolio",
        "kpi_trend",
        "delivery_health",
        "risk_audit",
        "ai_governance",
    ]
    programme_codes: list[str] = []
    period_months: Literal[3, 6, 12, 24] = 12
    kpi_codes: list[str] = []
    format: Literal["pdf", "csv"] = "pdf"
    currency: str = "INR"


@router.post("/generate", response_class=Response)
async def generate_report(
    req: ReportRequest,
    session: AsyncSession = Depends(get_session),
) -> Response:
    """Generate any of the 9 configurable report types as PDF or CSV."""
    programmes = await _resolve_programmes(session, req.programme_codes)
    prog_ids = [p.id for p in programmes]
    cutoff = datetime.utcnow() - timedelta(days=30 * req.period_months)

    builders = {
        "executive_summary": lambda: _ctx_executive_summary(session, programmes, prog_ids, cutoff),
        "qbr_pack": lambda: _ctx_qbr_pack(session, programmes, prog_ids, cutoff),
        "board_pack": lambda: _ctx_board_pack(session, programmes, prog_ids, cutoff),
        "margin_loss": lambda: _ctx_margin_loss(session, programmes, prog_ids, cutoff),
        "evm_portfolio": lambda: _ctx_evm_portfolio(session, programmes, prog_ids, cutoff),
        "kpi_trend": lambda: _ctx_kpi_trend(session, programmes, prog_ids, cutoff, req.kpi_codes),
        "delivery_health": lambda: _ctx_delivery_health(session, programmes, prog_ids, cutoff),
        "risk_audit": lambda: _ctx_risk_audit(session, programmes, prog_ids, cutoff),
        "ai_governance": lambda: _ctx_ai_governance(session, programmes, prog_ids, cutoff),
    }

    ctx = await builders[req.report_type]()
    date_stamp = datetime.utcnow().strftime("%Y%m%d")

    if req.format == "csv":
        content = build_csv_report(ctx["csv_rows"], ctx.get("csv_headers"))
        media_type = "text/csv"
        filename = f"{req.report_type}-{date_stamp}.csv"
    else:
        content = build_report_pdf(ctx["title"], ctx["subtitle"], ctx["sections"])
        media_type = "application/pdf"
        filename = f"{req.report_type}-{date_stamp}.pdf"

    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
