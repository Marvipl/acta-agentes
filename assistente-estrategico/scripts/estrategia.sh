#!/usr/bin/env bash
# estrategia.sh — Helpers do Assistente Estratégico da Acta Robotics.
#
# Cobre apenas o que é específico deste agente: detectar perguntas ainda sem
# resposta no canal de estratégia e responder em thread. Para ler a lista
# "Action Plan - Staff C-level", a dash e o canvas de resumos, use os comandos
# já existentes em pauta-staff/scripts/slack.sh (reuso somente leitura).
#
# Requer variáveis de ambiente:
#   SLACK_BOT_TOKEN    token do bot (xoxb-...)
#   SLACK_CHANNEL_ID   ID do canal de estratégia (ex.: C0123456789)
#
# Requer: curl, jq
#
# Uso:
#   ./scripts/estrategia.sh testar                       # diagnóstico de rede + token
#   ./scripts/estrategia.sh bot_id                       # ID de usuário (U...) do próprio bot
#   ./scripts/estrategia.sh pendentes [dias]             # perguntas sem resposta (JSON; padrão 7 dias)
#   ./scripts/estrategia.sh responder <thread_ts> "txt"  # responde em thread; imprime o ts
#   ./scripts/estrategia.sh postar "texto"               # mensagem avulsa no canal; imprime o ts

set -euo pipefail

: "${SLACK_BOT_TOKEN:?Defina SLACK_BOT_TOKEN}"
: "${SLACK_CHANNEL_ID:?Defina SLACK_CHANNEL_ID}"

API="https://slack.com/api"
AUTH=(-H "Authorization: Bearer ${SLACK_BOT_TOKEN}")

_checa() {
  local resp="$1"
  if [ -z "$resp" ]; then
    echo "ERRO Slack: resposta vazia — provável bloqueio de rede para slack.com" >&2
    exit 2
  fi
  if [ "$(echo "$resp" | jq -r .ok 2>/dev/null)" != "true" ]; then
    echo "ERRO Slack: $(echo "$resp" | jq -r .error 2>/dev/null)" >&2
    exit 1
  fi
}

testar() {
  local http="000" resp
  rm -f /tmp/slack_test_estrategia.json
  http=$(curl -s -o /tmp/slack_test_estrategia.json -w "%{http_code}" \
    "${AUTH[@]}" "$API/auth.test") || true
  if [ ! -s /tmp/slack_test_estrategia.json ] || [ "$http" = "000" ] || [ "$http" = "403" ]; then
    echo "FALHA DE REDE (HTTP $http): não foi possível alcançar slack.com." >&2
    exit 2
  fi
  resp=$(cat /tmp/slack_test_estrategia.json)
  if [ "$(echo "$resp" | jq -r .ok 2>/dev/null)" != "true" ]; then
    echo "TOKEN INVÁLIDO: $(echo "$resp" | jq -r .error 2>/dev/null)" >&2
    exit 1
  fi
  echo "OK: conectado como $(echo "$resp" | jq -r .user) no workspace $(echo "$resp" | jq -r .team)"
}

bot_id() {
  local resp
  resp=$(curl -s "${AUTH[@]}" "$API/auth.test")
  _checa "$resp"
  echo "$resp" | jq -r '.user_id'
}

pendentes() {
  # Perguntas de humanos ainda sem resposta do bot, nos últimos N dias (padrão 7).
  # Uma thread está pendente quando a última mensagem humana dela é mais recente
  # que a última resposta do bot (ou o bot nunca respondeu). Saída: JSON array de
  #   {thread_ts, tipo: "nova"|"follow-up", pergunta, ultima_msg, user}
  # onde `pergunta` é a mensagem raiz da thread e `ultima_msg` a última mensagem
  # humana (igual à pergunta quando não há replies).
  local dias="${1:-7}" bot oldest hist
  bot=$(bot_id)
  oldest=$(( $(date +%s) - dias * 86400 ))
  hist=$(curl -s "${AUTH[@]}" \
    "$API/conversations.history?channel=${SLACK_CHANNEL_ID}&limit=200&oldest=${oldest}")
  _checa "$hist"
  echo "$hist" | jq -c --arg bot "$bot" \
    '[.messages[] | select((.subtype // "") == "" and (.bot_id == null) and .user != $bot
                           and ((.thread_ts // .ts) == .ts))] | .[]' \
  | while read -r msg; do
      local ts replies thread ult_bot ult_hum tipo
      ts=$(echo "$msg" | jq -r '.ts')
      replies=$(echo "$msg" | jq -r '.reply_count // 0')
      if [ "$replies" = "0" ]; then
        echo "$msg" | jq -c '{thread_ts: .ts, tipo: "nova", pergunta: .text, ultima_msg: .text, user}'
        continue
      fi
      thread=$(curl -s "${AUTH[@]}" \
        "$API/conversations.replies?channel=${SLACK_CHANNEL_ID}&ts=${ts}&limit=200")
      _checa "$thread"
      ult_bot=$(echo "$thread" | jq -r --arg bot "$bot" \
        '[.messages[] | select(.user == $bot)] | last | .ts // "0"')
      ult_hum=$(echo "$thread" | jq -r --arg bot "$bot" \
        '[.messages[] | select((.subtype // "") == "" and (.bot_id == null) and .user != $bot)]
         | last | .ts // "0"')
      if awk -v a="$ult_hum" -v b="$ult_bot" 'BEGIN { exit !(a + 0 > b + 0) }'; then
        if [ "$ult_bot" = "0" ]; then tipo="nova"; else tipo="follow-up"; fi
        echo "$thread" | jq -c --arg bot "$bot" --arg tipo "$tipo" \
          '{thread_ts: .messages[0].ts, tipo: $tipo, pergunta: .messages[0].text,
            ultima_msg: ([.messages[] | select((.subtype // "") == "" and (.bot_id == null)
                          and .user != $bot)] | last | .text),
            user: ([.messages[] | select((.subtype // "") == "" and (.bot_id == null)
                    and .user != $bot)] | last | .user)}'
      fi
    done | jq -s '.'
}

responder() {
  local thread="$1" texto="$2" payload resp
  payload=$(jq -n --arg c "$SLACK_CHANNEL_ID" --arg t "$texto" --arg th "$thread" \
    '{channel: $c, text: $t, thread_ts: $th}')
  resp=$(curl -s "${AUTH[@]}" -H "Content-Type: application/json; charset=utf-8" \
    -d "$payload" "$API/chat.postMessage")
  _checa "$resp"
  echo "$resp" | jq -r '.ts'
}

postar() {
  local texto="$1" payload resp
  payload=$(jq -n --arg c "$SLACK_CHANNEL_ID" --arg t "$texto" '{channel: $c, text: $t}')
  resp=$(curl -s "${AUTH[@]}" -H "Content-Type: application/json; charset=utf-8" \
    -d "$payload" "$API/chat.postMessage")
  _checa "$resp"
  echo "$resp" | jq -r '.ts'
}

cmd="${1:-}"
shift || true
case "$cmd" in
  testar)     testar ;;
  bot_id)     bot_id ;;
  pendentes)  pendentes "$@" ;;
  responder)  responder "$@" ;;
  postar)     postar "$@" ;;
  *)
    grep '^#   ./scripts/estrategia.sh' "$0" | sed 's/^#   //'
    exit 1
    ;;
esac
