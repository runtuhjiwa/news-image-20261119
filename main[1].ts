// news-image-20261119 — entry program.
//
// This program writes the day's news image to the output directory.
// The image itself (entry.png, drawn by draw.py) sits next to this file;
// the program copies it byte-for-byte to /output/entry.png, so both runs
// produce identical bytes. Standard library only, no network.
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here: string = dirname(fileURLToPath(import.meta.url));
const source: string = resolve(join(here, "entry.png"));
const outDir: string = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target: string = resolve(join(outDir, "entry.png"));

// A PNG always starts with these eight bytes; refuse to ship anything else.
const PNG_MAGIC: readonly number[] = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

function sha256(data: Buffer): string {
  return createHash("sha256").update(data).digest("hex");
}

if (!existsSync(source)) {
  throw new Error(`entry image not found next to main.ts: ${source}`);
}

const bytes: Buffer = readFileSync(source);
const magicOk: boolean = PNG_MAGIC.every((b, i) => bytes[i] === b);
if (!magicOk) {
  throw new Error(`entry image is not a PNG (bad magic bytes): ${source}`);
}
if (bytes.length > 1048576) {
  throw new Error(`entry image exceeds 1 MiB: ${bytes.length} bytes`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// Verify the copy is byte-identical, so both graded runs write the same bytes.
const copied: Buffer = readFileSync(target);
if (copied.length !== bytes.length || sha256(copied) !== sha256(bytes)) {
  throw new Error(`copied image differs from source: ${target}`);
}
console.log(`wrote ${target} (${bytes.length} bytes, sha256 ${sha256(bytes).slice(0, 12)}…)`);
