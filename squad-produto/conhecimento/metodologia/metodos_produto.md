# Métodos usados pelo squad de produto

## Jobs to be done (JTBD)
O cliente "contrata" um produto para progredir numa situação. Cada JTBD descreve situação, motivação e resultado esperado, com evidência. Dores (o que atrapalha) e ganhos (o que seria melhor) se ligam a um JTBD. Requisito que não serve a nenhum JTBD, dor, ganho ou norma é candidato a corte.

## Benchmark técnico
Antes de definir requisitos, compare o que já existe: 5 a 12 especificações comparáveis (com unidade e direção: maior, menor ou qualitativo), pelo menos 3 produtos (importados, nacionais e uma alternativa não robótica), valores normalizados com evidência (ficha técnica do fabricante é a fonte preferida), preço com tipo (lista, cotação, estimativa) e suporte no Brasil. O motor calcula melhor do mercado, mediana e líder por especificação. Requisitos comparáveis apontam para a especificação (`especificacao_ref`): o motor mostra se o alvo está abaixo da mediana, entre a mediana e o melhor, ou acima do melhor do mercado, e quais produtos já atendem.

## Oportunidade
Nota ponderada em critérios definidos antes das notas: intensidade da dor, tamanho do mercado, disposição a pagar, vantagem da Acta, aderência estratégica. Decisão: seguir, pivotar ou parar. Proposta de valor: para quem, que problema, nossa solução, diferente de quê, por que acreditar.

## Conceitos
Pelo menos três caminhos, incluindo integrar, revender ou fazer parceria, e não só construir. Critérios com pesos antes das notas. Produto da Acta ou de parceiro só vence se vencer a matriz. Isso vale também para cada componente da arquitetura (no mínimo duas alternativas).

## Requisitos
Prioridade MoSCoW (must, should, could, won't). Todo must tem critério de aceite verificável, métrica e valor-alvo. Todo JTBD-alvo é coberto por pelo menos um must; toda norma aplicável gera requisito. Todo must está no MVP.

## Caso de negócio
Três anos, com mix de venda e locação, base instalada, implantação, suporte, investimento de desenvolvimento e VPL. O motor mostra a sensibilidade do VPL a volume, custo unitário, investimento e preço. O ROI do cliente sai da economia operacional menos o que ele paga.

## Validação
Hipóteses em quatro categorias: desejabilidade (o cliente quer?), viabilidade (o negócio fecha?), factibilidade (conseguimos construir?) e regulatória. Risco = impacto × incerteza (1 a 5 cada). Toda hipótese com risco 15 ou mais tem experimento com critério de sucesso e de falha, e é testada antes de investir pesado.

## Roteiro e lançamento
MVP com todos os musts, releases com marco de decisão (continuar, ajustar ou parar), pilotos com critério de sucesso e segmento inicial definido.
