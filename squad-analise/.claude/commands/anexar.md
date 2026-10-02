---
description: Anexa documentos (arquivo ou pasta) à análise em andamento (documentos de apoio; dados entram pela ingestão)
argument-hint: <diretório da versão> <arquivo ou pasta> [...]
---
1. Rode `python -m motor.insumos importar $ARGUMENTS`.
2. Resuma para Marcus o que entrou e o que não pôde ser lido (`insumos/indice.md`).
3. Carimbe o briefing (`python -m motor.estado carimbar <dv> briefing --agente orquestrador`) e rode `python -m motor.estado status <dv>`. Os nós desatualizados voltam aos donos.
