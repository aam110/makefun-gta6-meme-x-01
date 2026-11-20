// Entry program for make.fun bounty gta6-meme-x-01.
//
// The post itself is the entry: the house reads it from X. This program's
// only job is to hand the house the post's address by copying POST.json
// from the repository root into the output directory.
//
// Node 22, standard library only, no network, deterministic: the two
// grader runs write the same bytes.

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outputDir, { recursive: true });
copyFileSync(join(botDir, "POST.json"), join(outputDir, "POST.json"));
