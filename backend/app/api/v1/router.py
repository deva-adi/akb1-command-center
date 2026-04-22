from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import (
    ai,
    commercial,
    currency,
    customer,
    data_import,
    delivery,
    forecasts,
    health,
    kpi,
    ops,
    pnl,
    programmes,
    reports,
    risks,
    settings,
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(programmes.router)
api_router.include_router(kpi.router)
api_router.include_router(risks.router)
api_router.include_router(customer.router)
api_router.include_router(currency.router)
api_router.include_router(delivery.sprints_router)
api_router.include_router(delivery.backlog_router)
api_router.include_router(delivery.evm_router)
api_router.include_router(delivery.flow_router)
api_router.include_router(delivery.phases_router)
api_router.include_router(delivery.phase_deliverables_router)
api_router.include_router(delivery.milestones_router)
api_router.include_router(commercial.dual_velocity_router)
api_router.include_router(commercial.blend_rules_router)
api_router.include_router(commercial.commercial_router)
api_router.include_router(commercial.losses_router)
api_router.include_router(commercial.rate_cards_router)
api_router.include_router(commercial.change_requests_router)
api_router.include_router(ai.tools_router)
api_router.include_router(ai.assignments_router)
api_router.include_router(ai.usage_router)
api_router.include_router(ai.code_metrics_router)
api_router.include_router(ai.sdlc_metrics_router)
api_router.include_router(ai.trust_router)
api_router.include_router(ai.governance_router)
api_router.include_router(ai.override_router)
api_router.include_router(ops.scenarios_router)
api_router.include_router(ops.resources_router)
api_router.include_router(ops.alerts_router)
api_router.include_router(ops.audit_router)
api_router.include_router(reports.router)
api_router.include_router(forecasts.router)
api_router.include_router(settings.router)
api_router.include_router(data_import.router)
api_router.include_router(pnl.router)
