---
description: "[Squad de estratégia] Mostra o estado do plano ou estudo (nós, desatualizados, portões, bloqueios)"
argument-hint: <diretório da versão>
---
> **Squad de estratégia** · pasta `squad-estrategia/`. Rode os comandos do motor a partir dessa pasta (`cd squad-estrategia && python -m motor...`); caminhos relativos como `nos/`, `projetos/` e `conhecimento/` são relativos a ela. Leia `squad-estrategia/CLAUDE.md`. Neste repositório os agentes deste squad têm o prefixo `est-`: quando o texto citar o agente `nome`, o agente registrado é `est-nome`.

Rode `python -m motor.estado status $ARGUMENTS` e `python -m motor.validar $ARGUMENTS --fase E4` e resuma para Marcus: fase atual, nós pendentes ou desatualizados com o dono de cada um, bloqueios e próxima ação.
