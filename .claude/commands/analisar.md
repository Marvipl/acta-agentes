---
description: "[Squad de análise de dados] Inicia uma análise de dados para um objetivo de negócio"
argument-hint: <rapido|padrao|completo> "<objetivo>" <pasta dos dados>
---
> **Squad de análise de dados** · pasta `squad-analise/`. Rode os comandos do motor a partir dessa pasta (`cd squad-analise && python -m motor...`); caminhos relativos como `nos/`, `projetos/` e `conhecimento/` são relativos a ela. Leia `squad-analise/CLAUDE.md`. Neste repositório os agentes deste squad têm o prefixo `dados-`: quando o texto citar o agente `nome`, o agente registrado é `dados-nome`.

Siga a skill `analisar` em `squad-analise/.claude/skills/analisar/SKILL.md` com os argumentos: $ARGUMENTS

**Publicação automática: passo final obrigatório, sem esperar novo pedido.** Assim que a versão for congelada (ou, se o fluxo não congelar, assim que Marcus aprovar o último portão), publique:
- na nuvem (variável de ambiente `CLAUDE_CODE_REMOTE=true`): siga `.claude/commands/publicar-drive.md` com `squad-analise` e a pasta da versão, enviando o pacote completo (documentos finais e metadados) para `Acta > Análises`. Se não houver `ACTA_DRIVE_CREDENCIAL` nem conector do Google Drive habilitado na sessão, peça a Marcus para habilitar e publique logo em seguida;
- no computador: `cd squad-analise && python -m motor.publicar <pasta da versão>`.
Termine a resposta final com o link da pasta no Drive e o total de arquivos publicados.
