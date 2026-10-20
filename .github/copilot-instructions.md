# 🤖 Diretrizes para Desenvolvimento com IA — Dollar Factory

Este arquivo orienta qualquer assistente ou agente de IA (Claude Code, Cursor, Copilot, ChatGPT, Antigravity) que esteja trabalhando neste repositório.

---

## 🏗️ Filosofia do Projeto
- **Zero Guru Fluff:** Não construímos sistemas falsos ou mágicos. Todo script deve executar uma função clara e verificável (mineração de dados, processamento de áudio/vídeo, rendering web).
- **Execução Leve e Local:** O pipeline de vídeo roda no Windows usando Python + `uv` + `ffmpeg`. Evite dependências pesadas de deep learning com compilação C++ complexa que não rodem com agilidade em GPUs integradas.
- **Isolamento de Módulos:**
  - `vitrine/`: Storefront Next.js (TypeScript, Tailwind). Não deve depender de scripts Python.
  - `fabrica-videos/`: Engine CLI em Python. Não deve quebrar se a vitrine não estiver rodando.
  - `mineracao-produtos/`: Scripts analíticos que produzem CSVs e alimentam o `produtos.json`.

---

## 📜 Convenções de Código

### Python (`fabrica-videos/` & `mineracao-produtos/`)
- Gerencie execução via `uv run --no-project ...` ou ambientes virtuais declarados.
- Use `pathlib.Path` para todos os caminhos de arquivos (compatibilidade multiplataforma Windows/POSIX).
- Scripts numerados sequencialmente (`1_...py`, `2_...py`) com responsabilidade única.
- Sempre imprima logs amigáveis com status no terminal (`[1/5 Roteiro]...`, `[OK]...`).

### TypeScript / Next.js (`vitrine/`)
- Next.js 15 App Router com Tailwind CSS v4.
- Mantenha `generateStaticParams()` em `/p/[id]` para renderização estática e performance máxima.
- Todo redirecionamento para a Amazon deve usar o componente `OutboundButton.tsx` para assegurar o disparo dos pixels de conversão.
- Mantenha sempre o rodapé de conformidade da FTC e Amazon Associates.

---

## 📌 Checklist ao Concluir uma Tarefa
1. Teste o script ou rode `npm run build` na `vitrine/` para garantir que não há erros de tipagem.
2. Atualize o arquivo [TASKS.md](../TASKS.md) marcando a tarefa concluída `[x]`.
3. Garanta que arquivos temporários de renderização (`.tmp`, `.mp4` brutos de trabalho) fiquem em `output/work/` para serem ignorados pelo `.gitignore`.
