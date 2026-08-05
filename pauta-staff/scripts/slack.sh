#!/usr/bin/env bash
# slack.sh — Helpers de Slack para os agentes da Acta Robotics.
#
# Requer variáveis de ambiente:
#   SLACK_BOT_TOKEN    token do bot (xoxb-...)
#   SLACK_CHANNEL_ID   ID do canal (ex.: C0123456789)
#   SLACK_DM_USER_IDS  opcional: IDs de usuário (U...) separados por vírgula,
#                      destinatários padrão de dm_arquivo (requer scope im:write);
#                      ou o valor especial "canal" para enviar a todos os membros
#                      humanos do canal (requer também channels:read e users:read;
#                      groups:read se o canal for privado)
#   SLACK_LIST_NAME    opcional: nome da lista de pendências (padrão:
#                      "Action Plan - Staff C-level"). Os comandos lista_*
#                      localizam a lista PELO NOME em tempo de execução
#                      (scopes lists:read, lists:write) — nenhum ID fixo.
#   SLACK_LIST_ID      opcional: ID (F...) fixo da lista — só use para apontar
#                      para uma lista específica, ignorando a busca por nome
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
#   ./scripts/slack.sh dm_arquivo <caminho> "comentário" [U111,U222|canal]  # padrão: SLACK_DM_USER_IDS
#   ./scripts/slack.sh membros_canal                  # IDs dos membros humanos do canal (sem bots)
#   ./scripts/slack.sh usuarios_canal                 # ID <tab> nome real <tab> display name, por membro
#   ./scripts/slack.sh lista_garantir                 # cria a lista se não existir e a compartilha no canal; imprime "id<tab>url"
#   ./scripts/slack.sh lista_itens                    # itens da lista de pendências (JSON simplificado)
#   ./scripts/slack.sh lista_criar_item "<pendência>" ["U1,U2"] ["AAAA-MM-DD"] [aberto|fazendo|concluido] ["comentário"]
#   ./scripts/slack.sh lista_url                      # permalink da lista de pendências
#   ./scripts/slack.sh ts "2026-07-13 23:59"         # converte data local em epoch (America/Sao_Paulo)

set -euo pipefail

: "${SLACK_BOT_TOKEN:?Defina SLACK_BOT_TOKEN}"
: "${SLACK_CHANNEL_ID:?Defina SLACK_CHANNEL_ID}"

API="https://slack.com/api"
AUTH=(-H "Authorization: Bearer ${SLACK_BOT_TOKEN}")

_checa() { # falha com mensagem clara se ok=false ou resposta vazia (rede)
  local resp="$1"
  if [ -z "$resp" ]; then
    echo "ERRO Slack: resposta vazia — provavel bloqueio de rede para slack.com" >&2
    exit 2
  fi
  if [ "$(echo "$resp" | jq -r .ok 2>/dev/null)" != "true" ]; then
    echo "ERRO Slack: $(echo "$resp" | jq -r .error 2>/dev/null)" >&2
    exit 1
  fi
}


testar() {
  # diagnóstico: rede + token. Distingue bloqueio de rede (curl falha, 000, 403,
  # x-deny-reason: host_not_allowed) de token inválido (ok=false, invalid_auth).
  local http="000" resp
  rm -f /tmp/slack_test.json
  http=$(curl -s -o /tmp/slack_test.json -w "%{http_code}" \
    "${AUTH[@]}" "$API/auth.test") || true
  if [ ! -s /tmp/slack_test.json ] || [ "$http" = "000" ] || [ "$http" = "403" ]; then
    echo "FALHA DE REDE (HTTP $http): nao foi possivel alcancar slack.com." >&2
    echo "O ambiente desta execucao esta bloqueando o dominio (procure por" >&2
    echo "x-deny-reason: host_not_allowed). Nao e problema de token." >&2
    exit 2
  fi
  resp=$(cat /tmp/slack_test.json)
  if [ "$(echo "$resp" | jq -r .ok 2>/dev/null)" != "true" ]; then
    echo "TOKEN INVALIDO: $(echo "$resp" | jq -r .error 2>/dev/null)" >&2
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

_upload() {
  # fluxo novo do Slack (files.upload foi descontinuado):
  # getUploadURLExternal -> POST binário -> completeUploadExternal
  local canal="$1" caminho="$2" comentario="${3:-}"
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
    -d "$(jq -n --argjson f "$files_json" --arg c "$canal" --arg ic "$comentario" \
          '{files:$f, channel_id:$c, initial_comment:$ic}')" \
    "$API/files.completeUploadExternal")
  _checa "$resp"
}

enviar_arquivo() {
  local caminho="$1" comentario="${2:-}"
  _upload "$SLACK_CHANNEL_ID" "$caminho" "$comentario"
  echo "Arquivo enviado: $(basename "$caminho")"
}

