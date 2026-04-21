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

  test("CSV import round-trip: preview → commit → rollback", async ({ page }) => {
    await page.goto("/data-hub");
    await expect(
      page.getByRole("heading", { name: /data hub/i }),
    ).toBeVisible();

    // Build a minimal programmes CSV in memory and drop it onto the upload zone.
    const csvContent = [
      "name,code,client,start_date,end_date,status,bac,revenue,team_size,offshore_ratio,delivery_model,currency_code",
      "E2E Test Programme,E2E-TST,TestCo,2026-01-01,2027-01-01,Green,1000000,1000000,10,0.50,Managed Services,USD",
    ].join("\n");

    const dropzone = page.locator("label[for='csv-upload']");
    await dropzone.dispatchEvent("dragover", { bubbles: true });
    await dropzone.dispatchEvent("dragleave", { bubbles: true });

    // Use file chooser to upload the CSV.
    const [fileChooser] = await Promise.all([
      page.waitForEvent("filechooser"),
      dropzone.click(),
    ]);
    await fileChooser.setFiles({
      name: "e2e-programmes.csv",
      mimeType: "text/csv",
      buffer: Buffer.from(csvContent),
    });

    // Preview should appear — the filename is shown in a <strong> inside the preview paragraph.
    await expect(page.getByRole("strong").filter({ hasText: /e2e-programmes\.csv/i })).toBeVisible();
    // Entity type dropdown renders once preview is ready.
    await expect(page.locator('[aria-label="Entity type"]')).toBeVisible();

    // Select entity type and commit.
    await page.selectOption('[aria-label="Entity type"]', "programmes");
    await page.getByRole("button", { name: /^commit$/i }).click();

    // Success banner — the unique "import #NNN" text only appears in the commit result banner.
    await expect(page.getByText(/import #\d+/i)).toBeVisible({ timeout: 15_000 });

    // Recent imports ledger should now show at least one entry.
    await expect(
      page.locator("ul li").filter({ hasText: /e2e-programmes\.csv/i }).first()
    ).toBeVisible();

    // Rollback.
    await page.getByRole("button", { name: /rollback/i }).first().click();
    await page.waitForTimeout(1000);
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
