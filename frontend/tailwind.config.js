/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // AKB1 brand palette — ARCHITECTURE.md §19
        navy: {
          DEFAULT: "#1B2A4A",
          50: "#E8EBF2",
          100: "#C5CCDD",
          500: "#1B2A4A",
          600: "#162038",
          700: "#0F1729",
        },
        ice: {
          DEFAULT: "#D5E8F0",
          50: "#F3F8FB",
          100: "#E4EEF4",
          500: "#D5E8F0",
          600: "#B6D0DD",
        },
        amber: {
          DEFAULT: "#F59E0B",
          500: "#F59E0B",
          600: "#D97706",
        },
        success: {
          DEFAULT: "#10B981",
          500: "#10B981",
          600: "#059669",
        },
        danger: {
          DEFAULT: "#EF4444",
          500: "#EF4444",
          600: "#DC2626",
        },
      },
      fontFamily: {
        sans: [
          "Inter",
          "system-ui",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "sans-serif",
        ],
        mono: ["JetBrains Mono", "ui-monospace", "SFMono-Regular", "monospace"],
      },
      boxShadow: {
        card: "0 1px 3px 0 rgba(27, 42, 74, 0.08), 0 1px 2px 0 rgba(27, 42, 74, 0.04)",
        "card-hover": "0 4px 12px 0 rgba(27, 42, 74, 0.12)",
      },
    },
  },
  plugins: [],
};
