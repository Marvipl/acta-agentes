#!/usr/bin/env bash
# slack.sh — Helpers de Slack para os agentes da Acta Robotics.
#
# Requer variáveis de ambiente:
#   SLACK_BOT_TOKEN   token do bot (xoxb-...)
#   SLACK_CHANNEL_ID  ID do canal (ex.: C0123456789)
#
# Requer: curl, jq, python3
#
# Uso:
#   ./scripts/slack.sh testar                            # diagnostico de rede + token
#   ./scripts/slack.sh postar "texto da mensagem" [thread_ts]
#   ./scripts/slack.sh historico [oldest_ts] [latest_ts]
#   ./scripts/slack.sh respostas <thread_ts>
#   ./scripts/slack.sh ultimo_arquivo_pauta          # imprime JSON {name, url_private, ts}
#   ./scripts/slack.sh listar_arquivos_docx           # JSON array dos .docx recentes do canal
#   ./scripts/slack.sh baixar <url_private> <destino>
#   ./scripts/slack.sh enviar_arquivo <caminho> "comentário inicial"
#   ./scripts/slack.sh ts "2026-07-13 23:59"         # converte data local em epoch (America/Sao_Paulo)

set -euo pipefail

: "${SLACK_BOT_TOKEN:?Defina SLACK_BOT_TOKEN}"
: "${SLACK_CHANNEL_ID:?Defina SLACK_CHANNEL_ID}"

API="https://slack.com/api"
AUTH=(-H "Authorization: Bearer ${SLACK_BOT_TOKEN}")

_checa() { # falha com mensagem clara se ok=false
  local resp="$1"
  if [ "$(echo "$resp" | jq -r .ok)" != "true" ]; then
    echo "ERRO Slack: $(echo "$resp" | jq -r .error)" >&2
    exit 1
  fi
}


testar() {
  # diagnóstico: rede + token. Distingue bloqueio de rede (403/host_not_allowed)
  # de token inválido (ok=false, invalid_auth).
  local http resp
  http=$(curl -s -o /tmp/slack_test.json -w "%{http_code}" \
    "${AUTH[@]}" "$API/auth.test" || echo "000")
  if [ "$http" = "000" ] || [ "$http" = "403" ]; then
    echo "FALHA DE REDE (HTTP $http): o ambiente provavelmente bloqueia slack.com." >&2
    echo "Verifique o transcript por x-deny-reason: host_not_allowed." >&2
    exit 2
  fi
  resp=$(cat /tmp/slack_test.json)
  if [ "$(echo "$resp" | jq -r .ok)" != "true" ]; then
    echo "TOKEN INVALIDO: $(echo "$resp" | jq -r .error)" >&2
    exit 1
  fi
  echo "OK: conectado como $(echo "$resp" | jq -r .user) no workspace $(echo "$resp" | jq -r .team)"
}

postar() {
  local texto="$1" thread="${2:-}"
  local payload
  payload=$(jq -n --arg c "$SLACK_CHANNEL_ID" --arg t "$texto" --arg th "$thread" \
    '{channel:$c, text:$t} + (if $th != "" then {thread_ts:$th} else {} end)')
  local resp
  resp=$(curl -s "${AUTH[@]}" -H "Content-Type: application/json; charset=utf-8" \
    -d "$payload" "$API/chat.postMessage")
  _checa "$resp"
  echo "$resp" | jq -r '.ts'   # imprime o ts da mensagem (útil para thread)
}

historico() {
  local oldest="${1:-0}" latest="${2:-}"
  local url="$API/conversations.history?channel=${SLACK_CHANNEL_ID}&limit=200&oldest=${oldest}"
  [ -n "$latest" ] && url="${url}&latest=${latest}&inclusive=true"
  local resp
  resp=$(curl -s "${AUTH[@]}" "$url")
  _checa "$resp"
  echo "$resp" | jq '.messages'
}

respostas() {
  local thread_ts="$1"
  local resp
  resp=$(curl -s "${AUTH[@]}" \
    "$API/conversations.replies?channel=${SLACK_CHANNEL_ID}&ts=${thread_ts}&limit=200")
  _checa "$resp"
  echo "$resp" | jq '.messages'
}


