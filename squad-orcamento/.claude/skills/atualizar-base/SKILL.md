---
name: atualizar-base
description: "Registra cotações, listas de preço, lead times e custos reais na base de conhecimento do squad, medindo o erro dos benchmarks. Use sempre que chegar uma cotação de fornecedor ou um dado real de custo, prazo ou horas."
---

# Atualizar a base de conhecimento

1. Receba o documento (PDF, e-mail, planilha). Sem documento, não há registro.
2. Salve uma cópia em `conhecimento/precos/cotacoes/` com nome `AAAA-MM-DD_fornecedor_item.ext`.
3. Acione o agente `data-calibracao` para registrar com `python -m motor.base registrar-cotacao` (moeda e incoterm originais, validade, lead time).
4. Se a cotação substitui um benchmark usado em algum orçamento, informe `--estimativa-anterior` e `--projeto`. Isso alimenta `historico/benchmark_vs_cotacao.csv`, o aprendizado da partida a frio.
5. Rode `python -m motor.base validar`.
6. Se algum orçamento aberto usava esse item, avise Marcus: o item pode sair de "cotação humana necessária" e o nó `bom` daquele orçamento deve ser atualizado pelo agente `suprimentos`.
