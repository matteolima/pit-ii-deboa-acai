"""Gera o diagrama de caso de uso geral (UML) da plataforma Deboa Açaí em SVG.

Uso: python3 ferramentas/gerar_caso_de_uso.py
Saída: diagramas/fontes/01-caso-de-uso-geral.svg (renderizado para PNG por ferramentas/renderizar.mjs)
"""
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "diagramas" / "fontes" / "01-caso-de-uso-geral.svg"

ROXO, ROXO_ESCURO, UVA, LIMA = "#000000", "#000000", "#000000", "#000000"
W, H = 1560, 1560

# Casos de uso: (id, texto, coluna, linha)
CASOS = [
    ("UC01", "Consultar cardápio", 0, 0),
    ("UC02", "Personalizar produto", 0, 1),
    ("UC03", "Gerenciar carrinho", 0, 2),
    ("UC04", "Aplicar cupom", 0, 3),
    ("UC05", "Criar conta", 0, 4),
    ("UC06", "Fazer login", 0, 5),
    ("UC07", "Finalizar pedido (checkout)", 0, 6),
    ("UC09", "Acompanhar pedido", 0, 7),
    ("UC10", "Consultar histórico / repetir", 0, 8),
    ("UC11", "Cancelar pedido", 0, 9),
    ("UC12", "Gerenciar perfil e privacidade", 0, 10),
    ("UC08", "Pagar com Pix ou cartão", 0, 11),
    ("UC25", "Confirmar pagamento (webhook)", 0, 12),
    ("UC13", "Gerenciar fila de pedidos", 1, 0),
    ("UC14", "Registrar pedido de balcão", 1, 1),
    ("UC15", "Imprimir comanda", 1, 2),
    ("UC16", "Marcar item esgotado", 1, 3),
    ("UC17", "Movimentar estoque", 1, 4),
    ("UC18", "Abrir / fechar loja", 1, 5),
    ("UC19", "Cancelar e estornar pedido", 1, 6),
    ("UC20", "Gerenciar cardápio e preços", 1, 7),
    ("UC21", "Gerenciar marketing e cupons", 1, 8),
    ("UC22", "Consultar financeiro", 1, 9),
    ("UC23", "Gerenciar equipe e papéis", 1, 10),
    ("UC24", "Configurar loja e aparência", 1, 11),
    ("UC26", "Expirar e conciliar pagamentos", 1, 12),
]

COL_X = [540, 960]
TOP, PASSO = 190, 92
RX, RY = 160, 32


def pos(cid):
    for i, _t, c, l in CASOS:
        if i == cid:
            return COL_X[c], TOP + l * PASSO
    raise KeyError(cid)


ATORES = {
    "Visitante": (120, 360),
    "Cliente": (120, 950),
    "Mercado Pago": (120, 1380),
    "Atendente": (1440, 330),
    "Gerente": (1440, 730),
    "Proprietário": (1440, 1130),
    "Agendador": (1440, 1440),
}

ASSOCIACOES = {
    "Visitante": ["UC01", "UC02", "UC03", "UC04", "UC05", "UC06"],
    "Cliente": ["UC07", "UC08", "UC09", "UC10", "UC11", "UC12"],
    "Atendente": ["UC13", "UC14", "UC15", "UC16", "UC17"],
    "Gerente": ["UC18", "UC19"],
    "Proprietário": ["UC20", "UC21", "UC22", "UC23", "UC24"],
    "Mercado Pago": ["UC08", "UC25"],
    "Agendador": ["UC26"],
}

INCLUDES = [("UC07", "UC08", "«include»"), ("UC04", "UC03", "«extend»"), ("UC13", "UC15", "«include»")]
GENERALIZACOES = [("Cliente", "Visitante"), ("Gerente", "Atendente"), ("Proprietário", "Gerente")]


def ator(nome, x, y):
    return f"""
  <g stroke="{ROXO}" stroke-width="3" fill="none">
    <circle cx="{x}" cy="{y - 48}" r="16" fill="#fff"/>
    <line x1="{x}" y1="{y - 32}" x2="{x}" y2="{y + 8}"/>
    <line x1="{x - 24}" y1="{y - 18}" x2="{x + 24}" y2="{y - 18}"/>
    <line x1="{x}" y1="{y + 8}" x2="{x - 20}" y2="{y + 38}"/>
    <line x1="{x}" y1="{y + 8}" x2="{x + 20}" y2="{y + 38}"/>
  </g>
  <text x="{x}" y="{y + 62}" text-anchor="middle" class="ator">{escape(nome)}</text>"""


