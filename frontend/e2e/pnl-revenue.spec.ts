import { expect, test } from "@playwright/test";

/**
 * M7.1 Revenue section — renders against the live Docker backend with
 * real Phoenix data. Asserts all five cards appear, each carries a
 * value, and the snapshot-date subtitle confirms the backend answered.
 */
test.describe("/pnl Revenue section (M7.1)", () => {
  test("renders five Phoenix cards with values and a snapshot subtitle", async ({
    page,
  }) => {
    await page.goto("/pnl?programme=PHOENIX");

    const grid = page.getByTestId("revenue-cards");
    await expect(grid).toBeVisible();

    // Five card labels.
    await expect(grid.getByText("Booked revenue")).toBeVisible();
    await expect(grid.getByText("Billed revenue")).toBeVisible();
    await expect(grid.getByText("Collected revenue")).toBeVisible();
    await expect(grid.getByText("Unbilled WIP")).toBeVisible();
    await expect(grid.getByText("AR balance")).toBeVisible();

    // Phoenix Mar 2026 values from the seed: booked 820K, AR 144.32K.
    // formatCurrency renders them with the K suffix.
    await expect(grid.getByText(/\$820\.0 K/)).toBeVisible();
    await expect(grid.getByText(/\$144\.3 K/)).toBeVisible();

    // Subtitle records the snapshot the backend picked. The Margin
    // Waterfall section (M7.3) has a similar subtitle, so scope the
    // match to the first occurrence, which is the Revenue card.
    await expect(
      page.getByText(/Snapshot 2026-03-01.*scenario Monthly Actuals/).first(),
    ).toBeVisible();
  });

  test("shows the pick-a-programme prompt when ?programme= is absent", async ({
    page,
  }) => {
    await page.goto("/pnl");
    await expect(
      page.getByText(/Pick a programme to see revenue/i),
    ).toBeVisible();
  });
});
