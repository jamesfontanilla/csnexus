import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import { fileURLToPath } from "url";
import path from "path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [react()],
  test: {
    root: __dirname,
    environment: "jsdom",
    setupFiles: ["./src/__tests__/setup.ts"],
    globals: true,
  },
});
