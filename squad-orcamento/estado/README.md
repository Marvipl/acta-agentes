# Estado do orçamento

Cada orçamento é um conjunto de nós JSON em `nos/`. Cada nó tem um dono, uma fase e dependências. O carimbo de um nó guarda o hash das entradas que ele usou; se uma entrada muda depois, o nó aparece como **desatualizado** em `python -m motor.estado status`, e só ele (e o que depende dele) precisa ser refeito.

| Nó | Dono | Fase | Depende de |
|---|---|---|---|
| `meta` | chief-estimator | F0 | — |
| `briefing` | chief-estimator | F0 | meta |
| `especificacao` | descoberta | F0 | briefing |
| `requisitos` | requisitos | F0 | briefing, especificacao |
| `escopo` | chief-estimator | F1 | requisitos |
| `solucao` | engenharia-robotica | F1 | requisitos, escopo |
| `operacoes` | operacoes-posvenda | F1 | solucao |
| `cronograma` | gestao-projetos | F2 | escopo, solucao, operacoes |
| `bom` | suprimentos | F2 | solucao |
| `tributos` | tributario | F3 | meta, solucao, bom |
| `custos_indiretos` | cost-engineering | F3 | solucao, bom, cronograma, operacoes |
| `riscos` | contratos-riscos | F3 | escopo, solucao, bom, cronograma |
| `preco` | comercial-pricing | F4 | requisitos, solucao, operacoes, cronograma, bom, tributos, custos_indiretos, riscos |
| `contrato` | contratos-riscos | F4 | cronograma, preco, riscos |
| `financeiro` | financeiro | F4 | preco, contrato |

## Convenções
- Incerteza em 3 pontos: `{"min", "provavel", "max"}`.
- Fonte: `{"tipo": "cotacao|base_interna|benchmark|premissa", "ref": "...", "data": "AAAA-MM-DD", "validade_dias": n}` (BOM) ou texto com origem e data (demais nós).
- Percentuais como frações (0.15 = 15%). Datas `AAAA-MM-DD`; meses `AAAA-MM`.
- Perfis de esforço com o nome exato de `conhecimento/mao_de_obra/custo_hora.csv`.
- Toda atividade do cronograma lista os `wbs_ids` que cobre; esforço e BOM se ligam ao cronograma pelo `wbs_id`.
- `especificacao`: status por dimensão (`conhecimento/descoberta/dimensoes.csv`) e perguntas-chave; a nota de prontidão sai de `python -m motor.prontidao <dv>`.
- Nó ainda não preenchido contém `"_template": true`; o dono remove a chave ao preencher.

## Modo rápido
No modo rápido, nós sem especialista dedicado são preenchidos em versão simplificada por outro agente (ver skill `orcar`). O carimbo registra quem preencheu.
