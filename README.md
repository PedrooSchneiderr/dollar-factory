# 🇺🇸 Dollar Factory — US E-Commerce & Affiliate Automation Engine

> Sistema modular e automatizado para operar vendas em dólar no mercado dos Estados Unidos através de Afiliados Amazon US / TikTok Shop, impulsionado por mineração de dados e geração de vídeos virais curtos com Inteligência Artificial.

---

## 📌 Visão Geral da Arquitetura

O projeto é estruturado em **4 módulos independentes**, permitindo que você ou agentes de IA trabalhem e evoluam cada componente sem acoplamento:

```
dollar-factory/
├── vitrine/                  # Storefront em Next.js 15 + Tailwind CSS (Deploy Vercel)
│                             # Alternativa: Beacons.ai / Stan Store / Amazon Storefront
├── mineracao-produtos/       # Engine de descoberta e scorecard de produtos virais Amazon US
├── fabrica-videos/           # Pipeline de automação de vídeo curto (Python + TTS + FFmpeg + Whisper)
│   ├── config/               # Catálogo de produtos (produtos.json) e vozes neurais (vozes.json)
│   ├── scripts/              # Etapas 1 a 5 (Roteiro -> Narração -> Clipes -> Legendas -> Montagem)
│   ├── assets/               # Mídia, avatares de personagens e trilhas
│   └── run_pipeline.py       # Orquestrador CLI de geração de vídeos
├── contas/                   # Guias operacionais (Wise ACH, W-8BEN, aquecimento TikTok/Reels)
├── PLAN.md                   # Plano mestre de arquitetura, estratégia e regras de negócio
├── TASKS.md                  # Quadro de tarefas padronizado (Kanban/Sprint backlog para IA)
└── .github/                  # Instruções para Coding Assistants (Claude Code, Cursor, Copilot)
```

---

## 🚀 Como Executar Localmente

### Pré-requisitos
- **Node.js** >= 18.x
- **Python** >= 3.10
- **uv** (Package manager rápido para Python): `winget install astral-sh.uv`
- **FFmpeg**: Disponível no PATH do sistema

---

### 1. Subir a Vitrine (Storefront Local)

```bash
cd vitrine
npm install
npm run dev
# Acesse: http://localhost:3005 (ou a porta informada no terminal)
```

**Principais Recursos da Vitrine:**
- Busca instantânea por `#Código` do vídeo (ex.: `#01`, `#02`).
- Filtro por nichos americanos (*Kitchen Hacks*, *Pet Must-Haves*, *Cleaning*, etc.).
- Página individual de cada produto (`/p/[id]`) com player de vídeo 9:16 embedado.
- Botão com redirecionamento para a Amazon US e rastreamento de cliques (Meta Pixel, TikTok Pixel e `/api/click`).
- Aviso legal obrigatório da FTC e Amazon Associates no rodapé.

---

### 2. Rodar a Mineração de Produtos

```bash
cd mineracao-produtos

# 1. Coleta produtos em alta no Amazon US Movers & Shakers
uv run --no-project python 1_puxar_movers_shakers.py

# 2. Valida volume de busca no Google US (Search Autocomplete signals)
uv run --no-project python 2_validar_trend.py

# 3. Aplica scorecard de 20 pontos e aprova os campeões
uv run --no-project python 3_scorecard.py
```

---

### 3. Gerar Vídeos Curtos com IA (Fábrica de Vídeos)

Para gerar um vídeo completo de 30 segundos (vertical 1080x1920, com narração nativa dos EUA, legendas dinâmicas estilo CapCut, badges e gancho viral):

```bash
cd fabrica-videos

# Gera o vídeo para o Produto #01 (versão de roteiro 1):
uv run --no-project --with edge-tts python run_pipeline.py --id 01 --version v1

# Gera para o Produto #02:
uv run --no-project --with edge-tts python run_pipeline.py --id 02 --version v1
```

O vídeo final `.mp4` é exportado em `fabrica-videos/output/` e automaticamente copiado para `vitrine/public/videos/`.

---

## 👥 Como Contribuir (Padrão para Devs & Agentes de IA)

Consulte:
- [PLAN.md](./PLAN.md): Para entender as decisões de negócio, canais de distribuição e monetização.
- [TASKS.md](./TASKS.md): Para pegar a próxima tarefa pendente ou atualizar status.
- [.github/copilot-instructions.md](./.github/copilot-instructions.md): Regras de codificação e prompts recomendados.
