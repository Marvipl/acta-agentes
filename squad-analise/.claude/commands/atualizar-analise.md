---
description: Refaz uma análise com dados novos de mesma estrutura e mostra o que mudou
argument-hint: <pasta da versão anterior> <pasta dos dados novos>
---
1. `python -m motor.estado nova-versao <dv anterior> --motivo "dados novos"` → `<dv novo>`.
2. `python -m motor.ingestao importar <dv novo> <dados novos>` e `python -m motor.perfil <dv novo>`; peça ao `qualidade-privacidade` para conferir se a estrutura e a qualidade continuam iguais.
3. `python -m motor.rodar <dv novo>` e `python -m motor.comparar <dv anterior> <dv novo>`.
4. Mostre a Marcus `saidas/comparacao.md`: o que mudou além da incerteza. Insights afetados voltam para o red team analítico; siga a skill `analisar` a partir da D3.
