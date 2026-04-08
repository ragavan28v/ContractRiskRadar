import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eff6ff",
          100: "#dbeafe",
          500: "#2563eb",
          600: "#1d4ed8"
        },
        risk: {
          low: "#22c55e",
          moderate: "#eab308",
          high: "#ef4444"
        }
      }
    }
  },
  plugins: []
};

export default config;

