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
- [x] **Evolução da Fábrica de Vídeos ("Pro 2.0" Rick Sanchez):**
  - Integração da persona **Rick Sanchez** (`1_gerar_roteiro.py`) com 3 variações de roteiro sarcástico/viral ridicularizando tarefas primitivas da Terra.
  - Calibração de voz neural ágil com pitch/rate customizados em `vozes.json` e corte automático de silêncio (`silenceremove` em `2_gerar_narracao.py`).
  - Legendas no estilo **Neon Portal Green** em `4_transcrever_whisper.py` (`#39FF14`).
  - Overlay animado do avatar recortado (`assets/rick/rick_portal.png`) flutuando no canto da tela no `5_montar_video.py`.
  - Orquestrador atualizado com suporte a `--persona rick` em `run_pipeline.py`.
- [x] **Vitrine Storefront Next.js (`vitrine/`):**
  - Estrutura completa em Next.js 15 + Tailwind CSS v4.
  - Barra de busca instantânea por código do vídeo (`#01` a `#10`).
  - Filtro interativo por nichos (*Kitchen*, *Pets*, *Home*, *Car*).
  - Páginas individuais de produto (`/p/[id]`) com player de vídeo vertical 9:16 embedado.
  - Botão de saída com tracking de cliques (`OutboundButton.tsx` + `/api/click`).
  - Rodapé obrigatório de conformidade FTC & Amazon Associates.
  - Build de produção (`next build`) testado e validado sem erros (15/15 páginas estáticas geradas).
- [x] **Versionamento & GitHub:**
  - Repositório publicado em `https://github.com/PedrooSchneiderr/dollar-factory`.
  - README.md profissional com badges, diagrama de arquitetura e tabela de produtos campeões.
- [x] **Auditoria e Reconstrução do Catálogo (20/10/2026):**
  - Conferidas as ASINs do catálogo antigo direto na Amazon US: só o `#02` era válido (5 retornavam 404 e 4 apontavam para outros produtos).
  - `fabrica-videos/config/produtos.json` reescrito com 10 produtos reais (ASIN, título, preço, nota, reviews e imagens da própria Amazon).
  - Limitações: `old_price` foi igualado a `price` (não verifiquei preço de lista); os vídeos antigos `#01` e `#02` usavam dados desatualizados.
- [x] **Correções pós-análise externa (`ANALISE_EXTERNA.md`):**
  - `vitrine/src/data/produtos.json` sincronizado com o catálogo verificado (antes ainda tinha ASINs falsas e fotos do Unsplash).
  - `next.config.mjs` liberou `m.media-amazon.com` para as imagens.
  - `/api/click` agora só grava arquivo fora da Vercel e usa `console.log` em produção.
  - Fonte única do catálogo: `fabrica-videos/scripts/1_gerar_roteiro.py` e `3_baixar_clipes.py` agora leem `vitrine/src/data/produtos.json`. O arquivo `fabrica-videos/config/produtos.json` ficou obsoleto e deve ser removido com `git rm`.
  - Pendente: rodar `npm run build`; corrigir `4_transcrever_whisper.py` (não transcreve de verdade).
- [x] **Documentação & Guias Operacionais:**
  - Guia em `contas/guia_operacional_us.md` para abertura de conta ACH (Wise/Payoneer), formulário fiscal W-8BEN e aquecimento de contas US.

---

## 🟡 Em Andamento (In Progress)

- [ ] **Geração do Lote de Vídeos Pro 2.0 (Produtos #01 ao #10 com Persona Rick Sanchez):**
  - Executar a esteira Pro 2.0 para gerar as versões v1 e v2 para todos os produtos aprovados.

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
