#!/usr/bin/env bash
# achar_pauta_anterior.sh — localiza no canal o arquivo da ÚLTIMA reunião de
# Staff C-Level, validando pelo CONTEÚDO (título Staff/C-Level + data interna),
# e não apenas pelo nome ou pela ordem de upload.
#
# Uso:
#   ./scripts/achar_pauta_anterior.sh [ANTES_DE_ISO] [DESTINO] [TIPO]
#     ANTES_DE_ISO  limite superior exclusivo para a data interna (padrão: hoje+1).
#                   Na rotina de terça, passe a data da PRÓXIMA quarta para
#                   garantir que a pauta desta semana (se existir) seja ignorada.
#     DESTINO       caminho do arquivo baixado (padrão: /tmp/pauta_anterior.docx)
#     TIPO          staff (padrão) ou conselho — critério de validação do título
#
# Saída (stdout): JSON {"path", "name", "data_iso", "data_texto"} do escolhido.
# Exit 3 se nenhum candidato válido for encontrado.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ANTES_DE="${1:-$(python3 -c "import datetime;print((datetime.date.today()+datetime.timedelta(days=1)).isoformat())")}"
DESTINO="${2:-/tmp/pauta_anterior.docx}"
TIPO="${3:-staff}"

melhor_json=""
melhor_data=""
melhor_ts=""

candidatos=$("$DIR/slack.sh" listar_arquivos_docx)
n=$(echo "$candidatos" | jq 'length')
[ "$n" -eq 0 ] && { echo "Nenhum .docx no canal" >&2; exit 3; }

for i in $(seq 0 $((n-1))); do
  name=$(echo "$candidatos" | jq -r ".[$i].name")
  url=$(echo "$candidatos" | jq -r ".[$i].url_private")
  ts=$(echo "$candidatos" | jq -r ".[$i].ts")
  tmp="/tmp/candidato_$i.docx"
  if ! "$DIR/slack.sh" baixar "$url" "$tmp" >/dev/null 2>&1; then
    echo "AVISO: falha ao baixar $name — pulando" >&2
    continue
  fi
  v=$(python3 "$DIR/validar_pauta.py" "$tmp" --tipo "$TIPO" || true)
  valido=$(echo "$v" | jq -r '.valido')
  data=$(echo "$v" | jq -r '.data_iso // empty')
  if [ "$valido" != "true" ]; then
    echo "descartado: $name ($(echo "$v" | jq -r '.motivo'))" >&2
    rm -f "$tmp"; continue
  fi
  if [ "$data" \>= "$ANTES_DE" ]; then
    echo "descartado: $name (data interna $data >= limite $ANTES_DE)" >&2
    rm -f "$tmp"; continue
  fi
  # escolhe a maior data interna; empate -> upload mais recente
  if [ -z "$melhor_data" ] || [ "$data" \> "$melhor_data" ] || \
     { [ "$data" = "$melhor_data" ] && [ "$(echo "$ts > $melhor_ts" | bc)" = "1" ]; }; then
    melhor_data="$data"; melhor_ts="$ts"
    cp "$tmp" "$DESTINO"
    melhor_json=$(echo "$v" | jq --arg p "$DESTINO" --arg n "$name" '. + {path:$p, name:$n}')
  fi
  rm -f "$tmp"
done

[ -z "$melhor_json" ] && { echo "Nenhuma pauta/ata valida do tipo $TIPO encontrada" >&2; exit 3; }
echo "$melhor_json"
