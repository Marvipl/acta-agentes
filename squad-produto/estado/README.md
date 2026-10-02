# Estado da especificação

Nós JSON em `nos/`, cada um com dono, fase e dependências. O carimbo guarda o hash das entradas; se uma entrada muda, o nó aparece como **desatualizado**.

| Nó | Dono | Fase | Depende de |
|---|---|---|---|
| `meta` | chief-produto | P0 | — |
| `briefing` | chief-produto | P0 | meta |
| `enquadramento` | enquadramento | P0 | briefing |
| `mercado` | pesquisa-mercado | P1 | enquadramento |
| `clientes` | pesquisa-cliente | P1 | enquadramento |
| `concorrencia` | analise-concorrencial | P1 | enquadramento |
| `normas` | regulatorio-normas | P1 | enquadramento |
| `oportunidade` | estrategista-produto | P1 | mercado, clientes, concorrencia, normas |
| `conceitos` | estrategista-produto | P2 | oportunidade, concorrencia, clientes |
| `requisitos` | requisitos-produto | P2 | conceitos, clientes, normas, concorrencia |
| `arquitetura` | arquiteto-solucao | P3 | conceitos, requisitos |
| `negocio` | pricing-negocio | P3 | conceitos, clientes, mercado, arquitetura |
| `validacao` | validacao-experimentos | P3 | oportunidade, conceitos, requisitos, arquitetura, negocio |
| `roadmap` | roadmap-gtm | P3 | requisitos, arquitetura, validacao, negocio |

## Convenções
- Evidências nos nós de descoberta com prefixos `MKT`, `CLI`, `CON`, `NOR`.
- Benchmark (`concorrencia`): `especificacoes` (unidade e direção) e `produtos[].specs` com valor normalizado e evidência; requisitos comparáveis apontam para a especificação em `especificacao_ref`.
- Requisitos citam em `origem` ids de JTBD, dor, ganho, norma ou evidência.
- Percentuais como frações; meses `AAAA-MM`; incerteza em 3 pontos.
- No modo oportunidade, só os nós até `conceitos` e `negocio` são obrigatórios.
