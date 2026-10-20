# Análise Externa — Dollar Factory

> Análise crítica e sincera encomendada a um consultor externo (IA), com leitura direta do código e documentação do repositório em 2026-10-20.

## Veredito geral

**Nota: 3/10 para "virar renda real nos próximos meses do jeito que está"; 6/10 para "projeto de aprendizado/portfólio técnico".** A execução técnica (pipeline de vídeo, vitrine) é sólida para um projeto solo. O problema é a tese de negócio: baixíssima margem (afiliado Amazon = 1-10%, não 3-10% "limpo" como o PLAN.md sugere) combinada com riscos de conta (IP, ToS de plataforma, Associates) que podem zerar tudo de uma vez, mais um catálogo que, no estado atual, está **tecnicamente quebrado em produção**.

---

## Top 5 riscos, em ordem de gravidade

| # | Risco | Fato ou opinião | Mitigação |
|---|---|---|---|
| 1 | **Vitrine serve catálogo quebrado** — `vitrine/src/data/produtos.json` ainda tem ASINs antigos/fake (ex. `B0C1V5Z9X2` para o #01), `amazon_url` apontando para busca genérica (`amazon.com/s?k=...`) em vez do produto, e `image_url`/`gallery_urls` são fotos do **Unsplash**, não da Amazon. O catálogo corrigido existe só em `fabrica-videos/config/produtos.json`. | **Fato verificado no código**, não opinião. | Antes de qualquer coisa: copiar o `produtos.json` corrigido para `vitrine/src/data/produtos.json` e rodar `npm run build` de novo. Depois, unificar os dois arquivos (symlink ou script de sync) para nunca mais divergir. |
| 2 | **Persona Rick Sanchez** — uso de personagem protegido por copyright (Adult Swim/WBD) em conteúdo comercial monetizado. | Fato: é PI de terceiros. Opinião/risco: strike de copyright no TikTok é real e documentado publicamente (Content ID / denúncias de direitos autorais), mas não tenho certeza da probabilidade exata de detecção para uma voz genérica + avatar recortado — plataformas de vídeo curto são mais sensíveis a áudio/vídeo-fonte do que a nome falado. Ainda assim, isso NÃO protege de reclamação manual do detentor dos direitos. | Trocar por persona genérica própria (sem nome de personagem real) antes de publicar em escala. É o risco mais fácil de eliminar — e o PLAN.md já lista Walter White/Saul Goodman/Peter Griffin como alternativas, **todos também PI de terceiros**, mesmo problema. |
| 3 | **Imagens da Amazon usadas fora da Product Advertising API** — `3_baixar_clipes.py` baixa `image_url`/`gallery_urls` (hotlinked de `m.media-amazon.com`) e grava dentro do vídeo monetizado; a vitrine também usa `<img src={item.image_url}>` direto. O Amazon Associates Operating Agreement restringe uso de "Amazon Content" a ferramentas aprovadas (PA-API, SiteStripe, widgets oficiais). | Não tenho certeza absoluta da redação atual (2026) do Operating Agreement, mas essa restrição é historicamente estável e bem documentada. Trate como risco real, não como opinião infundada. | Usar a Product Advertising API (precisa de conta Associates aprovada + vendas qualificadas, que é catch-22) ou fotografar/filmar o produto fisicamente. |
| 4 | **"Aquecimento" com VPN/proxy residencial + eSIM para simular localização US** (`guia_operacional_us.md`, seção 3). | Fato: isso é manipulação deliberada de sinal de localização para enganar o algoritmo de distribuição. TikTok e Meta proíbem uso de VPN/proxy para burlar geolocalização e engajamento falso em seus termos de uso; não tenho certeza do texto exato de 2026, mas a prática é conhecida como causa comum de shadowban/banimento em nichos de "finance/affiliate". | Comprar um device físico americano + SIM real, ou simplesmente postar normal e deixar o algoritmo distribuir organicamente por idioma/conteúdo (funciona pior no começo, mas sem risco de banimento). |
| 5 | **Conta nova de afiliado + TikTok com zero histórico tentando vender produto de margem 1-4%** — matemática do negócio não fecha com volume pequeno (ver abaixo). | Opinião fundamentada em como funciona o programa Amazon Associates (comissões por categoria variam de 1% a ~10%, a maioria das categorias "gadget" fica em 3-4%). | Ver seção de estratégia abaixo — repensar oferta antes de escalar produção de vídeo. |

Risco adicional real mas menor: **`/api/click/route.ts` grava em arquivo local (`fs.appendFileSync`) — isso não funciona na Vercel** (filesystem é somente leitura em produção serverless, exceto `/tmp` efêmero). O gatilho de "30 cliques/dia" do TASKS.md para decidir migração de fase nunca vai ter dado nenhum se vocês deployarem assim.

---

## Matemática do negócio

**Premissas que eu assumi** (fato: o repositório não documenta nenhuma taxa de conversão esperada em lugar nenhum):
- Comissão Amazon por categoria "Home/Kitchen/Pet/Automotive": **3-4%** (não o "fator 5x" vago do PLAN.md — isso é conversão cambial, não margem de afiliado, e o PLAN.md mistura os dois conceitos).
- Preço médio do catálogo: ~$20.

| Cenário | Views/vídeo | CTR p/ bio | Cliques/vídeo | Conv. link→compra | Vendas/vídeo | Comissão/venda | Receita/vídeo |
|---|---|---|---|---|---|---|---|
| Pessimista | 300 | 0,5% | 1,5 | 1% | 0,015 | $0,70 | $0,01 |
| Realista | 3.000 | 1% | 30 | 2% | 0,6 | $0,70 | $0,42 |
| Otimista | 30.000 | 2% | 600 | 3% | 18 | $0,70 | $12,60 |

Isso é **por vídeo, taxa única**, não mensal. A conta de afiliado tem fricção extra grave que o PLAN.md ignora: o cliente precisa sair do app, abrir o navegador/Amazon app, buscar `#01` na vitrine (fricção adicional que o fluxo "link in bio" já tem sozinho), e ainda confiar no site. Taxas reais de cliques de link-in-bio para compra costumam ficar **bem abaixo de 1%** em contas novas sem prova social.

**Primeira venda**: com 3 vídeos/semana no cenário realista, ~1-3 semanas. **Primeiro R$1.000** (~$180 em comissões, a ~$0,70/venda = ~260 vendas): no cenário realista isso exige **centenas de vídeos virais** — ou seja, meses, e só se pelo menos alguns vídeos realmente viralizarem (views na casa de 100k+), porque a margem por venda é baixa demais para volume linear sustentar.

**Conclusão da matemática**: o modelo só "fecha" se um vídeo viralizar de verdade (100k-1M views). Produção de volume sem viralização não compensa o tempo investido, dado 1-4% de comissão.

---

## Estratégia: é o formato certo?

**Opinião, não fato**: não. Para quem está começando do zero, afiliado Amazon com comissão de 1-4% é historicamente um dos piores pontos de entrada para monetização via TikTok — o próprio mercado migrou para **TikTok Shop** (comissões maiores, configuráveis, checkout nativo sem sair do app) justamente porque o modelo "link in bio para Amazon" tem fricção alta e paga pouco. Vocês já cogitam TikTok Shop no PLAN.md mas não implementaram.

- **Vitrine própria**: não vale o esforço nessa fase. Vocês gastaram tempo de engenharia considerável (Next.js, API routes, SSG) para resolver um problema que a própria **Opção C do PLAN.md (Beacons.ai/Stan Store, "10 minutos")** resolve de graça, sem bug de produção, sem manutenção de dois arquivos JSON desincronizados. A vitrine só se justifica depois que o pixel de conversão e volume de tráfego comprovarem que o controle de dados vale o custo de manutenção — ou seja, Fase 2, não Fase 1.
- **Caminho com mais chance**: TikTok Shop com produtos de comissão mais alta (muitas vezes 10-20%, configurada pelo seller), ou nicho com afiliado de infoproduto/SaaS (comissão 20-50%) em vez de físico de baixo ticket.

---

## Qualidade do conteúdo

- Voz genérica (`en-US-GuyNeural`) sem imitar Rick **não entrega a promessa visual do roteiro** ("I'm Rick Sanchez") — gera dissonância entre o que a legenda/hook promete e o que a narração entrega, o que no algoritmo de retenção de TikTok tende a aumentar abandono nos primeiros segundos, exatamente o sinal que mais pesa para distribuição.
- Vídeos com foto estática + zoom/pan (Ken Burns) **competem contra criadores que filmam demonstração real com as próprias mãos** — isso é o fator que mais separa "amazon finds" virais dos que não performam. Pesquisa de produto escrita (pain_point, benefits) está genuinamente bem feita; a entrega visual é o elo fraco.
- Isso é opinião baseada em como o algoritmo do TikTok pondera retenção nos primeiros 1-3s, não um fato mensurável sem testar.

---

## Revisão técnica — bugs e dívida técnica concretos

| Arquivo:linha | Problema |
|---|---|
| `vitrine/src/data/produtos.json` (todo o arquivo) | **Bug crítico**: catálogo desatualizado/quebrado ainda em uso pela vitrine ao vivo (ver risco #1). |
| `vitrine/src/app/api/click/route.ts:8-9` | `fs.appendFileSync` não funciona em produção na Vercel (serverless, FS somente leitura). O "gatilho de 30 cliques/dia" do TASKS.md nunca vai disparar assim. |
| `fabrica-videos/scripts/4_transcrever_whisper.py` (todo arquivo) | O nome promete Whisper (transcrição real por IA), mas o script **não transcreve nada** — ele fatia o texto do roteiro já conhecido em blocos de 3 palavras e distribui o tempo proporcionalmente à contagem de palavras. Isso não bate com a cadência real da fala (sílabas/palavra variam, e o `silenceremove` do passo 2 já alterou o timing do áudio sem avisar o passo 4). Legenda vai dessincronizar visivelmente em frases irregulares. |
| `mineracao-produtos/1_puxar_movers_shakers.py:50-51` | Scraping de HTML da Amazon via regex (`p13n-sc-truncate`) é extremamente frágil — qualquer mudança de markup ou bloqueio por CAPTCHA (que o próprio script já prevê como path comum) faz cair no fallback, que é só o catálogo manual. Ou seja: **a "mineração automatizada" na prática não mina nada novo** — é decoração sobre um catálogo editado à mão. |
| `mineracao-produtos/3_scorecard.py:19-50` | O scorecard de "20 pontos" é hardcoded e tautológico: a lista de `wow_keywords` foi escrita pensando nos produtos que já estavam no catálogo, então qualquer produto novo tende a pontuar baixo por não usar essas palavras-chave específicas. Não é um filtro de qualidade de verdade. |
| `mineracao-produtos/produtos_aprovados.csv` | É a saída do pipeline de mineração, e contém o catálogo **antigo** (ASINs/URLs de busca, não os corrigidos). Está órfão em relação ao catálogo real atual — confunde quem olhar o repo achando que esse CSV é a fonte de verdade. |
| `fabrica-videos/scripts/3_baixar_clipes.py:35` | `next(p for p in products if p["id"] == product_id)` sem fallback — se o ID não existir, lança `StopIteration` sem mensagem clara (diferente do script 1, que trata o caso com erro legível). |
| Duplicação de catálogo (`fabrica-videos/config/produtos.json` vs `vitrine/src/data/produtos.json`) | Dívida estrutural: dois arquivos JSON como fonte de verdade do mesmo dado, sem script de sincronização. Causa raiz do bug #1 acima e vai se repetir toda vez que o catálogo for atualizado. |

**O que eu simplificaria**: eliminar a duplicação de `produtos.json` (um só arquivo, a vitrine importa via symlink ou a fábrica de vídeo lê do mesmo caminho); remover a etapa "4_transcrever_whisper" ou trocar por um Whisper real (`faster-whisper` local, leve o suficiente para rodar na GPU integrada) já que o nome promete isso; simplificar o scorecard de mineração para um checklist manual — ele não está automatizando nada que falta automatizar.

---

## Plano de 30 dias (prioridades)

**Semana 1**: corrigir o bug do catálogo da vitrine (sync com `fabrica-videos/config/produtos.json`), trocar persona Rick por persona genérica autoral, rodar `npm run build` e deploy real na Vercel.

**Semana 2**: aplicar para Amazon Associates (precisa de 1+ vídeo postado e vitrine pública), criar conta TikTok com device/SIM real (não VPN), começar aquecimento orgânico sem spoofing de localização.

**Semana 3**: postar 1 vídeo/dia sem Rick, testar 2-3 produtos diferentes do catálogo, medir CTR real (não estimado) via o pixel/click tracking consertado.

**Semana 4**: avaliar: se nenhum vídeo passou de ~5k views, o problema é formato de conteúdo, não produto — pausar produção em massa e revisar o gancho visual (demonstração real, não zoom em foto).

**O que NÃO fazer**: gerar 80 vídeos (8 produtos × v1/v2) antes de validar que 1 formato funciona; manter o Rick Sanchez; usar VPN/proxy para fingir localização US; deployar a vitrine sem corrigir o catálogo.

---

## O que eu faria no seu lugar

Pausaria a fábrica de vídeo por 3-4 dias, corrigiria o bug do catálogo, trocaria para uma persona própria sem risco de IP, e postaria manualmente (celular, sem automação, sem VPN) 5-10 vídeos testando ganchos diferentes nos primeiros 3 segundos com o mesmo produto (#02, que já tem 206k reviews — prova social forte). Só escalaria produção depois de achar 1 formato que passe de ~10k views orgânicos. Isso evita gastar semanas de engenharia renderizando vídeos para um formato que ainda não foi validado com audiência real.

---

## O que eu precisaria saber para ser mais preciso

- Texto atual (2026) do Amazon Associates Operating Agreement sobre uso de imagens/vídeos de produto.
- Política atual do TikTok sobre VPN/geolocalização para monetização de criador.
- Elegibilidade real de afiliado brasileiro no TikTok Shop US (muda com frequência).
- Taxas de comissão reais por categoria no Associates hoje (variam e o programa já mudou tabelas várias vezes).

Não tenho certeza suficiente sobre esses quatro pontos para afirmar como fato — tratei como risco plausível com base em como esses programas funcionaram historicamente, não como regra confirmada para a data de hoje.