def borda_elipse(cx, cy, tx, ty):
    """Ponto na borda da elipse em direção a (tx, ty)."""
    import math
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    t = 1 / math.sqrt((dx / RX) ** 2 + (dy / RY) ** 2)
    return cx + dx * t, cy + dy * t


partes = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Rubik, Arial, sans-serif">',
    """<defs>
    <marker id="seta" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10" fill="none" stroke="#000000" stroke-width="1.5"/></marker>
    <marker id="heranca" viewBox="0 0 12 12" refX="12" refY="6" markerWidth="14" markerHeight="14" orient="auto-start-reverse"><path d="M0,0 L12,6 L0,12 Z" fill="#fff" stroke="#000000" stroke-width="1.5"/></marker>
  </defs>
  <style>
    .uc { font-size: 17px; fill: #000000; }
    .id { font-size: 12px; fill: #000000; font-weight: 700; }
    .ator { font-size: 19px; font-weight: 700; fill: #000000; }
    .rot { font-size: 13px; fill: #000000; font-style: italic; }
  </style>""",
    f'<rect width="{W}" height="{H}" fill="#fff"/>',
    f'<text x="{W / 2}" y="48" text-anchor="middle" font-size="30" font-weight="700" fill="{ROXO}">Diagrama de Caso de Uso Geral — Plataforma Deboa Açaí</text>',
    f'<rect x="320" y="90" width="900" height="{TOP + 12 * PASSO + 60 - 90}" rx="24" fill="#ffffff" stroke="{ROXO}" stroke-width="3"/>',
    f'<text x="350" y="122" font-size="20" font-weight="700" fill="{ROXO}">Sistema: deboaacai.com.br</text>',
]

# Associações (atrás das elipses)
for nome, casos in ASSOCIACOES.items():
    ax, ay = ATORES[nome]
    for c in casos:
        cx, cy = pos(c)
        ex, ey = borda_elipse(cx, cy, ax, ay - 10)
        partes.append(f'<line x1="{ax}" y1="{ay - 10}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{ROXO}" stroke-width="1.6" opacity="0.75"/>')

# Generalizações entre atores
for filho, pai in GENERALIZACOES:
    fx, fy = ATORES[filho]
    px, py = ATORES[pai]
    y1, y2 = (fy - 70, py + 72) if fy > py else (fy + 72, py - 70)
    partes.append(f'<line x1="{fx}" y1="{y1}" x2="{px}" y2="{y2}" stroke="{ROXO}" stroke-width="2" marker-end="url(#heranca)"/>')

# Casos de uso
for cid, texto, _c, _l in CASOS:
    x, y = pos(cid)
    externo = cid in ("UC25", "UC26")
    partes.append(f'<ellipse cx="{x}" cy="{y}" rx="{RX}" ry="{RY}" fill="{"#e6e6e6" if externo else "#fff"}" stroke="{ROXO}" stroke-width="2.2"/>')
    partes.append(f'<text x="{x}" y="{y - 6}" text-anchor="middle" class="id">{cid}</text>')
    partes.append(f'<text x="{x}" y="{y + 15}" text-anchor="middle" class="uc">{escape(texto)}</text>')

# include / extend (linhas tracejadas)
for a, b, rot in INCLUDES:
    ax, ay = pos(a)
    bx, by = pos(b)
    x1, y1 = borda_elipse(ax, ay, bx, by)
    x2, y2 = borda_elipse(bx, by, ax, ay)
    off = 60 + abs(ay - by) * 0.12
    partes.append(f'<path d="M{x1 + 40:.1f},{y1:.1f} C{ax + RX + off},{ay} {bx + RX + off},{by} {x2 + 40:.1f},{y2:.1f}" fill="none" stroke="{UVA}" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#seta)"/>')
    partes.append(f'<text x="{max(ax, bx) + RX + 30}" y="{(ay + by) / 2 + 5}" class="rot">{rot}</text>')

for nome, (x, y) in ATORES.items():
    partes.append(ator(nome, x, y))

partes.append(f'<text x="40" y="{H - 24}" font-size="14" fill="{ROXO}">Casos em cinza são disparados por atores externos: Mercado Pago (gateway de pagamento) e Agendador (funções agendadas Netlify / pg_cron). Setas de ponta branca = generalização. O estorno (UC19) também é enviado ao Mercado Pago.</text>')
partes.append("</svg>")

SAIDA.parent.mkdir(parents=True, exist_ok=True)
SAIDA.write_text("\n".join(partes), encoding="utf-8")
print(f"ok: {SAIDA}")
