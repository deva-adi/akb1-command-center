# Lineage Keys Reference (v5.7.0)

**Status:** Locked on 2026-04-22. Changes require explicit sign-off.

Lineage keys are the stable identifiers that connect every metric rendered
in the UI to the backend endpoint that explains it. A key names a metric
cell precisely enough for the backend to resolve it to contributing atomic
rows. The format supports deep-linking, drill-across, drill-up, and
calculation-to-data drill, all tested by the M9 drill integrity harness.

---

## Format

A lineage key has exactly four dot-separated segments:

```
{tab}.{metric}.{slice}.{aggregation}
```

**Examples:**

| Key | What it names |
|---|---|
| `pnl.gross_margin_pct.programme.month` | Gross margin percentage, one row per programme per month, scoped to the P&L Cockpit tab. |
| `executive.utilisation.resource.current` | Current utilisation per resource on the Executive Overview tab. |
| `delivery.cpi.programme.rolling_3m` | CPI by programme, three-month rolling aggregation, on Delivery Health. |
| `pnl.dso.none.none` | Portfolio-level DSO with no slice and no time aggregation. |

---

## Rules

1. **Four segments, always.** No more, no fewer. If a dimension does not
   apply to the metric, use the literal word `none` in that slot. Empty
   segments are rejected.
2. **Lowercase ASCII only.** Letters a-z, digits 0-9, and underscores are
   allowed inside a segment. No uppercase, hyphens, spaces, or
   non-ASCII characters. Segments may not start or end with an
   underscore.
3. **Dots separate segments. Underscores join words inside a segment.**
   So `gross_margin_pct` is one segment, `gross.margin.pct` is three.
4. **Fixed vocabularies on three of the four segments.** The backend
   parser (`backend/app/services/lineage_keys.py`) validates `tab`,
   `slice`, and `aggregation` against the lists below and raises
   `LineageKeyError` (mapped to HTTP 422 via the standard error
   envelope) on unknown values. `metric` is free because new formulas
   get added over time; the convention is to match a formula identifier
   from `docs/FORMULAS.md` when one exists.

---

## Fixed vocabularies

### `tab` (12 entries)

Matches the tab slug used in the frontend route.

```
pnl
executive
delivery
risk
flow
financials
ai
bench
commercial
backlog
scenario
ops
```

### `slice` (7 entries)

Drill-target cardinality. Tells the caller what kind of row the lineage
entries will be.

```
programme
resource
sprint
month
phase
portfolio
none
```

### `aggregation` (6 entries)

Time reducer applied to the metric before returning.

```
current
month
quarter
ytd
rolling_3m
none
```

---

## Filter query parameters

The universal filter set applied across all P&L endpoints uses these
canonical query parameter names:

```
programme, from, to, tier, scenario_name, portfolio, month
```

### Backwards-compat aliases

The parser silently accepts the following aliases and normalises them to
the canonical names. No warning, no deprecation log. Response envelopes
always emit the canonical names, never the alias form.

| Alias | Canonical |
|---|---|
| `programme_code` | `programme` |
| `period_start` | `from` |
| `period_end` | `to` |

This alias map exists because v5.6-era snippets and curl examples in
operator notes may still use the older names. Rather than hunting them
all down during M3, the parser accepts both on the way in and emits only
the canonical form on the way out.

---

## Translation table for renames

When a tab slug or other vocabulary entry changes in a future release,
the previous entry becomes a deprecated alias for two minor versions
before removal. Add the alias under this section and keep the old key
functional until then. No entry removed without an explicit session
sign-off and a tracking note in `docs/TECH_DEBT.md`.

No aliases currently active.

---

## Implementation references

- Parser and vocabularies: `backend/app/services/lineage_keys.py`
- Filter parser: `backend/app/api/v1/pnl_filters.py`
- Response schemas: `backend/app/schemas/pnl.py`
- Error envelope: `backend/app/api/v1/error_envelope.py`
