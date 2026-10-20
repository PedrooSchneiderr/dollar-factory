# Prompt para o Antigravity do PC com GPU

Cole o texto abaixo (bloco de código) no Antigravity do PC com a placa de vídeo, depois de clonar o repositório.

## Antes de colar (você, no PowerShell do outro PC)

```powershell
winget install Git.Git
winget install GitHub.cli
gh auth login
git clone https://github.com/PedrooSchneiderr/dollar-factory.git C:\Arquivos\dollar-factory
```

Depois abra a pasta `C:\Arquivos\dollar-factory` no Antigravity e cole o prompt.

## Prompt

```text
Você vai continuar o projeto "Dollar Factory" neste PC, que tem uma GPU NVIDIA forte.
O repositório já está clonado nesta pasta. Siga as etapas em ordem e me mostre a saída de cada comando antes de seguir.

ETAPA 1 - Contexto
Leia, nesta ordem: AGENTS.md, README.md, PLAN.md, TASKS.md, ANALISE_EXTERNA.md e .github/copilot-instructions.md.
Resuma em 10 linhas o que o projeto é e quais são as decisões em vigor. Não invente nada.

ETAPA 2 - Verificar o ambiente
Rode e me mostre a saída:
  nvidia-smi
  python --version
  uv --version
  ffmpeg -version
  node --version
Se faltar algo, instale com winget (astral-sh.uv, Gyan.FFmpeg, OpenJS.NodeJS.LTS) e rode de novo.
Me diga o modelo da GPU e a VRAM.

ETAPA 3 - Dependências
  cd vitrine && npm install && npm run build
Reporte qualquer erro. Não altere código sem me avisar.

ETAPA 4 - Testar a fábrica de vídeo atual
  cd fabrica-videos
  uv run --no-project --with edge-tts python run_pipeline.py --id 02 --version v1
Confirme se existe o arquivo em fabrica-videos\output\ e informe a duração do vídeo com ffprobe.

ETAPA 5 - Preparar a voz com GPU
Com base na VRAM encontrada, proponha UMA opção entre F5-TTS, Chatterbox e RVC para uma voz de PERSONAGEM ORIGINAL
(um cientista maluco e cínico).
REGRAS: não clone a voz de atores reais nem de personagens protegidos (Rick Sanchez) para vídeos comerciais.
Use como referência apenas áudio que seja meu ou licenciado.
Mostre o plano de instalação (PyTorch com CUDA, versões) e espere minha aprovação antes de instalar.

ETAPA 6 - Melhorar o vídeo (só depois de eu aprovar)
  - Cenas de 1,5 a 2 segundos, fundo desfocado com o produto centralizado.
  - Legendas palavra por palavra com faster-whisper (substituir scripts/4_transcrever_whisper.py).
  - Personagem com boca reativa ao áudio.
  - Sons sintetizados com FFmpeg (whoosh e ding no preço) e música de fundo baixa.
  - Roteiros de 20 a 25 segundos com gancho de problema nos primeiros 3 segundos.
Implemente um item por vez, teste, e só então marque em TASKS.md.

REGRAS GERAIS
  - O catálogo único é vitrine/src/data/produtos.json. Não crie cópias.
  - Não declare que algo funciona sem ter rodado. Registre o que não foi testado.
  - Faça commit e push só quando eu pedir.
```

## Depois de gerar algo no outro PC

Vídeos e áudios não vão para o Git (estão no `.gitignore`). Mande por Drive ou pendrive.
Código e documentação: `git add -A`, `git commit` e `git push`, e neste PC `git pull`.
