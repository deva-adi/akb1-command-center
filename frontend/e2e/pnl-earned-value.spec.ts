import { expect, test } from "@playwright/test";

/**
 * M7.7 Earned Value and Receivables — renders against the live Docker
 * backend. EVM sub-card carries the CPI and SPI numbers with a combined
 * sparkline. Receivables sub-card carries the DSO days hero with AR and
 * Unbilled WIP underneath. Each sub-card shows its own snapshot date.
 */
test.describe("/pnl Earned Value and Receivables (M7.7)", () => {
  test("renders CPI, SPI, DSO days, AR and Unbilled WIP for Phoenix", async ({
    page,
  }) => {
    await page.goto("/pnl?programme=PHOENIX");

    const evm = page.getByTestId("evr-evm-card");
    await expect(evm).toBeVisible();
    const cpi = page.getByTestId("evr-cpi");
    await expect(cpi).toContainText("0.87");
    const spi = page.getByTestId("evr-spi");
    await expect(spi).toContainText("0.84");
    await expect(page.getByTestId("evr-formula")).toContainText(
      "CPI = EV / AC",
    );
    await expect(page.getByTestId("evr-formula")).toContainText(
      "SPI = EV / PV",
    );
    await expect(page.getByTestId("evr-sparkline")).toBeVisible();

    const receivables = page.getByTestId("evr-receivables-card");
    await expect(receivables).toBeVisible();
    await expect(page.getByTestId("evr-dso-days")).toContainText("6.0 days");
    await expect(page.getByTestId("evr-dso-rag")).toHaveAttribute(
      "data-rag-palette",
      "green",
    );
    await expect(page.getByTestId("evr-dso-ar")).toContainText("$144.3 K");
    await expect(page.getByTestId("evr-dso-unbilled")).toContainText(
      "$98.4 K",
    );
  });

  test("each sub-card subtitle shows its own snapshot date", async ({
    page,
  }) => {
    await page.goto("/pnl?programme=PHOENIX");
    await expect(page.getByTestId("evr-evm-card")).toContainText(
      /Snapshot \d{4}-\d{2}-\d{2}/,
    );
    await expect(page.getByTestId("evr-receivables-card")).toContainText(
      /Snapshot \d{4}-\d{2}-\d{2}/,
    );
  });

  test("shows the pick-a-programme prompt when ?programme= is absent", async ({
    page,
  }) => {
    await page.goto("/pnl");
    await expect(
      page.getByText(/Pick a programme to see earned value and receivables/i),
    ).toBeVisible();
  });
});
