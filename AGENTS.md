# AGENTS.md — Dollar Factory

Este arquivo é lido automaticamente pelo Antigravity (e por outros agentes) ao abrir o repositório.
Leia nesta ordem antes de qualquer tarefa: `README.md`, `PLAN.md`, `TASKS.md`, `ANALISE_EXTERNA.md`
e `.github/copilot-instructions.md` (regras de código: Python com `pathlib` e `uv`, Next.js 15 + Tailwind v4).

## Decisões em vigor
- **Fonte única do catálogo:** `vitrine/src/data/produtos.json`. A fábrica de vídeos lê este mesmo arquivo. Nunca recriar uma cópia.
- **Dados verificados:** toda ASIN, preço, nota e imagem deve ser conferida na página real da Amazon US antes de entrar no catálogo.
- **Risco de propriedade intelectual:** o personagem e a voz do Rick Sanchez são de terceiros. Não clonar a voz de atores reais para vídeos comerciais. Preferir personagem e voz originais.
- **Imagens da Amazon:** os termos do Associates restringem o uso. Preferir demonstração real filmada ou B-roll livre (Pexels/Pixabay).
- **Não inventar números:** status de vídeo, preços de lista e métricas só entram em documentos se verificados.

## Ambiente
- Windows. Python via `uv run --no-project`, FFmpeg no PATH, Node >= 18.
- A fábrica de vídeo (`fabrica-videos/`) deve rodar sem a vitrine ativa.
- Vídeos `.mp4` e `output/work/` ficam fora do Git (ver `.gitignore`).
- Se houver GPU NVIDIA: usar PyTorch com CUDA para geração de voz. Em máquinas sem GPU, manter o caminho em CPU (`edge-tts`, `faster-whisper` com `int8`).

## Ao concluir uma tarefa
1. Testar o script ou rodar `npm run build` na `vitrine/`.
2. Atualizar `TASKS.md`.
3. Registrar limitações reais (o que não foi testado) em vez de afirmar que funciona.
