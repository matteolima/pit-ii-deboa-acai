// Captura os mockups (telas oficiais) do site publicado https://deboaacai.com.br
// Somente navegação e leitura: nenhum pedido é enviado e nenhum login é feito.
// Uso: cd ferramentas && node capturar_mockups.mjs
import { chromium } from "playwright-core";
import { mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const RAIZ = join(dirname(fileURLToPath(import.meta.url)), "..");
const OUT = join(RAIZ, "mockups");
const SITE = process.env.SITE ?? "https://deboaacai.com.br";
mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ channel: "chrome" });

async function shots(viewport, isMobile, list) {
  const ctx = await browser.newContext({ viewport, isMobile, hasTouch: isMobile, deviceScaleFactor: 2, locale: "pt-BR", timezoneId: "America/Fortaleza" });
  const page = await ctx.newPage();
  for (const [nome, path, prep, full = true] of list) {
    await page.goto(SITE + path, { waitUntil: "networkidle" });
    if (prep) await prep(page);
    await page.waitForTimeout(1200); // animações de entrada
    await page.screenshot({ path: join(OUT, `${nome}.png`), fullPage: full });
    console.log("ok", nome);
  }
  await ctx.close();
}

// Monta um carrinho pelo próprio site (adiciona refrigerante e suco), sem finalizar.
async function addSimple(page, slug) {
  await page.goto(`${SITE}/produto/${slug}`, { waitUntil: "networkidle" });
  const radios = page.locator('input[type="radio"]');
  if (await radios.count()) await radios.first().check({ force: true });
  await page.getByRole("button", { name: /adicionar/i }).last().click();
  await page.waitForURL(/carrinho/, { timeout: 10000 }).catch(() => {});
}

const mobile = { width: 390, height: 844 };
await shots(mobile, true, [
  ["01-inicio-celular", "/"],
  ["02-cardapio-celular", "/cardapio"],
  ["03-produto-acai-no-copo-celular", "/produto/acai-no-copo"],
  ["04-carrinho-celular", "/carrinho", async (p) => { await addSimple(p, "refrigerante"); await addSimple(p, "suco"); await p.goto(SITE + "/carrinho", { waitUntil: "networkidle" }); }],
  ["05-checkout-celular", "/carrinho", async (p) => { await addSimple(p, "refrigerante"); await p.goto(SITE + "/checkout", { waitUntil: "networkidle" }); }],
  ["06-entrar-celular", "/entrar"],
  ["07-cadastro-celular", "/cadastro"],
  ["08-cancelamento-celular", "/cancelamento"],
]);
await shots({ width: 1366, height: 820 }, false, [
  ["09-inicio-computador", "/", null, false],
  ["10-cardapio-computador", "/cardapio", null, false],
  ["11-produto-computador", "/produto/barca-deboa", null, false],
]);
await browser.close();
