# Guia Operacional — Contas EUA, Recebimento em Dólar (ACH) e Aquecimento de Algoritmo

Este documento contém o passo a passo operacional não-código para ligar a distribuição da sua estrutura `dollar-factory`.

---

## 1. Recebimento em Dólar do Brasil (Sem precisar de LLC na Fase 1)

O programa **Amazon Associates US (`affiliate-program.amazon.com`)** paga comissões em dólar via **Direct Deposit (ACH)** em conta bancária americana. Para receber do Brasil como Pessoa Física sem abrir empresa nos EUA:

1. **Abra uma conta na Wise (Conta Multimoeda) ou Payoneer:**
   - Na **Wise**: ative o saldo em **USD (Dólar Americano)** e clique em *"Obter dados de conta"* (Account Details). Você receberá um **Routing Number (ABA)** de 9 dígitos e um **Account Number** americano (geralmente via Community Federal Savings Bank ou Column N.A.).
   - Na **Payoneer**: acesse *Receive -> Global Payment Service -> USD* para pegar o seu **Routing Number** e **Account Number** (Checking).
2. **Configure no Amazon Associates US:**
   - Em *Account Settings -> Change Payment Method*, selecione **Pay me by direct deposit**, escolha **United States** como localização do banco e insira o nome do banco, Routing Number e Account Number da sua Wise/Payoneer.
   - No questionário fiscal (**Tax Information Interview**), preencha como **Individual / Non-US Person (Formulário W-8BEN)**: informe seu CPF no campo de Foreign TIN e marque que 0% dos serviços são executados fisicamente dentro dos EUA (isenção de retenção na fonte para comissões de afiliado estrangeiro).

---

## 2. Cadastro no Amazon Associates US (Sem reprovação)

1. **Faça o deploy da Vitrine (`dollar-factory/vitrine`) na Vercel ANTES de se cadastrar:**
   - A Amazon exige uma URL pública real listada em *Website and Mobile App List*.
   - A nossa vitrine já possui o aviso obrigatório da FTC no rodapé (*"As an Amazon Associate I earn from qualifying purchases."*).
2. **Troque a tag de afiliado no catálogo:**
   - Assim que criar a conta e receber sua Store ID (ex.: `seuusuario-20`), substitua `cleverusfinds-20` pela sua tag real no arquivo `fabrica-videos/config/produtos.json` e `vitrine/src/data/produtos.json`.

---

## 3. Configuração das Contas (TikTok, Instagram Reels e YouTube Shorts) para Público 100% EUA

Para que o algoritmo entregue seus vídeos para compradores nos Estados Unidos (e não para brasileiros):

1. **Aparelho / Ambiente Limpo:**
   - Se for postar pelo celular: use um aparelho secundário sem chip brasileiro inserido (ou com um **eSIM americano** barato como Tello US — US$ 5/mês — ou Airalo US) + idioma do sistema em **English (United States)** + região **United States** + VPN/Proxy Residencial US fixa (mesma cidade sempre, ex.: Miami ou New York).
   - Se for postar pelo PC: use um navegador anti-detect (ex.: AdsPower ou Dolphin Anty no plano grátis para até 2-10 perfis) com **Proxy Residencial Estático dos EUA** (custa ~US$ 3–5/mês por IP).
2. **Criação dos 3 Perfis da Marca:**
   - Nome sugerido: **CleverUS Finds** (`@cleverusfinds` ou similar).
   - Bio em inglês:
     > 🇺🇸 Viral Problem-Solving Gadgets That Actually Work
     > 👇 Type the #Code from our videos in the search bar below:
     > 🔗 [link-da-sua-vitrine.vercel.app]
3. **Protocolo de Aquecimento (Dias 1 a 3 antes do 1º post):**
   - Durante 15 minutos por dia, pesquise no TikTok/Reels termos em inglês: `#amazonfinds`, `#tiktokmademebuyit`, `#kitchenhacks`, `#cleaningtiktok`.
   - Assista vídeos em inglês até o final, curta, salve nos favoritos e siga 15–20 grandes criadores americanos de Amazon Finds.
   - **Jamais** pesquise perfis brasileiros ou interaja com conteúdo em português nessa conta.

---

## 4. Rotina Diária de Produção (15 Minutos/Dia)

1. **Gerar novos vídeos na Fábrica Local (`fabrica-videos/`):**
   ```powershell
   cd C:\Arquivos\PAPO-DE-MUDANCA\dollar-factory\fabrica-videos
   uv run --no-project --with edge-tts python run_pipeline.py --id 01 --version v1
   uv run --no-project --with edge-tts python run_pipeline.py --id 01 --version v2
   uv run --no-project --with edge-tts python run_pipeline.py --id 02 --version v1
   ```
   *(Dica de Ouro: quando quiser usar vídeos reais do produto em ação, basta salvar de 2 a 4 clipes `.mp4` dentro de `fabrica-videos/assets/clipes_brutos/produto_01/` — o script `3_baixar_clipes.py` detecta automaticamente e aplica o corte e remix anti-copyright!)*

2. **Melhores Horários para Postar (Horário de Brasília -> Foco Costa Leste EUA):**
   - **Manhã:** 09:00 às 10:30 BRT
   - **Noite (Pico Principal nos EUA):** 20:00 às 22:30 BRT
