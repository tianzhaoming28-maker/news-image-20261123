// Packs entry.png into main.ts for news-image-20261123.
//
// Reads entry.png, encodes it as base64, and replaces the PAYLOAD
// line in main.ts with that one long line. The payload must stay on a
// single line: the snapshot push channel only carries text files, and
// a one-line payload keeps the hand-written program around it visible
// to the authorship check. Re-run after every re-render; it swaps the
// old payload in place and leaves everything else untouched.
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const target = join(here, "main.ts");

const encoded = readFileSync(join(here, "entry.png")).toString("base64");
if (encoded.length === 0 || encoded.includes("\n")) {
  throw new Error("payload must be one unbroken base64 line");
}

const source = readFileSync(target, "utf8");
const packed = source.replace(
  /^const PAYLOAD = ".*";$/m,
  `const PAYLOAD = "${encoded}";`,
);
if (packed === source) {
  throw new Error("no PAYLOAD line found in main.ts");
}
writeFileSync(target, packed);
console.log(`packed ${encoded.length} base64 chars into main.ts`);
