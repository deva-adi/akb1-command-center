import { defineConfig, devices } from "@playwright/test";

const PORT = Number(process.env.FRONTEND_PORT ?? 9000);

/**
 * Playwright config — AKB1 Command Center E2E.
 *
 * Tests assume the full Docker stack is already up at
 * http://127.0.0.1:${FRONTEND_PORT}. Default FRONTEND_PORT is 9000.
 *
 * Locally:
 *   docker compose up -d
 *   npx playwright install chromium
 *   npm run test:e2e
 */
export default defineConfig({
  testDir: "./e2e",
  timeout: 30_000,
  expect: { timeout: 5_000 },
  fullyParallel: false,
  retries: 0,
  reporter: [["list"], ["html", { open: "never", outputFolder: "playwright-report" }]],
  use: {
    baseURL: `http://127.0.0.1:${PORT}`,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
});
