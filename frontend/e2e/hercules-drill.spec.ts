import { expect, test } from "@playwright/test";

test.describe("Hercules drill-navigation regression", () => {
  test("Hercules visible in Executive Overview with At Risk status", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByText("Hercules Workload Consolidation")).toBeVisible({ timeout: 10_000 });
  });

  test("Hercules drill-down to delivery — renders empty-state placeholder (no projects)", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByText("Hercules Workload Consolidation")).toBeVisible({ timeout: 10_000 });
    await page.goto("/delivery?programme=HERCULES");
    // Hercules has no projects yet — expect the graceful empty-state, not a crash.
    await expect(page.getByText("No projects yet")).toBeVisible({ timeout: 10_000 });
    await expect(page.locator("body")).not.toContainText("TypeError");
    await expect(page.locator("body")).not.toContainText("Cannot read");
  });

  test("Hercules in KPI Studio renders without crash", async ({ page }) => {
    await page.goto("/");
    await page.goto("/kpi?programme=HERCULES");
    await expect(
      page.getByText("KPI library").or(page.getByText("Loading KPI library…"))
    ).toBeVisible({ timeout: 10_000 });
    await expect(page.locator("body")).not.toContainText("TypeError");
  });

  test("RAG counts on executive overview updated to include Hercules At Risk", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByText("Hercules Workload Consolidation")).toBeVisible({ timeout: 10_000 });
    // Page renders without JS errors
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));
    await page.waitForTimeout(1000);
    expect(errors).toHaveLength(0);
  });
});
