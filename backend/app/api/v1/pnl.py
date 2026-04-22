"""P&L Cockpit endpoints for v5.7.0 Tab 12.

This module houses the eight endpoints under ``/api/v1/pnl``. In M3a the
module is scaffolding only: the router is defined and registered so the
shared infrastructure (filter parser, error envelope, lineage resolver)
can be imported and wired. Endpoint handlers land in M3b.
"""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/pnl", tags=["pnl"])
