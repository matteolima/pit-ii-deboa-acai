# Deboa Açaí: Plataforma de Pedidos e Gestão (PIT II)

Projeto Integrador Transdisciplinar em Engenharia de Software II, Universidade Cruzeiro do Sul, 2026-2.
**Estudante:** Cláudio Matteo Assunção Lima (RGM 35320451)

**Solução em funcionamento:** https://deboaacai.com.br

A Deboa Açaí é uma açaiteria de Imperatriz-MA. Antes, todos os pedidos chegavam pelo WhatsApp e eram anotados à mão. A plataforma substitui esse processo:

- o cliente monta o açaí do seu jeito, paga com Pix ou cartão e acompanha o pedido pelo celular;
- a equipe recebe, prepara, imprime e entrega os pedidos em um painel único;
- o proprietário administra o cardápio, o estoque, o marketing e o financeiro.

O sistema está em produção, com vendas reais, desde novembro de 2026.

## Entregáveis

| Entregável | Arquivo |
|---|---|
| Documentação do projeto (Soluções 1, 2 e 3) | [docs/Documentacao-PIT-II-Claudio-Matteo.docx](docs/Documentacao-PIT-II-Claudio-Matteo.docx) |
| Entrega (dados do estudante, repositório, codificação e testes) | [docs/Entrega-PIT-II-Claudio-Matteo.docx](docs/Entrega-PIT-II-Claudio-Matteo.docx) |
| Diagramas UML (casos de uso, classes, sequências) e mapas | [diagramas/](diagramas/) |
| Wireframes (baixa fidelidade) | [wireframes/](wireframes/) |
| Mockups (telas oficiais do site) | [mockups/](mockups/) |
| Roteiro e formulário dos testes com pares | [testes/roteiro-de-testes.md](testes/roteiro-de-testes.md) |

### Conteúdo da documentação

- **Solução 1:**
  - 24 histórias de usuário com critérios de aceitação, regras de negócio e requisitos não funcionais;
  - backlog priorizado;
  - tarefas.
- **Solução 2:**
  - diagrama de caso de uso geral;
  - 16 casos de uso expandidos;
  - diagrama de classes;
  - diagramas de sequência de cadastro, login, consulta, carrinho e venda;
  - projeto físico e dicionário de dados.
- **Solução 3:**
  - 18 wireframes;
  - mockups das telas oficiais;
  - mapa conceitual;
  - mapa navegacional.

## Estrutura do repositório

```
docs/            documentos .docx do PIT
diagramas/       imagens PNG dos diagramas e dos mapas
  fontes/        fontes editáveis (Mermaid .mmd e SVG)
wireframes/      wireframes PNG
  fontes/        wireframes em HTML
mockups/         capturas das telas oficiais (deboaacai.com.br)
testes/          roteiro e formulário dos testes com pares
ferramentas/     scripts que geram as imagens e os documentos
```

## Tecnologias da plataforma

| Camada | Tecnologia |
|---|---|
| Front-end | Next.js 16, React 19, TypeScript, Tailwind CSS 4, PWA instalável |
| Back-end | Next.js Server Actions e rotas de API (Node.js 22), funções PL/pgSQL |
| Banco de dados | PostgreSQL (Supabase) com Row Level Security, Realtime e Storage |
| Pagamentos | Mercado Pago (Pix e cartão), webhook com assinatura e conciliação automática |
| Mapas e frete | Amazon Location Service (endereço → coordenadas → distância → faixa de frete) |
| Hospedagem | Netlify (aplicação e funções agendadas) e Supabase |
| Testes | Vitest + PGlite (170 testes de unidade e integração) e Playwright (ponta a ponta) |

A arquitetura é organizada em camadas, no padrão MVC:

- **Model:** regras de negócio em `src/domain` e no banco de dados;
- **View:** páginas e componentes React;
- **Controller:** Server Actions e rotas de API.

A tabela completa está na documentação.

---

## Guia de uso

### Para o cliente (site)

1. **Abrir a loja:** acesse https://deboaacai.com.br.
   - No topo, o selo mostra se a loja está **Aberta** ou **Fechada**.
   - O horário atual é todos os dias, das 15h às 22h.
2. **Escolher o produto:** toque em **Cardápio**, escolha a categoria e o produto.
3. **Montar o açaí:**
   - escolha o tamanho, os acompanhamentos (alguns são grátis, os demais somam ao valor), a cobertura e a fruta;
   - escreva uma observação, se quiser;
   - toque em **Adicionar**.
