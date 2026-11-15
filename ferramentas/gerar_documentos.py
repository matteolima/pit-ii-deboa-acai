"""Gera os dois documentos .docx do PIT II a partir do conteúdo e das imagens do repositório.

Uso: python3 ferramentas/gerar_documentos.py   (requer: pip install python-docx==1.1.2)
Saída: docs/Documentacao-PIT-II-Claudio-Matteo.docx e docs/Entrega-PIT-II-Claudio-Matteo.docx
"""
import json
import struct
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

sys.path.insert(0, str(Path(__file__).parent))
import conteudo as C  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DOCS = RAIZ / "docs"


# ---------------- utilidades ----------------
MODELO = RAIZ / "ferramentas" / "modelo" / "modelo-cruzeiro-do-sul.docx"
PRETO = RGBColor(0, 0, 0)
LARG = 15.0  # largura útil (cm) do papel timbrado: A4 com margens de 3 cm


def novo_doc():
    """Abre o modelo da universidade (papel timbrado no cabeçalho) e esvazia o corpo."""
    d = Document(str(MODELO))
    body = d.element.body
    for el in list(body):
        if not el.tag.endswith("sectPr"):
            body.remove(el)
    for rid, rel in list(d.part.rels.items()):  # remove as imagens do documento antigo
        if rel.reltype.endswith("/image"):
            del d.part.rels[rid]
    st = d.styles["normal"]
    st.font.name = "Arial"
    st.element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:hAnsi"), "Arial")
    st.font.size = Pt(11)
    st.font.color.rgb = PRETO
    for n, sz in (("Heading 1", 18), ("Heading 2", 14), ("Heading 3", 12)):
        h = d.styles[n]
        h.font.name = "Arial"
        rf = h.element.get_or_add_rPr().get_or_add_rFonts()
        for k in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(k), "Arial")
        h.font.size = Pt(sz)
        h.font.bold = True
        h.font.color.rgb = PRETO
    d.styles["Heading 1"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return d


def titulo(d, texto, nivel=1):
    h = d.add_heading(texto, nivel)
    for r in h.runs:
        r.font.color.rgb = PRETO
        r.font.name = "Arial"
    return h


def campo(par, instr):
    r = par.add_run()
    a = OxmlElement("w:fldChar"); a.set(qn("w:fldCharType"), "begin")
    b = OxmlElement("w:instrText"); b.set(qn("xml:space"), "preserve"); b.text = instr
    c = OxmlElement("w:fldChar"); c.set(qn("w:fldCharType"), "separate")
    t = OxmlElement("w:t"); t.text = "Clique com o botão direito → Atualizar campo" if "TOC" in instr else "1"
    e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), "end")
    for x in (a, b, c):
        r._r.append(x)
    r2 = par.add_run(); r2._r.append(t)
    r3 = par.add_run(); r3._r.append(e)


def centro(d, texto, tam=12, negrito=False, depois=6):
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(depois)
    r = p.add_run(texto)
    r.font.size = Pt(tam)
    r.bold = negrito
    return p


def quebra(d):
    d.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def par(d, texto, negrito_ate=None, estilo=None):
    p = d.add_paragraph(style=estilo)
    if negrito_ate and texto.startswith(negrito_ate):
        p.add_run(negrito_ate).bold = True
        p.add_run(texto[len(negrito_ate):])
    else:
        p.add_run(texto)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if not estilo else p.alignment
    return p


def lista(d, itens, numerada=False):
    for k, i in enumerate(itens):
        p = d.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.6)
        p.paragraph_format.first_line_indent = Cm(-0.5)
        p.paragraph_format.space_after = Pt(2)
        p.add_run(f"{k + 1}. " if numerada else "• ")
        p.add_run(i)


def bordas(t):
    tblPr = t._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{lado}")
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "6"); e.set(qn("w:space"), "0"); e.set(qn("w:color"), "000000")
        b.append(e)
    tblPr.append(b)


def sombrear(cel, cor="FFFFFF"):
    tcPr = cel._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), cor)
    tcPr.append(sh)


