---
description: "[Squad de estratégia] Revisão trimestral do plano estratégico congelado"
argument-hint: <diretório da versão> <T1|T2|T3|T4>
---
> **Squad de estratégia** · pasta `squad-estrategia/`. Rode os comandos do motor a partir dessa pasta (`cd squad-estrategia && python -m motor...`); caminhos relativos como `nos/`, `projetos/` e `conhecimento/` são relativos a ela. Leia `squad-estrategia/CLAUDE.md`. Neste repositório os agentes deste squad têm o prefixo `est-`: quando o texto citar o agente `nome`, o agente registrado é `est-nome`.

Siga a skill `revisao-trimestral` em `squad-estrategia/.claude/skills/revisao-trimestral/SKILL.md` para: $ARGUMENTS

**Publicação automática: passo final obrigatório, sem esperar novo pedido.** Assim que a versão for congelada (ou, se o fluxo não congelar, assim que Marcus aprovar o último portão), publique:
- na nuvem (variável de ambiente `CLAUDE_CODE_REMOTE=true`): siga `.claude/commands/publicar-drive.md` com `squad-estrategia` e a pasta da versão, enviando o pacote completo (documentos finais e metadados) para `Acta > Planejamento Estratégico`. Se não houver `ACTA_DRIVE_CREDENCIAL` nem conector do Google Drive habilitado na sessão, peça a Marcus para habilitar e publique logo em seguida;
- no computador: `cd squad-estrategia && python -m motor.publicar <pasta da versão>`.
Termine a resposta final com o link da pasta no Drive e o total de arquivos publicados.
