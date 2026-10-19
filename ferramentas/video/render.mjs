// Uso: node render.mjs <videos.json> <pasta-de-saida-png>
// Gera um PNG 1080x1920 por slide, com o slide.html desta pasta.
import { chromium } from "playwright";
import fs from "fs"; import path from "path"; import { fileURLToPath } from "url";
const here = path.dirname(fileURLToPath(import.meta.url));
const [,, json, out] = process.argv; const posts = JSON.parse(fs.readFileSync(json)); fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 432, height: 768 }, deviceScaleFactor: 2.5 });
await p.goto("file://" + path.join(here, "slide.html"));
let bad = 0;
for (const post of posts) for (let i = 0; i < post.slides.length; i++) {
  const ok = await p.evaluate(s => show(s), post.slides[i]);
  await p.evaluate(async () => { await Promise.all([...document.images].map(im => im.complete ? 1 : new Promise(r => { im.onload = im.onerror = r })) ) });
  if (!ok) { console.log("TEXTO NAO COUBE:", post.slug, "slide", i); bad++; }
  await p.screenshot({ path: path.join(out, `${post.slug}-${i}.png`) });
}
await b.close(); console.log(bad ? "corrija os slides acima" : "ok"); process.exit(bad ? 1 : 0);