def tabela(d, cab, linhas, larg=None, tam=10):
    t = d.add_table(rows=1, cols=len(cab))
    bordas(t)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, c in enumerate(cab):
        cel = t.rows[0].cells[i]
        cel.text = ""
        r = cel.paragraphs[0].add_run(c); r.bold = True; r.font.size = Pt(tam)
    for ln in linhas:
        cells = t.add_row().cells
        for i, v in enumerate(ln):
            cells[i].text = ""
            for j, parte in enumerate(str(v).split("\n")):
                pp = cells[i].paragraphs[0] if j == 0 else cells[i].add_paragraph()
                pp.paragraph_format.line_spacing = 1.0
                pp.paragraph_format.space_after = Pt(0)
                pp.add_run(parte).font.size = Pt(tam)
    if larg:
        f = min(1.0, LARG / sum(larg))
        larg = [w * f for w in larg]
        for row in t.rows:
            for i, w in enumerate(larg):
                row.cells[i].width = Cm(w)
    d.add_paragraph().paragraph_format.space_after = Pt(0)
    return t


def png_tam(path):
    b = open(path, "rb").read(24)
    return struct.unpack(">II", b[16:24])


def imagem(d, path, legenda, max_w=LARG, max_h=21.0):
    path = Path(path)
    if not path.exists():
        par(d, f"[imagem pendente: {path.name}]")
        return
    w, h = png_tam(path)
    largura = min(max_w, max_h * w / h)
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(path), width=Cm(largura))
    c = d.add_paragraph(); c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = c.add_run(legenda); r.italic = True; r.font.size = Pt(10)


def girado(path):
    """Cópia girada 90° (para diagramas largos ocuparem a página em pé, como no modelo)."""
    import subprocess
    out = RAIZ / "ferramentas" / ".cache" / f"{Path(path).stem}-girado.png"
    out.parent.mkdir(exist_ok=True)
    subprocess.run(["sips", "-r", "270", str(path), "--out", str(out)], check=True, capture_output=True)
    return out


def cabecalho_aluno(d, extra=None):
    for t in (f"Nome: {C.ALUNO}", f"RGM: {C.RGM}"):
        p = d.add_paragraph(); r = p.add_run(t); r.bold = True
    if extra:
        par(d, extra)


