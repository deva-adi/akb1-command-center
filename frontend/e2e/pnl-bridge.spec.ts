import { expect, test } from "@playwright/test";

/**
 * M7.2 Margin Bridge section — renders against the live Docker backend
 * with real Phoenix Feb->Mar data. Asserts the -340 bps total and the
 * four driver labels appear, and that the aria-label on the chart
 * container carries every bar's value for screen readers.
 */
test.describe("/pnl Margin Bridge section (M7.2)", () => {
  test("renders the Phoenix Feb->Mar bridge with -340 bps total", async ({
    page,
  }) => {
    await page.goto("/pnl?programme=PHOENIX");

    const chart = page.getByTestId("margin-bridge-chart");
    await expect(chart).toBeVisible();

    // Subtitle carries the snapshot dates and the total delta.
    await expect(
      page.getByText(
        /Gross margin 31\.4% on 2026-02-01.*28\.0% on 2026-03-01.*total delta −340 bps/,
      ),
    ).toBeVisible();

    // Accessibility label packs every bar for screen readers.
    const label = await chart.getAttribute("aria-label");
    expect(label).toContain("prior 31.4%");
    expect(label).toContain("current 28.0%");
    expect(label).toContain("total −340 bps");
    expect(label).toContain("price +147 bps");
    expect(label).toContain("volume +62 bps");
    expect(label).toContain("mix −506 bps");
    expect(label).toContain("cost −43 bps");
  });

  test("shows the pick-a-programme prompt when ?programme= is absent", async ({
    page,
  }) => {
    await page.goto("/pnl");
    await expect(
      page.getByText(/Pick a programme to see the margin bridge/i),
    ).toBeVisible();
  });
});
