"""Gera os wireframes (baixa fidelidade, tons de cinza) das telas da plataforma Deboa Açaí.

Uso: python3 ferramentas/gerar_wireframes.py   (depois: cd ferramentas && npm run renderizar)
Saída: wireframes/fontes/*.html  ->  wireframes/*.png
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
OUT = RAIZ / "wireframes" / "fontes"
OUT.mkdir(parents=True, exist_ok=True)

CSS = """
*{box-sizing:border-box;margin:0}
body{font-family:Arial,Helvetica,sans-serif;background:#fff;padding:24px;color:#333}
.tela{border:3px solid #333;border-radius:28px;background:#fafafa;overflow:hidden;display:inline-block}
.mob{width:390px;min-height:780px}
.desk{width:1280px;min-height:760px;border-radius:10px}
.cap{font:700 15px Arial;padding:10px 16px;background:#333;color:#fff;letter-spacing:.5px}
.top{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-bottom:2px solid #bbb;background:#fff}
.logo{width:96px;height:36px;border:2px solid #666;display:grid;place-items:center;font-size:11px;font-weight:700}
.ic{width:30px;height:30px;border:2px solid #666;border-radius:50%;display:inline-grid;place-items:center;font-size:12px}
.pad{padding:14px 16px}
.img{background:repeating-linear-gradient(45deg,#ddd 0 10px,#eee 10px 20px);border:2px solid #999;display:grid;place-items:center;color:#666;font-size:12px}
.box{border:2px solid #999;border-radius:12px;padding:10px;background:#fff;margin-bottom:10px}
.row{display:flex;gap:10px;align-items:center}
.sp{justify-content:space-between}
.col{display:flex;flex-direction:column;gap:8px}
.t1{font-size:22px;font-weight:700;margin-bottom:8px}
.t2{font-size:16px;font-weight:700;margin-bottom:6px}
.ln{height:10px;background:#ccc;border-radius:5px;margin:5px 0}
.btn{border:2px solid #333;border-radius:999px;padding:10px 14px;text-align:center;font-weight:700;font-size:14px;background:#fff}
.btn.pri{background:#333;color:#fff}
.inp{border:2px solid #999;border-radius:10px;padding:10px;font-size:13px;color:#888;background:#fff}
.lbl{font-size:12px;font-weight:700;margin:6px 0 3px}
.chip{border:2px solid #999;border-radius:999px;padding:5px 10px;font-size:12px;white-space:nowrap}
.chip.on{background:#333;color:#fff;border-color:#333}
.tabs{display:flex;gap:6px;overflow:hidden;padding:10px 16px;border-bottom:2px solid #ddd}
.nota{font-size:11px;color:#777;font-style:italic}
.side{width:230px;background:#e6e6e6;border-right:2px solid #bbb;padding:14px;min-height:720px}
.side .it{padding:9px 10px;border-radius:8px;font-size:13px;margin-bottom:4px}
.side .it.on{background:#333;color:#fff}
.main{flex:1;padding:22px}
table{border-collapse:collapse;width:100%;font-size:13px;background:#fff}
td,th{border:1.5px solid #bbb;padding:8px;text-align:left}
th{background:#eee}
.kpi{flex:1;border:2px solid #999;border-radius:12px;padding:14px;background:#fff}
.kpi b{display:block;font-size:24px;margin-top:6px}
.kan{flex:1;background:#eee;border-radius:10px;padding:8px;min-height:560px}
.qr{width:200px;height:200px;margin:10px auto;background:repeating-conic-gradient(#333 0 25%,#fff 0 50%) 0 0/20px 20px;border:6px solid #fff;outline:2px solid #333}
.foot{margin-top:auto;padding:12px 16px;border-top:2px solid #bbb;background:#fff}
.flex1{flex:1}
"""


def page(nome, titulo, corpo, tipo="mob"):
    html = f"""<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>{titulo}</title><style>{CSS}</style>
<body><div class="tela {tipo}"><div class="cap">WIREFRAME · {titulo}</div>{corpo}</div></body></html>"""
    (OUT / f"{nome}.html").write_text(html, encoding="utf-8")


TOPO = '<div class="top"><div class="ic">☰</div><div class="logo">LOGO DEBOA</div><div class="row"><div class="ic">👤</div><div class="ic">🛒</div></div></div>'


def card(nome="Produto", preco="R$ 00,00", esgot=False):
    return f'''<div class="box row"><div class="img" style="width:84px;height:84px;border-radius:10px">foto</div>
<div class="flex1"><div class="t2">{nome}</div><div class="ln" style="width:90%"></div><div class="ln" style="width:60%"></div>
<div class="row sp"><b>{preco}</b>{'<span class="chip">Esgotado</span>' if esgot else '<span class="btn" style="padding:4px 12px">+</span>'}</div></div></div>'''


def campo(rot, ph):
    return f'<div class="lbl">{rot}</div><div class="inp">{ph}</div>'


def lado(ativo):
    itens = ["Visão geral", "Cardápio", "Acompanhamentos e adicionais", "Pedidos (painel)", "Estoque", "Financeiro",
             "Marketing", "Clientes", "Loja e horários", "Aparência", "Equipe", "Auditoria", "❓ Ajuda"]
    lis = "".join(f'<div class="it{" on" if i == ativo else ""}">{i}</div>' for i in itens)
    return f'<div class="side"><div class="logo" style="margin-bottom:8px">LOGO</div><div class="nota" style="margin-bottom:12px">Nome · Proprietário</div>{lis}</div>'


# ---------- Área do cliente (celular) ----------
page("01-inicio", "Início", TOPO + '''<div class="pad">
<div class="img" style="height:150px;border-radius:16px">Banner da campanha (carrossel)</div>
<div class="row sp" style="margin:12px 0"><span class="chip on">● Aberto agora · fecha 23h</span><span class="nota">Entrega ~40 min</span></div>
<div class="t2">Categorias</div>
<div class="row" style="flex-wrap:wrap;gap:8px;margin-bottom:12px"><span class="chip">Copos</span><span class="chip">Tigelas</span><span class="chip">Barcas</span><span class="chip">Bebidas</span></div>
<div class="t2">Destaques</div>''' + card("Copo 500 ml") + card("Tigela Deboa") + card("Barca") + '''
<div class="btn pri">Ver cardápio completo</div></div>
<div class="foot"><div class="ln" style="width:50%"></div><div class="row"><span class="ic">W</span><span class="ic">I</span><span class="ic">M</span></div><div class="nota">Rodapé: contato, redes, links legais</div></div>''')

page("02-cardapio", "Cardápio", TOPO + '''<div class="tabs"><span class="chip on">Copos</span><span class="chip">Tigelas</span><span class="chip">Barcas</span><span class="chip">Cremes</span><span class="chip">Bebidas</span></div>
<div class="pad"><div class="t1">Copos</div>''' + card("Copo 300 ml", "R$ 00,00") + card("Copo 400 ml") + card("Copo 500 ml") + card("Copo 700 ml", "R$ 00,00", True) + card("Copo 1 litro") + '''
<div class="nota">Abas fixas no topo; itens esgotados aparecem desabilitados.</div></div>''')

page("03-produto", "Produto (configurador)", TOPO + '''<div class="img" style="height:180px">Foto do produto</div><div class="pad">
<div class="t1">Copo de açaí</div><div class="ln"></div><div class="ln" style="width:70%"></div>
<div class="box"><div class="row sp"><b>1. Tamanho</b><span class="chip">obrigatório</span></div>
<div class="row" style="gap:6px;margin-top:8px"><span class="chip">300 ml</span><span class="chip on">500 ml</span><span class="chip">700 ml</span></div></div>
<div class="box"><div class="row sp"><b>2. Acompanhamentos</b><span class="nota">até 4 grátis</span></div>
<div class="col" style="margin-top:6px"><div class="row sp"><span>☑ Leite em pó</span><span>− 1 +</span></div><div class="row sp"><span>☑ Granola</span><span>− 1 +</span></div><div class="row sp"><span>☐ Paçoca</span><span>+ R$ 0,00</span></div></div></div>
<div class="box"><b>3. Cobertura</b><div class="ln" style="width:80%"></div></div>
<div class="box"><b>4. Fruta</b><div class="ln" style="width:60%"></div></div>
<div class="lbl">Observação</div><div class="inp">Ex.: sem açúcar…</div></div>
<div class="foot row sp"><span>− 1 +</span><span class="btn pri flex1">Adicionar · R$ 00,00</span></div>''')

page("04-carrinho", "Carrinho", TOPO + '''<div class="pad"><div class="t1">Seu carrinho</div>
<div class="box"><div class="t2">Deseja adicionar mais alguma coisa?</div><div class="row"><span class="chip">+ Água</span><span class="chip">+ Refrigerante</span><span class="chip">Ver cardápio</span></div></div>
<div class="box"><div class="row sp"><b>Copo 500 ml</b><b>R$ 00,00</b></div><div class="nota">Leite em pó, Granola, Leite condensado, Banana</div><div class="row sp" style="margin-top:6px"><span>− 1 +</span><span class="nota">Editar · Remover</span></div></div>
<div class="box"><div class="row sp"><b>Tigela Deboa</b><b>R$ 00,00</b></div><div class="nota">Opções escolhidas…</div><div class="row sp" style="margin-top:6px"><span>− 2 +</span><span class="nota">Editar · Remover</span></div></div>
<div class="lbl">Cupom de desconto</div><div class="row"><div class="inp flex1">CÓDIGO</div><span class="btn">Aplicar</span></div>
<div class="box" style="margin-top:12px"><div class="row sp"><span>Subtotal</span><span>R$ 00,00</span></div><div class="row sp"><span>Desconto</span><span>− R$ 0,00</span></div><div class="row sp"><b>Total</b><b>R$ 00,00</b></div><div class="nota">Frete calculado no checkout</div></div></div>
<div class="foot"><div class="btn pri">Continuar para o checkout</div></div>''')

page("05-checkout", "Checkout", TOPO + '''<div class="pad"><div class="t1">Finalizar pedido</div>
<div class="row" style="margin-bottom:10px"><span class="btn pri flex1">Entrega</span><span class="btn flex1">Retirar na loja</span></div>
<div class="box"><b>Endereço</b>''' + campo("Rua e número", "Rua…, 123") + campo("Bairro", "Bairro") + campo("Complemento / referência", "Apto, ponto de referência") + '''
<div class="img" style="height:110px;margin-top:8px;border-radius:10px">Mapa: confirme o ponto</div><div class="row sp" style="margin-top:6px"><span class="nota">Distância 2,3 km</span><b>Frete R$ 0,00</b></div></div>
<div class="box"><b>Contato</b>''' + campo("Nome", "Seu nome") + campo("WhatsApp", "(99) 9 9999-9999") + '''</div>
<div class="box"><b>Pagamento</b><div class="row" style="margin-top:6px"><span class="chip on">Pix</span><span class="chip">Cartão de crédito</span></div></div></div>
<div class="foot"><div class="row sp"><b>Total</b><b>R$ 00,00</b></div><div class="btn pri" style="margin-top:8px">Fazer pedido</div></div>''')

page("06-pagamento-pix", "Pagamento Pix", TOPO + '''<div class="pad" style="text-align:center"><div class="t1">Pedido DBA-000000</div>
<div class="nota">Pague com Pix para enviar o pedido à loja</div><div class="qr"></div>
<div class="btn pri">Copiar código Pix (copia e cola)</div>
<div class="inp" style="margin-top:8px;font-size:11px">00020126…código…6304ABCD</div>
<div class="box" style="margin-top:12px"><b>Expira em 29:41</b><div class="ln"></div></div>
<div class="btn">Abrir no app do banco</div>
<div class="nota" style="margin-top:12px">A tela atualiza sozinha quando o pagamento é aprovado.</div></div>''')

page("07-acompanhamento", "Acompanhamento do pedido", TOPO + '''<div class="pad"><div class="t1">Pedido DBA-000000</div><span class="chip on">Em preparação</span>
<div class="box" style="margin-top:12px"><div class="col">
<div>● Pagamento aprovado <span class="nota">19:02</span></div><div>● Pedido aceito <span class="nota">19:04</span></div><div><b>● Em preparação</b> <span class="nota">19:05</span></div><div style="color:#aaa">○ Saiu para entrega</div><div style="color:#aaa">○ Entregue</div></div></div>
<div class="box"><b>Itens</b><div class="ln"></div><div class="ln" style="width:70%"></div><div class="row sp"><b>Total</b><b>R$ 00,00</b></div></div>
<div class="box"><b>Entrega</b><div class="ln" style="width:85%"></div><div class="nota">Previsão: 19:40</div></div>
<div class="btn">Falar com a loja no WhatsApp</div><div class="btn" style="margin-top:8px">Ativar notificações</div>
<div class="nota" style="margin-top:8px">Cancelar pedido (enquanto a loja não aceitou)</div></div>''')

page("08-entrar", "Entrar", TOPO + '''<div class="pad"><div class="t1" style="margin-top:20px">Entrar</div><div class="nota">Para acompanhar pedidos e salvar endereços</div>
<div class="btn" style="margin:18px 0">G  Continuar com o Google</div><div class="row"><div class="ln flex1"></div><span class="nota">ou</span><div class="ln flex1"></div></div>
''' + campo("E-mail", "voce@email.com") + campo("Senha", "••••••••") + '''
<div class="nota" style="text-align:right;margin:6px 0">Esqueci minha senha</div><div class="btn pri">Entrar</div>
<div class="nota" style="text-align:center;margin-top:14px">Não tem conta? <b>Criar conta</b></div></div>''')

page("09-cadastro", "Cadastro", TOPO + '''<div class="pad"><div class="t1" style="margin-top:20px">Criar conta</div>
<div class="btn" style="margin:12px 0">G  Continuar com o Google</div>''' + campo("Nome completo", "Seu nome") + campo("WhatsApp", "(99) 9 9999-9999") + campo("E-mail", "voce@email.com") + campo("Senha", "mínimo 8 caracteres") + '''
<div class="col" style="margin:12px 0;font-size:13px"><span>☐ Li e aceito os Termos e a Política de Privacidade</span><span>☐ Quero receber promoções (opcional)</span></div>
<div class="btn pri">Criar conta</div><div class="nota" style="text-align:center;margin-top:12px">Já tem conta? <b>Entrar</b></div></div>''')

page("10-meus-pedidos", "Minha conta · Meus pedidos", TOPO + '''<div class="tabs"><span class="chip">Perfil</span><span class="chip on">Pedidos</span><span class="chip">Endereços</span><span class="chip">Privacidade</span></div><div class="pad"><div class="t1">Meus pedidos</div>''' + "".join(
    f'<div class="box"><div class="row sp"><b>DBA-00000{i}</b><span class="chip">{s}</span></div><div class="nota">dd/mm/aaaa · 2 itens · R$ 00,00</div><div class="row" style="margin-top:6px"><span class="btn" style="padding:6px 10px">Ver detalhes</span><span class="btn" style="padding:6px 10px">Repetir pedido</span></div></div>'
    for i, s in [(9, "Em preparação"), (8, "Entregue"), (7, "Retirado"), (6, "Cancelado")]) + '</div>')

# ---------- Área da equipe (computador/tablet) ----------
def kanban():
    cols = [("Novos", 2), ("Aceitos", 1), ("Em preparo", 2), ("Prontos", 1), ("Em entrega", 1)]
    out = ""
    for nome, n in cols:
        cards = "".join('<div class="box"><div class="row sp"><b>DBA-000000</b><span class="nota">12 min</span></div><div class="nota">Cliente · Entrega · Pix ✓</div><div class="ln"></div><div class="row" style="margin-top:6px"><span class="btn pri" style="padding:5px 10px;font-size:12px">Avançar</span><span class="btn" style="padding:5px 10px;font-size:12px">🖨</span></div></div>' for _ in range(n))
        out += f'<div class="kan"><div class="t2">{nome} ({n})</div>{cards}</div>'
    return out


page("11-painel-pedidos", "Painel de pedidos (equipe)", '''<div class="top"><div class="logo">LOGO</div><div class="row"><span class="chip on">● Loja aberta</span><span class="btn">+ Pedido de balcão</span><span class="btn">🔔 Som ligado</span><span class="btn">Impressora: conectada</span></div></div>
<div class="pad row" style="align-items:stretch">''' + kanban() + '</div>', "desk")

page("12-pedido-balcao", "Pedido de balcão", '''<div class="top"><div class="logo">LOGO</div><span class="btn">← Voltar ao painel</span></div><div class="pad row" style="align-items:flex-start;gap:20px">
<div class="flex1"><div class="t1">Novo pedido de balcão</div><div class="tabs" style="padding:0 0 10px"><span class="chip on">Copos</span><span class="chip">Tigelas</span><span class="chip">Barcas</span><span class="chip">Bebidas</span></div>
<div class="row" style="flex-wrap:wrap;gap:10px">''' + "".join('<div class="box" style="width:200px"><div class="img" style="height:80px">foto</div><b>Produto</b><div class="nota">R$ 00,00</div></div>' for _ in range(8)) + '''</div></div>
<div style="width:380px"><div class="box"><div class="t2">Comanda</div><div class="row sp"><span>1× Copo 500 ml</span><span>R$ 00,00</span></div><div class="nota">opções…</div><div class="row sp"><span>2× Água</span><span>R$ 00,00</span></div><hr style="margin:8px 0"><div class="row sp"><b>Total</b><b>R$ 00,00</b></div></div>
''' + campo("Nome do cliente (opcional)", "Cliente") + '''<div class="lbl">Pagamento</div><div class="row"><span class="chip on">Dinheiro</span><span class="chip">Pix na maquininha</span><span class="chip">Cartão</span></div>
<div class="btn pri" style="margin-top:12px">Registrar e imprimir comanda</div></div></div>''', "desk")


def admin(nome, titulo, ativo, conteudo):
    page(nome, titulo, f'<div class="row" style="align-items:stretch">{lado(ativo)}<div class="main">{conteudo}</div></div>', "desk")


admin("13-admin-visao-geral", "Admin · Visão geral", "Visão geral", '''<div class="t1">Visão geral</div><div class="row" style="margin-bottom:16px"><span class="chip on">Hoje</span><span class="chip">7 dias</span><span class="chip">30 dias</span></div>
<div class="row" style="margin-bottom:16px"><div class="kpi">Faturamento<b>R$ 0.000,00</b></div><div class="kpi">Pedidos<b>00</b></div><div class="kpi">Ticket médio<b>R$ 00,00</b></div><div class="kpi">Cancelados<b>0</b></div></div>
<div class="row" style="align-items:stretch"><div class="box flex1"><b>Vendas por dia</b><div class="img" style="height:260px;margin-top:8px">gráfico de barras</div></div>
<div class="box" style="width:360px"><b>Mais vendidos</b>''' + "".join('<div class="row sp" style="margin-top:8px"><span>Produto</span><span>00</span></div>' for _ in range(6)) + '''</div></div>
<div class="box"><b>Alertas</b><div class="nota">Estoque abaixo do mínimo · pedidos aguardando há mais de 10 min</div></div>''')

admin("14-admin-cardapio", "Admin · Cardápio", "Cardápio", '''<div class="row sp"><div class="t1">Cardápio</div><span class="btn pri">Salvar alterações</span></div>
<div class="tabs" style="padding:0 0 12px"><span class="chip on">Copos</span><span class="chip">Tigelas</span><span class="chip">Barcas</span><span class="chip">Bebidas</span></div>
<table><tr><th>Foto</th><th>Produto</th><th>Tamanhos e preços</th><th>Grupos de opções</th><th>Disponível</th><th></th></tr>''' + "".join(
    '<tr><td><div class="img" style="width:56px;height:56px">foto</div></td><td><b>Produto</b><div class="nota">descrição…</div></td><td>300 ml R$ 00,00<br>500 ml R$ 00,00</td><td>Acompanhamentos (até 4 grátis)<br>Cobertura · Fruta</td><td>◉ Sim</td><td><span class="btn" style="padding:5px 10px">Editar</span></td></tr>' for _ in range(5)) + '</table>')

admin("15-admin-estoque", "Admin · Estoque", "Estoque", '''<div class="row sp"><div class="t1">Estoque</div><div class="row"><span class="btn">+ Ingrediente</span><span class="btn pri">Registrar entrada</span></div></div>
<table><tr><th>Ingrediente</th><th>Unidade</th><th>Em estoque</th><th>Reservado</th><th>Mínimo</th><th>Situação</th><th></th></tr>''' + "".join(
    f'<tr><td>Ingrediente {i}</td><td>kg</td><td>00,0</td><td>0,0</td><td>00,0</td><td>{"⚠ abaixo do mínimo" if i == 2 else "OK"}</td><td>Ajustar · Ficha técnica</td></tr>' for i in range(1, 8)) + '''</table>
<div class="box" style="margin-top:16px"><b>Últimas movimentações</b><div class="ln"></div><div class="ln" style="width:80%"></div><div class="ln" style="width:60%"></div></div>''')

admin("16-admin-financeiro", "Admin · Financeiro", "Financeiro", '''<div class="row sp"><div class="t1">Financeiro</div><div class="row"><div class="inp">01/11 – 30/11</div><span class="btn">Exportar CSV</span></div></div>
<div class="row" style="margin:12px 0"><div class="kpi">Bruto<b>R$ 0.000,00</b></div><div class="kpi">Taxas Mercado Pago<b>R$ 00,00</b></div><div class="kpi">Líquido<b>R$ 0.000,00</b></div><div class="kpi">Estornos<b>R$ 00,00</b></div><div class="kpi">Fretes<b>R$ 00,00</b></div></div>
<div class="row" style="align-items:stretch"><div class="box flex1"><b>Por forma de pagamento</b><div class="img" style="height:200px;margin-top:8px">gráfico</div></div><div class="box flex1"><b>Por produto</b><div class="img" style="height:200px;margin-top:8px">tabela/ranking</div></div></div>''')

admin("17-admin-marketing", "Admin · Marketing", "Marketing", '''<div class="t1">Marketing</div><div class="row" style="align-items:flex-start">
<div class="box flex1"><div class="t2">Cupons</div><table><tr><th>Código</th><th>Desconto</th><th>Uso</th><th>Ativo</th></tr><tr><td>BEMVINDO</td><td>10%</td><td>00/100</td><td>◉</td></tr><tr><td>FRETEGRATIS</td><td>Frete</td><td>00/∞</td><td>○</td></tr></table>
<div class="t2" style="margin-top:12px">Novo cupom</div>''' + campo("Código", "EX: PROMO10") + campo("Tipo e valor", "Porcentagem · 10") + campo("Validade", "dd/mm – dd/mm") + '''<div class="btn pri" style="margin-top:10px">Criar cupom</div></div>
<div class="box flex1"><div class="t2">Banners da página inicial</div><div class="img" style="height:120px">banner 1</div><div class="img" style="height:120px;margin-top:8px">banner 2</div><div class="btn" style="margin-top:10px">+ Novo banner</div></div></div>''')

admin("18-admin-loja-horarios", "Admin · Loja e horários", "Loja e horários", '''<div class="t1">Loja e horários</div><div class="row" style="align-items:flex-start">
<div class="box flex1"><div class="t2">Status agora</div><div class="row"><span class="btn pri">Aberta</span><span class="btn">Pausar 30 min</span><span class="btn">Fechar hoje</span></div>
<div class="t2" style="margin-top:14px">Horários</div>''' + "".join(f'<div class="row sp" style="margin:6px 0"><span>{d}</span><span class="inp" style="padding:5px 10px">15:00 – 23:00</span></div>' for d in ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]) + '''</div>
<div class="box flex1"><div class="t2">Entrega</div><div class="row sp"><span>Até 1 km</span><b>Grátis</b></div><div class="row sp"><span>1 a 2,5 km</span><b>R$ 7,00</b></div><div class="row sp"><span>2,5 a 6 km</span><b>R$ 10,00</b></div>
''' + campo("Pedido mínimo", "R$ 00,00") + campo("Tempo de preparo", "30 min") + '''<div class="img" style="height:140px;margin-top:10px">Mapa: localização da loja</div></div></div>''')

print("ok:", len(list(OUT.glob("*.html"))), "telas")
