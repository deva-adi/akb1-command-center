import { expect, test } from "@playwright/test";

/**
 * M9 cross-cutting drill-integrity audit.
 *
 * Twelve describe blocks, one per tab. Each block fires at least one
 * drill that exercises the brief's definition of a non-leaf element
 * (a click that opens a panel, changes a route, or expands a detail
 * view) and asserts the result renders without error.
 *
 * Locator order: getByTestId first, getByRole second, getByText last.
 * The known pre-existing strict-mode locator regressions in
 * golden-path.spec.ts and hercules-drill.spec.ts are documented in
 * CLAUDE_MEMORY.md Section 4.5 and are not retried here.
 *
 * Tabs 01 to 11 use the sidebar NavLink as the drill: navigating from
 * a neutral starting route to the target tab and asserting the URL
 * changes and the destination page renders. Sidebar nav is the most
 * stable cross-tab drill path because it is anchored on
 * <nav aria-label="Primary"> in Layout.tsx and the labels come from
 * the canonical TABS registry in lib/tabRegistry.ts.
 *
 * Tab 12 is a section-scroll cockpit, not a click-drill panel model
 * (confirmed with Adi 2026-04-23 ahead of M9). The four Tab 12 tests
 * are render smoke tests that assert each section's stable testid is
 * visible at /pnl?programme=PHOENIX without page-level error.
 */

const NEUTRAL_START_FOR_TAB_01 = "/kpi";
const NEUTRAL_START_OTHERS = "/";

async function clickTabAndAssert(
  page: import("@playwright/test").Page,
  startRoute: string,
  navLabel: string,
  tabNumber: string,
  expectedPath: string,
  pageAnchorText: RegExp | string,
) {
  await page.goto(startRoute);
  const nav = page.getByRole("navigation", { name: "Primary" });
  await expect(nav).toBeVisible();
  // Sidebar NavLink renders two spans (label + number) so the
  // accessible name is "<label> <number>". Match the full computed
  // name so the locator is unambiguous in strict mode.
  const accessibleName = `${navLabel} ${tabNumber}`;
  await nav
    .getByRole("link", { name: accessibleName, exact: true })
    .click();
  await expect(page).toHaveURL(new RegExp(`${expectedPath.replace(/\//g, "\\/")}$`));
  await expect(page.getByText(pageAnchorText).first()).toBeVisible();
}

test.describe("Tab 01 Executive Summary", () => {
  test("sidebar drill from /kpi to / renders Executive Summary heading", async ({
    page,
  }) => {
    await clickTabAndAssert(
      page,
      NEUTRAL_START_FOR_TAB_01,
      "Executive",
      "01",
      "/",
      "Executive Summary",
    );
  });
});

test.describe("Tab 02 KPI Studio", () => {
  test("sidebar drill from / to /kpi renders KPI library card", async ({
    page,
  }) => {
    await clickTabAndAssert(
      page,
      NEUTRAL_START_OTHERS,
      "KPI Studio",
      "02",
      "/kpi",
      "KPI library",
    );
  });
});

test.describe("Tab 03 Delivery Health", () => {
  test("sidebar drill from / to /delivery renders Delivery Health heading", async ({
    page,
  }) => {
    await clickTabAndAssert(
      page,
      NEUTRAL_START_OTHERS,
      "Delivery",
      "03",
      "/delivery",
      "Delivery Health",
    );
  });
});

test.describe("Tab 04 Velocity and Flow", () => {
  test("sidebar drill from / to /velocity renders Velocity & Flow heading", async ({
    page,
  }) => {
    await clickTabAndAssert(
      page,
      NEUTRAL_START_OTHERS,
      "Velocity & Flow",
      "04",
      "/velocity",
      "Velocity & Flow",
    );
  });
});

test.describe("Tab 05 Margin and EVM", () => {
  test("sidebar drill from / to /margin renders Margin & EVM heading", async ({
    page,
  }) => {
    await clickTabAndAssert(
      page,
      NEUTRAL_START_OTHERS,
      "Margin & EVM",
      "05",
      "/margin",
      "Margin & EVM",
    );
  });
});

