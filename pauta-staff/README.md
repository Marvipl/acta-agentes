# pauta-staff — Agente da Dash do Staff C-Level

> Pasta autocontida dentro do repo `acta-agentes`, seguindo a filosofia do repositório: aqui fica só conteúdo estável (playbook e scripts); dados que mudam toda semana (atividades, analytics, resumo, pauta) vivem no Slack, nunca aqui. Os prompts das três rotinas estão em `referencia/prompt_agente_pauta_*.md`, no padrão dos demais agentes.
> Não conflita com os demais agentes: nenhum arquivo fora de `pauta-staff/` é lido ou modificado, não há instalação de dependências e nada é gravado em configuração global do repositório.

O acompanhamento da Reunião de Staff C-Level é feito em dois artefatos nativos do Slack, mantidos por rotinas do **Claude Code Routines** — não há mais pauta em Word:

- **Lista "Action Plan - Staff C-level"** — fonte única das atividades (Pendência / Responsável / Data prevista / Status / Comentário). O time cria as ações e atualiza status direto nela.
- **Dash (canvas do canal #staff)** — aba Canvas fixa no topo do canal, com: 📊 Analytics (indicadores, desempenho individual e histórico semanal — o histórico vive na própria dash), 📝 Resumo da última reunião (manual), ✅ Action items (espelho da lista), 📌 Lembretes (manual), 📋 Pauta padrão (Projetos / Comercial / Financeiro) e ➕ Pauta adicional (manual).

Rotinas:

- **Segunda 09:00** — lembrete único no canal: atualizar status/comentário na lista até 23:59 (mencionando responsáveis por itens em aberto) e adicionar pauta adicional direto na dash.
- **Terça 09:00** — o agente lê a lista, atualiza os blocos do bot na dash (indicadores com comparação vs. semana passada, tabela por pessoa, histórico +1 linha, espelho de action items) e avisa no canal. As seções manuais nunca são tocadas.
- **Diariamente 09:00** — lembretes de vencimento: DM privada aos responsáveis por atividades que vencem em 3 dias, e aviso consolidado no canal privado #avisos-action-items para as vencidas há 1 dia que seguem não concluídas.

Após a reunião de quarta, o time cola o resumo na dash, cria as novas ações direto na lista e limpa a seção de pauta adicional. Atas em Word são história — os scripts de DOCX permanecem no repo apenas como legado/uso do fluxo do conselho.

## Estrutura

```
pauta-staff/
  SKILL.md                           Estrutura da dash + fluxos das rotinas (leitura obrigatória da rotina)
  README.md                          Este arquivo
  scripts/slack.sh                   Helpers de Slack: mensagens, DMs, lista (lista_*), dash/canvas (dash_*, canvas_*), canais
  templates/, scripts/gerar_pauta.py, scripts/ler_docx.py,
  scripts/validar_pauta.py, scripts/achar_pauta_anterior.sh,
  exemplos/pauta_exemplo.json        LEGADO (era da pauta em DOCX) — mantidos para o fluxo do conselho
```

Comandos principais do `scripts/slack.sh` (rode sem argumentos para ver todos): `postar`, `postar_em`, `dm_texto`, `historico`, `canal_por_nome`, `lista_garantir`, `lista_itens`, `lista_criar_item`, `lista_url`, `dash_canvas_id`, `dash_url`, `canvas_conteudo`, `canvas_substituir`, `canvas_inserir_apos`, `ts`.

## Pré-requisitos

1. **App do Slack**: bot scopes `chat:write`, `channels:read`, `channels:history`, `users:read`, `files:read`, `lists:read`, `lists:write`, `canvases:read`, `canvases:write`, `im:write`, `groups:read` (canal privado de avisos); bot convidado ao canal principal E ao canal privado #avisos-action-items.
2. **Lista e dash**: localizadas em tempo de execução — a lista **pelo nome** ("Action Plan - Staff C-level"; `lista_garantir` cria e compartilha se não existir; overrides `SLACK_LIST_NAME`/`SLACK_LIST_ID`), a dash como **canvas do canal** (`dash_canvas_id`). Nenhum ID em configuração. A criação da dash é ato único (já feito); as rotinas não a recriam.
3. **Ambiente de nuvem das rotinas**: variáveis `SLACK_BOT_TOKEN` (xoxb-...) e `SLACK_CHANNEL_ID`; acesso de rede Custom com `slack.com` e `files.slack.com` nos domínios permitidos (mantendo a lista padrão de gerenciadores de pacotes); script de configuração vazio. Nenhum segredo na instrução ou no repo.
4. Ferramentas no ambiente de execução: `curl`, `jq`, `python3` (padrão nas sessões do Claude Code).

## Teste local (faça antes de agendar)

```bash
export SLACK_BOT_TOKEN=xoxb-...
export SLACK_CHANNEL_ID=C...
chmod +x pauta-staff/scripts/*.sh

# 1) Slack funciona?
pauta-staff/scripts/slack.sh testar

# 2) lista funciona? (resolução pelo nome — nenhum ID necessário)
pauta-staff/scripts/slack.sh lista_garantir   # cria e compartilha se não existir
pauta-staff/scripts/slack.sh lista_itens | jq 'group_by(.status) | map({status: .[0].status, n: length})'

# 3) dash acessível?
pauta-staff/scripts/slack.sh dash_url
pauta-staff/scripts/slack.sh canvas_conteudo "$(pauta-staff/scripts/slack.sh dash_canvas_id)" | head -c 400

# 4) DM funciona? (use seu próprio ID U...)
pauta-staff/scripts/slack.sh dm_texto U0SEUID "teste — pode ignorar"

# 5) canal de avisos visível? (bot precisa estar convidado)
pauta-staff/scripts/slack.sh canal_por_nome avisos-action-items
```

## Rotinas (claude.ai/code/routines, ou /schedule no CLI, ou Desktop → Schedule → New Remote Task)

Todas apontam para este repositório, com as duas variáveis de ambiente
configuradas. Horários no fuso local (America/Sao_Paulo). Prompts completos
em `referencia/`:

| Rotina | Agendamento | Cron UTC | Prompt |
|---|---|---|---|
| 1 — lembrete de segunda | segundas 09:00 | `0 12 * * 1` | `prompt_agente_pauta_coleta.md` |
| 2 — atualização da dash | terças 09:00 | `0 12 * * 2` | `prompt_agente_pauta_consolida.md` |
| 3 — lembretes de vencimento | diária 09:00 | `0 12 * * *` | `prompt_agente_pauta_lembretes.md` |

## Notas operacionais

- Routines está em research preview; cada execução consome os limites de uso do
  plano. As rotinas pertencem à conta que as criou.
- A dash é o canvas do canal: seções ✍️ (Resumo, Lembretes, Pauta adicional)
  são exclusivamente manuais; os blocos do bot (indicadores, tabelas de
  desempenho/histórico/action items) são substituídos por inteiro na terça —
  edições manuais nesses blocos serão sobrescritas. Se alguém apagar um bloco
  do bot, a rotina o recria na terça seguinte.
- O histórico semanal de analytics vive na tabela da própria dash (o bot só
  acrescenta linhas) — apagar linhas apaga histórico, sem backup.
- Lembretes de vencimento (Rotina 3) são disparados por igualdade de data —
  DM quando faltam exatos 3 dias, aviso no canal 1 dia após o vencimento (quem
  concluir até o fim do dia do vencimento não entra no aviso) — então cada
  atividade gera no máximo um lembrete e um aviso, sem estado entre execuções.
  Atividades cuja data passou enquanto a rotina esteve pausada não recebem
  aviso retroativo; ajuste a data prevista na lista para reativá-las.
- Não renomeie a lista no Slack: a localização é pelo nome exato
  "Action Plan - Staff C-level". Se precisar renomear, defina SLACK_LIST_NAME
  (ou SLACK_LIST_ID) no ambiente das rotinas com o novo nome/ID.
- Acompanhamento de mudanças na lista: cada membro ativa as atualizações da
  lista no próprio feed de Atividade do Slack — abordagem adotada, sem ruído
  no canal. Aviso coletivo por mudança de status exigiria automação manual no
  Workflow Builder (não há API para o bot criá-la).
- Se o Slack retornar `not_in_channel` ou "canal não encontrado", o bot não
  foi convidado ao canal em questão (`/invite @bot`).
- Para obter o ID de usuário (U...) de alguém: perfil da pessoa no Slack →
  menu "⋮" → "Copiar ID do membro". DMs do bot chegam pela aba de mensagens
  do app — se alguém não estiver recebendo, confira se não silenciou o app.
