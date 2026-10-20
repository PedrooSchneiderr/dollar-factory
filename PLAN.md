# 📋 PLAN.md — Plano Estratégico & Regras de Negócio

> Documento mestre de arquitetura de negócio, infraestrutura técnica e tomada de decisão para a operação **Dollar Factory**.

---

## 1. Tese do Negócio (Vender para os EUA a partir do Brasil)

### Por que Estados Unidos?
1. **Moeda Forte (Fator 5x):** Cada comissão de US$ 10 a US$ 25 equivale a R$ 50 a R$ 130 limpos.
2. **Cultura de Compra por Impulso (1-Click Buy):** O consumidor americano compra produtos entre US$ 15 e US$ 45 no cartão de crédito instantaneamente, sem hesitar com frete ou parcelamento.
3. **Conversão de Marketing Direto Brasileiro:** Vídeos curtos com ganchos agressivos e demonstração visual de problema/solução (estilo infoproduto brasileiro) convertem muito acima da média no TikTok/Reels americano.

---

## 2. Decisão de Arquitetura: Fase 1 (Afiliados) vs. Fase 2 (Loja Própria)

| Critério | Fase 1: Afiliados Amazon US + Vitrine | Fase 2: Loja Própria Dropshipping US |
| :--- | :--- | :--- |
| **Capital Inicial** | R$ 0 a R$ 150 (quase zero) | US$ 300–800 (abertura de LLC, gateway, apps) |
| **Burocracia** | Conta Wise / Payoneer ACH (Pessoa Física) | Exige LLC americana (Firstbase/doola) + Stripe US |
| **Logística e Estoque** | 100% Amazon Prime (entrega 1-2 dias) | CJ Dropshipping / Zendrop US Warehouse (3-7 dias) |
| **Risco Operacional** | **Zero:** Sem chargebacks, sem suporte | Reembolsos, disputas de cartão, atendimento |
| **Margem por Venda** | 3% a 10% (+ comissão sobre o carrinho de 24h) | 60% a 70% de margem bruta |
| **Regra de Transição** | **Começar aqui imediatamente** | **Migrar apenas o produto que bater >30 cliques/dia sustentados por 7 dias** |

---

## 3. Opções de Vitrine / Loja (Storefront)

O projeto foi desenhado para ser flexível quanto à hospedagem da vitrine, dependendo do perfil do operador:

### Opção A — Vitrine Next.js Própria (`dollar-factory/vitrine`)
- **Vantagens:** Domínio próprio (ex: `cleverusfinds.com`), controle total dos eventos do Meta Pixel e TikTok Pixel, busca inteligente por `#Código` do vídeo, sem custos de mensalidade (deploy gratuito na Vercel).
- **Ideal para:** Desenvolvedores e automações completas.

### Opção B — Amazon Storefront Oficial (`amazon.com/shop/...`)
- **Vantagens:** A própria Amazon hospeda e gerencia tudo. Confiança máxima do consumidor (já está dentro do app da Amazon).
- **Como ingressar:** Inscrição no *Amazon Influencer Program* vinculando uma conta de rede social com engajamento.

### Opção C — Link-in-Bio Especializado (Beacons.ai / Stan Store)
- **Vantagens:** Zero código, montagem em 10 minutos, layout de loja virtual para celular com fotos, preços e códigos `#01` a `#10`.
- **Ideal para:** Quem não quer se preocupar com servidores e quer focar 100% na criação e postagem dos vídeos.

---

## 4. Estratégia de Conteúdo e Vídeo Viral

- **Formato:** *Character Product Reviews* (ex.: Rick Sanchez, Walter White, Saul Goodman, Peter Griffin).
- **Estrutura dos Vídeos (15 a 30 segundos):**
  1. **0–3s (Gancho Visual & Bordão):** Identificação imediata da dor + choque inicial.
  2. **3–15s (Agitação & Demonstração Rápida):** Cortes a cada 1.5–2s mostrando o produto em ação física.
  3. **15–25s (Benefícios & Prova):** Menção do preço atrativo em dólar e avaliações.
  4. **25–30s (CTA Nativo):** *"Link in bio — type code #XX"*.
- **Sound Design:** Remoção de silêncios (`silenceremove`), batida de fundo sutil (12% volume), efeitos de transição (*whoosh*) e sino de caixa registradora (*ding* no preço).

---

## 5. Distribuição e Algoritmo nos EUA

Para garantir que o conteúdo seja distribuído para o público americano:
1. **Configuração do Dispositivo/Navegador:** Idioma em `English (United States)`, região `United States`.
2. **Conexão:** Uso de VPN residencial ou Proxy Residencial Estático US durante o registro e publicações.
3. **Aquecimento:** 3 a 5 dias de consumo prévio de conteúdo gringo do mesmo nicho antes do primeiro post.
4. **Horário Nobre (Costa Leste EUA - EST):** Postar entre 08h–10h e 20h–22h30 (horário de Brasília).
