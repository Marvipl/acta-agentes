#!/usr/bin/env bash
# Consolida uma branch claude/* no main.
#
# Faz o merge direto no main e apaga a branch. Conflito com o main, ou mudança
# em .github/workflows (o token das Actions não pode gravá-la), vira PR para
# Marcus resolver. Com REVISAR_CODIGO=true, mudanças de código (motor, scripts,
# ferramentas) também viram PR em vez de entrar direto.
#
# Uso: consolidar.sh <branch>
set -uo pipefail

BRANCH="${1:?informe a branch}"
BASE="${BASE:-main}"

case "$BRANCH" in
  claude/*) ;;
  *) echo "Ignorando $BRANCH: só branches claude/* são consolidadas."; exit 0 ;;
esac

resumo() { echo "$1" | tee -a "${GITHUB_STEP_SUMMARY:-/dev/null}"; }

# Caminhos que contam como código e por isso exigem revisão.
eh_codigo() {
  case "$1" in
    */motor/*|motor/*) return 0 ;;
    ferramentas/*|.github/*) return 0 ;;
    .claude/settings*.json|.mcp.json) return 0 ;;
    *requirements*.txt|*package.json|*package-lock.json) return 0 ;;
    *.py|*.js|*.mjs|*.cjs|*.ts|*.sh|*.ps1|*.bat|*.cmd) return 0 ;;
  esac
  return 1
}

git fetch -q origin "$BASE" "refs/heads/$BRANCH:refs/remotes/origin/$BRANCH" || {
  echo "Branch $BRANCH não existe mais."; exit 0; }

TIP=$(git rev-parse "origin/$BRANCH")

apagar_branch() {
  # Só apaga se ninguém empurrou nada novo desde o merge.
  git push -q --force-with-lease="refs/heads/$BRANCH:$TIP" origin ":refs/heads/$BRANCH" \
    && resumo "Branch $BRANCH apagada." \
    || resumo "Branch $BRANCH recebeu commits novos; mantida."
}

if [ "$(git rev-list --count "origin/$BASE..$TIP")" = 0 ]; then
  resumo "$BRANCH já está no $BASE."
  [ "${APAGAR_BRANCH:-true}" = true ] && apagar_branch
  exit 0
fi

mapfile -t ARQUIVOS < <(git diff --name-only "origin/$BASE...$TIP")
CODIGO=()
for f in "${ARQUIVOS[@]}"; do eh_codigo "$f" && CODIGO+=("$f"); done

abrir_pr() {
  local motivo="$1"
  local existente
  existente=$(gh pr list --head "$BRANCH" --base "$BASE" --state open --json number --jq '.[0].number' 2>/dev/null)
  local corpo="Consolidação automática da branch \`$BRANCH\` no \`$BASE\`.

**Por que não foi mergeada direto:** $motivo"
  if [ "${REVISAR_CODIGO:-false}" = true ] && [ ${#CODIGO[@]} -gt 0 ]; then
    corpo+="

Arquivos de código alterados:
$(printf -- '- `%s`\n' "${CODIGO[@]:0:50}")"
  fi
  corpo+="

Ao aprovar, faça o merge deste PR."
  if [ -n "$existente" ]; then
    gh pr comment "$existente" --body "Novos commits em \`$BRANCH\`. $motivo" >/dev/null 2>&1 || true
    resumo "PR #$existente atualizado para revisão: $motivo"
  else
    local titulo
    titulo=$(git log -1 --format=%s "$TIP")
    if gh pr create --base "$BASE" --head "$BRANCH" --title "[revisar] $titulo" --body "$corpo" >/dev/null; then
      resumo "PR aberto para revisão de $BRANCH: $motivo"
    else
      resumo "Não consegui abrir o PR de $BRANCH (veja a permissão de PRs das Actions). Motivo: $motivo"
    fi
  fi
}

if [ "${REVISAR_CODIGO:-false}" = true ] && [ ${#CODIGO[@]} -gt 0 ]; then
  abrir_pr "a branch altera código (${#CODIGO[@]} arquivo(s))."
  exit 0
fi

git config user.name "acta-consolidacao"
git config user.email "acta-consolidacao@users.noreply.github.com"

for tentativa in 1 2 3; do
  git fetch -q origin "$BASE"
  git checkout -q -B "$BASE" "origin/$BASE"
  ANTES=$(git rev-parse "origin/$BASE")
  if ! git merge -q --no-ff "$TIP" -m "Consolida $BRANCH no $BASE" -m "$(git log -1 --format=%s "$TIP")"; then
    git merge --abort 2>/dev/null
    abrir_pr "conflito com o $BASE."
    exit 0
  fi
  if git push -q origin "$BASE"; then
    resumo "$BRANCH consolidada no $BASE (${#ARQUIVOS[@]} arquivo(s))."
    [ "${APAGAR_BRANCH:-true}" = true ] && apagar_branch
    exit 0
  fi
  git fetch -q origin "$BASE"
  if [ "$(git rev-parse "origin/$BASE")" = "$ANTES" ]; then
    # O main não mudou: o push foi recusado (por exemplo, a branch altera
    # .github/workflows). Fica para Marcus mergear.
    abrir_pr "o GitHub recusou o push automático no $BASE (mudanças em workflows só entram por PR)."
    exit 0
  fi
  echo "O $BASE mudou durante o merge; tentando de novo ($tentativa)."
  sleep $((tentativa * 3))
done

resumo "Não consegui empurrar o merge de $BRANCH para o $BASE."
exit 1
