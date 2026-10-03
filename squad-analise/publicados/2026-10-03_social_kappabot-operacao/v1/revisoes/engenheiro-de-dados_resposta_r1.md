# Resposta do engenheiro de dados ao parecer do especialista (D1, r1)

- Projeto: `projetos/2026-10-03_social_kappabot-operacao/v1` · 2026-10-03 · agente `engenheiro-de-dados`
- Entrada: `revisoes/especialista_D1.md`. Saída corrigida: `nos/contrato.json` (recarimbado).
- Números: nenhum resultado digitado no contrato. Só parâmetros (PAR01 a PAR12), datas de calendário e premissas (PR). As consultas de apoio foram agregadas e preliminares, sem operador individual, e a análise registrada as refaz.

## Ponto decisivo: M11 contra M10 (A5)

**Aceito, corrigido.** O texto de M11 dizia "descontadas as pausas", mas a fórmula truncava cada pausa no teto e contava o teto inteiro como trabalho. M10 excluía os mesmos intervalos. Isso inflava horas e FTE (CR1, CR8). Em consulta preliminar, trocar truncar por excluir reduz as horas totais de forma relevante.
- **M11, base:** intervalo acima do teto sai da jornada (gap = 0), pela mesma regra de M10. O teto é PAR02 entre tarefas diferentes e PAR01 entre linhas da mesma tarefa e do mesmo usuário (A2).
- **S1 (sensibilidade obrigatória):** o intervalo acima do teto recebe a mediana dos intervalos válidos do recorte. Em consulta preliminar, fica perto da base.
- **S2 (limite superior):** truncar no teto, que era o comportamento anterior. Fica só como limite superior.
- **M12, M13, M14, M23:** passam a usar o ciclo da regra base. M12 e M13 reportam também S1 e S2.
- **M10:** passa a medir só intervalos entre tarefas diferentes. O intervalo entre linhas da mesma tarefa é coleta (M09).

## Teto de intervalo (A4, F12)

**Aceito.** PAR02 segue 900 s como base, com `cenario_conservador` = 600 s e `cenario_estresse` = 300 s. A sensibilidade fica 300, 600 e 1.800 s, e 1.800 s é o limite superior. A nota de PAR02 registra por que 300 s fica abaixo do ciclo do pedido-a-pedido documentado (PR16 mais etiqueta e primeiro endereço). M28 e M13 usam 600 s como conservador. A escolha do conservador é decisão de Marcus, com validação da operação da Social (PQ03, reescrita).

## Calendário, dia útil e mensalização (A10, seção 2)

**Aceito.**
- **PAR10 (novo):** 04/06 feriado (Corpus Christi); 05/06 ponte; 07/09 feriado; 08/06 e 24/09 sem explicação de calendário. Os dois últimos são dia sem operação no cenário base e lacuna de extração no alternativo (M15). A taxa por dia com registro não muda entre os dois, só o volume mensal.
- **Dia pleno (M15):** segunda a sexta com registro, fora de feriados, pontes (PAR10) e do dia parcial. Pós-pausa: 09/06, 08/09 e 25/09. O último dia pleno da carga é pós-pausa, então M15 pede a taxa corrente com e sem dias pós-pausa e com e sem a última semana incompleta.
- **Mensalização (M15, M20):** taxa × dias úteis de referência do calendário do mês (segunda a sexta, menos feriados e pontes) + volume de sábados observado.
- **Sábados:** ficam fora do dia pleno e das taxas, e dentro dos totais mensais. Se a Social trabalha em escala de seis dias (PQ05), o sábado vira dia de operação com taxa própria, e entra a sensibilidade semanal do FTE em M13.
- **Pico de retomada (M18):** reescrevi a nota. É fila que precisa ser separada de fato, não só artefato. O p90 segue como referência de frota, e o máximo pós-pausa é argumento de horário estendido (H02).
- **Data de extração:** 2026-09-28 (manhã), inferida pelo último carimbo e pelo dia parcial. O upload ao Drive (02/10) vai na versão. A confirmar em PQ01.
- **Censura à direita:** tarefas em andamento na extração não aparecem. Setembro é mês parcial (M20).

## Ajustes A1 a A10