_abrir_dm() { # user_id -> imprime o ID do canal de DM (D...)
  local user="$1" resp
  resp=$(curl -s "${AUTH[@]}" -H "Content-Type: application/json; charset=utf-8" \
    -d "$(jq -n --arg u "$user" '{users:$u}')" "$API/conversations.open")
  _checa "$resp"
  echo "$resp" | jq -r '.channel.id'
}

usuarios_canal() {
  # imprime "ID<tab>nome real<tab>display name" por membro humano do canal
  # (exclui bots, o Slackbot e contas desativadas)
  local resp user uresp
  resp=$(curl -s "${AUTH[@]}" \
    "$API/conversations.members?channel=${SLACK_CHANNEL_ID}&limit=200")
  _checa "$resp"
  for user in $(echo "$resp" | jq -r '.members[]'); do
    [ "$user" = "USLACKBOT" ] && continue
    uresp=$(curl -s "${AUTH[@]}" "$API/users.info?user=${user}")
    _checa "$uresp"
    echo "$uresp" | jq -r 'select((.user.is_bot or .user.deleted) | not) |
      [.user.id, .user.profile.real_name // "", .user.profile.display_name // ""] | @tsv'
  done
}

membros_canal() {
  # imprime os IDs dos membros humanos do canal, separados por vírgula
  usuarios_canal | cut -f1 | paste -sd, -
}

LISTA_NOME_PADRAO="Action Plan - Staff C-level"

_lista_id() {
  # resolve o ID da lista de pendências: SLACK_LIST_ID (se definida) ou busca
  # pelo nome (SLACK_LIST_NAME ou padrão) entre as listas acessíveis ao bot
  if [ -n "${SLACK_LIST_ID:-}" ]; then echo "$SLACK_LIST_ID"; return; fi
  local nome="${SLACK_LIST_NAME:-$LISTA_NOME_PADRAO}" resp id
  resp=$(curl -s "${AUTH[@]}" "$API/files.list?types=list&count=100")
  _checa "$resp"
  id=$(echo "$resp" | jq -r --arg n "$nome" \
    '[.files[] | select((.title // .name) == $n)] | sort_by(.created) | last | .id // empty')
  if [ -z "$id" ]; then
    echo "ERRO: lista \"$nome\" nao encontrada — rode lista_garantir para cria-la" >&2
    exit 1
  fi
  echo "$id"
}

lista_garantir() {
  # garante que a lista de pendências existe (cria com o schema padrão se
  # necessário) e está compartilhada com o canal; imprime "id<tab>url"
  local nome="${SLACK_LIST_NAME:-$LISTA_NOME_PADRAO}" resp id
  resp=$(curl -s "${AUTH[@]}" "$API/files.list?types=list&count=100")
  _checa "$resp"
  id=$(echo "$resp" | jq -r --arg n "$nome" \
    '[.files[] | select((.title // .name) == $n)] | sort_by(.created) | last | .id // empty')
  if [ -z "$id" ]; then
    resp=$(curl -s "${AUTH[@]}" -H "Content-Type: application/json; charset=utf-8" \
      -d "$(jq -n --arg n "$nome" '{name: $n, schema: [
        {key:"pendencia", name:"Pendência", type:"text", is_primary_column:true},
        {key:"responsavel", name:"Responsável", type:"user"},
        {key:"data_prevista", name:"Data prevista", type:"date"},
        {key:"status", name:"Status", type:"select", options:{choices:[
          {value:"aberto",    label:"Aberto",    color:"red"},
          {value:"fazendo",   label:"Fazendo",   color:"yellow"},
          {value:"concluido", label:"Concluído", color:"green"}]}},
        {key:"comentario", name:"Comentário", type:"text"}]}')" \
      "$API/slackLists.create")
    _checa "$resp"
    id=$(echo "$resp" | jq -r '.list_id')
    echo "lista \"$nome\" criada: $id" >&2
  fi
  resp=$(curl -s "${AUTH[@]}" -H "Content-Type: application/json; charset=utf-8" \
    -d "$(jq -n --arg l "$id" --arg c "$SLACK_CHANNEL_ID" \
          '{list_id:$l, access_level:"write", channel_ids:[$c]}')" \
    "$API/slackLists.access.set")
  _checa "$resp"
  local url
  url=$(curl -s "${AUTH[@]}" "$API/files.info?file=$id" | jq -r '.file.permalink')
  printf '%s\t%s\n' "$id" "$url"
}