# ---------------- Documentação ----------------
def documentacao():
    d = novo_doc()
    cabecalho_aluno(d, f"Projeto: Plataforma de pedidos e gestão Deboa Açaí – {C.SITE}")

    titulo(d, "Solução – 1 (Histórias de Usuário):")
    par(d, "A Deboa Açaí é uma açaiteria de Imperatriz-MA que recebia pedidos apenas pelo WhatsApp. A plataforma permite "
           "que o cliente monte o açaí, pague online (Pix ou cartão) e acompanhe o pedido; a equipe opera um painel em tempo "
           "real e o proprietário administra cardápio, estoque, marketing e financeiro. Atores: Cliente (inclui o visitante "
           "não logado), Atendente, Gerente e Proprietário.")
    for h in C.HISTORIAS:
        par(d, f"Como {h[1].lower()}, eu quero {h[3]}, para {h[4]}.")
    for (i, req, tit, quero, para, ca, rn, rnf, pri, pts) in C.HISTORIAS:
        prio = " / ".join(f"[{'X' if p == pri else '  '}] {p}" for p in "ABCDE")
        tabela(d, [f"ID: {i}", f"Título: {tit}"], [
            ("Requerente:", req),
            ("Ação:", f"Eu quero {quero}, para {para}."),
            ("Critérios de aceitação:", "\n".join(f"CA#{k + 1} - {x}" for k, x in enumerate(ca))),
            ("Regras de negócio:", "\n".join(f"RN#{k + 1} - {x}" for k, x in enumerate(rn))),
            ("Requisito não funcional:", "\n".join(f"RNF#{k + 1} - {x}" for k, x in enumerate(rnf))),
            ("Prioridade:", prio),
            ("Pontos de história:", str(pts)),
        ], [4.2, 10.8])

    titulo(d, "Solução – 1 (Backlog Priorizado):")
    ordem = sorted(C.HISTORIAS, key=lambda h: ("ABCDE".index(h[8]), -h[9], h[0]))
    tabela(d, ["ID", "História do Usuário", "Estimativa em Pontos", "Prioridade"],
           [(h[0], h[2], h[9], k + 1) for k, h in enumerate(ordem)], [1.5, 8.5, 2.8, 2.2])
    par(d, f"Total: {sum(h[9] for h in C.HISTORIAS)} pontos de história.")

    titulo(d, "Solução – 1 (Tarefas):")
    par(d, "Tarefas técnicas derivadas de cada história; todas concluídas na versão publicada.")
    linhas = [(h[0], t, "Concluída") for h in C.HISTORIAS for t in C.TAREFAS.get(h[0], [])]
    tabela(d, ["História", "Tarefa", "Situação"], linhas, [2, 10.5, 2.5])

    quebra(d)
    titulo(d, "Solução – 2 (Diagrama de caso de uso geral):")
    imagem(d, RAIZ / "diagramas/01-caso-de-uso-geral.png", "Figura 1 – Diagrama de caso de uso geral", LARG, 20)
    tabela(d, ["Ator", "Descrição"], [
        ("Visitante", "Pessoa que navega na loja sem estar logada."),
        ("Cliente", "Visitante identificado (conta ou convidado com nome e WhatsApp) que faz pedidos. Especializa Visitante."),
        ("Atendente", "Funcionário que opera o painel de pedidos, balcão, impressão, disponibilidade e estoque."),
        ("Gerente", "Atendente com permissão para abrir/fechar a loja e cancelar/estornar pedidos."),
        ("Proprietário", "Gerente com acesso total: cardápio, preços, marketing, financeiro, equipe e configurações."),
        ("Mercado Pago", "Sistema externo de pagamentos (Pix e cartão) que notifica a plataforma por webhook."),
        ("Agendador", "Funções agendadas (Netlify e pg_cron) que expiram pedidos não pagos e conciliam pagamentos."),
    ], [3.5, 11.5])

    titulo(d, "Solução – 2 (Casos de uso expandidos):")
    for (uid, nome, atores, us, pre, pos, fluxo, alt) in C.CASOS:
        par(d, f"Nome: {nome}", "Nome:")
        par(d, f"Identificador: #{uid}", "Identificador:")
        par(d, f"Atores: {atores}", "Atores:")
        h = next(x for x in C.HISTORIAS if x[0] == us)
        par(d, f"Descrição: Como {h[1].lower()}, eu quero {h[3]}, para {h[4]}.", "Descrição:")
        par(d, f"Pré-condições: {pre}", "Pré-condições:")
        par(d, f"Pós-condições: {pos}", "Pós-condições:")
        p = d.add_paragraph(); p.add_run("Caso básico de ação:").bold = True
        lista(d, fluxo, numerada=True)
        if alt:
            p = d.add_paragraph(); p.add_run("Fluxos alternativos:").bold = True
            lista(d, alt)
        d.add_paragraph()

    quebra(d)
    titulo(d, "Solução – 2 (Diagrama de Classes):")
    par(d, "Classes do domínio (no banco as tabelas estão em inglês, por exemplo Pedido = orders). Valores monetários são "
           "inteiros em centavos. ItemPedido e OpcaoDoItem guardam uma cópia de nomes e preços no momento da compra.")
    imagem(d, RAIZ / "diagramas/03-diagrama-de-classes.png", "Figura 2 – Diagrama de classes", LARG, 19)

    seqs = [("Cadastro", "04-sequencia-cadastro"), ("Login", "05-sequencia-login"), ("Consulta", "06-sequencia-consulta"),
            ("Carrinho", "07-sequencia-carrinho"), ("Venda", "08-sequencia-venda")]
    for k, (nome, arq) in enumerate(seqs):
        quebra(d)
        titulo(d, f"Solução – 2 (Diagrama de Sequência {'de ' if nome in ('Login', 'Consulta', 'Venda') else ''}{nome}):")
        imagem(d, girado(RAIZ / f"diagramas/{arq}.png"), f"Figura {k + 3} – Sequência de {nome.lower()} (página girada)", LARG, 19.5)

    quebra(d)
    titulo(d, "Solução – 2 (Projeto Físico do Banco de Dados):")
    par(d, "Banco PostgreSQL (Supabase), com Row Level Security em todas as tabelas e regras críticas (criar pedido, transições "
           "de status, estoque) em funções no banco. Dicionário de dados das tabelas principais, gerado das migrações SQL:")
    dic = json.loads((RAIZ / "ferramentas/tabelas.json").read_text(encoding="utf-8"))
    for nome in ["profiles", "customer_addresses", "consents", "categories", "products", "product_variants", "option_lists",
                 "options", "product_option_groups", "orders", "order_items", "order_item_options", "order_status_history",
                 "payments", "refunds", "coupons", "coupon_redemptions", "campaigns", "banners", "ingredients",
                 "stock_movements", "store_settings", "business_hours", "print_jobs", "audit_log"]:
        if nome in dic:
            p = d.add_paragraph(); p.add_run(f"Tabela {nome}").bold = True
            tabela(d, ["Coluna", "Tipo", "Restrições"], dic[nome], [4.5, 3.8, 6.7], tam=9)

    quebra(d)
    titulo(d, "Solução – 3 (Wire frame):")
    wfs = sorted((RAIZ / "wireframes").glob("*.png"))
    for k, f in enumerate(wfs):
        nome = f.stem.split("-", 1)[1].replace("-", " ").capitalize()
        mob = int(f.stem[:2]) <= 10
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.add_run(f"Tela – {nome}").bold = True
        imagem(d, f, f"Wireframe {k + 1}", 8 if mob else LARG, 19)
        if k < len(wfs) - 1:
            quebra(d)

    quebra(d)
    titulo(d, "Solução – 3 (Mockup):")
    par(d, f"Telas oficiais publicadas em {C.SITE} (capturas reais do sistema).")
    mks = sorted((RAIZ / "mockups").glob("*.png"))
    for k, f in enumerate(mks):
        nome = f.stem.split("-", 1)[1].replace("-", " ").capitalize()
        larga = "computador" in f.stem
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.add_run(f"Tela – {nome}").bold = True
        imagem(d, f, f"Mockup {k + 1}", LARG if larga else 8.5, 19.5)
        if k < len(mks) - 1:
            quebra(d)

    quebra(d)
    titulo(d, "Solução – 3 (Mapa Conceitual):", 1)
    imagem(d, RAIZ / "diagramas/09-mapa-conceitual.png", "Mapa conceitual da plataforma", LARG, 19.5)
    quebra(d)
    titulo(d, "Solução – 3 (Mapa Navegacional):", 1)
    imagem(d, girado(RAIZ / "diagramas/10-mapa-navegacional.png"), "Mapa navegacional – rotas reais do sistema (página girada)", LARG, 19.5)
    out = DOCS / "Documentacao-PIT-II-Claudio-Matteo.docx"
    d.save(out)
    return out


