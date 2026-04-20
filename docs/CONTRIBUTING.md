# CONTRIBUTING — AKB1 Command Center v5.2

Thank you for your interest in contributing to the AKB1 Command Center! This guide walks you through how to set up your development environment, follow our code style, and submit contributions.

---

## Code of Conduct

Be respectful, inclusive, and constructive. We enforce a zero-tolerance policy on harassment, discrimination, and toxicity. Report violations to team@akb1.internal.

---

## Getting Started

### Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| Docker Desktop | v4.25+ | Windows: enable WSL 2 backend |
| Python | 3.12+ | For local backend development without Docker |
| Node.js | 18+ (LTS) | For local frontend development without Docker |
| npm | 9+ | Bundled with Node.js |
| Git | 2.40+ | Windows: Git for Windows or Git Bash |

> **Note:** You do NOT need PostgreSQL. AKB1 uses SQLite (zero-config). Just Docker is sufficient to run everything.

### Environment Setup

#### 1. Clone the Repository

```bash
# All platforms
git clone https://github.com/deva-adi/akb1-command-center.git
cd akb1-command-center
```

#### 2. Backend Setup (Local Development)

**macOS / Linux:**

```bash
cd backend/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Ruff, Black, MyPy, pytest
```

**Windows (PowerShell):**

```powershell
cd backend\
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

**Windows (Git Bash / WSL2):**

```bash
cd backend/
python -m venv venv
source venv/Scripts/activate  # Git Bash
# source venv/bin/activate    # WSL2
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

**Environment configuration:**

Copy `.env.example` to `.env` in the project root:

```env
DATABASE_URL=sqlite:///data/akb1.db
AKB1_ENV=development
AKB1_LOG_LEVEL=DEBUG
```

**Initialize database:**

```bash
# Apply Alembic migrations
alembic upgrade head
python manage.py db upgrade
python manage.py seed-demo-data  # Load demo dataset
```

**Start backend server:**

```bash
python app.py
# Backend runs on http://localhost:5000
```

#### 3. Frontend Setup

**Install Node dependencies:**

```bash
cd frontend/
npm install
```

**Environment configuration:**

Create `.env.local` in the `frontend/` directory:

```env
REACT_APP_API_BASE_URL=http://localhost:5000/api/v1
REACT_APP_ENV=development
```

**Start frontend dev server:**

```bash
npm start
# Frontend runs on http://localhost:3000
```

#### 4. Database Setup (Optional — Local PostgreSQL)

If you prefer running PostgreSQL locally instead of Docker:

```bash
# Create database
createdb akb1_cc_dev

# Configure DATABASE_URL in .env.local
DATABASE_URL=postgresql://username:password@localhost:5432/akb1_cc_dev

# Run migrations
python manage.py db upgrade
```

#### 5. Docker Compose (All-in-One)

Alternatively, use Docker Compose to start everything:

```bash
docker-compose -f docker-compose.dev.yml up -d
# Services:
# - Backend: http://localhost:5000
# - Frontend: http://localhost:3000
# - PostgreSQL: localhost:5432
# - Redis cache: localhost:6379
```

---

## Code Style & Standards

### Python Backend

**Formatter: black**

```bash
pip install black
black backend/ --line-length 100
```

**Linter: ruff**

```bash
pip install ruff
ruff check backend/ --fix
```

**Type checking: mypy (recommended)**

```bash
pip install mypy
mypy backend/ --ignore-missing-imports
```

**Style guide:**

- Line length: 100 characters
- Indent: 4 spaces
- Class/function naming: `snake_case` for functions, `PascalCase` for classes
- Docstrings: Google style (required for all public functions)
- Imports: Group by standard library, third-party, local (alphabetically)

**Example Python function:**

```python
def calculate_cpi(earned_value: float, actual_cost: float) -> float:
    """
    Calculate Cost Performance Index.

    Args:
        earned_value: Monetary value of work completed (USD).
        actual_cost: Actual cash spent (USD).

    Returns:
        CPI ratio. CPI > 1.0 indicates cost efficiency.

    Raises:
        ValueError: If actual_cost is zero or negative.
    """
    if actual_cost <= 0:
        raise ValueError("Actual cost must be positive")
    return earned_value / actual_cost
```

### JavaScript/React Frontend

**Formatter: prettier**

```bash
npm install --save-dev prettier
npx prettier --write "frontend/**/*.{js,jsx,ts,tsx}"
```

**Linter: eslint**

```bash
npm install --save-dev eslint eslint-config-react-app
npx eslint frontend/ --fix
```

**Style guide:**

- Line length: 100 characters
- Indent: 2 spaces
- Component naming: `PascalCase`
- Function/variable naming: `camelCase`
- Props validation: PropTypes or TypeScript (required)
- Comments: JSDoc for complex functions

