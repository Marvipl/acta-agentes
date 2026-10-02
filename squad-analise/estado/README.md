# Estado da análise

Nós JSON em `nos/` com dono, fase e dependências (carimbo e desatualização como nos outros squads). Além deles:

- `etapas/NN_nome.sql|py`: preparação; só cria tabelas `prep_*` a partir de `base_*`.
- `analises/ANA-xxx.py`: uma análise registrada no plano, com `rodar(con, ctx)` devolvendo valores, tabelas e notas.
- `evidencias/INS-xxx.json`: livro de evidências, um registro por insight, com estado.

| Nó | Dono | Fase | Depende de |
|---|---|---|---|
| `meta` | orquestrador | D0 | — |
| `briefing` | orquestrador | D0 | meta |
| `decisao` | arquiteto-da-decisao | D0 | briefing |
| `contrato` | engenheiro-de-dados | D1 | decisao |
| `especialista` | perfilador-setorial | D1 | decisao, contrato |
| `qualidade` | qualidade-privacidade | D1 | contrato, especialista |
| `plano` | planejador-analitico | D2 | decisao, contrato, especialista, qualidade |
| `impacto` | analista-de-impacto | D4 | decisao, plano |

## Insight (evidencias/INS-xxx.json)

```json
{
  "id": "INS-001",
  "estado": "descoberto|quantificado|validado|acionavel|aprovado",
  "afirmacao": "texto com {{v.apelido}}",
  "pergunta_ref": "P1",
  "criterio_ref": "CR1",
  "valores": {
    "apelido": "ANA-001.chave"
  },
  "nivel": "descritivo|associativo|causal",
  "robustez": [
    {
      "recorte": "",
      "analise": "",
      "resultado": "passa|falha|parcial",
      "nota": ""
    }
  ],
  "confirmacao": {
    "analise": "",
    "resultado": "confirma|nao_confirma"
  },
  "red_team_analitico": {
    "veredito": "sobrevive|ressalva|cai",
    "nota": ""
  },
  "impacto": {
    "modelo": "IMP-001"
  },
  "acao": "",
  "dono": "",
  "premissas": [
    ""
  ],
  "red_team_decisao": {
    "veredito": "",
    "nota": ""
  },
  "confianca": "alta|media|baixa",
  "historico": []
}
```
