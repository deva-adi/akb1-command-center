import { expect, test } from "@playwright/test";

/**
 * M7.3 Margin Waterfall section — renders against the live Docker
 * backend with real Phoenix data. Asserts the four layer labels,
 * the layer percentages in the chart aria-label, the three drop
 * bps pills between bars, and the snapshot subtitle.
 */
test.describe("/pnl Margin Waterfall section (M7.3)", () => {
  test("renders the four Phoenix layers with drop annotations", async ({
    page,
  }) => {
    await page.goto("/pnl?programme=PHOENIX");

    const chart = page.getByTestId("margin-waterfall-chart");
    await expect(chart).toBeVisible();

    // Subtitle carries snapshot + scenario + revenue base.
    await expect(
      page.getByText(
        /Snapshot 2026-03-01 · scenario Monthly Actuals · revenue base 820,000/,
      ),
    ).toBeVisible();

    // Accessibility label packs every layer + every drop.
    const label = await chart.getAttribute("aria-label");
    expect(label).toContain("Gross margin 28.0%");
    expect(label).toContain("Contribution margin 12.5%");
    expect(label).toContain("Portfolio margin 8.2%");
    expect(label).toContain("Net margin 4.1%");
    expect(label).toContain("gross to contribution −1550 bps");
    expect(label).toContain("contribution to portfolio −430 bps");
    expect(label).toContain("portfolio to net −410 bps");

    // Drop pills row renders three pills.
    const drops = page.getByTestId("margin-waterfall-drops");
    await expect(drops.getByText("−1550 bps")).toBeVisible();
    await expect(drops.getByText("−430 bps")).toBeVisible();
    await expect(drops.getByText("−410 bps")).toBeVisible();
  });

  test("shows the pick-a-programme prompt when ?programme= is absent", async ({
    page,
  }) => {
    await page.goto("/pnl");
    await expect(
      page.getByText(/Pick a programme to see the margin waterfall/i),
    ).toBeVisible();
  });
});
