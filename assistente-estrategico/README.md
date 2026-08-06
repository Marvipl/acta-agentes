# assistente-estrategico — Assistente Estratégico do CEO

> Pasta do agente estratégico dentro do repo `acta-agentes`, seguindo a filosofia do
> repositório: aqui fica só conteúdo estável (playbook e script); as conversas vivem no
> Slack e as evidências nas fontes dos outros agentes. Os prompts das rotinas estão em
> `referencia/prompt_agente_estrategico*.md`, no padrão dos demais agentes.

O assistente responde perguntas estratégicas do CEO num canal dedicado do Slack
(sugestão: **#estrategia**, privado), sempre com base em evidências reais, e posta uma
leitura estratégica semanal cruzando execução interna e mercado. Ele enxerga:

- **Execução**: lista "Action Plan - Staff C-level", dash do staff (indicadores +
  histórico semanal) e canvas "Resumos de reuniões — Staff C-Level" — tudo somente
  leitura, via os helpers já existentes de `pauta-staff/scripts/slack.sh`.
- **Mercado**: briefings diários do Agente de Notícias na pasta `Acta/Briefings` do
  Google Drive.
- **Planejamento**: documento de planejamento estratégico no Drive (localizado por
  título; override `DRIVE_DOC_PLANEJAMENTO`).
- **Referência**: portfólio, ICP e guardrails deste repo.

CRM e financeiro ficam para integrações futuras — até lá, o agente declara a lacuna
quando a pergunta depender desses dados, em vez de estimar.

## Como funciona a interação: dois modos

O assistente atende no canal #estrategia pelo MESMO app dos demais agentes
(actabot), em um de dois modos — que convivem sem duplicar respostas, pois a
detecção de pendências é idempotente:

**Modo A — rotina disparada via API (recomendado: sem servidor, cobra da
assinatura).** As rotinas do Claude Code aceitam um **gatilho de API** (beta): um
endpoint `POST .../routines/{id}/fire` que dispara a rotina na hora. Como o Slack
não tem passo nativo de web request para chamar esse endpoint, a ponte é um
**Google Apps Script** (mesmo padrão do `EnviarBriefingActa.gs` já em produção):
acionador a cada 1 minuto, olha o canal e, havendo mensagem humana nova (ou
follow-up em thread), dispara a rotina de Q&A. Latência típica de ponta a ponta:
**~2 a 4 minutos** (até 1 min de detecção + subida da sessão na nuvem + análise).
Custo: Apps Script é gratuito e a rotina consome a assinatura do claude.ai, como
os demais agentes.

**Modo B — servidor em tempo real (opcional: segundos, requer host + API key).**
`bot/bot.py` (Socket Mode — sem URL pública) recebe cada mensagem no instante em
que é postada, roda o **Claude Agent SDK** com o playbook `SKILL.md` e responde na
thread em segundos, com memória por thread. Requer uma máquina sempre ligada e
`ANTHROPIC_API_KEY` (cobrança por token, separada da assinatura). Fora do
#estrategia responde a @menção.

Descartado: **Claude Tag** (app oficial da Anthropic no Slack) responde em tempo
real, mas não lê listas do Slack, canvas nem o Drive — não alcança as fontes deste
agente.

Comece pelo Modo A; suba o Modo B só se a latência de minutos incomodar no uso
real.

## Estrutura

```
assistente-estrategico/
  SKILL.md                 Fontes, método de resposta e fluxos (leitura obrigatória)
  README.md                Este arquivo
  scripts/estrategia.sh    Helpers de canal: pendentes (perguntas sem resposta), responder, postar
  gatilho/DispararAssistente.gs  Apps Script que dispara a rotina de Q&A via API (Modo A)
  bot/bot.py               Servidor em tempo real (Socket Mode + Claude Agent SDK)
  bot/prompt_bot.md        Instruções do modo tempo real (somadas ao SKILL.md)
  bot/drive.py             Leitura de briefings/planejamento no Drive via service account
  bot/requirements.txt     Dependências Python do servidor
  bot/Dockerfile           Imagem pronta para qualquer host (build a partir da raiz)
```

A leitura de lista/dash/canvas reusa `pauta-staff/scripts/slack.sh` (somente leitura;
nenhum arquivo de `pauta-staff/` é modificado).

## Modo A — rotina disparada via API (sem servidor)

1. **Criar a rotina de Q&A** (ver tabela de rotinas abaixo) com o prompt
   `referencia/prompt_agente_estrategico.md` e o agendamento horário (que fica como
   varredura de segurança).
2. **Adicionar o gatilho de API** à rotina em claude.ai/code/routines (Add API
   trigger) e copiar a URL de disparo e o bearer token. O recurso é beta
   (header `anthropic-beta: experimental-cc-routine-2026-04-01`); se o formato
   mudar, confira code.claude.com/docs/en/routines.
3. **Apps Script**: em script.google.com, criar um projeto com o conteúdo de
   `gatilho/DispararAssistente.gs`; em Configurações do projeto → Propriedades do
   script, definir `SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID` (canal #estrategia),
   `ROUTINE_FIRE_URL` e `ROUTINE_FIRE_TOKEN`; criar um acionador temporizado
   ("a cada minuto") para a função `dispararSeHouverNovidade`.
4. Pronto: mensagem nova no canal → rotina dispara em ~1 min → resposta na thread.
   Disparo repetido não duplica resposta (fluxo idempotente); se um disparo
   falhar, a varredura horária cobre. O payload do disparo é tratado como mero
   despertador — a rotina ignora instruções vindas nele (regra no prompt).

Alternativa à ponte, sem Apps Script: um automatizador SaaS (Zapier/Make) com
gatilho "nova mensagem no canal" chamando a mesma URL de disparo.

## Modo B — subindo o bot em tempo real

1. **App do Slack** (api.slack.com/apps → app do actabot):
   - *Socket Mode*: ativar e criar um App-Level Token com scope `connections:write`
     (token `xapp-...`).
   - *Event Subscriptions* → Subscribe to bot events: `message.groups` (canal
     privado), `message.channels` e `app_mention`. Reinstalar o app no workspace.
   - Scope adicional de bot: `reactions:write` (o bot marca 👀 na mensagem que está
     processando).
2. **Google Drive** (para briefings e planejamento fora das rotinas): criar uma
   service account no Google Cloud, baixar o JSON e COMPARTILHAR a pasta `Acta/` do
   Drive (leitor) com o e-mail da service account. Sem isso o bot funciona, mas
   declara a lacuna de mercado/planejamento nas respostas.
3. **Rodar** (qualquer máquina sempre ligada — mini PC no escritório, VPS, Cloud Run
   com `min-instances=1`):

   ```bash
   # direto
   pip install -r assistente-estrategico/bot/requirements.txt
   npm install -g @anthropic-ai/claude-code   # CLI usado pelo Agent SDK (requer Node 18+)
   export SLACK_BOT_TOKEN=xoxb-... SLACK_APP_TOKEN=xapp-...
   export SLACK_CHANNEL_ID=C...               # canal #estrategia
   export SLACK_STAFF_CHANNEL_ID=C...         # canal do staff
   export ANTHROPIC_API_KEY=sk-ant-...
   export GOOGLE_SERVICE_ACCOUNT_FILE=/caminho/service-account.json   # opcional
   python3 assistente-estrategico/bot/bot.py

   # ou via Docker (build a partir da RAIZ do repo)
   docker build -f assistente-estrategico/bot/Dockerfile -t acta-assistente .
   docker run -d --restart=always --env-file .env acta-assistente
   ```

O arquivo `bot/.sessoes.json` (memória thread → sessão) é local e não versionado.

## Pré-requisitos

1. **Canal**: criar o canal privado #estrategia e convidar o bot (`/invite @actabot`).
   Membros: CEO (e quem mais deva ver as análises).
2. **App do Slack**: os scopes já usados pelo actabot bastam, conferindo:
   `chat:write`, `groups:read`, `groups:history` (canal privado), `channels:read`,
   `channels:history`, `users:read`, `lists:read`, `canvases:read`, `files:read`.
   Nenhum scope de escrita além de `chat:write` é necessário (o agente não edita
   lista nem canvas; `lists:write` só se for usar a criação de item sob pedido).
3. **Ambiente de nuvem das rotinas**: variáveis `SLACK_BOT_TOKEN` (xoxb-...),
   `SLACK_CHANNEL_ID` (ID do canal #estrategia) e `SLACK_STAFF_CHANNEL_ID` (ID do
   canal do staff, para dash e resumos); acesso de rede Custom com `slack.com` e
   `files.slack.com`; conector **Google Drive** ativo (briefings e planejamento).
   Opcional: `DRIVE_DOC_PLANEJAMENTO` com o nome exato do doc de planejamento.
   Nenhum segredo na instrução ou no repo.
4. Ferramentas no ambiente de execução: `curl`, `jq`, `python3` (padrão nas sessões
   do Claude Code).

## Teste local (faça antes de agendar)

```bash
export SLACK_BOT_TOKEN=xoxb-...
export SLACK_CHANNEL_ID=C...        # canal #estrategia
export SLACK_STAFF_CHANNEL_ID=C...  # canal do staff
chmod +x assistente-estrategico/scripts/*.sh pauta-staff/scripts/*.sh

# 1) Slack funciona?
assistente-estrategico/scripts/estrategia.sh testar

# 2) detecção de perguntas funciona? (poste uma pergunta no canal antes)
assistente-estrategico/scripts/estrategia.sh pendentes | jq

# 3) fontes do staff acessíveis? (leitura via helpers do pauta-staff)
pauta-staff/scripts/slack.sh lista_itens | jq length
SLACK_CHANNEL_ID=$SLACK_STAFF_CHANNEL_ID pauta-staff/scripts/slack.sh dash_url

# 4) resposta em thread funciona? (use o thread_ts retornado em `pendentes`)
assistente-estrategico/scripts/estrategia.sh responder <thread_ts> "teste — pode ignorar"
```

## Rotinas (claude.ai/code/routines, ou /schedule no CLI, ou Desktop → Schedule → New Remote Task)

Ambas apontam para este repositório, com as três variáveis de ambiente e o conector
Google Drive configurados. Horários no fuso local (America/Sao_Paulo). Prompts
completos em `referencia/`:

| Rotina | Agendamento | Cron UTC | Prompt |
|---|---|---|---|
| 1 — perguntas & respostas | horária (varredura) + gatilho de API (Modo A) | `0 11-23 * * 1-5` | `prompt_agente_estrategico.md` |
| 2 — leitura estratégica semanal | sextas 08:00 | `0 11 * * 5` | `prompt_agente_estrategico_semanal.md` |

No Modo A, a rotina 1 é o coração do Q&A: o Apps Script a dispara via API a cada
novidade e o agendamento horário fica como varredura de segurança. Se o Modo B
(servidor) estiver no ar, a rotina 1 pode ficar só na varredura — a detecção de
pendências é idempotente e os modos não se duplicam.

## Notas operacionais

- Execuções da rotina 1 sem pergunta pendente são curtas e silenciosas (nada é
  postado no canal); ainda assim consomem uma execução do plano — ajuste a janela do
  cron se quiser economizar.
- A detecção de pendências olha os últimos 7 dias de mensagens do canal. Pergunta com
  mais de 7 dias sem resposta sai do radar — reposte-a.
- Mensagens que não são perguntas (avisos, links soltos) podem ficar sem resposta por
  decisão do agente; isso não gera erro nem spam.
- Perguntas que dependem de CRM/financeiro: o agente responde com o que há e declara
  a lacuna. Quando essas integrações chegarem, entram como novas fontes no
  `SKILL.md` — o método de resposta não muda.
- Se o Slack retornar `not_in_channel`, o bot não foi convidado ao canal em questão
  (`/invite @actabot` no #estrategia e no canal do staff).
- O agente nunca escreve na dash, nos canvas ou na lista do staff (exceto criação de
  item de Action Plan explicitamente pedida pelo CEO numa pergunta).