listar_arquivos_docx() {
  # lista até 20 arquivos .docx mais recentes do canal (JSON array: name, url_private, ts)
  local resp
  resp=$(curl -s "${AUTH[@]}" \
    "$API/conversations.history?channel=${SLACK_CHANNEL_ID}&limit=200")
  _checa "$resp"
  echo "$resp" | jq '
    [.messages[] | select(.files) | . as $m | .files[]
     | select(.name | test("(?i)\\.docx$"))
     | {name, url_private, ts: $m.ts}]
    | sort_by(.ts) | reverse | .[0:20]'
}

ultimo_arquivo_pauta() {
  # varre as últimas 200 mensagens do canal e pega o arquivo .docx mais recente
  # cujo nome contenha "pauta" ou "ata" (sem diferenciar maiúsculas/acentos básicos)
  local resp
  resp=$(curl -s "${AUTH[@]}" \
    "$API/conversations.history?channel=${SLACK_CHANNEL_ID}&limit=200")
  _checa "$resp"
  echo "$resp" | jq -r '
    [.messages[] | select(.files) | . as $m | .files[]
     | select(.name | test("(?i)(pauta|ata)"))
     | select(.name | test("(?i)\\.docx$"))
     | {name, url_private, ts: $m.ts}]
    | sort_by(.ts) | last // empty'
}

baixar() {
  local url="$1" destino="$2"
  curl -sL "${AUTH[@]}" "$url" -o "$destino"
  # sanidade: DOCX é um ZIP, começa com "PK"
  if [ "$(head -c 2 "$destino")" != "PK" ]; then
    echo "ERRO: download nao parece um DOCX valido (login redirect?)" >&2
    exit 1
  fi
  echo "$destino"
}

enviar_arquivo() {
  # fluxo novo do Slack (files.upload foi descontinuado):
  # getUploadURLExternal -> POST binário -> completeUploadExternal
  local caminho="$1" comentario="${2:-}"
  local nome tamanho resp url file_id
  nome=$(basename "$caminho")
  tamanho=$(wc -c < "$caminho" | tr -d ' ')

  resp=$(curl -s "${AUTH[@]}" -G "$API/files.getUploadURLExternal" \
    --data-urlencode "filename=${nome}" --data-urlencode "length=${tamanho}")
  _checa "$resp"
  url=$(echo "$resp" | jq -r .upload_url)
  file_id=$(echo "$resp" | jq -r .file_id)

  curl -s -X POST "$url" -F "file=@${caminho}" > /dev/null

  local files_json
  files_json=$(jq -n --arg id "$file_id" --arg t "$nome" '[{id:$id, title:$t}]')
  resp=$(curl -s "${AUTH[@]}" -H "Content-Type: application/json; charset=utf-8" \
    -d "$(jq -n --argjson f "$files_json" --arg c "$SLACK_CHANNEL_ID" --arg ic "$comentario" \
          '{files:$f, channel_id:$c, initial_comment:$ic}')" \
    "$API/files.completeUploadExternal")
  _checa "$resp"
  echo "Arquivo enviado: ${nome}"
}

ts() {
  # converte "YYYY-MM-DD HH:MM" (horário de São Paulo) em epoch unix
  python3 - "$1" <<'PY'
import sys, datetime, zoneinfo
dt = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d %H:%M")
dt = dt.replace(tzinfo=zoneinfo.ZoneInfo("America/Sao_Paulo"))
print(int(dt.timestamp()))
PY
}

cmd="${1:-}"; shift || true
case "$cmd" in
  testar)                testar ;;
  postar)                postar "$@" ;;
  historico)             historico "$@" ;;
  respostas)             respostas "$@" ;;
  ultimo_arquivo_pauta)  ultimo_arquivo_pauta ;;
  listar_arquivos_docx)  listar_arquivos_docx ;;
  baixar)                baixar "$@" ;;
  enviar_arquivo)        enviar_arquivo "$@" ;;
  ts)                    ts "$@" ;;
  *) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 1 ;;
esac
