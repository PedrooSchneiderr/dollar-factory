# 🇺🇸 Dollar Factory — US Affiliate & AI Video Automation Engine

<div align="center">

![Next.js 15](https://img.shields.io/badge/Next.js-15.0-black?style=for-the-badge&logo=next.js&logoColor=white)
![Tailwind CSS v4](https://img.shields.io/badge/Tailwind-v4.0-38bdf8?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-6.0+-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)
![Edge TTS](https://img.shields.io/badge/Edge--TTS-Neural_Voice-0078d4?style=for-the-badge&logo=microsoft&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active_Development-success?style=for-the-badge)

<p align="center">
  <strong>Sistema modular e automatizado para vendas em dólar no mercado dos EUA através de Afiliados Amazon US / TikTok Shop, combinando mineração de dados, pipeline de vídeo curto com IA e vitrine própria de alta conversão.</strong>
</p>

[Visão Geral](#-visão-geral) • [Arquitetura](#-arquitetura-do-ecossistema) • [Catálogo #01-#10](#-catálogo-de-produtos-campeões) • [Como Executar](#-como-executar-localmente) • [Roadmap](#-roadmap--próximos-passos)

---

</div>

## 📌 Visão Geral

O **Dollar Factory** foi concebido para resolver o maior gargalo de quem quer faturar em dólar a partir do Brasil: **escalar produção de conteúdo viral para audiência americana sem gastar com anúncios ou equipamentos caros**.

### ✨ Pilares do Projeto
1. **Fator 5x de Conversão:** Recebimento direto em moeda forte via ACH (Wise/Payoneer). Cada comissão de \$15-\$25 rende R$ 75-130 líquidos.
2. **Mineração Baseada em Dados:** Scorecard automatizado que avalia produtos com base em *Movers & Shakers* da Amazon US e tendências de busca do Google US.
3. **Fábrica Autônoma de Vídeos:** Geração de vídeos verticais 9:16 (1080x1920) com narração neural nativa dos EUA, legendas dinâmicas estilo CapCut, badges de urgência e sound design.
4. **Vitrine Própria Otimizada:** Storefront Next.js 15 ultra-rápido com busca instantânea por código `#XX`, player de vídeo embedado e rastreamento de cliques com conformidade FTC.

---

## 🏗️ Arquitetura do Ecossistema

O repositório é 100% desacoplado em 4 módulos independentes:

```
dollar-factory/
├── 🌐 vitrine/                  # Storefront em Next.js 15 + Tailwind CSS v4 (Deploy Vercel)
│   ├── app/                     # App Router (/ e /p/[id] com SSG)
│   ├── components/              # SearchBar, ProductGrid, VideoModal, OutboundButton
│   └── public/videos/           # Vídeos sincronizados da fábrica
│
├── ⛏️ mineracao-produtos/       # Engine de descoberta e validação Amazon US
│   ├── 1_puxar_movers_shakers.py # Scraper de tendências
│   ├── 2_validar_trend.py       # Validação de volume de busca Google US
│   └── 3_scorecard.py           # Matriz de 20 pontos de conversão
│
├── 🎬 fabrica-videos/           # Pipeline de geração de vídeos curtos verticais (1080x1920)
│   ├── config/                  # produtos.json (catálogo) e vozes.json (Edge-TTS)
│   ├── scripts/                 # Roteiro -> Narração -> Clipes -> Legendas -> FFmpeg
│   ├── assets/                  # Overlays (Rick Sanchez), trilhas e efeitos sonoros
│   └── run_pipeline.py          # Orquestrador CLI unificado
│
├── 💼 contas/                   # Guias operacionais para o mercado americano
│   └── guia_operacional_us.md   # Setup ACH Wise, W-8BEN e aquecimento de contas
│
├── 📋 PLAN.md                   # Decisões estratégicas de negócio e regras da Fase 1 vs 2
├── 📋 TASKS.md                  # Quadro Kanban padronizado de tarefas
└── 🤖 .github/copilot-instructions.md # Diretrizes técnicas para desenvolvimento com IA
```

### 🔄 Fluxo de Dados

```mermaid
flowchart TD
    subgraph MINERACAO["⛏️ 1. Mineração de Produtos"]
        A["Amazon Movers & Shakers"] --> B["Google Trends Signals"]
        B --> C["Scorecard de 20 Pontos"]
        C --> D["config/produtos.json"]
    end

    subgraph FABRICA["🎬 2. Fábrica de Vídeos IA"]
        D --> E["1_gerar_roteiro.py\n(Hooks Virais / Rick Sanchez)"]
        E --> F["2_gerar_narracao.py\n(Edge-TTS American Voices)"]
        F --> G["3_baixar_clipes.py\n(Ken Burns / Remix Anti-Copyright)"]
        G --> H["4_transcrever_whisper.py\n(Legendas Dinâmicas .ASS)"]
        H --> I["5_montar_video.py\n(FFmpeg Render 1080x1920)"]
    end

    subgraph VITRINE["🌐 3. Vitrine & Conversão"]
        I --> J["vitrine/public/videos/"]
        D --> K["Vitrine Next.js 15\n(busca por #Código)"]
        J --> K
        K --> L["Amazon US Associates\n(Comissão em Dólar)"]
    end
```

---

## 🏆 Catálogo de Produtos Campeões (Aprovados)

Estes 10 produtos passaram pelo funil de 20 pontos de impulso e apelo visual.

> [!NOTE]
> **Catálogo reconstruído (20/10/2026):** o catálogo anterior tinha ASINs inexistentes ou que apontavam para outros produtos, e imagens genéricas do Unsplash. Agora cada item abaixo foi **conferido na página real da Amazon US** (ASIN, título, preço, nota, reviews e imagens). Preços e reviews mudam, então reconfira antes de postar.
>
> Pendências antes de publicar: pedir aprovação no Amazon Associates e revisar o uso das imagens da Amazon pelos termos do programa.

| Código | Produto | Nicho | Preço US$ | Avaliações | Status do Vídeo |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **`#01`** | **Electric Spin Scrubber** (B0B7RSV894) | Home & Cleaning | \$35.99 | 13.6k (4.3⭐) | ⏳ A gerar |
| **`#02`** | **ChomChom Pet Hair Roller** (B00BAGTNAQ) | Pet Must-Haves | \$24.99 | 206k (4.5⭐) | ⚠️ Piloto antigo, regerar |
| **`#03`** | **Fullstar Veggie Chopper** (B0764HS4SL) | Kitchen Hacks | \$24.99 | 122k (4.5⭐) | ⏳ A gerar |
| **`#04`** | **Mini Chip Bag Sealer** (B0C2TD5SKJ) | Kitchen Hacks | \$9.99 | 3.8k (3.8⭐) | ⏳ A gerar |
| **`#05`** | **Touchless Soap Dispenser** (B078XDFDPY) | Home & Cleaning | \$27.99 | 39k (4.3⭐) | ⏳ A gerar |
| **`#06`** | **Car Vent Cleaning Gel** (B081T7N948) | Car & Everyday | \$7.99 | 101k (4.1⭐) | ⏳ A gerar |
| **`#07`** | **Dog Bath Shampoo Brush** (B01FE3IIC4) | Pet Must-Haves | \$11.99 | 25k (4.5⭐) | ⏳ A gerar |
| **`#08`** | **Cordless Car Vacuum** (B07KG2X2GZ) | Car & Everyday | \$24.99 | 49k (4.3⭐) | ⏳ A gerar |
| **`#09`** | **Sweater Fuzz Remover** (B008I25368) | Home & Cleaning | \$8.99 | 95k (4.4⭐) | ⏳ A gerar |
| **`#10`** | **Dog Lick Mat** (B0BBTS457S) | Pet Must-Haves | \$7.99 | 3.8k (4.4⭐) | ⏳ A gerar |

---

## 🚀 Como Executar Localmente

### Pré-requisitos
- **Node.js** >= 18.x
- **Python** >= 3.10
- **uv** (Gerenciador ultrarrápido para Python): `winget install astral-sh.uv`
- **FFmpeg**: Configurado nas variáveis de ambiente (`PATH`)

---

### 1. Subir a Vitrine Next.js

```bash
cd vitrine
npm install
npm run dev
```
Acesse em: `http://localhost:3000` (ou porta informada no terminal).

**Destaques da Vitrine:**
- 🔍 Busca instantânea por `#Código` (ex.: `#01`, `#02`).
- 📱 Design 100% Mobile-First voltado para tráfego do TikTok e Instagram Reels.
- ⚡ Renderização estática instantânea (`generateStaticParams`).
- 🛡️ Conformidade total com regras da FTC e Amazon Associates.

---

### 2. Executar a Mineração de Novos Produtos

```bash
cd mineracao-produtos

# 1. Puxa itens em ascensão da Amazon US
uv run --no-project python 1_puxar_movers_shakers.py

# 2. Cruza com sinais de busca do Google US
uv run --no-project python 2_validar_trend.py

# 3. Aplica o scorecard e gera produtos_aprovados.csv
uv run --no-project python 3_scorecard.py
```

---

### 3. Gerar Vídeos com IA (Fábrica de Vídeos)

Para renderizar um vídeo completo (vertical 1080x1920 com legendas `.ass`, áudio neural e badges):

```bash
cd fabrica-videos

# Gera para o Produto #01 (versão v1):
uv run --no-project --with edge-tts python run_pipeline.py --id 01 --version v1

# Gera para o Produto #02:
uv run --no-project --with edge-tts python run_pipeline.py --id 02 --version v1
```

O vídeo final é gravado em `fabrica-videos/output/` e automaticamente copiado para `vitrine/public/videos/`.

---

## 🎯 Próximos Passos (Sprint Atual)

- [ ] **Fábrica Pro 2.0 (Persona Rick Sanchez):** Roteiros sarcásticos e irreverentes, voz rápida estilizada e sticker/overlay animado (`assets/rick/rick_portal.png`).
- [ ] **Sound Design:** Remoção de silêncios mortos (`silenceremove`), transições *whoosh* e efeito *ding* no preço.
- [ ] **Lote Completo de Vídeos:** Renderização dos produtos `#03` ao `#10`.
- [ ] **Deploy Vercel:** Publicação da vitrine com domínio próprio.

---

## ⚖️ Conformidade Legal & FTC

> **Aviso de Afiliado (FTC Disclosure):**
> *As an Amazon Associate, we earn from qualifying purchases at no additional cost to the buyer. All prices, ratings, and stock availability are accurate at the time of scraping and are subject to change on Amazon.com.*

---

<div align="center">
  <sub>Dollar Factory Engine • Desenvolvido para operações de escala internacional.</sub>
</div>
