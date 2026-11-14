"""Gera os dois documentos .docx do PIT II a partir do conteúdo e das imagens do repositório.

Uso: python3 ferramentas/gerar_documentos.py   (requer: pip install python-docx==1.1.2)
Saída: docs/Documentacao-PIT-II-Claudio-Matteo.docx e docs/Entrega-PIT-II-Claudio-Matteo.docx
"""
import json
import struct
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

sys.path.insert(0, str(Path(__file__).parent))
import conteudo as C  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DOCS = RAIZ / "docs"
ROXO = RGBColor(0x3A, 0x02, 0x44)


# ---------------- utilidades ----------------
def novo_doc():
    d = Document()
    s = d.sections[0]
    s.page_width, s.page_height = Cm(21), Cm(29.7)
    s.left_margin = s.top_margin = Cm(3)
    s.right_margin = s.bottom_margin = Cm(2)
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    st.font.size = Pt(12)
    st.paragraph_format.line_spacing = 1.5
    st.paragraph_format.space_after = Pt(6)
    for n, sz in (("Heading 1", 16), ("Heading 2", 14), ("Heading 3", 12)):
        h = d.styles[n]
        h.font.name = "Arial"
        h.element.rPr.rFonts.set(qn("w:ascii"), "Arial")
        h.element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
        h.font.size = Pt(sz)
        h.font.bold = True
        h.font.color.rgb = ROXO
        h.paragraph_format.space_before = Pt(12)
    # rodapé com número de página
    p = s.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    campo(p, "PAGE")
    return d


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
    for i in itens:
        p = d.add_paragraph(style="List Number" if numerada else "List Bullet")
        p.add_run(i)
        p.paragraph_format.space_after = Pt(2)


def sombrear(cel, cor="F3E3FE"):
    tcPr = cel._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), cor)
    tcPr.append(sh)


def tabela(d, cab, linhas, larg=None, tam=10):
    t = d.add_table(rows=1, cols=len(cab))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, c in enumerate(cab):
        cel = t.rows[0].cells[i]
        cel.text = ""
        r = cel.paragraphs[0].add_run(c); r.bold = True; r.font.size = Pt(tam)
        sombrear(cel)
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
        for row in t.rows:
            for i, w in enumerate(larg):
                row.cells[i].width = Cm(w)
    d.add_paragraph().paragraph_format.space_after = Pt(0)
    return t


def png_tam(path):
    b = open(path, "rb").read(24)
    return struct.unpack(">II", b[16:24])


def imagem(d, path, legenda, max_w=16.0, max_h=21.0):
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


def secao(d, paisagem):
    s = d.add_section()
    if paisagem:
        s.orientation = WD_ORIENT.LANDSCAPE
        s.page_width, s.page_height = Cm(29.7), Cm(21)
    else:
        s.orientation = WD_ORIENT.PORTRAIT
        s.page_width, s.page_height = Cm(21), Cm(29.7)
    s.left_margin = s.top_margin = Cm(3 if not paisagem else 2)
    s.right_margin = s.bottom_margin = Cm(2)
    return s


def capa(d, titulo, subtitulo):
    centro(d, C.INSTITUICAO.upper(), 14, True)
    centro(d, f"Curso de {C.CURSO}", 12)
    centro(d, C.DISCIPLINA, 12, depois=120)
    centro(d, C.ALUNO, 14, True)
    centro(d, f"RGM: {C.RGM}", 12, depois=120)
    centro(d, titulo, 20, True)
    centro(d, subtitulo, 13, depois=160)
    centro(d, f"Imperatriz – MA · {C.SEMESTRE}", 12)
    quebra(d)


def sumario(d):
    d.add_heading("Sumário", 1)
    campo(d.add_paragraph(), 'TOC \\o "1-2" \\h \\z \\u')
    quebra(d)


