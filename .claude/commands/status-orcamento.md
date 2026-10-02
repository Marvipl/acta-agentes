---
description: "[Squad de orçamento] Mostra o estado de um orçamento (nós, desatualizações, aprovações e bloqueios)"
argument-hint: <diretório da versão>
---
> **Squad de orçamento** · pasta `squad-orcamento/`. Rode os comandos do motor a partir dessa pasta (`cd squad-orcamento && python -m motor...`); caminhos relativos como `nos/`, `projetos/` e `conhecimento/` são relativos a ela. Leia `squad-orcamento/CLAUDE.md`. Neste repositório os agentes deste squad têm o prefixo `orc-`: quando o texto citar o agente `nome`, o agente registrado é `orc-nome`.

Rode `python -m motor.estado status $ARGUMENTS` e `python -m motor.validar $ARGUMENTS --fase F6` e resuma para Marcus: fase atual, nós pendentes ou desatualizados com o dono de cada um, bloqueios e próxima ação.
