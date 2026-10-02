---
description: "[Squad de análise de dados] Refaz uma análise com dados novos de mesma estrutura e mostra o que mudou"
argument-hint: <pasta da versão anterior> <pasta dos dados novos>
---
> **Squad de análise de dados** · pasta `squad-analise/`. Rode os comandos do motor a partir dessa pasta (`cd squad-analise && python -m motor...`); caminhos relativos como `nos/`, `projetos/` e `conhecimento/` são relativos a ela. Leia `squad-analise/CLAUDE.md`. Neste repositório os agentes deste squad têm o prefixo `dados-`: quando o texto citar o agente `nome`, o agente registrado é `dados-nome`.

1. `python -m motor.estado nova-versao <dv anterior> --motivo "dados novos"` → `<dv novo>`.
2. `python -m motor.ingestao importar <dv novo> <dados novos>` e `python -m motor.perfil <dv novo>`; peça ao `qualidade-privacidade` para conferir se a estrutura e a qualidade continuam iguais.
3. `python -m motor.rodar <dv novo>` e `python -m motor.comparar <dv anterior> <dv novo>`.
4. Mostre a Marcus `saidas/comparacao.md`: o que mudou além da incerteza. Insights afetados voltam para o red team analítico; siga a skill `analisar` a partir da D3.