| # | Parecer | Resposta |
|---|---|---|
| A1 | Linha de um endereço: testar bipe por unidade. | **Testado em agregado.** No pedido-a-pedido da Royal Canin o tempo dessas linhas não cresce com as unidades: sem sinal de bipe por unidade, o Fim parece a última coleta (E7). Em colmeia, linhas de um endereço têm tempo próprio alto: investigar na D3 (E3). Registrado em M08, NQ03 e `verificacoes`. |
| A2 | Pausa dentro da linha ou da tarefa. | **Aceito.** M09 corta PAR01 por intervalo entre confirmações (dentro da linha e entre linhas da tarefa), e a fórmula por tarefa vira variante. M11 limita o intervalo dentro da tarefa por PAR01. M08 ganha `linha_longa` (duração acima de PAR02 que passa em PAR01) e reporta com e sem elas. |
| A3 | Piso e linha de base sem o robô. | **Aceito como sensibilidade.** PAR11 (início da operação do robô, 2026-07-20, do briefing) e `pre_robo` alimentam M08, M12, M14 e M26. O piso físico em si é regra da qualidade (M08 e M09 o citam; vale para média de linha ou tarefa, nunca para intervalo isolado de checkout ou colmeia). |
| A4 | Conservador de 600 s e estresse de 300 s. | **Aceito.** Ver acima. |
| A5 | Crédito das pausas em M11. | **Aceito.** Ver ponto decisivo. |
| A6 | Palete e caixa fechada fora do escopo do robô. | **Aceito como marcação.** Nova `linha_palete` (area_origem PALLET ALTO ou PORTA PALET ALTO, ou Qtde CxG > 0). Sai da produtividade (M14), da demanda de robô (M22, CR4 e CR5) e da base tarifável do robô (M06). Fica no volume físico. Carga útil do Kappabot: [●]. |
| A7 | Checkout com mais de uma unidade. | **Aceito.** Subclasse `checkout_multiunidade` em M02, reportada à parte em M09, M21 (PR03 cobra por pedido de uma peça) e M22 (PR08). Em consulta preliminar ela existe em pouquíssimas linhas e ondas, fora da Royal Canin. |
| A8 | Tarefas abertas por meses e fechadas em lote. | **Parcial.** A regra de marcação é da qualidade (NQ02). O contrato ancora a exclusão da produtividade (M08) e da base tarifável até confirmação da Social (M06), com o volume físico marcado. Pendência registrada. |
| A9 | Deduplicar produto por pedido em M06. | **Não é possível:** a tabela não traz código de produto. M06 passa a reportar os dois limites: soma (base) e máximo entre as linhas do pedido (supõe segmentos repetidos). O inferior é o conservador para a receita (CR2). Em consulta preliminar, poucos pedidos têm mais de uma linha e a diferença entre os limites é pequena. Viés declarado. |
| A10 | Calendário e carga. | Ver seção acima. |

## Seção 3.6 e 3.1

- **3.1, PR12:** PAR09 registra a hipótese de jornada contratual de escala de seis dias. M13 declara FTE como presença num dia útil, não quadro, e traz a sensibilidade semanal com sábado. PQ05 reescrita com a hipótese. Horas ativas abaixo de PR12 entram como limite inferior, não como anomalia (M11, M12). Espera por onda é leitura alternativa (H13): M10 passa a trazer a fração de intervalos acima do teto por hora.
- **3.6.1 e 3.6.2 (M10 contra M11, M09):** feitos.
- **3.6.3 (M05 em lote):** **aceito como viés declarado** (M05, M14). Não calculável: sem o código do endereço, a visita distinta não existe na tabela. Fica a favor da exclusão da colmeia em CR7, e o plano deve declarar.
- **3.6.4 (M08, média de razões):** M08 mantém a média para reconciliar com o relatório e manda usar a razão ponderada em benchmark.
- **3.6.5 (M16 e M19, processamento):** nota em M16 e M22, e PQ06 nova (hora de criação ou liberação, horário de corte).
- **3.6.6 (sábado):** feito em M15 e M13.
- **3.6.7 (M24):** **não adotado como base.** Mantive uma linha por dia, porque reproduz a ordem de grandeza do slide 12 e o limite de uma hora não tem fonte setorial ([●]). A sensibilidade de uma hora de jornada ativa ficou explícita. O plano decide.
- **3.6.8 (M25):** nota de login novo, sobrevivência e alocação, e controle por tipo de onda.
- **3.6.9 (M02):** nota de segmentação por endereços e unidades por pedido (H07). O formato do Pedido como marcador de canal fica para a D3 ([●]).
- **3.2 e 3.8:** sem mudança de definição. M10 traz a fração de sobreposição (H05) e M08 a sensibilidade sem sobreposição. H08 vai para o planejador.

## Faixas (F1 a F13)

As faixas são da qualidade. No contrato entraram os limites de jornada (F11): PAR12, com jornada ativa e amplitude máximas e descanso entre jornadas. F13 já estava coberta: Data é o dia do Fim, e a jornada usa o dia do Início.

## Pendências para outros nós

- **Planejador:** taxa corrente com e sem pós-pausa e última semana (M15); linha de base sem robô; S1 e S2 de M11; H01 a H13.
- **Qualidade-privacidade:** marcar `linha_longa`, `linha_palete`, `checkout_multiunidade` e tarefas em lote, sem apagar do volume.
- **Marcus:** PQ03 (conservador de 600 s), PQ05 (escala de seis dias) e PQ01.
