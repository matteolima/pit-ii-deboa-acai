// Mockups do painel administrativo. Abre uma janela do Chrome na tela de login: a própria pessoa
// entra com a conta dela; o script espera o login e captura somente telas sem dados de clientes
// nem faturamento. O perfil temporário (com a sessão) fica fora do repositório e é apagado no fim.
// Uso: cd ferramentas && node capturar_admin.mjs
import { chromium } from "playwright-core";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const RAIZ = join(dirname(fileURLToPath(import.meta.url)), "..");
const SITE = "https://deboaacai.com.br";
const perfil = mkdtempSync(join(process.env.TMPDIR ?? tmpdir(), "pit-admin-"));

const ctx = await chromium.launchPersistentContext(perfil, {
  channel: "chrome", headless: false, viewport: { width: 1366, height: 820 }, deviceScaleFactor: 2,
  locale: "pt-BR", ignoreDefaultArgs: ["--enable-automation"],
});
try {
  const page = ctx.pages()[0] ?? (await ctx.newPage());
  await page.goto(`${SITE}/entrar?next=%2Fadmin`);
  console.log("Aguardando login na janela do Chrome (até 15 min)...");
  await page.waitForURL((u) => u.pathname.startsWith("/admin"), { timeout: 15 * 60_000 });
  const telas = [
    ["12-admin-cardapio", "/admin/cardapio"],
    ["13-admin-acompanhamentos", "/admin/opcoes"],
    ["14-admin-estoque", "/admin/estoque"],
    ["15-admin-marketing", "/admin/marketing"],
    ["16-admin-loja-e-horarios", "/admin/loja"],
    ["17-admin-aparencia", "/admin/aparencia"],
    ["18-admin-ajuda", "/admin/ajuda"],
    ["19-painel-pedido-de-balcao", "/painel/balcao"],
  ];
  for (const [nome, path] of telas) {
    await page.goto(SITE + path, { waitUntil: "networkidle" });
    await page.waitForTimeout(1200);
    await page.screenshot({ path: join(RAIZ, "mockups", `${nome}.png`) }); // só a primeira tela (sem rolar)
    console.log("ok", nome);
  }
} finally {
  await ctx.close();
  rmSync(perfil, { recursive: true, force: true });
}
