---
description: "[Squad de estratégia] Inicia o planejamento estratégico (plano) ou o estudo de uma decisão (estudo)"
argument-hint: <plano|estudo> "<ciclo>" "<título>" [pastas ou arquivos] [pergunta ou contexto]
---
> **Squad de estratégia** · pasta `squad-estrategia/`. Rode os comandos do motor a partir dessa pasta (`cd squad-estrategia && python -m motor...`); caminhos relativos como `nos/`, `projetos/` e `conhecimento/` são relativos a ela. Leia `squad-estrategia/CLAUDE.md`. Neste repositório os agentes deste squad têm o prefixo `est-`: quando o texto citar o agente `nome`, o agente registrado é `est-nome`.

Siga a skill `estrategia` em `squad-estrategia/.claude/skills/estrategia/SKILL.md` com os argumentos: $ARGUMENTS

**Publicação automática: passo final obrigatório, sem esperar novo pedido.** Assim que a versão for congelada (ou, se o fluxo não congelar, assim que Marcus aprovar o último portão), publique:
- na nuvem (variável de ambiente `CLAUDE_CODE_REMOTE=true`): siga `.claude/commands/publicar-drive.md` com `squad-estrategia` e a pasta da versão, enviando o pacote completo (documentos finais e metadados) para `Acta > Planejamento Estratégico`. Se o conector do Google Drive não estiver habilitado na sessão, peça a Marcus para habilitar e publique logo em seguida;
- no computador: `cd squad-estrategia && python -m motor.publicar <pasta da versão>`.
Termine a resposta final com o link da pasta no Drive e o total de arquivos publicados.
