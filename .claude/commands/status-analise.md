---
description: "[Squad de análise de dados] Mostra o estado da análise (nós, insights, portões, bloqueios)"
argument-hint: <pasta da versão>
---
> **Squad de análise de dados** · pasta `squad-analise/`. Rode os comandos do motor a partir dessa pasta (`cd squad-analise && python -m motor...`); caminhos relativos como `nos/`, `projetos/` e `conhecimento/` são relativos a ela. Leia `squad-analise/CLAUDE.md`. Neste repositório os agentes deste squad têm o prefixo `dados-`: quando o texto citar o agente `nome`, o agente registrado é `dados-nome`.

Rode `python -m motor.estado status $ARGUMENTS`, `python -m motor.insights checar $ARGUMENTS` e `python -m motor.validar $ARGUMENTS --fase D4` e resuma para Marcus: fase atual, nós pendentes com dono, insights por estado, bloqueios e próxima ação.
