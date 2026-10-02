# Base de conhecimento do squad de estratégia

Toda afirmação externa precisa de fonte, data e classificação (`confirmado`, `reportado`, `estimativa`, `interno`). Ver `fontes/regras_fontes.md`.

| Pasta / arquivo | Conteúdo | Quem mantém |
|---|---|---|
| `contexto/acta.md` | Contexto da empresa e trabalho em andamento do plano 2027 | Chief Strategist + Marcus |
| `fontes/regras_fontes.md` | Classificação e qualidade de fontes; pontos cegos conhecidos | Chief Strategist |
| `metodologia/frameworks.md` | Escolhas estratégicas, hipóteses, TOWS, portfólio, OKRs, pré-mortem | Chief Strategist |
| `enquadramento/dimensoes.csv` | Dimensões e pesos da prontidão do enquadramento | Chief Strategist |
| `enquadramento/banco_perguntas.csv` | Perguntas-chave de enquadramento que já funcionaram | Calibração |
| `historico/previsto_vs_realizado.csv` | Metas e previsões x realizado, por trimestre | Calibração (revisão trimestral) |
| `licoes_aprendidas.md` / `propostas_melhoria.md` | Lições e mudanças propostas nas instruções dos agentes | Calibração |

A capacidade do time vem, por padrão, da planilha do squad de orçamento (`config.json` → `capacidade_time_csv`), para existir uma única fonte.
