"""Tab 10 Reports & Exports endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import (
    AuditLog,
    CommercialScenario,
    CustomerAction,
    CustomerSatisfaction,
    EvmSnapshot,
    KpiSnapshot,
    Program,
    Risk,
    ScopeCreepLog,
    SlaIncident,
)
from app.services.reports import build_audit_zip, build_qbr_pdf

router = APIRouter(prefix="/reports", tags=["reports"])


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
    """Bundle the audit-evidence JSON dumps for the requested scope.

    Payload includes: audit_log, risks, scope_creep_log, sla_incidents,
    kpi_snapshots, customer_satisfaction. Filtered to a programme when
    program_id is provided.
    """
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


def _row_to_dict(row: object) -> dict[str, object]:
    result: dict[str, object] = {}
    for col in row.__table__.columns:  # type: ignore[attr-defined]
        value = getattr(row, col.name)
        if hasattr(value, "isoformat"):
            result[col.name] = value.isoformat()
        else:
            result[col.name] = value
    return result