**Example React component:**

```jsx
/**
 * CPI Card displays Cost Performance Index.
 * @param {number} cpi - Cost Performance Index value (>1.0 is good)
 * @param {string} programme - Programme name for context
 * @returns {JSX.Element} Rendered card
 */
export function CPICard({ cpi, programme }) {
  const status = cpi >= 1.0 ? "green" : cpi >= 0.95 ? "yellow" : "red";

  return (
    <div className={`card card-${status}`}>
      <h3>{programme}</h3>
      <p className="metric-value">{cpi.toFixed(3)}</p>
      <p className="metric-label">Cost Performance Index</p>
    </div>
  );
}
```

### SQL & Database

- **Line length:** 100 characters
- **Indentation:** 2 spaces
- **Keyword casing:** UPPERCASE (SELECT, FROM, WHERE, etc.)
- **Table/column naming:** `snake_case`
- **Migrations:** Always include both UP and DOWN migrations

**Example migration:**

```python
# migrations/versions/003_add_ai_metrics_table.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        "ai_metrics",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("programme_id", sa.String(50), sa.ForeignKey("programmes.id")),
        sa.Column("month", sa.Date, nullable=False),
        sa.Column("ai_tools_count", sa.Integer, default=0),
        sa.Column("ai_velocity_uplift_pct", sa.Numeric(5, 2), default=0),
    )

def downgrade():
    op.drop_table("ai_metrics")
```

---

## Testing Requirements

**All code contributions must include tests.** Test coverage minimum: 80% for new code.

### Running Tests

**Python (pytest):**

```bash
cd backend/
pytest tests/ -v --cov=. --cov-report=html
# Coverage report: htmlcov/index.html
```

**JavaScript (Jest):**

```bash
cd frontend/
npm test -- --coverage
# Coverage report: coverage/
```

### Test Structure

**Backend test example (pytest):**

```python
# tests/test_formulas.py
import pytest
from backend.formulas import calculate_cpi

def test_calculate_cpi_normal():
    """Test CPI calculation with normal values."""
    assert calculate_cpi(450000, 425000) == pytest.approx(1.059, rel=0.001)

def test_calculate_cpi_underrun():
    """Test CPI when cost is underrun (good performance)."""
    assert calculate_cpi(500000, 400000) == 1.25

def test_calculate_cpi_overrun():
    """Test CPI when cost is overrun (poor performance)."""
    assert calculate_cpi(400000, 500000) == 0.8

def test_calculate_cpi_zero_actual_cost():
    """Test CPI raises error when actual cost is zero."""
    with pytest.raises(ValueError, match="Actual cost must be positive"):
        calculate_cpi(450000, 0)
```

**Frontend test example (Jest):**

```jsx
// frontend/__tests__/CPICard.test.jsx
import React from "react";
import { render, screen } from "@testing-library/react";
import { CPICard } from "../components/CPICard";

describe("CPICard", () => {
  it("renders with green status when CPI >= 1.0", () => {
    render(<CPICard cpi={1.059} programme="Healthcare" />);
    expect(screen.getByText("Healthcare")).toBeInTheDocument();
    expect(screen.getByText(/1\.059/)).toBeInTheDocument();
    expect(screen.getByText(/green/).className).toContain("card-green");
  });

  it("renders with yellow status when 0.95 <= CPI < 1.0", () => {
    render(<CPICard cpi={0.98} programme="Fintech" />);
    expect(screen.getByText(/card-yellow/));
  });
});
```

### Formula Tests (Required)

**All 37 formulas must have unit tests.** Each test must:

1. Verify the formula calculates correctly with known inputs
2. Test edge cases (zero, negative, very large values)
3. Compare against documented worked examples from FORMULAS.md

**Example — CPI formula test:**

```python
# tests/test_formulas_cpi.py
def test_cpi_formula_healthcare_april():
    """Test CPI against documented worked example from FORMULAS.md."""
    earned_value = 450000
    actual_cost = 425000
    expected_cpi = 1.059
    
    cpi = calculate_cpi(earned_value, actual_cost)
    assert cpi == pytest.approx(expected_cpi, rel=0.001)
    # Expected: CPI 1.059 indicates 5.9% cost underrun

def test_cpi_formula_fintech_april():
    """Test CPI against Fintech worked example from FORMULAS.md."""
    earned_value = 280000
    actual_cost = 310000
    expected_cpi = 0.903
    
    cpi = calculate_cpi(earned_value, actual_cost)
    assert cpi == pytest.approx(expected_cpi, rel=0.001)
    # Expected: CPI 0.903 indicates 9.7% cost overrun
```

