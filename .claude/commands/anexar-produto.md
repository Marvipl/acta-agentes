---
description: "[Squad de produto] Anexa documentos (arquivo ou pasta) à especificação em andamento"
argument-hint: <diretório da versão> <arquivo ou pasta> [...]
---
> **Squad de produto** · pasta `squad-produto/`. Rode os comandos do motor a partir dessa pasta (`cd squad-produto && python -m motor...`); caminhos relativos como `nos/`, `projetos/` e `conhecimento/` são relativos a ela. Leia `squad-produto/CLAUDE.md`. Neste repositório os agentes deste squad têm o prefixo `prod-`: quando o texto citar o agente `nome`, o agente registrado é `prod-nome`.

1. Rode `python -m motor.insumos importar $ARGUMENTS`.
2. Resuma para Marcus o que entrou e o que não pôde ser lido (`insumos/indice.md`).
3. Carimbe o briefing (`python -m motor.estado carimbar <dv> briefing --agente chief-produto`) e rode `python -m motor.estado status <dv>`. Os nós desatualizados voltam aos donos.
