---
description: "[Squad de análise de dados] Anexa documentos (arquivo ou pasta) à análise em andamento (documentos de apoio; dados entram pela ingestão)"
argument-hint: <diretório da versão> <arquivo ou pasta> [...]
---
> **Squad de análise de dados** · pasta `squad-analise/`. Rode os comandos do motor a partir dessa pasta (`cd squad-analise && python -m motor...`); caminhos relativos como `nos/`, `projetos/` e `conhecimento/` são relativos a ela. Leia `squad-analise/CLAUDE.md`. Neste repositório os agentes deste squad têm o prefixo `dados-`: quando o texto citar o agente `nome`, o agente registrado é `dados-nome`.

1. Rode `python -m motor.insumos importar $ARGUMENTS`.
2. Resuma para Marcus o que entrou e o que não pôde ser lido (`insumos/indice.md`).
3. Carimbe o briefing (`python -m motor.estado carimbar <dv> briefing --agente orquestrador`) e rode `python -m motor.estado status <dv>`. Os nós desatualizados voltam aos donos.
