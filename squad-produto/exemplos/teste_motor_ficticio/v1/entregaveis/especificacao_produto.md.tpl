# Especificação de produto — {{meta.produto}}

Segmento: {{meta.segmento}} · versão v{{meta.versao}} · data-base {{meta.data_base}}

<!-- Regra: números só por variáveis entre chaves duplas. Afirmações externas citam o id da evidência. -->

## 1. Resumo
<!-- DOCUMENTAÇÃO: problema, para quem, solução escolhida, por que agora, o que pedimos (investimento, pilotos). -->

## 2. Oportunidade
Nota da oportunidade: {{fmt.oportunidade_nota}} de 5.
<!-- ESTRATEGISTA: problema, segmento, JTBD-alvo, proposta de valor, evidências principais (confirmado x reportado). -->

## 3. Cliente
<!-- PESQUISA DE CLIENTE: personas (decisor, usuário, pagador), JTBD, dores e ganhos, alternativas atuais e seus custos. -->

## 4. Mercado e benchmark
Benchmark com {{fmt.n_concorrentes}} produtos e {{fmt.n_especificacoes}} especificações comparáveis; {{fmt.cobertura_benchmark}} das especificações preenchidas, {{fmt.benchmark_confirmado}} delas com fonte confirmada. Requisitos comparados com o mercado: {{fmt.n_requisitos_benchmark}} ({{fmt.n_requisitos_abaixo_mediana}} abaixo da mediana).
<!-- PESQUISA DE MERCADO e BENCHMARK: segmentos com faixa; tabela-resumo do benchmark (melhor do mercado e mediana nas especificações que decidem a compra); posição dos nossos alvos; lacunas de mercado. -->

## 5. Conceito escolhido
<!-- ESTRATEGISTA: conceitos avaliados (construir, integrar, revender, parceria), matriz e justificativa. -->

## 6. Requisitos
Requisitos: {{fmt.n_requisitos}} (must: {{fmt.n_must}}). Detalhe no PRD.

## 7. Arquitetura da solução
Custo unitário provável: {{fmt.custo_unitario}} (faixa {{fmt.custo_unitario_min}} a {{fmt.custo_unitario_max}}).
<!-- ARQUITETO: componentes, fazer/comprar/parceria com alternativas, TRL, riscos técnicos, normas. -->

## 8. Modelo de negócio

| | Ano 1 | Ano 2 | Ano 3 |
|---|---|---|---|
| Unidades novas | {{fmt.unidades_ano1}} | {{fmt.unidades_ano2}} | {{fmt.unidades_ano3}} |
| Receita | {{fmt.receita_ano1}} | {{fmt.receita_ano2}} | {{fmt.receita_ano3}} |
| Margem de contribuição | {{fmt.margem_contribuicao_ano1}} | {{fmt.margem_contribuicao_ano2}} | {{fmt.margem_contribuicao_ano3}} |
| Fluxo acumulado | {{fmt.acumulado_ano1}} | {{fmt.acumulado_ano2}} | {{fmt.acumulado_ano3}} |

VPL em 3 anos: {{fmt.vpl_3anos}} · payback do investimento: {{fmt.payback}} · maior sensibilidade: {{fmt.maior_sensibilidade}}.

Para o cliente: investimento {{fmt.roi_investimento_cliente}}, mensalidade {{fmt.roi_mensalidade_cliente}}, economia líquida anual {{fmt.roi_economia_anual}}, payback em {{fmt.roi_payback_meses}} meses.
<!-- PRICING: preço, disposição a pagar com evidência, premissas. -->

## 9. Validação
Hipóteses registradas: {{fmt.n_hipoteses}}.
<!-- VALIDAÇÃO: as hipóteses de maior risco, os experimentos e os critérios de sucesso e falha. -->

## 10. Roteiro e lançamento
<!-- ROADMAP E GTM: MVP e releases com marcos de decisão, pilotos, segmento inicial, canais, mensagem. -->

## 11. Riscos e decisões pendentes
