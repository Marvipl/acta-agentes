---
description: "[Squad de produto] Mostra o estado da especificação (nós, desatualizados, portões, bloqueios)"
argument-hint: <diretório da versão>
---
> **Squad de produto** · pasta `squad-produto/`. Rode os comandos do motor a partir dessa pasta (`cd squad-produto && python -m motor...`); caminhos relativos como `nos/`, `projetos/` e `conhecimento/` são relativos a ela. Leia `squad-produto/CLAUDE.md`. Neste repositório os agentes deste squad têm o prefixo `prod-`: quando o texto citar o agente `nome`, o agente registrado é `prod-nome`.

Rode `python -m motor.estado status $ARGUMENTS` e `python -m motor.validar $ARGUMENTS --fase P4` e resuma para Marcus: fase atual, nós pendentes ou desatualizados com o dono de cada um, bloqueios e próxima ação.
