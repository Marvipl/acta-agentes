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

## É um bot do Slack? (como funciona a interação)

Sim — ele usa o MESMO app do Slack dos demais agentes (actabot) e posta como ele.
Mas, como toda a operação deste repo, ele roda em **Claude Code Routines**, que são
agendadas (intervalo mínimo de 1 hora), não um servidor sempre ligado. Na prática:

- Você posta a pergunta no canal #estrategia a qualquer momento.
- A rotina horária (dias úteis, horário comercial) encontra as perguntas ainda sem
  resposta — inclusive follow-ups seus em threads já respondidas — e responde na
  thread. Latência típica: até 1 hora.
- Para resposta imediata: rode a rotina manualmente ("Run now" em
  claude.ai/code/routines) ou abra uma sessão do Claude Code neste repo e converse —
  o playbook `assistente-estrategico/SKILL.md` é carregado como skill.
- Um bot de verdade em tempo real (respondendo a @menção no segundo) exigiria um
  servidor próprio com a Events API do Slack — fora do stack atual; fica como evolução
  possível se a latência de 1 hora incomodar.

## Estrutura

```
assistente-estrategico/
  SKILL.md                 Fontes, método de resposta e fluxos das rotinas (leitura obrigatória)
  README.md                Este arquivo
  scripts/estrategia.sh    Helpers próprios: pendentes (perguntas sem resposta), responder, postar
```

A leitura de lista/dash/canvas reusa `pauta-staff/scripts/slack.sh` (somente leitura;
nenhum arquivo de `pauta-staff/` é modificado).

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
| 1 — perguntas & respostas | dias úteis, de hora em hora, 08h–20h | `0 11-23 * * 1-5` | `prompt_agente_estrategico.md` |
| 2 — leitura estratégica semanal | sextas 08:00 | `0 11 * * 5` | `prompt_agente_estrategico_semanal.md` |

A rotina 2 é opcional — comece só com a 1 se preferir validar o formato das respostas
antes.

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
