import { expect, test } from "@playwright/test";

/**
 * M6 /pnl stub renders in the live Docker stack, with ContextRail
 * showing the Tab segment and, when ?programme= is set, the Programme
 * segment too. Nav entry appears in the sidebar.
 */
test.describe("/pnl stub (M6)", () => {
  test("loads with title and remaining-sections placeholder", async ({ page }) => {
    await page.goto("/pnl");
    await expect(
      page.getByRole("heading", { level: 1, name: /P&L Cockpit/i }),
    ).toBeVisible();
    await expect(
      page.getByText(/Remaining sections land in M7\.2 through M7\.7/i),
    ).toBeVisible();
    const rail = page.getByTestId("context-rail");
    await expect(rail).toBeVisible();
    await expect(rail.getByText("Portfolio")).toBeVisible();
    await expect(rail.getByText("P&L Cockpit")).toBeVisible();
  });

  test("ContextRail adds Programme segment with ?programme=PHOENIX", async ({
    page,
  }) => {
    await page.goto("/pnl?programme=PHOENIX");
    const rail = page.getByTestId("context-rail");
    await expect(rail).toBeVisible();
    await expect(rail.getByText("Phoenix")).toBeVisible();
  });

  test("sidebar nav shows the P&L Cockpit entry numbered 12", async ({
    page,
  }) => {
    await page.goto("/");
    const nav = page.getByRole("navigation", { name: /primary/i });
    await expect(nav.getByText("P&L Cockpit")).toBeVisible();
    await expect(nav.getByText("12")).toBeVisible();
  });
});
