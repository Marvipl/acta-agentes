---
description: "[Squad de orçamento] Inicia um orçamento com o squad (modo rapido ou completo)"
argument-hint: <rapido|completo> "<cliente>" "<projeto>" [pasta ou arquivos] [texto do pedido]
---
> **Squad de orçamento** · pasta `squad-orcamento/`. Rode os comandos do motor a partir dessa pasta (`cd squad-orcamento && python -m motor...`); caminhos relativos como `nos/`, `projetos/` e `conhecimento/` são relativos a ela. Leia `squad-orcamento/CLAUDE.md`. Neste repositório os agentes deste squad têm o prefixo `orc-`: quando o texto citar o agente `nome`, o agente registrado é `orc-nome`.

Siga a skill `orcar` em `squad-orcamento/.claude/skills/orcar/SKILL.md` com os argumentos: $ARGUMENTS

**Publicação automática: passo final obrigatório, sem esperar novo pedido.** Assim que a versão for congelada (ou, se o fluxo não congelar, assim que Marcus aprovar o último portão), publique:
- na nuvem (variável de ambiente `CLAUDE_CODE_REMOTE=true`): siga `.claude/commands/publicar-drive.md` com `squad-orcamento` e a pasta da versão, enviando o pacote completo (documentos finais e metadados) para `Acta > Orçamentos`. Se não houver `ACTA_DRIVE_CREDENCIAL` nem conector do Google Drive habilitado na sessão, peça a Marcus para habilitar e publique logo em seguida;
- no computador: `cd squad-orcamento && python -m motor.publicar <pasta da versão>`.
Termine a resposta final com o link da pasta no Drive e o total de arquivos publicados.
