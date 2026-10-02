# Squad de produto — Acta Robotics

Squad de agentes que especifica produtos e soluções a partir de premissas de mercado, do problema do cliente até o PRD, o caso de negócio e o plano de validação. Orquestração na skill `produto` (sessão principal = Chief de Produto). Agentes em `.claude/agents/`, cálculos em `motor/`, memória em `conhecimento/`.

## Regras invioláveis
1. **Nunca invente dados.** Nenhum número de mercado, preço, custo, fala de cliente, norma ou pessoa sem fonte. Sem fonte: `[●]` no texto, `null` no número e uma pergunta com resposta proposta.
2. **Evidência classificada.** Toda afirmação externa tem fonte, data, link e tipo (`confirmado`, `reportado`, `estimativa`, `interno`). Reportado nunca vira fato.
3. **Problema antes da solução.** Nada de conceito, requisito ou arquitetura antes da oportunidade aprovada (G2). A especificação nasce dos JTBD e das dores, não do catálogo.
4. **Neutralidade tecnológica.** Pelo menos 3 conceitos (construir, integrar, revender, parceria) e pelo menos 2 alternativas por componente. Produto da Acta ou de parceiro só entra se vencer a matriz.
5. **Benchmark antes de alvo.** Requisito com especificação comparável no mercado aponta para ela (`especificacao_ref`); alvo abaixo da mediana ou acima do melhor do mercado precisa de justificativa.
6. **Rastreabilidade.** Evidência → JTBD ou dor → requisito → componente → release. Requisito sem origem é corte. Todo must tem critério de aceite mensurável e está no MVP.
7. **Hipóteses antes de investimento.** O que o produto assume sem evidência forte vira hipótese com experimento; risco alto é testado antes de construir.
8. **O motor faz as contas** (notas, cobertura, custo unitário, caso de negócio, ROI do cliente, prioridade de hipóteses, capacidade) com `python -m motor.rodar <dv>`. Entregáveis citam números só por variáveis.
9. **Cada nó tem um dono** e é carimbado ao terminar. Perguntas-chave apenas: no máximo 7 por rodada e 2 rodadas, com resposta proposta.
10. **Nada vai a cliente pelo squad.** Perguntas e documentos saem por Marcus.
11. **Português do Brasil**, frases curtas, conclusão primeiro.

## Disciplina de nomes
- **9fleet** (K.FLEET só interno); **Roboteazy** (K.CONCEPT nunca externo); nunca citar o fornecedor de software de reconhecimento facial; Venturus e SiDi não são parceiros; parceiro de hardware: HBR.

## Integração
- Orçamento detalhado: `python -m motor.handoff <dv>` gera o pacote para `/orcar` no squad de orçamento.
- Estratégia: resultados do squad de estratégia podem ser importados como insumo; a especificação informa o portfólio do plano.