4. **Carrinho:**
   - você é levado ao carrinho, onde pode adicionar mais itens, mudar quantidades ou remover;
   - para usar um cupom, digite o código e toque em **Aplicar**. Um cupom inválido é removido automaticamente.
5. **Finalizar:** toque em **Continuar** e escolha:
   - **Entrega:** informe o endereço e confirme o ponto no mapa. O frete é calculado pela distância.
   - **Retirar na loja:** não precisa informar endereço.
6. **Seus dados:** entre na conta (Google ou e-mail) ou continue como convidado, informando nome e WhatsApp.
7. **Pagamento:**
   - **Pix:** escaneie o QR Code ou toque em **Copiar código**. O código vale por 30 minutos.
   - **Cartão de crédito:** preencha o formulário seguro do Mercado Pago.
8. **Acompanhar:**
   - depois da aprovação, a tela mostra o status: aceito, em preparo, pronto, saiu para entrega, entregue;
   - ative as notificações para ser avisado;
   - use o botão do WhatsApp para falar com a loja.
9. **Cancelar:** é possível cancelar enquanto a loja ainda não aceitou o pedido. O valor pago é estornado automaticamente.
10. **Minha conta:**
    - **Meus pedidos** mostra o histórico, com a opção **Repetir pedido**;
    - também há endereços salvos e privacidade (exportar ou excluir dados, conforme a LGPD).

**Instalar como aplicativo:**

- **Android:** no Chrome, toque em ⋮ e depois em **Instalar app**.
- **iPhone:** no Safari, toque em Compartilhar e depois em **Adicionar à Tela de Início**.
- **Windows:** no Edge, use o ícone **Instalar** na barra de endereço.

### Para a equipe (painel de pedidos)

1. Entre com seu login e toque em **Painel**. No celular, o botão fica no topo.
2. Toque na faixa para **ativar o som** de novos pedidos e em **Ativar notificações**. Isso só é necessário na primeira vez em cada aparelho.
3. Se usar a impressora térmica Bluetooth, toque em **Conectar impressora**.
4. Pedidos pagos chegam na coluna **Novos**, com alerta sonoro. Para cada pedido:
   - toque em **Aceitar**: a comanda é impressa;
   - avance o pedido por **Em preparo**, **Pronto**, **Saiu para entrega** (ou retirado) e **Entregue**.
5. Para **pedidos feitos pessoalmente ou por telefone**, toque em **+ Pedido de balcão**:
   - escolha os itens e a forma de pagamento;
   - toque em **Registrar**.
6. Quando algo acabar, marque o item como **esgotado** em Admin → Cardápio. Ele some da venda na hora.
7. Registre as entradas de mercadoria em **Admin → Estoque**.

**Gerente:** além do que a equipe faz, pode **pausar, fechar ou abrir** a loja em Admin → Loja e horários e **cancelar ou estornar** pedidos.

### Para o proprietário (painel administrativo `/admin`)

| Área | Para que serve |
|---|---|
| Visão geral | Faturamento, pedidos e ticket médio do período |
| Cardápio / Acompanhamentos e adicionais | Produtos, tamanhos, preços, fotos e regras de cada grupo de opções |
| Estoque | Ingredientes, saldo, mínimo, fichas técnicas e movimentações |
| Financeiro | Vendas por período, por produto e por forma de pagamento, taxas, estornos e exportação CSV |
| Marketing | Cupons, campanhas e banners da página inicial |
| Clientes | Base de clientes, respeitando o consentimento de marketing |
| Loja e horários | Horários, pausas, faixas de frete, pedido mínimo e tempo de preparo |
| Aparência | Logotipo e cores da marca |
| Equipe | Convidar funcionários e definir papéis (atendente, gerente, proprietário) |
| Auditoria | Registro de quem alterou o quê |
| Ajuda | Perguntas frequentes sobre o uso do sistema, por papel |

---

## Como regenerar os artefatos

Requisitos:

- Node.js 22 e Google Chrome instalados (para renderizar as imagens);
- Python 3 com `python-docx==1.1.2` (para gerar os documentos).

```bash
cd ferramentas
npm install
python3 gerar_caso_de_uso.py      # diagrama de caso de uso (SVG)
python3 gerar_wireframes.py       # wireframes (HTML)
npm run renderizar                # Mermaid/SVG/HTML -> PNG
node capturar_mockups.mjs         # mockups do site publicado (somente leitura)
python3 gerar_documentos.py       # docs/*.docx
```

## Segurança

Este repositório contém apenas documentação e artefatos do PIT. Ele **não** contém:

- chaves;
- senhas;
- dados de clientes;
- variáveis de ambiente da loja.
