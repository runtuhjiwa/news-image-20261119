// main.ts — entry program for the make.fun bounty "news-image-20261119" (v2).
//
// Copies the pre-rendered infographic `entry.png` (sitting next to this
// file) to the harness output directory as `entry.png`.
//
// Output directory: $MAKEFUN_OUTPUT_DIR when set, otherwise /output.
// The copy is verified before exiting: the file must be a PNG (magic
// bytes), must be <= 1 MiB, and must be byte-identical (SHA-256) to the
// entry.png in this repo. Any failed check exits non-zero.
//
// Run:  node main.ts
// (Node 22, standard library only; no network, no randomness.)

import { createHash } from "node:crypto";
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024;

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

function sha256(filePath: string): string {
  return createHash("sha256").update(readFileSync(filePath)).digest("hex");
}

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const source = join(here, "entry.png");
  if (!existsSync(source)) {
    fail(`entry.png not found next to main.ts (${source})`);
  }

  const sourceBytes = readFileSync(source);
  if (sourceBytes.length > MAX_BYTES) {
    fail(`entry.png is ${sourceBytes.length} bytes, over the 1 MiB limit`);
  }
  if (!sourceBytes.subarray(0, PNG_MAGIC.length).equals(PNG_MAGIC)) {
    fail("entry.png is not a PNG (bad magic bytes)");
  }
  const sourceHash = createHash("sha256").update(sourceBytes).digest("hex");

  const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
  mkdirSync(outDir, { recursive: true });
  const target = join(outDir, "entry.png");
  copyFileSync(source, target);

  const targetStat = statSync(target);
  if (targetStat.size !== sourceBytes.length) {
    fail(`copied size mismatch: ${targetStat.size} != ${sourceBytes.length}`);
  }
  const targetHash = sha256(target);
  if (targetHash !== sourceHash) {
    fail(`copied SHA-256 mismatch: ${targetHash} != ${sourceHash}`);
  }

  console.log(`main.ts: wrote ${target} (${targetStat.size} bytes, sha256 ${targetHash})`);
}

main();
