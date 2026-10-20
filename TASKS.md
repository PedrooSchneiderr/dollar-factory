# 📋 TASKS.md — Quadro de Tarefas & Backlog (AI-Driven)

> Padrão de rastreamento de tarefas para desenvolvimento solo ou colaborativo com agentes de IA (Claude Code, Cursor, Copilot, Antigravity).

---

## 🟢 Concluídas (Done)

- [x] **Setup do Projeto e Isolamento:**
  - Criação da pasta raiz `dollar-factory/` isolada de outros apps em `C:\Arquivos\PAPO-DE-MUDANCA\`.
  - Configuração do `.gitignore` protegendo dependências, caches e vídeos renderizados.
- [x] **Módulo de Mineração de Produtos (`mineracao-produtos/`):**
  - Implementação de `1_puxar_movers_shakers.py` (coleta Amazon US Movers & Shakers).
  - Implementação de `2_validar_trend.py` (validação de volume de busca Google US).
  - Implementação de `3_scorecard.py` (scorecard de 20 pontos de impulso e apelo visual).
  - Catálogo inicial com 10 produtos campeões aprovados em `produtos.json` e `produtos_aprovados.csv`.
- [x] **Fábrica Local de Vídeos com IA (`fabrica-videos/`):**
  - Implementação dos 5 scripts modulares da esteira (roteiro, narração neural, clipes, legendas `.ass`, montagem FFmpeg).
  - Implementação do orquestrador CLI `run_pipeline.py`.
  - Mapeamento de vozes neurais americanas (`vozes.json`).
  - Geração bem-sucedida dos primeiros vídeos piloto em vertical 1080x1920:
    - `output/2026-10-19_produto_01_v1.mp4` (*Electric Spin Scrubber*)
    - `output/2026-10-19_produto_02_v1.mp4` (*Reusable Pet Hair Roller*)
- [x] **Vitrine Storefront Next.js (`vitrine/`):**
  - Estrutura completa em Next.js 15 + Tailwind CSS v4.
  - Barra de busca instantânea por código do vídeo (`#01` a `#10`).
  - Filtro interativo por nichos (*Kitchen*, *Pets*, *Home*, *Car*).
  - Páginas individuais de produto (`/p/[id]`) com player de vídeo vertical 9:16 embedado.
  - Botão de saída com tracking de cliques (`OutboundButton.tsx` + `/api/click`).
  - Rodapé obrigatório de conformidade FTC & Amazon Associates.
  - Build de produção (`next build`) testado e validado sem erros (15/15 páginas estáticas geradas).
- [x] **Documentação & Guias Operacionais:**
  - Guia em `contas/guia_operacional_us.md` para abertura de conta ACH (Wise/Payoneer), formulário fiscal W-8BEN e aquecimento de contas US.

---

## 🟡 Em Andamento (In Progress)

- [ ] **Evolução do Módulo de Vídeo ("Pro 2.0" com Personagens):**
  - Integração da persona e voz do **Rick Sanchez** para roteiros irreverentes no formato *Character Review*.
  - Adição do avatar recortado (`assets/rick/rick_portal.png`) sobreposto no canto da tela com animação de pulso.
  - Sound design: corte de pausas mortas (`silenceremove`), efeitos de transição (*whoosh*) e som de caixa registradora (*ding*).

---

## 🔵 Próximas Tarefas (Backlog Priorizado)

### Sprint 1: Qualidade e Conversão de Vídeo
- [ ] **Módulo de Download de Vídeos Reais da Amazon US:**
  - Criar script automatizado para baixar o vídeo `.mp4` oficial da galeria do produto da Amazon US (via Playwright / headless) e salvar em `assets/clipes_brutos/produto_XX/`.
- [ ] **Geração do Lote de Vídeos #03 ao #10:**
  - Gerar as versões v1 e v2 para os 8 produtos restantes do catálogo.
- [ ] **Soundtrack Library:**
  - Adicionar 3 a 5 trilhas royalty-free em `assets/musica/` (estilo lo-fi beat / upbeat TikTok) para mixagem automática a 12% de volume.

### Sprint 2: Vitrine & Distribuição
- [ ] **Deploy da Vitrine na Vercel (ou configuração no Beacons.ai):**
  - Conectar repositório na Vercel ou preencher vitrine no Beacons.ai para colocar a URL na bio.
- [ ] **Criação e Aquecimento das Contas:**
  - Criar perfil no TikTok, Instagram e YouTube Shorts com as diretrizes do `guia_operacional_us.md`.
  - Iniciar protocolo de aquecimento de 3 dias.

### Sprint 3: Otimização de Comissões & Escala
- [ ] **Cadastro no Amazon Associates US:**
  - Submeter aplicação com a URL pública da vitrine após publicação dos primeiros vídeos.
- [ ] **Substituição da Tag de Afiliado:**
  - Atualizar `cleverusfinds-20` pela tag real nos arquivos `produtos.json`.
- [ ] **Monitoramento de Cliques (Gatilho de 30 cliques/dia):**
  - Analisar logs de `/api/click` para selecionar os produtos candidatos à Fase 2 (loja própria dropshipping com armazém US).
