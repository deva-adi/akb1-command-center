import { expect, test } from "@playwright/test";

/**
 * M7.5 Losses with Attribution — renders against the live Docker
 * backend with real Phoenix data. Asserts the four loss rows, the
 * cumulative running total, the red total RAG chip (Phoenix sits at
 * 237.8% of programme revenue), and the breakdown chart labels.
 */
test.describe("/pnl Losses section (M7.5)", () => {
  test("renders four Phoenix loss rows with revenue-foregone and bps-lost", async ({
    page,
  }) => {
    await page.goto("/pnl?programme=PHOENIX");

    const table = page.getByTestId("losses-table");
    await expect(table).toBeVisible();

    const scope = page.getByTestId("losses-row-scope-creep");
    await expect(scope).toContainText("Scope Creep");
    await expect(scope).toContainText("In Progress");
    await expect(scope).toContainText("$1.20 M");
    await expect(scope).toContainText("$1.71 M");
    await expect(scope).toContainText("14,634 bps");

    const rework = page.getByTestId("losses-row-rework-defect-leakage");
    await expect(rework).toContainText("$420.0 K");
    await expect(rework).toContainText("$1.62 M"); // cumulative

    const bench = page.getByTestId("losses-row-bench-tax");
    await expect(bench).toContainText("Mitigated");
    await expect(bench).toContainText("$1.80 M"); // cumulative

    const est = page.getByTestId("losses-row-estimation-miss");
    await expect(est).toContainText("$1.95 M"); // cumulative final

    const totalRow = page.getByTestId("losses-total-row");
    await expect(totalRow).toContainText("$1.95 M");
    await expect(totalRow).toContainText(/237\.8% of programme revenue/);
    const chip = page.getByTestId("losses-total-rag");
    await expect(chip).toHaveAttribute("data-rag-palette", "red");
    await expect(chip).toHaveText("Red");

    const chart = page.getByTestId("losses-breakdown-chart");
    await expect(chart).toBeVisible();
    const label = await chart.getAttribute("aria-label");
    expect(label).toContain("Scope Creep $1.20 M (61.5%)");
    expect(label).toContain("Rework & Defect Leakage $420.0 K (21.5%)");
  });

  test("shows the pick-a-programme prompt when ?programme= is absent", async ({
    page,
  }) => {
    await page.goto("/pnl");
    await expect(
      page.getByText(/Pick a programme to see losses with attribution/i),
    ).toBeVisible();
  });
});
