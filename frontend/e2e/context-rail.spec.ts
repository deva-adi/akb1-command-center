import { expect, test } from "@playwright/test";

/**
 * M5 manual-check spec. Loads two existing tabs with a programme filter
 * on the URL and asserts ContextRail renders the expected breadcrumb
 * chain (Portfolio > Tab > Programme). Runs against the Docker stack.
 */
test.describe("ContextRail", () => {
  test("renders on /margin with ?programme=PHOENIX", async ({ page }) => {
    await page.goto("/margin?programme=PHOENIX");
    const rail = page.getByTestId("context-rail");
    await expect(rail).toBeVisible();
    await expect(rail.getByText("Portfolio")).toBeVisible();
    await expect(rail.getByText("Margin & EVM")).toBeVisible();
    await expect(rail.getByText("Phoenix")).toBeVisible();
  });

  test("renders on /delivery with ?programme=ATLAS", async ({ page }) => {
    await page.goto("/delivery?programme=ATLAS");
    const rail = page.getByTestId("context-rail");
    await expect(rail).toBeVisible();
    await expect(rail.getByText("Portfolio")).toBeVisible();
    await expect(rail.getByText("Delivery")).toBeVisible();
    await expect(rail.getByText("Atlas")).toBeVisible();
  });
});
