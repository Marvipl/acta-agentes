---
description: "[Squad de produto] Registra resultado de experimento ou compara premissas com o realizado após o lançamento"
argument-hint: <diretório da versão> [experimento|lancamento]
---
> **Squad de produto** · pasta `squad-produto/`. Rode os comandos do motor a partir dessa pasta (`cd squad-produto && python -m motor...`); caminhos relativos como `nos/`, `projetos/` e `conhecimento/` são relativos a ela. Leia `squad-produto/CLAUDE.md`. Neste repositório os agentes deste squad têm o prefixo `prod-`: quando o texto citar o agente `nome`, o agente registrado é `prod-nome`.

Siga a skill `revisao-produto` em `squad-produto/.claude/skills/revisao-produto/SKILL.md` para: $ARGUMENTS

**Publicação automática: passo final obrigatório, sem esperar novo pedido.** Assim que a versão for congelada (ou, se o fluxo não congelar, assim que Marcus aprovar o último portão), publique:
- na nuvem (variável de ambiente `CLAUDE_CODE_REMOTE=true`): siga `.claude/commands/publicar-drive.md` com `squad-produto` e a pasta da versão, enviando o pacote completo (documentos finais e metadados) para `Acta > Produtos`. Se o conector do Google Drive não estiver habilitado na sessão, peça a Marcus para habilitar e publique logo em seguida;
- no computador: `cd squad-produto && python -m motor.publicar <pasta da versão>`.
Termine a resposta final com o link da pasta no Drive e o total de arquivos publicados.
