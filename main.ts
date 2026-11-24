// Entry program for post-x-promote-make-your-own-bounty-01 (Node 22, stdlib only).
// The entry is the X post itself; this program only hands its address in:
// it copies POST.json from the repository root to /output/POST.json,
// where the gate reads it. Nothing scored is computed here.
//
// Local run:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const source = join(botDir, 'POST.json');
const target = join(outDir, 'POST.json');

let text: string;
try {
  text = readFileSync(source, 'utf8');
} catch (err) {
  console.error(`cannot read POST.json from ${botDir}: ${(err as Error).message}`);
  process.exit(1);
}

const parsed: unknown = JSON.parse(text);
if (typeof parsed !== 'object' || parsed === null || typeof (parsed as { url?: unknown }).url !== 'string') {
  console.error('POST.json must be an object with a string "url" field');
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(target, text);
console.log(`POST.json copied to ${target}`);
