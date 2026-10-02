# Estado do plano

Cada ciclo é um conjunto de nós JSON em `nos/`, cada um com dono, fase e dependências. O carimbo guarda o hash das entradas usadas; se uma entrada muda, o nó aparece como **desatualizado** em `python -m motor.estado status`.

| Nó | Dono | Fase | Depende de |
|---|---|---|---|
| `meta` | chief-strategist | E0 | — |
| `briefing` | chief-strategist | E0 | meta |
| `enquadramento` | enquadramento | E0 | briefing |
| `mercado` | inteligencia-mercado | E1 | enquadramento |
| `concorrencia` | concorrencia | E1 | enquadramento |
| `regulatorio` | regulatorio-fomento | E1 | enquadramento |
| `interno` | desempenho-interno | E1 | enquadramento |
| `capacidades` | capacidades-organizacao | E1 | enquadramento |
| `diagnostico` | chief-strategist | E1 | mercado, concorrencia, regulatorio, interno, capacidades |
| `opcoes` | arquiteto-estrategia | E2 | diagnostico |
| `portfolio` | portfolio-iniciativas | E2 | diagnostico, opcoes |
| `financeiro_opcoes` | financeiro-estrategico | E2 | opcoes, portfolio, interno |
| `okrs` | okr-kpi | E3 | diagnostico, opcoes |
| `organizacao` | capacidades-organizacao | E3 | opcoes, capacidades, okrs |
| `iniciativas` | portfolio-iniciativas | E3 | opcoes, portfolio, okrs, organizacao |
| `financeiro` | financeiro-estrategico | E3 | opcoes, portfolio, interno, organizacao, iniciativas |
| `riscos` | riscos-governanca | E3 | opcoes, iniciativas, financeiro |
| `governanca` | riscos-governanca | E3 | okrs, riscos, opcoes |

## Convenções
- Evidências ficam nos nós de diagnóstico (`mercado`, `concorrencia`, `regulatorio`, `interno`, `capacidades`), com prefixos `MKT`, `CON`, `REG`, `INT`, `CAP`. As análises citam os ids.
- Modelo financeiro (opções e cenários): `anos`, `caixa_inicial`, `impostos_receita_pct`, `linhas` (receita por ano e margem bruta), `despesas`, `pessoal_anual` (opcional; no plano, o pessoal vem de `organizacao`), `capex`, `fomento` e `captacao` com mês e status.
- Percentuais como frações. Meses `AAAA-MM`. Perfis com os nomes da planilha de capacidade.
- Nó não preenchido contém `"_template": true`; o dono remove a chave ao preencher.
- No modo estudo, só os nós até `financeiro_opcoes` são obrigatórios.