---

## Pull Request Process

### 1. Create a Branch

Use descriptive branch names:

```bash
git checkout -b feature/add-new-loss-category
# or
git checkout -b fix/cpi-calculation-bug
# or
git checkout -b docs/update-formulas-guide
```

**Branch naming conventions:**

- `feature/` — New feature or enhancement
- `fix/` — Bug fix
- `docs/` — Documentation
- `refactor/` — Code refactor (no logic change)
- `test/` — Test additions
- `chore/` — Maintenance (dependencies, config)

### 2. Make Changes

- **Commit early and often** with clear messages
- **One logical change per commit**
- **Reference issues:** Use `#123` in commit message to link to GitHub issue

**Example commit messages:**

```
feat: Add custom loss category support (revenue leakage tracking)

- Allow users to define custom loss categories via CSV
- Validate custom categories against reserved names
- Store in database with programme scope
- Tested: 5 new test cases for validation

Closes #245
```

```
fix: CPI calculation error when actual_cost is zero

- Add defensive check for zero/negative actual_cost
- Raise ValueError with clear message
- Updated test_formulas_cpi.py with edge cases

Fixes #312
```

### 3. Write/Update Tests

```bash
# Ensure all tests pass before pushing
cd backend/ && pytest tests/ -v
cd frontend/ && npm test -- --coverage
```

### 4. Update Documentation

- **Code changes:** Update docstrings + relevant .md guides
- **Formula changes:** Update FORMULAS.md with worked examples
- **API changes:** Update DATA_INGESTION.md endpoint specs
- **Feature changes:** Update contributing guidelines if needed

### 5. Push & Open Pull Request

```bash
git push origin feature/add-new-loss-category
```

**PR template (auto-populated):**

```markdown
## Description
Brief summary of changes (2–3 sentences).

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Enhancement
- [ ] Documentation
- [ ] Refactor

## Related Issue
Closes #123

## Changes Made
- Bullet list of changes
- With clear detail
- One per line

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Code Style
- [ ] Ran black/prettier
- [ ] Ran ruff/eslint
- [ ] No type warnings (mypy/TypeScript)

## Formula Changes (if applicable)
- [ ] Updated FORMULAS.md with worked examples
- [ ] All 37 formula tests passing
- [ ] Cross-referenced with CTO_QUESTIONS.md

## Checklist
- [ ] Tests pass (pytest + Jest)
- [ ] Coverage >= 80%
- [ ] Documentation updated
- [ ] No breaking changes (or justified)
- [ ] AKB1 brand guidelines followed (colors, fonts)
```

### 6. Code Review

- **Minimum 2 reviews** required before merge
- **Review checklist:**
  - Code style compliance (black, ruff, prettier, eslint)
  - Test coverage adequate
  - Documentation clear
  - No security issues
  - Formula logic correct (if applicable)

### 7. Merge

Once approved:

```bash
# Merge via GitHub UI (preferred) or command line
git checkout main
git merge feature/add-new-loss-category
git push origin main
```

---

## Contribution Areas

We welcome contributions in these areas:

### 1. New Loss Categories
Add custom revenue leakage categories (e.g., "Environmental Rework", "Client Training").

**Files to modify:**
- `backend/models/loss.py` — Loss category enum
- `backend/api/losses.py` — API validation
- `frontend/components/LossEntry.jsx` — Form UI
- `tests/test_losses.py` — Test new category

**Example:**

```python
# backend/models/loss.py
class LossCategory(enum.Enum):
    SCOPE_ABSORPTION = "Scope Absorption"
    REWORK = "Rework"
    BENCH_CARRY = "Bench Carry"
    ENVIRONMENTAL_REWORK = "Environmental Rework"  # NEW
```

### 2. Smart Ops Scenarios
Add decision support scenarios (e.g., "What-if I lose 2 architects in Q3?").

**Files:**
- `backend/services/scenario.py` — Scenario engine
- `backend/api/scenarios.py` — API endpoints
- `frontend/pages/SmartOps.jsx` — UI
- `tests/test_scenarios.py` — Tests

### 3. Chart Types
Add new visualization types (Sankey, Sunburst, etc.).

**Files:**
- `frontend/components/charts/` — React chart components
- `frontend/api/chartData.js` — Data aggregation
- `tests/` — Jest tests

### 4. CSV Templates
Add new CSV import templates (e.g., "resource_skills.csv", "client_contact.csv").

**Files:**
- `backend/models/` — New SQLAlchemy model
- `backend/api/csv_upload.py` — Validation + import logic
- `backend/templates/` — CSV sample file
- `DATA_INGESTION.md` — Document template spec
- `tests/test_csv_import.py` — CSV validation tests