lista_itens() {
  # imprime os itens da lista de pendências como JSON simplificado:
  # [{id, pendencia, responsavel: [U...], data_prevista, status, comentario}]
  local lid resp
  lid=$(_lista_id)
  resp=$(curl -s "${AUTH[@]}" -H "Content-Type: application/json; charset=utf-8" \
    -d "$(jq -n --arg l "$lid" '{list_id:$l, limit:100}')" \
    "$API/slackLists.items.list")
  _checa "$resp"
  echo "$resp" | jq '[.items[] | {
    id,
    pendencia:     ([.fields[] | select(.key=="pendencia").text]     | first // ""),
    responsavel:   ([.fields[] | select(.key=="responsavel").user]   | first // []),
    data_prevista: ([.fields[] | select(.key=="data_prevista").value] | first // ""),
    status:        ([.fields[] | select(.key=="status").value]       | first // ""),
    comentario:    ([.fields[] | select(.key=="comentario").text]    | first // "")
  }]'
}

_lista_schema() { # imprime o schema (colunas) da lista; $1 = list_id
  local resp
  resp=$(curl -s "${AUTH[@]}" "$API/files.info?file=$1")
  _checa "$resp"
  echo "$resp" | jq '.file.list_metadata.schema'
}

lista_criar_item() {
  # cria um item na lista de pendências (colunas resolvidas pelo schema, por chave)
  # uso: lista_criar_item "<pendência>" ["U1,U2"] ["AAAA-MM-DD"] [status] ["comentário"]
  local pend="$1" users="${2:-}" data="${3:-}" status="${4:-aberto}" coment="${5:-}"
  local lid schema payload resp
  lid=$(_lista_id)
  schema=$(_lista_schema "$lid")
  payload=$(jq -n --argjson s "$schema" --arg l "$lid" --arg p "$pend" \
      --arg u "$users" --arg d "$data" --arg st "$status" --arg c "$coment" '
    def col(k): ($s[] | select(.key==k) | .id);
    def rt(t): [{"type":"rich_text","elements":[{"type":"rich_text_section",
                 "elements":[{"type":"text","text":t}]}]}];
    {list_id: $l, initial_fields:
      ([{column_id: col("pendencia"), rich_text: rt($p)},
        {column_id: col("status"), select: [$st]}]
       + (if $u != "" then [{column_id: col("responsavel"), user: ($u | split(","))}] else [] end)
       + (if $d != "" then [{column_id: col("data_prevista"), date: [$d]}] else [] end)
       + (if $c != "" then [{column_id: col("comentario"), rich_text: rt($c)}] else [] end))}')
  resp=$(curl -s "${AUTH[@]}" -H "Content-Type: application/json; charset=utf-8" \
    -d "$payload" "$API/slackLists.items.create")
  _checa "$resp"
  echo "$resp" | jq -r '.item.id'
}

lista_url() {
  # imprime o permalink da lista de pendências
  local lid resp
  lid=$(_lista_id)
  resp=$(curl -s "${AUTH[@]}" "$API/files.info?file=$lid")
  _checa "$resp"
  echo "$resp" | jq -r '.file.permalink'
}

dm_arquivo() {
  # envia o arquivo por mensagem individual a cada usuário da lista (3º argumento
  # ou SLACK_DM_USER_IDS). "canal" = todos os membros humanos do canal. Falha em
  # um destinatário não interrompe os demais; exit 1 apenas se houve
  # destinatários e nenhuma DM saiu.
  local caminho="$1" comentario="${2:-}" ids="${3:-${SLACK_DM_USER_IDS:-}}"
  if [ "$ids" = "canal" ]; then
    ids=$(membros_canal)
    if [ -z "$ids" ]; then
      echo "ERRO: modo canal — nenhum membro humano encontrado no canal" >&2
      return 1
    fi
    echo "Modo canal: destinatarios ${ids}"
  fi
  if [ -z "$ids" ]; then
    echo "AVISO: SLACK_DM_USER_IDS vazio e nenhuma lista informada — nenhuma DM enviada" >&2
    return 0
  fi
  local enviadas=0 falhas=0 user canal
  IFS=',' read -ra _lista <<< "$ids"
  for user in "${_lista[@]}"; do
    user="${user//[[:space:]]/}"
    [ -z "$user" ] && continue
    if canal=$(_abrir_dm "$user") && (_upload "$canal" "$caminho" "$comentario"); then
      echo "DM enviada para ${user}"
      enviadas=$((enviadas + 1))
    else
      echo "AVISO: falha na DM para ${user} (scope im:write ausente ou ID invalido?)" >&2
      falhas=$((falhas + 1))
    fi
  done
  echo "DMs: ${enviadas} enviada(s), ${falhas} falha(s)"
  [ "$enviadas" -gt 0 ] || [ "$falhas" -eq 0 ]
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
  dm_arquivo)            dm_arquivo "$@" ;;
  membros_canal)         membros_canal ;;
  usuarios_canal)        usuarios_canal ;;
  lista_garantir)        lista_garantir ;;
  lista_itens)           lista_itens ;;
  lista_criar_item)      lista_criar_item "$@" ;;
  lista_url)             lista_url ;;
  ts)                    ts "$@" ;;
  *) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 1 ;;
esac
