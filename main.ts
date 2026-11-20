// news-image-20261119 — "The World, Thursday 19 November 2026"
//
// This entry is a newspaper front page summing up Thursday 19 November
// 2026: the Trump–Xi–Putin summit in Shenzhen, the ICJ genocide verdict
// against Myanmar, Anthropic's record IPO pricing, and the unrest in
// Bangladesh, plus the day's smaller stories. The page itself is the
// entry.png file sitting next to this script (drawn by draw_news.py);
// this program only delivers that exact file to the grader, placing it
// at $MAKEFUN_OUTPUT_DIR/entry.png — "/output" inside the grader
// container, or any directory you point it at locally:
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Node 22 standard library only. No dependencies, no network, no
// arguments.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// Resolve the image relative to this file, not the working directory,
// so the program works no matter where it is launched from.
const scriptDir = dirname(fileURLToPath(import.meta.url));
const frontPage = resolve(scriptDir, "entry.png");

// The grader reads the image from here; the environment variable lets
// the same code run locally and in the container.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

if (!existsSync(frontPage)) {
  throw new Error(`front page image not found: ${frontPage}`);
}

// A fresh container mount may not have the output directory yet.
mkdirSync(outDir, { recursive: true });

copyFileSync(frontPage, target);
console.log(`front page written to ${target}`);
