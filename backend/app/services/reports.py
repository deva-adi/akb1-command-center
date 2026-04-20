"""Report generation — QBR brief + audit package.

Keeps PDF assembly behind a thin service layer so the API handler stays
small and the same functions can be reused from scheduled jobs later.
"""
from __future__ import annotations

import io
import json
import zipfile
from datetime import datetime
from typing import Any

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

NAVY = HexColor("#1B2A4A")
AMBER = HexColor("#F59E0B")
ICE = HexColor("#D5E8F0")


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    title = ParagraphStyle(
        "AkbTitle",
        parent=base["Title"],
        textColor=NAVY,
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        spaceAfter=4,
    )
    subtitle = ParagraphStyle(
        "AkbSubtitle",
        parent=base["Heading3"],
        textColor=NAVY,
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        spaceAfter=12,
    )
    h2 = ParagraphStyle(
        "AkbH2",
        parent=base["Heading2"],
        textColor=NAVY,
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        spaceBefore=14,
        spaceAfter=6,
    )
    body = ParagraphStyle(
        "AkbBody",
        parent=base["BodyText"],
        textColor=NAVY,
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        spaceAfter=8,
    )
    return {"title": title, "subtitle": subtitle, "h2": h2, "body": body}


def _kv_table(pairs: list[tuple[str, str]], col1: float = 55, col2: float = 115) -> Table:
    data = [[k, v] for k, v in pairs]
    tbl = Table(data, colWidths=[col1 * mm, col2 * mm])
    tbl.setStyle(
        TableStyle(
            [
                ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
                ("TEXTCOLOR", (0, 0), (-1, -1), NAVY),
                ("BACKGROUND", (0, 0), (0, -1), ICE),
                ("BOX", (0, 0), (-1, -1), 0.4, NAVY),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, NAVY),
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        ),
    )
    return tbl


def build_qbr_pdf(context: dict[str, Any]) -> bytes:
    """Render a single-page QBR PDF for a programme context."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=f"QBR Brief — {context.get('programme', {}).get('name', '—')}",
        author="AKB1 Command Center",
    )
    styles = _styles()
    story: list[Any] = []
    programme = context.get("programme", {})

    story.append(Paragraph(f"QBR Brief · {programme.get('name', '—')}", styles["title"]))
    story.append(
        Paragraph(
            f"Programme code <b>{programme.get('code', '—')}</b> &nbsp;·&nbsp; "
            f"Client <b>{programme.get('client', '—')}</b> &nbsp;·&nbsp; "
            f"Generated {datetime.utcnow().strftime('%Y-%m-%d %H:%MZ')}",
            styles["subtitle"],
        ),
    )

    story.append(Paragraph("Snapshot", styles["h2"]))
    snapshot = context.get("snapshot", {})
    story.append(
        _kv_table(
            [
                ("Status", snapshot.get("status", "—")),
                ("Revenue (native)", snapshot.get("revenue", "—")),
                ("Latest CPI", snapshot.get("cpi", "—")),
                ("Latest SPI", snapshot.get("spi", "—")),
                ("Latest margin", snapshot.get("margin", "—")),
                ("Renewal probability", snapshot.get("renewal_score", "—")),
            ]
        ),
    )

    story.append(Paragraph("Commentary", styles["h2"]))
    commentary = context.get("commentary", "No commentary available.")
    story.append(Paragraph(commentary.replace("\n", "<br/>"), styles["body"]))

    top_risks = context.get("top_risks") or []
    if top_risks:
        story.append(Paragraph("Top risks by financial impact", styles["h2"]))
        data = [["Title", "Severity", "Impact", "Owner"]]
        for r in top_risks[:5]:
            data.append(
                [
                    r.get("title", "—"),
                    r.get("severity", "—"),
                    r.get("impact_display", "—"),
                    r.get("owner", "—"),
                ]
            )
        tbl = Table(data, colWidths=[70 * mm, 24 * mm, 32 * mm, 34 * mm])
        tbl.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                    ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#FFFFFF")),
                    ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 10),
                    ("FONT", (0, 1), (-1, -1), "Helvetica", 9),
                    ("TEXTCOLOR", (0, 1), (-1, -1), NAVY),
                    ("BOX", (0, 0), (-1, -1), 0.4, NAVY),
                    ("INNERGRID", (0, 0), (-1, -1), 0.2, NAVY),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]
            ),
        )
        story.append(tbl)

    open_actions = context.get("open_actions") or []
    if open_actions:
        story.append(Spacer(1, 6))
        story.append(Paragraph("Open steering-committee actions", styles["h2"]))
        data = [["Description", "Owner", "Due", "Priority"]]
        for a in open_actions[:6]:
            data.append(
                [
                    a.get("description", "—"),
                    a.get("owner", "—"),
                    a.get("due_date", "—"),
                    a.get("priority", "—"),
                ]
            )
        tbl = Table(data, colWidths=[88 * mm, 30 * mm, 22 * mm, 20 * mm])
        tbl.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), AMBER),
                    ("TEXTCOLOR", (0, 0), (-1, 0), NAVY),
                    ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 10),
                    ("FONT", (0, 1), (-1, -1), "Helvetica", 9),
                    ("TEXTCOLOR", (0, 1), (-1, -1), NAVY),
                    ("BOX", (0, 0), (-1, -1), 0.4, NAVY),
                    ("INNERGRID", (0, 0), (-1, -1), 0.2, NAVY),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]
            ),
        )
        story.append(tbl)

    story.append(Spacer(1, 12))
    story.append(
        Paragraph(
            "Generated by AKB1 Command Center v5.2 · Source: "
            "github.com/deva-adi/akb1-command-center",
            ParagraphStyle(
                "Footer",
                parent=styles["body"],
                fontSize=8,
                textColor=HexColor("#7B8AA1"),
                alignment=1,
            ),
        ),
    )

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()


def build_audit_zip(bundle: dict[str, Any]) -> bytes:
    """Package an audit evidence ZIP from a JSON-serialisable bundle."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, payload in bundle.items():
            data = (
                payload
                if isinstance(payload, (bytes, bytearray))
                else json.dumps(payload, default=str, indent=2).encode("utf-8")
            )
            suffix = ".bin" if isinstance(payload, (bytes, bytearray)) else ".json"
            zf.writestr(f"{name}{suffix}", data)
        zf.writestr(
            "README.txt",
            "AKB1 Command Center — Audit evidence package\n"
            f"Generated: {datetime.utcnow().isoformat()}Z\n"
            "Contents: each .json is a direct dump of the referenced table, "
            "filtered to the requested scope. See docs/SECURITY_GUIDE.md for the "
            "audit-readiness mapping.\n",
        )
    buf.seek(0)
    return buf.getvalue()