# ---------------- Entrega ----------------
def entrega():
    d = novo_doc()
    cabecalho_aluno(d)
    p = d.add_paragraph(); p.add_run("Documentação:").bold = True
    p = d.add_paragraph(); p.add_run("Link do repositório:").bold = True
    par(d, C.REPO)
    par(d, "Diretório com os documentos:")
    par(d, f"{C.REPO}/tree/main/docs")
    par(d, f"Doc PIT 2: {C.REPO}/blob/main/docs/Documentacao-PIT-II-Claudio-Matteo.docx")

    p = d.add_paragraph(); p.add_run("Codificação:").bold = True
    tabela(d, ["Linguagem do Back-end", "TypeScript (Node.js 22) – Next.js 16 Server Actions e rotas de API; regras críticas em PL/pgSQL"], [
        ("Banco de Dados", "PostgreSQL (Supabase)"),
        ("Hospedagem", "Netlify (aplicação + funções agendadas) e Supabase (banco, autenticação, arquivos)"),
        ("Plataforma", "Web (responsivo para smartphone, tablet e computador) e instalável (PWA)"),
        ("Modo de Codificação", "(X) Tradicional\n( ) Low-code\n( ) No-code"),
        ("Link do repositório no GitHub com os códigos abertos", C.REPO),
        ("Link da solução em / funcionamento", C.SITE),
        ("Link do vídeo narrado (no mínimo 5 min)", C.VIDEO),
    ], [5.5, 9.5], tam=11)

    par(d, "Solução codificada no modo tradicional, em TypeScript, com arquitetura em camadas equivalente ao padrão MVC "
           "(as orientações sugerem Java/PHP/C#/Python; optou-se por TypeScript por ser a mesma linguagem no front-end e no "
           "back-end e pelo suporte nativo do Next.js):")
    tabela(d, ["Papel MVC", "Onde está no código"], C.ARQUITETURA_MVC, [4, 11])
    par(d, "Exemplo de regra de negócio (Model) – cálculo do frete por faixa de distância:")
    ex = d.add_paragraph()
    r = ex.add_run("export function quoteByDistance(distanceKm: number, tiers = DEFAULT_DELIVERY_TIERS): DeliveryQuote {\n"
                   "  const d = roundToMeters(distanceKm);\n  const tier = tiers.find((t) => d <= t.maxKm);\n"
                   "  if (!tier) return { available: false, distanceKm: d, reason: \"out_of_range\" };\n"
                   "  return { available: true, distanceKm: d, feeCents: tier.feeCents };\n}")
    r.font.name = "Courier New"; r.font.size = Pt(9)
    par(d, "Boas práticas aplicadas:")
    lista(d, ["Preços, frete e cupons sempre recalculados no servidor/banco (o navegador envia apenas ids e quantidades).",
              "Row Level Security em todas as tabelas e permissões por papel (atendente, gerente, proprietário).",
              "Idempotência em pedidos, pagamentos e movimentos de estoque.",
              "Webhook do Mercado Pago com assinatura HMAC e conciliação agendada a cada 5 minutos.",
              "Limites de tentativas por origem, com IP guardado apenas como hash.",
              "Segredos somente em variáveis de ambiente; LGPD: consentimentos, exportação/exclusão e anonimização."])

    p = d.add_paragraph(); r = p.add_run("Testes da Solução"); r.bold = True; r.font.size = Pt(14)
    par(d, "Testes automatizados (Vitest + PGlite, migrações reais em PostgreSQL em memória): 170 testes, 170 aprovados em "
           "14/11/2026. Testes de ponta a ponta (Playwright): 10 cenários nos perfis celular e computador.")
    tabela(d, ["Arquivo de teste", "O que verifica", "Testes"], [
        ("database.test.ts", "Migrações, RLS, criação de pedido, transições, estoque, cupons, retenção", 51),
        ("pricing.test.ts", "Preço de itens, adicionais grátis/pagos, limites", 18),
        ("printing.test.ts", "Formatação da comanda e fila de impressão", 16),
        ("storefront.test.ts", "Redirecionamento seguro, geocodificação, carrinho, cotação e checkout", 16),
        ("delivery.test.ts", "Faixas de frete e distância", 10),
        ("order-flow.test.ts", "Máquina de estados do pedido", 9),
        ("reports.test.ts", "Relatórios financeiros", 9),
        ("store-hours.test.ts", "Horários, pausas e dias especiais", 9),
        ("operation.test.ts", "Painel da loja, valores em dinheiro e horários exibidos", 8),
        ("mercadopago.test.ts", "Assinatura do webhook e status de pagamento", 7),
        ("coupons.test.ts", "Validação e cálculo de cupons", 6),
        ("seo.test.ts / theme.test.ts", "Dados estruturados e contraste das cores", 8),
        ("auth.test.ts", "Permissões por papel", 3),
    ], [4.2, 8.8, 2], tam=9)

    p = d.add_paragraph(); p.add_run("Laudo de Qualidade").bold = True
    p = d.add_paragraph(); r = p.add_run("RASCUNHO – substituir nomes, datas e resultados pelos testes reais dos colegas antes da entrega."); r.italic = True
    for nome, data, ok, nok, nt in C.LAUDO:
        tabela(d, [f"Nome: {nome}", f"Data do teste: {data}"], [
            ("O que testou e funcionou:", ok),
            ("O que testou e não funcionou – O que deve ser corrigido:", nok),
            ("Funcionalidade não testada (faltou ou não foi implementada):", nt),
        ], [5.5, 9.5])

    p = d.add_paragraph(); p.add_run("Evidências:").bold = True
    par(d, "Link das evidências com imagens e vídeos: (inserir link)")
    p = d.add_paragraph(); p.add_run("Problemas identificados:").bold = True
    for prob, _ in C.PROBLEMAS_CORRIGIDOS:
        par(d, prob)
    p = d.add_paragraph(); p.add_run("Recomendações:").bold = True
    par(d, "Com base nos problemas identificados, foram aplicadas (e já publicadas) as seguintes ações corretivas:")
    lista(d, [c for _, c in C.PROBLEMAS_CORRIGIDOS])
    par(d, "Próximos passos: exercitar em produção o pagamento com cartão e o estorno real, validar notificações e impressora "
           "no aparelho da loja e agendar backup semanal do banco.")
    p = d.add_paragraph(); p.add_run("Vídeo da Solução atualizada").bold = True
    tabela(d, ["Link para o vídeo", C.VIDEO], [], [5, 10])
    out = DOCS / "Entrega-PIT-II-Claudio-Matteo.docx"
    d.save(out)
    return out


if __name__ == "__main__":
    DOCS.mkdir(exist_ok=True)
    print("ok:", documentacao())
    print("ok:", entrega())
