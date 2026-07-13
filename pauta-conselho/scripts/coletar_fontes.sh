#!/usr/bin/env bash
# coletar_fontes.sh — coleta as fontes da pauta do Conselho:
#   1) a última pauta/ata de CONSELHO consolidada no canal (validada pelo conteúdo);
#   2) TODAS as pautas/atas de STAFF C-Level com data interna posterior à última
#      reunião de conselho (e anterior ao limite).
#
# Reutiliza a caixa de ferramentas de pauta-staff/scripts (slack.sh, validar_pauta.py,
# achar_pauta_anterior.sh).
#
# Uso:
#   ./pauta-conselho/scripts/coletar_fontes.sh [ANTES_DE_ISO]
#     ANTES_DE_ISO  limite superior exclusivo (padrão: hoje+1)
#
# Saída (stdout): JSON
#   {"conselho": {path,name,data_iso,...}, "staff": [{path,name,data_iso}, ...]}
# Arquivos baixados: /tmp/conselho_anterior.docx e /tmp/staff_fonte_<data>_<i>.docx
# Exit 3 se não houver pauta de conselho válida no canal.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS="$(cd "$DIR/../../pauta-staff/scripts" && pwd)"

ANTES_DE="${1:-$(python3 -c "import datetime;print((datetime.date.today()+datetime.timedelta(days=1)).isoformat())")}"

# 1) última pauta/ata de conselho
conselho_json=$("$TOOLS/achar_pauta_anterior.sh" "$ANTES_DE" /tmp/conselho_anterior.docx conselho)
data_conselho=$(echo "$conselho_json" | jq -r '.data_iso')
echo "conselho anterior: $(echo "$conselho_json" | jq -r '.name') ($data_conselho)" >&2

# 2) todas as pautas/atas de staff com data interna em (data_conselho, ANTES_DE)
staff_json="[]"
candidatos=$("$TOOLS/slack.sh" listar_arquivos_docx)
n=$(echo "$candidatos" | jq 'length')
i=0
while [ "$i" -lt "$n" ]; do
  name=$(echo "$candidatos" | jq -r ".[$i].name")
  url=$(echo "$candidatos" | jq -r ".[$i].url_private")
  tmp="/tmp/candidato_staff_$i.docx"
  if "$TOOLS/slack.sh" baixar "$url" "$tmp" >/dev/null 2>&1; then
    v=$(python3 "$TOOLS/validar_pauta.py" "$tmp" --tipo staff || true)
    if [ "$(echo "$v" | jq -r '.valido')" = "true" ]; then
      data=$(echo "$v" | jq -r '.data_iso')
      if [ "$data" \> "$data_conselho" ] && [ "$data" \< "$ANTES_DE" ]; then
        dest="/tmp/staff_fonte_${data}_${i}.docx"
        cp "$tmp" "$dest"
        staff_json=$(echo "$staff_json" | jq --arg p "$dest" --arg nm "$name" --arg d "$data" \
          '. + [{path:$p, name:$nm, data_iso:$d}]')
        echo "fonte staff: $name ($data)" >&2
      fi
    fi
  fi
  rm -f "$tmp"
  i=$((i+1))
done

# dedup por data interna (fica o mais recente por data, que aparece primeiro na
# listagem por ts desc) e ordena cronologicamente
staff_json=$(echo "$staff_json" | jq 'group_by(.data_iso) | map(.[0]) | sort_by(.data_iso)')

jq -n --argjson c "$conselho_json" --argjson s "$staff_json" '{conselho:$c, staff:$s}'
