const { execSync } = require("child_process");

const step = process.argv[2] || "tsc";

if (step === "tsc") {
  console.log("=== TypeScript Type Check ===");
  try {
    const out = execSync("node node_modules/typescript/bin/tsc --noEmit 2>&1", {
      cwd: __dirname,
      encoding: "utf8",
      timeout: 90000,
    });
    if (out.trim()) console.log(out.trim());
    console.log("TSC_RESULT: PASS");
  } catch (e) {
    console.log("TSC_RESULT: FAIL");
    if (e.stdout) console.log(e.stdout);
  }
} else if (step === "vite") {
  console.log("=== Vite Production Build ===");
  try {
    const out = execSync("node node_modules/vite/bin/vite.js build 2>&1", {
      cwd: __dirname,
      encoding: "utf8",
      timeout: 90000,
    });
    console.log(out.trim().split("\n").slice(-5).join("\n"));
    console.log("VITE_RESULT: PASS");
  } catch (e) {
    console.log("VITE_RESULT: FAIL");
    if (e.stdout) console.log(e.stdout);
    if (e.stderr) console.log(e.stderr);
  }
}
