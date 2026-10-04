---
description: "[Squad de produto] Inicia a especificação de um produto (completo) ou a avaliação de uma oportunidade (oportunidade)"
argument-hint: <completo|oportunidade> "<segmento>" "<produto>" [pastas ou arquivos] [contexto]
---
> **Squad de produto** · pasta `squad-produto/`. Rode os comandos do motor a partir dessa pasta (`cd squad-produto && python -m motor...`); caminhos relativos como `nos/`, `projetos/` e `conhecimento/` são relativos a ela. Leia `squad-produto/CLAUDE.md`. Neste repositório os agentes deste squad têm o prefixo `prod-`: quando o texto citar o agente `nome`, o agente registrado é `prod-nome`.

Siga a skill `produto` em `squad-produto/.claude/skills/produto/SKILL.md` com os argumentos: $ARGUMENTS

**Publicação automática: passo final obrigatório, sem esperar novo pedido.** Assim que a versão for congelada (ou, se o fluxo não congelar, assim que Marcus aprovar o último portão), publique:
- na nuvem (variável de ambiente `CLAUDE_CODE_REMOTE=true`): siga `.claude/commands/publicar-drive.md` com `squad-produto` e a pasta da versão, enviando o pacote completo (documentos finais e metadados) para `Acta > Produtos`. Se não houver `ACTA_DRIVE_CREDENCIAL` nem conector do Google Drive habilitado na sessão, peça a Marcus para habilitar e publique logo em seguida;
- no computador: `cd squad-produto && python -m motor.publicar <pasta da versão>`.
Termine a resposta final com o link da pasta no Drive e o total de arquivos publicados.
