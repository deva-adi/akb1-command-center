import { expect, test } from "@playwright/test";

/**
 * M6 /pnl stub renders in the live Docker stack, with ContextRail
 * showing the Tab segment and, when ?programme= is set, the Programme
 * segment too. Nav entry appears in the sidebar.
 */
test.describe("/pnl stub (M6)", () => {
  test("loads with title and the seven-sections summary paragraph", async ({ page }) => {
    await page.goto("/pnl");
    await expect(
      page.getByRole("heading", { level: 1, name: /P&L Cockpit/i }),
    ).toBeVisible();
    await expect(
      page.getByText(/Seven sections active in v5\.7\.0/i),
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

  test("P&L Cockpit nav forwards an active programme query param", async ({
    page,
  }) => {
    // Regression for the post-v5.7.0 housekeeping fix: when the user
    // is on a programme-filtered tab and clicks P&L Cockpit in the
    // sidebar, the ?programme= param must travel with them so the
    // cockpit lands on the same programme. Other tab NavLinks are
    // unchanged on purpose.
    await page.goto("/delivery?programme=PHOENIX");
    const nav = page.getByRole("navigation", { name: /primary/i });
    await nav.getByRole("link", { name: "P&L Cockpit", exact: true }).click();
    await expect(page).toHaveURL(/\/pnl\?programme=PHOENIX$/);
    await expect(
      page.getByRole("heading", { level: 1, name: /P&L Cockpit/i }),
    ).toBeVisible();
  });
});
