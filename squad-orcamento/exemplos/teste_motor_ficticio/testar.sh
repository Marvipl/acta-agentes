#!/usr/bin/env bash
# Teste do motor com dados FICTÍCIOS. Não altera a base real (usa a base do exemplo).
set -e
cd "$(dirname "$0")/../.."
EX=exemplos/teste_motor_ficticio
export SQUAD_CONHECIMENTO=$EX/conhecimento
rm -rf $EX/v1/saidas $EX/v1/revisoes $EX/v1/controle.json $EX/v1/estado.json
mkdir -p $EX/v1/saidas $EX/v1/revisoes
for n in meta briefing especificacao requisitos escopo solucao operacoes cronograma bom tributos custos_indiretos riscos preco contrato financeiro; do
  python -m motor.estado carimbar $EX/v1 $n --agente teste > /dev/null
done
python -m motor.estado aprovar $EX/v1 --gate G1 --por teste > /dev/null
python -m motor.estado aprovar $EX/v1 --gate G2 --por teste > /dev/null
python -m motor.rodar $EX/v1
echo "--- validação (o bloqueio do item B02 é esperado: benchmark em item crítico no modo completo)"
python -m motor.prontidao $EX/v1 || true
python -m motor.validar $EX/v1 --fase F4 || true
