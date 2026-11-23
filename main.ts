// Day one, day seven — entry program (Node 22, standard library only).
//
// The video is the entry, and the house reads it straight from TikTok.
// This program only hands over the video's address: it reads VIDEO.json
// from the repository root, checks it is a JSON object with a url string,
// and writes that same file into the grader's output directory. It opens
// no network, reads no clock and touches no file outside the repository,
// so the grader's two runs land on identical bytes.
//
// Local run, the way the grader does it:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";

const repoDir = resolve(process.env.MAKEFUN_BOT_DIR ?? "/bot");
const outputDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
const addressFile = join(repoDir, "VIDEO.json");

let raw: string;
try {
  raw = readFileSync(addressFile, "utf8");
} catch (err) {
  console.error(`cannot read ${addressFile}: ${(err as Error).message}`);
  process.exit(1);
}

let address: unknown;
try {
  address = JSON.parse(raw);
} catch {
  console.error("VIDEO.json is not valid JSON");
  process.exit(1);
}

if (
  typeof address !== "object" ||
  address === null ||
  typeof (address as { url?: unknown }).url !== "string" ||
  (address as { url: string }).url.trim() === ""
) {
  console.error('VIDEO.json must be an object with a non-empty string "url"');
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
writeFileSync(join(outputDir, "VIDEO.json"), raw);
