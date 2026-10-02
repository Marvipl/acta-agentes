# Base de conhecimento do squad

Esta pasta é a memória do squad. Os agentes não aprendem sozinhos entre sessões: o que evolui é esta base.
Toda linha precisa de **fonte e data**. Nenhum agente pode inventar valores aqui.

| Pasta / arquivo | Conteúdo | Quem mantém |
|---|---|---|
| `descoberta/dimensoes.csv` | Dimensões da especificação, críticas e pesos da nota de prontidão | Chief Estimator |
| `descoberta/banco_perguntas.csv` | Perguntas-chave por tipo de projeto e quantas vezes mudaram a estimativa | Data & Calibration |
| `precos/base_precos.csv` | Cotações reais recebidas (preço, data, validade, documento) | Data & Calibration (skill `atualizar-base`) |
| `precos/cotacoes/` | PDFs e e-mails das cotações | Você / Suprimentos |
| `mao_de_obra/custo_hora.csv` | Custo/hora por perfil (com encargos) | Renato (financeiro) |
| `mao_de_obra/capacidade_time.csv` | Pessoas, horas/mês e alocação atual por perfil | Gestão de Projetos + você |
| `produtividade/produtividade.csv` | Horas por unidade de trabalho (ex.: horas por robô implantado) | Data & Calibration |
| `lead_times/lead_times.csv` | Prazos reais de fornecedores | Data & Calibration |
| `tributos/` | Regras e alíquotas com fonte (NCM, TIPI/TEC, legislação) | Tributário + contador |
| `precificacao/referencias_comerciais_acta.csv` | Preços que a Acta já praticou ou propôs | Comercial |
| `fornecedores/fornecedores.csv` | Fornecedores, relação contratual e condições | Suprimentos |
| `engenharia/` | Benchmarks técnicos e de ROI (confiança baixa: usar só no modo rápido) | Engenharia |
| `metodologia/` | Classes de estimativa, checklist de completude | Chief Estimator |
| `historico/` | Estimado x realizado, benchmark x cotação, fatores de correção | Data & Calibration |
| `licoes_aprendidas.md` | Lições de cada orçamento e projeto | Data & Calibration |
| `propostas_melhoria.md` | Mudanças sugeridas nas instruções dos agentes (aguardam sua aprovação) | Data & Calibration |

## Partida a frio

A Acta começa sem histórico de projetos grandes. Por isso:
1. O primeiro sinal de aprendizado é **benchmark x cotação**: cada cotação real registrada com a estimativa anterior mede o erro dos benchmarks (`historico/benchmark_vs_cotacao.csv`). Com 3 ou mais registros, o squad propõe o fator `bom_benchmark`.
2. Orçamentos começam como classe 5 ou 4 e só sobem de classe com cotações reais nos itens críticos.
3. Cada projeto executado gera `realizado.json` e alimenta `historico/estimado_vs_realizado.csv` (skill `retro`).
