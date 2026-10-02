---
description: Anexa documentos (arquivo ou pasta) a um orçamento em andamento e indica o que precisa ser revisto
argument-hint: <diretório da versão> <arquivo ou pasta> [...]
---
1. Rode `python -m motor.insumos importar $ARGUMENTS`.
2. Leia `insumos/indice.md` e resuma para Marcus o que entrou (arquivo, status, observações). Arquivos com status `visual` precisam de leitura das imagens em `insumos/paginas/` ou do original.
3. Carimbe o briefing (`python -m motor.estado carimbar <dv> briefing --agente chief-estimator`) e rode `python -m motor.estado status <dv>`.
4. Os nós que ficarem desatualizados voltam aos donos, começando pela `descoberta`: os novos documentos podem responder perguntas abertas ou mudar requisitos.
