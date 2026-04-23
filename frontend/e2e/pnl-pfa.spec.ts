import { expect, test } from "@playwright/test";

/**
 * M7.4 PFA section — renders against the live Docker backend with
 * real Phoenix data. Asserts the three rows populate with values
 * derived from the two /pfa calls (revenue + gross_pct), the cost
 * row derives client-side, and the gross-margin variance carries
 * the red RAG palette for the seeded Phoenix margin shortfall.
 */
test.describe("/pnl PFA section (M7.4)", () => {
  test("renders Revenue, Cost, Gross Margin rows for Phoenix", async ({
    page,
  }) => {
    await page.goto("/pnl?programme=PHOENIX");

    const table = page.getByTestId("pfa-table");
    await expect(table).toBeVisible();

    // Revenue row: plan 850K, actual 820K, variance −$30.0 K (−3.5%).
    const revRow = page.getByTestId("pfa-row-revenue");
    await expect(revRow).toContainText("$850.0 K");
    await expect(revRow).toContainText("$820.0 K");
    await expect(revRow).toContainText("−$30.0 K");

    // Cost row (derived): plan ~$550K, actual $590.4K, variance +$40.4K.
    const costRow = page.getByTestId("pfa-row-cost-derived");
    await expect(costRow).toContainText("$550.0 K");
    await expect(costRow).toContainText("$590.4 K");
    await expect(costRow).toContainText("+$40.4 K");

    // Gross margin row: plan 35.3%, actual 28.0%, variance −729 bps red.
    const marRow = page.getByTestId("pfa-row-gross-margin");
    await expect(marRow).toContainText("35.3%");
    await expect(marRow).toContainText("28.0%");
    await expect(marRow).toContainText("−729 bps");
    const marVariance = marRow.locator("[data-variance-palette]");
    await expect(marVariance).toHaveAttribute("data-variance-palette", "red");

    // Forecast footnote is visible.
    await expect(page.getByTestId("pfa-forecast-footnote")).toContainText(
      "Forecast at Completion not seeded",
    );
  });

  test("shows the pick-a-programme prompt when ?programme= is absent", async ({
    page,
  }) => {
    await page.goto("/pnl");
    await expect(
      page.getByText(/Pick a programme to see plan vs forecast vs actual/i),
    ).toBeVisible();
  });
});