test.describe("Tab 06 Customer Intelligence", () => {
  test("sidebar drill from / to /customer renders Customer Intelligence heading", async ({
    page,
  }) => {
    await clickTabAndAssert(
      page,
      NEUTRAL_START_OTHERS,
      "Customer",
      "06",
      "/customer",
      "Customer Intelligence",
    );
  });
});

test.describe("Tab 07 AI Governance", () => {
  test("sidebar drill from / to /ai renders AI Governance heading", async ({
    page,
  }) => {
    await clickTabAndAssert(
      page,
      NEUTRAL_START_OTHERS,
      "AI Governance",
      "07",
      "/ai",
      "AI Governance",
    );
  });
});

test.describe("Tab 08 Smart Ops", () => {
  test("sidebar drill from / to /smart-ops renders Smart Ops heading", async ({
    page,
  }) => {
    await clickTabAndAssert(
      page,
      NEUTRAL_START_OTHERS,
      "Smart Ops",
      "08",
      "/smart-ops",
      "Smart Ops",
    );
  });
});

test.describe("Tab 09 Risk and Audit", () => {
  test("sidebar drill from / to /raid renders Risk & Audit heading", async ({
    page,
  }) => {
    await clickTabAndAssert(
      page,
      NEUTRAL_START_OTHERS,
      "Risk & Audit",
      "09",
      "/raid",
      "Risk & Audit",
    );
  });
});

test.describe("Tab 10 Reports and Exports", () => {
  test("sidebar drill from / to /reports renders Reports & Exports heading", async ({
    page,
  }) => {
    await clickTabAndAssert(
      page,
      NEUTRAL_START_OTHERS,
      "Reports",
      "10",
      "/reports",
      "Reports & Exports",
    );
  });
});

test.describe("Tab 11 Data Hub and Settings", () => {
  test("sidebar drill from / to /data-hub renders Data Hub & Settings heading", async ({
    page,
  }) => {
    await clickTabAndAssert(
      page,
      NEUTRAL_START_OTHERS,
      "Data Hub",
      "11",
      "/data-hub",
      "Data Hub & Settings",
    );
  });
});

test.describe("Tab 12 P&L Cockpit (render smoke for read-only sections)", () => {
  /**
   * Tab 12 has zero click-drill handlers in v5.7.0 by design (confirmed
   * with Adi 2026-04-23 ahead of M9). The cockpit is a section-scroll
   * view, not a panel-open view. These four tests exercise the deepest
   * non-leaf path available today: navigating with a programme filter
   * and asserting each section's stable testid renders without error.
   * Click-drill handlers (row-click to detail, card-click to breakdown)
   * are deferred to v5.8 alongside KPI Board, Levers, and Narrative.
   */

  test("Revenue section renders for PHOENIX without error", async ({ page }) => {
    await page.goto("/pnl?programme=PHOENIX");
    await expect(page.getByTestId("revenue-cards")).toBeVisible();
  });

  test("Losses section renders for PHOENIX with the seven-column table visible", async ({
    page,
  }) => {
    await page.goto("/pnl?programme=PHOENIX");
    await expect(page.getByTestId("losses-table")).toBeVisible();
    await expect(page.getByTestId("losses-total-rag")).toHaveAttribute(
      "data-rag-palette",
      "red",
    );
  });

  test("Pyramid section renders for PHOENIX with the chart and overall RAG chip", async ({
    page,
  }) => {
    await page.goto("/pnl?programme=PHOENIX");
    await expect(page.getByTestId("pyramid-block")).toBeVisible();
    await expect(page.getByTestId("pyramid-rag")).toBeVisible();
  });

  test("Earned Value and Receivables section renders for PHOENIX with both sub-cards", async ({
    page,
  }) => {
    await page.goto("/pnl?programme=PHOENIX");
    await expect(page.getByTestId("evr-section")).toBeVisible();
    await expect(page.getByTestId("evr-evm-card")).toBeVisible();
    await expect(page.getByTestId("evr-receivables-card")).toBeVisible();
  });
});
