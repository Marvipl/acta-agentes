---
name: revisao-trimestral
description: "Revisão trimestral do plano estratégico congelado: KRs, receita por linha, caixa, hipóteses, gatilhos de revisão e aprendizado. Use ao fim de cada trimestre ou quando um gatilho do plano disparar."
---

# Revisão trimestral

1. Identifique a versão congelada do plano (`projetos/<id>/v<n>` com `saidas/baseline.json`).
2. Acione `calibracao-estrategica` com o trimestre (T1 a T4). Ele monta o `realizado.json` com Marcus e Renato (cada número com documento), roda `python -m motor.revisao trimestre` e lê o relatório.
3. Apresente a Marcus: KRs por status, receita por linha contra o previsto, caixa, hipóteses refutadas, gatilhos disparados e a recomendação para cada um (ajustar iniciativa, ajustar meta, abrir nova versão do plano).
4. Decisões de Marcus viram ação: nova versão (`python -m motor.estado nova-versao`) quando a tese muda; ajustes menores ficam registrados no relatório do trimestre.
5. Feche com o aprendizado: lições, banco de perguntas, contexto da Acta e propostas de melhoria das instruções (via PR).
