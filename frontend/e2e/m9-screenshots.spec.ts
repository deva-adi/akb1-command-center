import { test } from "@playwright/test";

/**
 * M9 evidence-screenshot spec. Captures one full-page PNG per tab into
 * docs/drill-evidence/. Lives in its own spec so the audit-assertion
 * file (m9-drill-audit.spec.ts) stays focused on assertions.
 *
 * Tab 12 captures the Losses section with the four Phoenix loss rows
 * and the red total RAG chip in frame. Per Adi sign-off 2026-04-23
 * this IS the deepest drill view available in v5.7.0 (the cockpit is
 * a section-scroll model, not a panel-open model).
 *
 * Naming: docs/drill-evidence/tab-XX-name-drill.png
 */

const SCREENSHOT_DIR = "../docs/drill-evidence";

async function captureFullPage(
  page: import("@playwright/test").Page,
  route: string,
  filename: string,
) {
  await page.goto(route);
  await page.waitForLoadState("networkidle");
  await page.screenshot({
    path: `${SCREENSHOT_DIR}/${filename}`,
    fullPage: true,
  });
}

test.describe("M9 tab evidence screenshots", () => {
  test("tab 01 executive", async ({ page }) => {
    // Executive Summary has a live SSE alerts ticker that keeps the
    // network busy, so networkidle never settles. Wait for the page
    // heading instead, then a short buffer for charts to paint.
    await page.goto("/");
    await page.getByRole("heading", { name: "Executive Summary" }).waitFor();
    await page.waitForTimeout(1500);
    await page.screenshot({
      path: `${SCREENSHOT_DIR}/tab-01-executive-drill.png`,
      fullPage: true,
    });
  });

  test("tab 02 kpi-studio", async ({ page }) => {
    await captureFullPage(page, "/kpi", "tab-02-kpi-drill.png");
  });

  test("tab 03 delivery", async ({ page }) => {
    await captureFullPage(page, "/delivery", "tab-03-delivery-drill.png");
  });

  test("tab 04 velocity", async ({ page }) => {
    await captureFullPage(page, "/velocity", "tab-04-velocity-drill.png");
  });

  test("tab 05 margin", async ({ page }) => {
    await captureFullPage(page, "/margin", "tab-05-margin-drill.png");
  });

  test("tab 06 customer", async ({ page }) => {
    await captureFullPage(page, "/customer", "tab-06-customer-drill.png");
  });

  test("tab 07 ai-governance", async ({ page }) => {
    await captureFullPage(page, "/ai", "tab-07-ai-drill.png");
  });

  test("tab 08 smart-ops", async ({ page }) => {
    await captureFullPage(page, "/smart-ops", "tab-08-smart-ops-drill.png");
  });

  test("tab 09 raid", async ({ page }) => {
    await captureFullPage(page, "/raid", "tab-09-raid-drill.png");
  });

  test("tab 10 reports", async ({ page }) => {
    await captureFullPage(page, "/reports", "tab-10-reports-drill.png");
  });

  test("tab 11 data-hub", async ({ page }) => {
    await captureFullPage(page, "/data-hub", "tab-11-data-hub-drill.png");
  });

  test("tab 12 pnl with losses section in frame", async ({ page }) => {
    await page.goto("/pnl?programme=PHOENIX");
    await page.waitForLoadState("networkidle");
    // Scroll the Losses section into the middle of the viewport so the
    // four Phoenix loss rows and the red total RAG chip are clearly in
    // frame on the captured PNG.
    const lossesTable = page.getByTestId("losses-table");
    await lossesTable.scrollIntoViewIfNeeded();
    await page.screenshot({
      path: `${SCREENSHOT_DIR}/tab-12-pnl-drill.png`,
      fullPage: true,
    });
  });
});