# ---------------- Documentação ----------------
def documentacao():
    d = novo_doc()
    capa(d, "Plataforma Deboa Açaí", "Documentação do projeto: Soluções 1, 2 e 3")
    sumario(d)

    d.add_heading("1. Introdução", 1)
    par(d, "A Deboa Açaí é uma açaiteria de Imperatriz-MA que recebia pedidos apenas pelo WhatsApp, com anotações manuais, "
           "erros de valores, demora no atendimento e nenhum controle de estoque ou faturamento. Este Projeto Integrador "
           "documenta a plataforma própria de pedidos e gestão desenvolvida para a loja, publicada em produção em "
           f"{C.SITE} e em uso com vendas reais desde novembro de 2026.")
    par(d, "Objetivo geral: permitir que o cliente monte o açaí do seu jeito, pague online (Pix ou cartão) e acompanhe o pedido, "
           "enquanto a equipe recebe, prepara, imprime e entrega os pedidos em um painel único, e o proprietário administra "
           "cardápio, estoque, marketing e financeiro.")
    d.add_heading("1.1 Escopo", 2)
    lista(d, ["Loja virtual responsiva e instalável (PWA) para clientes.",
              "Pagamentos online pelo Mercado Pago (Pix e cartão de crédito) com confirmação automática.",
              "Painel operacional em tempo real para a equipe, pedidos de balcão e impressão de comandas Bluetooth.",
              "Painel administrativo: cardápio, opções, estoque com fichas técnicas, financeiro, marketing, clientes, equipe, auditoria e ajuda.",
              "Conformidade com a LGPD: consentimentos, exportação/exclusão de dados e rotina de retenção."])
    d.add_heading("1.2 Tecnologias e arquitetura", 2)
    tabela(d, ["Camada", "Tecnologia"], [
        ("Front-end", "Next.js 16 (React 19, TypeScript), Tailwind CSS 4, PWA"),
        ("Back-end", "Next.js Server Actions e rotas de API (Node.js 22, TypeScript); funções PL/pgSQL no banco"),
        ("Banco de dados", "PostgreSQL (Supabase) com Row Level Security, Realtime e Storage"),
        ("Integrações", "Mercado Pago (pagamentos), Amazon Location Service (endereços e distâncias), Google Identity (login), Web Push"),
        ("Hospedagem", "Netlify (aplicação e funções agendadas) + Supabase (banco e autenticação)"),
        ("Testes", "Vitest + PGlite (unidade e integração com banco real em memória) e Playwright (ponta a ponta)"),
    ], [4, 12])
    par(d, "Observação sobre a linguagem: as orientações sugerem MVC em Java, PHP, C#/.NET ou Python. A plataforma foi construída "
           "em TypeScript (Node.js) por ser a mesma linguagem no front-end e no back-end e pelo suporte nativo do Next.js. "
           "A organização em camadas corresponde ao padrão MVC conforme a tabela abaixo.")
    tabela(d, ["Papel MVC", "Onde está no código"], C.ARQUITETURA_MVC, [4, 12])

    # ---------- Solução 1 ----------
    quebra(d)
    d.add_heading("Solução 1 – Histórias de Usuário", 1)
    par(d, "As histórias foram levantadas com o proprietário da loja e com a operação real dos primeiros dias de vendas. "
           "Atores: Cliente (inclui o visitante não logado), Atendente, Gerente e Proprietário.")
    for h in C.HISTORIAS:
        par(d, f"US{h[0]} – Como {h[1].lower()}, eu quero {h[3]}, para {h[4]}.")
    quebra(d)
    d.add_heading("Solução 1 – Cartões das Histórias", 1)
    for (i, req, tit, quero, para, ca, rn, rnf, pri, pts) in C.HISTORIAS:
        prio = " ".join(f"[{'X' if p == pri else ' '}] {p}" for p in "ABCDE")
        tabela(d, ["Campo", f"US{i} – {tit}"], [
            ("Requerente", req),
            ("Ação", f"Eu quero {quero}."),
            ("Objetivo", f"Para {para}."),
            ("Critérios de aceitação", "\n".join(f"CA#{k + 1} – {x}" for k, x in enumerate(ca))),
            ("Regras de negócio", "\n".join(f"RN#{k + 1} – {x}" for k, x in enumerate(rn))),
            ("Requisitos não funcionais", "\n".join(f"RNF#{k + 1} – {x}" for k, x in enumerate(rnf))),
            ("Prioridade", prio),
            ("Pontos de história", str(pts)),
        ], [4, 12])
    d.add_heading("Solução 1 – Backlog Priorizado", 1)
    ordem = sorted(C.HISTORIAS, key=lambda h: ("ABCDE".index(h[8]), -h[9], h[0]))
    tabela(d, ["#", "ID", "História", "Requerente", "Prioridade", "Pontos"],
           [(k + 1, f"US{h[0]}", h[2], h[1], h[8], h[9]) for k, h in enumerate(ordem)], [1, 1.6, 7.4, 2.6, 1.8, 1.6])
    par(d, f"Total: {sum(h[9] for h in C.HISTORIAS)} pontos de história. Prioridade A = essencial para vender; E = desejável.")
    d.add_heading("Solução 1 – Tarefas", 1)
    par(d, "Tarefas técnicas derivadas de cada história. Todas foram concluídas na versão publicada; os itens marcados como "
           "“correção” surgiram da operação real e foram tratados como novas tarefas.")
    linhas = []
    for h in C.HISTORIAS:
        for t in C.TAREFAS.get(h[0], []):
            linhas.append((f"US{h[0]}", t, "Concluída"))
    tabela(d, ["História", "Tarefa", "Situação"], linhas, [2.2, 11.3, 2.5])

    # ---------- Solução 2 ----------
    quebra(d)
    d.add_heading("Solução 2 – Diagrama de Caso de Uso Geral", 1)
    imagem(d, RAIZ / "diagramas/01-caso-de-uso-geral.png", "Figura 1 – Diagrama de caso de uso geral", 16, 21)
    tabela(d, ["Ator", "Descrição"], [
        ("Visitante", "Pessoa que navega na loja sem estar logada."),
        ("Cliente", "Visitante identificado (conta ou convidado com nome e WhatsApp) que faz pedidos. Especializa Visitante."),
        ("Atendente", "Funcionário que opera o painel de pedidos, balcão, impressão, disponibilidade e estoque."),
        ("Gerente", "Atendente com permissão para abrir/fechar a loja e cancelar/estornar pedidos."),
        ("Proprietário", "Gerente com acesso total: cardápio, preços, marketing, financeiro, equipe e configurações."),
        ("Mercado Pago", "Sistema externo de pagamentos (Pix e cartão) que notifica a plataforma por webhook."),
        ("Agendador", "Funções agendadas (Netlify e pg_cron) que expiram pedidos não pagos e conciliam pagamentos."),
    ], [3.5, 12.5])
    d.add_heading("Solução 2 – Casos de Uso Expandidos", 1)
    for (uid, nome, atores, us, pre, pos, fluxo, alt) in C.CASOS:
        d.add_heading(f"{uid} – {nome}", 3)
        tabela(d, ["Campo", "Descrição"], [
            ("Identificador", uid), ("Atores", atores), ("História relacionada", f"US{us}"),
            ("Pré-condições", pre), ("Pós-condições", pos),
            ("Fluxo principal", "\n".join(f"{k + 1}. {x}" for k, x in enumerate(fluxo))),
            ("Fluxos alternativos", "\n".join(alt) if alt else "—"),
        ], [4, 12])

    secao(d, False)
    d.add_heading("Solução 2 – Diagrama de Classes", 1)
    par(d, "Classes do domínio (nomes em português; no banco as tabelas estão em inglês, por exemplo Pedido = orders). "
           "Valores monetários são inteiros em centavos para evitar erros de arredondamento. ItemPedido e OpcaoDoItem guardam "
           "uma cópia (snapshot) de nomes e preços no momento da compra.")
    imagem(d, RAIZ / "diagramas/03-diagrama-de-classes.png", "Figura 2 – Diagrama de classes", 16, 21.5)

    secao(d, True)
    seqs = [("Cadastro", "04-sequencia-cadastro"), ("Login", "05-sequencia-login"), ("Consulta", "06-sequencia-consulta"),
            ("Carrinho", "07-sequencia-carrinho"), ("Venda", "08-sequencia-venda")]
    for k, (nome, arq) in enumerate(seqs):
        if k:
            quebra(d)
        d.add_heading(f"Solução 2 – Diagrama de Sequência de {nome}", 1)
        imagem(d, RAIZ / f"diagramas/{arq}.png", f"Figura {k + 3} – Sequência de {nome.lower()}", 24.5, 14.2)

    secao(d, False)
    d.add_heading("Solução 2 – Projeto Físico do Banco de Dados", 1)
    par(d, "Banco PostgreSQL (Supabase). Fonte da verdade: migrações SQL versionadas (supabase/migrations do projeto da loja). "
           "Segurança por Row Level Security em todas as tabelas; regras críticas (criar pedido, transições de status, estoque) em "
           "funções no banco. A tabela abaixo é o dicionário de dados das tabelas principais, gerado da migração inicial.")
    dic = json.loads((RAIZ / "ferramentas/tabelas.json").read_text(encoding="utf-8"))
    for nome in ["profiles", "customer_addresses", "consents", "categories", "products", "product_variants", "option_lists",
                 "options", "product_option_groups", "orders", "order_items", "order_item_options", "order_status_history",
                 "payments", "refunds", "coupons", "coupon_redemptions", "campaigns", "banners", "ingredients",
                 "stock_movements", "store_settings", "business_hours", "print_jobs", "audit_log"]:
        if nome in dic:
            d.add_heading(nome, 3)
            tabela(d, ["Coluna", "Tipo", "Restrições"], dic[nome], [5, 4, 7], tam=9)

    # ---------- Solução 3 ----------
    quebra(d)
    d.add_heading("Solução 3 – Wireframes", 1)
    par(d, "Wireframes de baixa fidelidade (tons de cinza) das telas principais. Área do cliente desenhada para celular "
           "(mobile-first) e área da equipe para computador/tablet. Fontes HTML em wireframes/fontes.")
    wfs = sorted((RAIZ / "wireframes").glob("*.png"))
    for k, f in enumerate(wfs):
        titulo = f.stem.split("-", 1)[1].replace("-", " ").capitalize()
        mob = int(f.stem[:2]) <= 10
        imagem(d, f, f"Wireframe {k + 1} – {titulo}", 8.5 if mob else 16, 19)
        if k < len(wfs) - 1:
            quebra(d)

    quebra(d)
    d.add_heading("Solução 3 – Mockups (telas oficiais)", 1)
    par(d, f"Capturas das telas oficiais publicadas em {C.SITE}, com a identidade visual da marca (roxo açaí, verde-limão e "
           "amarelo). Captura automatizada (ferramentas/capturar_mockups.mjs) sem enviar pedidos.")
    mks = sorted((RAIZ / "mockups").glob("*.png"))
    for k, f in enumerate(mks):
        titulo = f.stem.split("-", 1)[1].replace("-", " ").capitalize()
        larga = "computador" in f.stem or "admin" in f.stem or "painel" in f.stem
        imagem(d, f, f"Mockup {k + 1} – {titulo}", 16 if larga else 9, 21)
        if k < len(mks) - 1:
            quebra(d)

    quebra(d)
    d.add_heading("Solução 3 – Mapa Conceitual", 1)
    imagem(d, RAIZ / "diagramas/09-mapa-conceitual.png", "Figura – Mapa conceitual da plataforma", 16, 21)
    secao(d, True)
    d.add_heading("Solução 3 – Mapa Navegacional", 1)
    imagem(d, RAIZ / "diagramas/10-mapa-navegacional.png", "Figura – Mapa navegacional (rotas reais do sistema)", 24.5, 14.5)

    secao(d, False)
    d.add_heading("Referências", 1)
    lista(d, ["MARQUES, A. Projeto Integrador Transdisciplinar em Engenharia de Software II. Universidade Cruzeiro do Sul, 2026.",
              "FOWLER, M. UML Essencial. 3. ed. Porto Alegre: Bookman, 2005.",
              "COHN, M. User Stories Applied: For Agile Software Development. Boston: Addison-Wesley, 2004.",
              "BRASIL. Lei nº 13.709/2018 – Lei Geral de Proteção de Dados Pessoais (LGPD).",
              "NEXT.JS. Documentation. Disponível em: https://nextjs.org/docs.",
              "SUPABASE. Documentation. Disponível em: https://supabase.com/docs.",
              "MERCADO PAGO. Developers – API de Pagamentos. Disponível em: https://www.mercadopago.com.br/developers."])
    out = DOCS / "Documentacao-PIT-II-Claudio-Matteo.docx"
    d.save(out)
    return out


