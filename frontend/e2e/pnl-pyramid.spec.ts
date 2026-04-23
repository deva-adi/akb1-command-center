import { expect, test } from "@playwright/test";

/**
 * M7.6 Pyramid + EVM + DSO sub-cards — renders against the live Docker
 * backend. Asserts the pyramid chart renders, the EVM sub-card carries
 * the CPI and SPI numbers + sparklines, and the DSO sub-card shows
 * current days + AR + Unbilled WIP without a trend (v5.8 per TECH_DEBT).
 */
test.describe("/pnl Pyramid section (M7.6)", () => {
  test("renders pyramid chart + EVM numbers + DSO values for Phoenix", async ({
    page,
  }) => {
    await page.goto("/pnl?programme=PHOENIX");

    // Pyramid chart renders with an RAG chip and footnote.
    const pyramidBlock = page.getByTestId("pyramid-block");
    await expect(pyramidBlock).toBeVisible();
    await expect(page.getByTestId("pyramid-chart")).toBeVisible();
    await expect(page.getByTestId("pyramid-rag")).toBeVisible();

    // Phoenix carries anomalous weights so the footnote fires.
    await expect(page.getByTestId("pyramid-chart-footnote")).toContainText(
      /Tier weight anomaly detected/,
    );

    // EVM sub-card.
    const evmCard = page.getByTestId("evm-sub-card");
    await expect(evmCard).toBeVisible();
    const cpi = page.getByTestId("evm-cpi");
    await expect(cpi).toContainText("0.87");
    await expect(cpi).toContainText("CPI = EV / AC");
    const spi = page.getByTestId("evm-spi");
    await expect(spi).toContainText("0.84");
    await expect(spi).toContainText("SPI = EV / PV");

    // Sparklines containers exist.
    await expect(page.getByTestId("evm-cpi-sparkline")).toBeVisible();
    await expect(page.getByTestId("evm-spi-sparkline")).toBeVisible();

    // DSO sub-card.
    const dsoCard = page.getByTestId("dso-sub-card");
    await expect(dsoCard).toBeVisible();
    await expect(page.getByTestId("dso-value")).toContainText("6.0 d");
    await expect(page.getByTestId("dso-rag")).toHaveAttribute(
      "data-rag-palette",
      "green",
    );
    await expect(page.getByTestId("dso-ar")).toContainText("$144.3 K");
    await expect(page.getByTestId("dso-unbilled")).toContainText("$98.4 K");
  });

  test("shows the pick-a-programme prompt when ?programme= is absent", async ({
    page,
  }) => {
    await page.goto("/pnl");
    await expect(
      page.getByText(/Pick a programme to see the resource pyramid/i),
    ).toBeVisible();
  });
});
