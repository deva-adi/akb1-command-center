import { expect, test } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

/**
 * Golden-path E2E — exercise the headline drill flow end-to-end.
 * Runs against the Docker compose stack.
 */

test.describe("AKB1 dashboard — golden path", () => {
  test("executive → delivery → kpi round-trip with currency switch", async ({ page }) => {
    await page.goto("/");

    // Tab 1 loads and shows the header.
    await expect(
      page.getByRole("heading", { name: /executive summary/i }),
    ).toBeVisible();

    // Programme status table is populated.
    await expect(
      page.getByText("Phoenix Platform Modernization"),
    ).toBeVisible();

    // Drill into Phoenix via its status row.
    await page.getByText("Phoenix Platform Modernization").click();
    await expect(page).toHaveURL(/\/delivery\?programme=PHOENIX/);

    await expect(
      page.getByRole("heading", { name: /delivery health/i }),
    ).toBeVisible();

    // Cross-tab drill into KPI Studio via the filter bar's "Open in" chip
    // (not the sidebar nav, which wouldn't carry the programme filter).
    await page
      .locator('nav[aria-label="Breadcrumb"] ~ div a[href*="/kpi?programme="]')
      .first()
      .click();
    await expect(page).toHaveURL(/\/kpi\?programme=PHOENIX/);

    // KPI library should be populated.
    await expect(page.getByText(/KPI library/i)).toBeVisible();

    // Currency selector flips the base.
    const currency = page.getByLabel("Base currency");
    await currency.selectOption("INR");
    await expect(currency).toHaveValue("INR");
  });

  test("reports tab offers downloads", async ({ page }) => {
    await page.goto("/reports");
    await expect(
      page.getByRole("heading", { name: /reports & exports/i }),
    ).toBeVisible();
    await expect(
      page.getByRole("link", { name: /portfolio-wide audit zip/i }),
    ).toBeVisible();
  });

  test("no axe-core violations on the executive dashboard", async ({ page }) => {
    await page.goto("/");
    // Let the React Query fetches settle.
    await expect(
      page.getByText("Phoenix Platform Modernization"),
    ).toBeVisible();

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa"])
      .analyze();

    // Fail only on serious/critical violations; log the rest. Keeps the
    // bar high without punishing every advisory recommendation.
    const blocking = results.violations.filter(
      (v) => v.impact === "serious" || v.impact === "critical",
    );
    if (blocking.length) {
      console.error(
        "Axe violations:\n" +
          blocking
            .map((v) => `  - ${v.id} (${v.impact}): ${v.description}`)
            .join("\n"),
      );
    }
    expect(blocking).toHaveLength(0);
  });
});