### 5. Localization
Add support for languages beyond English (e.g., Hindi, French, Japanese).

**Files:**
- `frontend/locales/` — JSON translation files
- `backend/services/i18n.py` — Backend translation
- `frontend/i18n.js` — i18next setup
- Tests for RTL languages (if applicable)

### 6. Accessibility
Improve WCAG 2.1 AA compliance (color contrast, keyboard navigation, screen reader support).

**Tools:**
- Axe DevTools (browser plugin)
- WAVE (accessibility checker)
- Manual keyboard navigation testing

**Areas of focus:**
- Chart tooltips (semantic HTML, ARIA labels)
- Form controls (labels, error messaging)
- Color contrast (text on dashboard cards)

### 7. Performance Optimization
Speed up dashboard loading, reduce bundle size, optimize database queries.

**Tools:**
- Lighthouse (frontend performance audit)
- pgAdmin EXPLAIN ANALYZE (slow query detection)
- webpack-bundle-analyzer (JavaScript bundle size)

---

## AKB1 Brand Guidelines

All visual contributions must follow AKB1 brand guidelines:

### Colors

- **Navy (Primary):** `#1B2A4A` — Headers, primary actions
- **Ice Blue (Secondary):** `#D5E8F0` — Accents, backgrounds, light elements
- **Amber (Highlight):** `#F59E0B` — Alerts, high-priority items, CTAs

**Usage:**
- White text on Navy (contrast ratio 7.5:1, WCAG AAA)
- Dark text on Ice Blue (contrast ratio 4.5:1, WCAG AA)
- Dark text on Amber (contrast ratio 4.5:1, WCAG AA)

### Fonts

- **Headers (h1, h2, h3):** Helvetica Neue Bold, 18px–28px
- **Body text:** Helvetica Neue Regular, 14px
- **Code:** Monospace (Monaco or Courier), 12px

### Typography Rules

- Line height: 1.5× font size (minimum)
- Letter spacing: 0.5px (headers only)
- All caps reserved for: Section labels, short CTAs (max 4 words)

### UI Components

- Rounded corners: 4px (buttons, cards)
- Shadows: Subtle (0.5px blur, 10% opacity)
- Spacing: 8px baseline (multiples of 8: 8, 16, 24, 32, 40)
- Icons: 24px or 32px (no custom off-brand colors)

**Brand colors are non-negotiable.** Do not submit PRs with alternative colors without prior discussion with the team.

---

## Release & Versioning

We follow **Semantic Versioning** (MAJOR.MINOR.PATCH):

- **MAJOR:** Breaking API changes, major feature launches
- **MINOR:** New features, backward-compatible enhancements
- **PATCH:** Bug fixes, minor improvements

**Release process:**

1. Update version in `backend/__init__.py` and `frontend/package.json`
2. Update `CHANGELOG.md` with release notes (date, features, fixes)
3. Create git tag: `git tag v5.1.0`
4. Push tag: `git push origin v5.1.0`
5. GitHub Actions auto-builds and deploys

---

## Getting Help

- **Documentation:** See README.md, FORMULAS.md, DATA_INGESTION.md, CTO_QUESTIONS.md
- **Issues:** Search existing GitHub issues or create a new one with a clear title and description
- **Discussions:** Join team discussions on Slack: #akb1-dev
- **Email:** team@akb1.internal (for sensitive/security issues)

---

## Code of Conduct Enforcement

We take community standards seriously. Violations will result in:

1. **First offense:** Warning + private conversation
2. **Second offense:** Temporary (7-day) ban from contributions
3. **Third offense:** Permanent removal from project

---

## FAQ

**Q: How long does PR review take?**
A: Typically 24–48 hours for minor changes, 3–5 days for major features.

**Q: Can I submit incomplete/WIP PRs?**
A: Yes! Mark as `[WIP]` in title. Helpful for early feedback, but final submission must be complete.

**Q: What if my PR is rejected?**
A: We'll explain why and suggest improvements. You're welcome to resubmit after addressing feedback.

**Q: Do I need to sign a CLA (Contributor License Agreement)?**
A: No CLA required. By submitting, you agree to license your work under the same license as the project.

**Q: Can I add dependencies?**
A: Please discuss in an issue first. Large dependencies (>1MB) require justification.

---

## Resources

- [Semantic Versioning](https://semver.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [AKB1 Command Center Architecture](./ARCHITECTURE.md)

---

## Thank You!

Your contributions make AKB1 Command Center better for everyone. We appreciate your time and effort. Welcome to the team! 🚀

---

**Last Updated:** 2026-04-16  
**Version:** 5.2  
**Maintainer:** Adi Kompalli — AKB1 Framework  
**License:** MIT
