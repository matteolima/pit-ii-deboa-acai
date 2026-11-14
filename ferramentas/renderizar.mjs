// Renderiza as fontes do PIT em PNG usando o Google Chrome instalado (playwright-core).
//   diagramas/fontes/*.mmd  -> diagramas/*.png   (Mermaid)
//   diagramas/fontes/*.svg  -> diagramas/*.png
//   wireframes/fontes/*.html -> wireframes/*.png
// Uso: cd ferramentas && npm install && npm run renderizar
import { chromium } from "playwright-core";
import { readFileSync, readdirSync, mkdirSync } from "node:fs";
import { dirname, join, basename } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const RAIZ = join(dirname(fileURLToPath(import.meta.url)), "..");
const MERMAID = readFileSync(join(RAIZ, "ferramentas/node_modules/mermaid/dist/mermaid.min.js"), "utf8");
const only = process.argv[2];

const browser = await chromium.launch({ channel: "chrome" });
const page = await browser.newPage({ deviceScaleFactor: 2, viewport: { width: 1600, height: 1000 } });

async function mermaid(src, out) {
  const code = readFileSync(src, "utf8");
  const html = `<!doctype html><meta charset="utf-8"><body style="margin:0;background:#fff">
  <div id="d" style="display:inline-block;padding:24px"></div>
  <script>${MERMAID}</script>
  <script>
    mermaid.initialize({ startOnLoad:false, theme:"base", fontFamily:"Arial, sans-serif",
      themeVariables:{ primaryColor:"#f3e3fe", primaryBorderColor:"#3a0244", primaryTextColor:"#24012b",
        lineColor:"#3a0244", secondaryColor:"#fffaf0", tertiaryColor:"#fffaf0", actorBkg:"#f3e3fe",
        actorBorder:"#3a0244", noteBkgColor:"#fff6c2", noteBorderColor:"#c9a800", fontSize:"16px" },
      sequence:{ useMaxWidth:false, mirrorActors:false, wrap:true, width:170, actorMargin:40, noteMargin:8, messageMargin:30 }, flowchart:{ useMaxWidth:false, htmlLabels:true }, class:{ useMaxWidth:false }, classDiagram:{ useMaxWidth:false } });
    mermaid.render("g", ${JSON.stringify(code)}).then(r => { const d=document.getElementById("d"); d.innerHTML = r.svg; const svg=d.querySelector("svg"); const vb=svg.viewBox.baseVal; svg.removeAttribute("style"); svg.setAttribute("width", vb.width); svg.setAttribute("height", vb.height); document.title = "ok"; })
      .catch(e => { document.title = "erro: " + e.message; });
  </script>`;
  await page.goto("about:blank");
  await page.setContent(html);
  await page.waitForFunction(() => document.title !== "", null, { timeout: 20000 });
  const t = await page.title();
  if (t !== "ok") throw new Error(`${basename(src)}: ${t}`);
  await page.locator("#d").screenshot({ path: out });
}

async function file(src, out, selector = "body > *:first-child") {
  await page.goto(pathToFileURL(src).href);
  await page.waitForLoadState("networkidle");
  await page.locator(selector).first().screenshot({ path: out });
}

const jobs = [];
for (const f of readdirSync(join(RAIZ, "diagramas/fontes"))) {
  const src = join(RAIZ, "diagramas/fontes", f);
  const out = join(RAIZ, "diagramas", f.replace(/\.(mmd|svg)$/, ".png"));
  if (f.endsWith(".mmd")) jobs.push([src, out, () => mermaid(src, out)]);
  if (f.endsWith(".svg")) jobs.push([src, out, () => file(src, out, "svg")]);
}
for (const f of readdirSync(join(RAIZ, "wireframes/fontes"))) {
  if (!f.endsWith(".html") || f.startsWith("_")) continue;
  const src = join(RAIZ, "wireframes/fontes", f);
  const out = join(RAIZ, "wireframes", f.replace(/\.html$/, ".png"));
  jobs.push([src, out, () => file(src, out, ".tela")]);
}
mkdirSync(join(RAIZ, "wireframes"), { recursive: true });
for (const [src, out, run] of jobs) {
  if (only && !src.includes(only)) continue;
  await run();
  console.log("ok", basename(out));
}
await browser.close();