# ---------------- Entrega ----------------
def entrega():
    d = novo_doc()
    capa(d, "Plataforma Deboa Açaí", "Entrega: dados do estudante, repositório, codificação e testes da solução")
    par(d, f"Nome: {C.ALUNO}", "Nome:")
    par(d, f"RGM: {C.RGM}", "RGM:")
    tabela(d, ["Item", "Informação"], [
        ("Linguagem do Back-end", "TypeScript (Node.js 22) – Next.js 16 Server Actions e rotas de API; regras críticas em PL/pgSQL"),
        ("Banco de Dados", "PostgreSQL (Supabase)"),
        ("Hospedagem", "Netlify (aplicação + funções agendadas) e Supabase (banco, autenticação, arquivos)"),
        ("Plataforma", "Web responsiva e instalável (PWA): celular, tablet e computador"),
        ("Modo de Codificação", "(X) Tradicional   ( ) Low-code   ( ) No-code"),
        ("Link do repositório no GitHub", C.REPO),
        ("Link da solução em funcionamento", C.SITE),
        ("Link do vídeo narrado (mínimo 5 min)", C.VIDEO),
    ], [5.5, 10.5])

    d.add_heading("Documentação", 1)
    par(d, f"Link do repositório: {C.REPO}")
    par(d, f"Diretório com os documentos: {C.REPO}/tree/main/docs")
    par(d, "Documentação do PIT II (Soluções 1, 2 e 3): docs/Documentacao-PIT-II-Claudio-Matteo.docx")
    par(d, "Diagramas (PNG e fontes Mermaid/SVG): diagramas/ · Wireframes: wireframes/ · Mockups: mockups/ · Guia de uso: README.md")

    d.add_heading("Codificação", 1)
    par(d, "A solução foi codificada no modo tradicional, em TypeScript, com arquitetura em camadas equivalente ao MVC:")
    tabela(d, ["Papel MVC", "Onde está no código"], C.ARQUITETURA_MVC, [4, 12])
    d.add_heading("Estrutura de diretórios do projeto da loja", 2)
    cod = d.add_paragraph()
    r = cod.add_run("src/\n  app/            páginas (View) e Server Actions (Controller)\n    (loja)/       área do cliente: cardápio, produto, carrinho, checkout, pedido, conta\n"
                    "    painel/       painel de pedidos e balcão\n    admin/        painel do proprietário\n    actions/      Server Actions (controle)\n"
                    "    api/          webhook do Mercado Pago e tarefas agendadas\n  components/     componentes de interface\n"
                    "  domain/         regras de negócio puras + testes (Model)\n  lib/            serviços: Supabase, pagamentos, geocodificação, push, impressão\n"
                    "supabase/migrations/  esquema do banco, funções e políticas RLS (Model)\ne2e/            testes de ponta a ponta (Playwright)")
    r.font.name = "Courier New"; r.font.size = Pt(9)
    cod.paragraph_format.line_spacing = 1.0
    d.add_heading("Exemplo de regra de negócio (Model) – frete por distância", 2)
    ex = d.add_paragraph()
    r = ex.add_run("export function quoteByDistance(distanceKm: number, tiers = DEFAULT_DELIVERY_TIERS): DeliveryQuote {\n"
                   "  const d = roundToMeters(distanceKm);\n  const tier = tiers.find((t) => d <= t.maxKm);\n"
                   "  if (!tier) return { available: false, distanceKm: d, reason: \"out_of_range\" };\n"
                   "  return { available: true, distanceKm: d, feeCents: tier.feeCents };\n}")
    r.font.name = "Courier New"; r.font.size = Pt(9)
    ex.paragraph_format.line_spacing = 1.0
    d.add_heading("Boas práticas aplicadas", 2)
    lista(d, ["Preços, frete e cupons sempre recalculados no servidor/banco (o navegador envia apenas ids e quantidades).",
              "Row Level Security em todas as tabelas e permissões por papel (atendente, gerente, proprietário).",
              "Idempotência em pedidos, pagamentos e movimentos de estoque (clique duplo não duplica).",
              "Webhook do Mercado Pago com assinatura HMAC e conciliação agendada a cada 5 minutos.",
              "Limites de tentativas por origem (pedido, Pix, cartão, cupom) com IP guardado apenas como hash.",
              "Segredos apenas em variáveis de ambiente (nunca no repositório).",
              "LGPD: consentimentos versionados, exportação/exclusão de dados e anonimização automática."])

    d.add_heading("Testes da Solução", 1)
    d.add_heading("Testes automatizados", 2)
    par(d, "Testes de unidade e de integração com Vitest; os testes de banco executam as migrações reais em um PostgreSQL "
           "em memória (PGlite). Execução em 14/11/2026: 170 testes, 170 aprovados.")
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
    ], [4.5, 9.5, 2])
    par(d, "Testes de ponta a ponta (Playwright, Chrome, celular e computador): navegação, cardápio, configurador, carrinho, "
           "checkout até antes do pagamento e teste de carga – 10 cenários, executados nos perfis celular e computador.")

    d.add_heading("Laudo de Qualidade – testes com pares", 2)
    par(d, "Cada colega testa a plataforma em " + C.SITE + " (pode montar o carrinho e ir até o checkout sem pagar) e preenche "
           "uma tabela. Formulário e roteiro: testes/roteiro-de-testes.md.")
    for k in range(1, 6):
        tabela(d, [f"Testador {k} – Nome:", "Data do teste:"], [
            ("O que testou e funcionou:", ""),
            ("O que testou e não funcionou – o que deve ser corrigido:", ""),
            ("Funcionalidade não testada (faltou ou não foi implementada):", ""),
        ], [8, 8])

    d.add_heading("Problemas identificados e correções", 2)
    par(d, "Problemas encontrados na operação real (primeiros dias de vendas) e já corrigidos na versão publicada:")
    tabela(d, ["Problema identificado", "Correção aplicada"], C.PROBLEMAS_CORRIGIDOS, [8, 8])
    d.add_heading("Recomendações", 2)
    lista(d, ["Completar o laudo com os 5 testadores e corrigir o que for apontado.",
              "Exercitar em produção o pagamento com cartão e o estorno real.",
              "Validar notificações e som no aparelho da loja e a impressora Bluetooth.",
              "Agendar backup semanal do banco e migrar para planos pagos quando a demanda crescer."])
    d.add_heading("Evidências", 2)
    par(d, "Link das evidências (imagens e vídeos): (inserir link)")
    d.add_heading("Vídeo da Solução atualizada", 2)
    tabela(d, ["Item", "Link"], [("Link para o vídeo", C.VIDEO)], [5, 11])
    out = DOCS / "Entrega-PIT-II-Claudio-Matteo.docx"
    d.save(out)
    return out


if __name__ == "__main__":
    DOCS.mkdir(exist_ok=True)
    print("ok:", documentacao())
    print("ok:", entrega())
