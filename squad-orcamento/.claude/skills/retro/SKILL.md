---
name: retro
description: "Retrospectiva de aprendizado do squad: registra o realizado de um projeto executado contra a baseline congelada, propõe fatores de correção e lições. Use quando um projeto orçado pelo squad terminar ou atingir um marco relevante com custos e horas reais."
---

# Retrospectiva e calibração

1. Identifique a versão congelada do orçamento (`projetos/<projeto_id>/v<n>` com `saidas/baseline.json`).
2. Peça a Marcus (ou ao financeiro) os números reais com documento de origem: horas por categoria, custo de equipamentos, indiretos por categoria, prazo em dias, custo recorrente mensal.
3. Liste com Marcus as **mudanças de escopo aprovadas** durante o projeto e o impacto de cada uma por categoria. Sem isso, a calibração confunde aumento de escopo com erro de estimativa.
4. Acione o agente `data-calibracao` com esses dados para montar `realizado.json`, rodar `python -m motor.calibrar registrar` e `python -m motor.calibrar propor`.
5. Apresente a Marcus os fatores propostos (categoria, fator, n, dispersão, status). Só fatores com status `aplicavel` podem ser aprovados; a aprovação é dele: `python -m motor.calibrar aprovar --categoria <c> --por Marcus`.
6. Peça a `data-calibracao` para atualizar o banco de perguntas (`conhecimento/descoberta/banco_perguntas.csv`): quais perguntas da descoberta mudaram de fato a solução, o custo ou o preço, e quais nunca mudam e podem virar premissa padrão.
7. Registre as lições em `conhecimento/licoes_aprendidas.md` e as propostas de mudança de instrução em `conhecimento/propostas_melhoria.md`. Mudança em `.claude/agents/` só por PR aprovado por Marcus.
