# Parecer do especialista setorial · D1 · faixas para a limpeza (r1)

- Projeto: `projetos/2026-10-03_social_kappabot-operacao/v1` · 2026-10-03 · agente `dados-especialista-setorial`
- Revisão r1, em resposta a `revisoes/sup-negocio_D1_r1.json`. A resposta ponto a ponto está em `revisoes/especialista-setorial_resposta_r1.md`.
  - A4 foi corrigido: o cenário conservador volta a 300 s.
  - H02 foi reescrita com a restrição de pessoas.
  - A CLT saiu como âncora de 900 s.
  - Afirmações sem fonte ficaram marcadas [●].
- Perfil assumido: gerente de operações e engenharia de armazém de 3PL no Brasil. Mede a separação no WMS e já avaliou AMR colaborativo (`perfil_especialista.md`, `nos/especialista.json`). A lente 2 (comercial e RaaS) tem confiança baixa.
- Entradas lidas: `perfil_especialista.md`, `nos/especialista.json`, `nos/decisao.json`, `saidas/perfil.md`.
  - Na r1 também: `nos/contrato.json` (5527342f3195), `nos/qualidade.json` (73fa3fc27d22) e o texto do deck (slides 6 e 17) e do relatório 9fleet v1 (p. 12 e 13).
  - Não li linhas de dados.
- Números: este parecer não traz resultado de análise. Aparecem só parâmetros do contrato (PAR, PR), faixas do setor com fonte e datas do calendário.

## Conclusão

1. **As faixas do perfil servem para a limpeza.** Confirmo as treze. Proponho dez ajustes de tratamento (seção 1). Nenhum deles apaga linha do volume. Eles mudam o que entra no tempo e o que entra no escopo do robô. A qualidade e o contrato atuais já aplicam quase todos. A exceção é o cenário conservador de A4, que precisa voltar a 300 s (seção 6).
2. **Teto de intervalo, em quatro cenários:**
   - base de 900 s;
   - **conservador de 300 s**;
   - 600 s como intermediário;
   - 1.800 s como limite superior.

   O teto menor dá menos horas manuais, menos economia, menos FTE e mais linhas por hora em CR3: é o cenário conservador para a oferta. A escolha é **decisão de Marcus no G2**, com validação da operação da Social (PQ03).
3. **Ajustes que mudam horas, FTE e linha de base** levam a marca `validar com pessoa do setor`:
   - o teto de intervalo (A4);
   - o crédito das pausas em M11 (A5);
   - o corte de abandono por intervalo dentro da tarefa (A2);
   - a linha de base manual limpa de pedidos do robô (A3, H06).
4. **Jornada ativa muito abaixo de PR12:** não é anomalia. É limite inferior. PR12 parece ser a jornada contratual de escala de seis dias, e não uma medida do WMS (3.1). FTE dividido por PR12 dá presença necessária, não quadro de pessoal.
5. **O que um gerente de 3PL estranharia primeiro:**
   - o bloco de cinco dias corridos sem registro em junho e o dia 24/09 sem registro;
   - o último dia pleno da carga (25/09) é dia pós-pausa;
   - uma curva horária que mede processamento, e não demanda;
   - uma colmeia medida sem a distribuição no put wall;
   - a possibilidade de o pedido-a-pedido ser feito com vários pedidos por viagem ([●], E1).
6. **Para enriquecer a oferta**, o plano deve testar H01 a H13 (seção 4). As de maior valor comercial:
   - frota compartilhada entre depositantes (pooling de picos, ALT6);
   - quanto das **pessoas-hora** dos picos de retomada a frota em janela estendida reduz. O Kappabot é colaborativo e precisa de separador na mesma hora, então H02 mede robôs **e** pessoas (CR4, CR8);
   - peso do tempo fora do relógio no pedido-a-pedido de poucos endereços;
   - reforço de pessoal nos dias de pico (CR8).

## 1. Faixas plausíveis: confirmação e ajustes

Coluna "Validar": **sim** quando a regra decide um critério (CR). Valida quem o perfil indica: a operação da Social e a engenharia da Acta autora do relatório 9fleet v1 (A08).

| # | Medida (unidade) | Faixa do perfil | Parecer | Tratamento proposto à qualidade e ao engenheiro | Fonte | Confiança | Validar |
|---|---|---|---|---|---|---|---|
| F1 | Tempo em Segundos por linha, executor manual (s) | 0 a 43.200 | **Confirmo** como limite do impossível. | −1 vale zero (NQ01). Negativo menor que −1 é erro de carimbo: tempo não mensurável, linha no volume. Acima de 43.200 s ou com Início antes do período (NQ02): abandono, fora do tempo. Ver A8 para o volume. | CLT, arts. 58, 59 e 59-A; Suriadi et al. (2017); contrato | alta | não |
| F1a | **Novo.** Tempo em Segundos em linha manual de um endereço (s) | — | **Acrescento.** O esperado é zero ou o instante da confirmação (NQ03). | Valor acima disso: marcar, sem excluir. Testar em agregado se cresce com Qtde Un (bipe por unidade) ou se o Fim é "finalizar pedido" (A1). | contrato (NQ03); documentação Senior | média | sim, se a cauda for relevante |
| F2 | Tempo em Segundos da conta do robô (s) | ≥ 0 | **Confirmo.** | No volume, fora de todo tempo (M03). Linhas antes do início da operação: marcar como teste (PQ04). Testar se um mesmo pedido tem linha do robô e linha humana (H06). | 9fleet v1, p. 4 e 7; contrato | média | sim (engenharia da Acta) |
| F3 | Tempo por coleta N−1, corte de abandono (s por coleta) | ≤ 300 (PAR01) | **Confirmo** para a linha do pedido-a-pedido (M08), **com ajuste A2** no checkout e na colmeia. | Reportar a fração cortada por tipo de onda e por hora. Corte concentrado no almoço indica tarefa aberta na refeição, não operador lento. | 9fleet v1, p. 6; contrato | média | não (PAR01 já aceito) |
| F4 | Tempo por coleta N−1, piso físico, só manual (s por coleta) | ≥ 3,6 | **Confirmo** como **marca** de lote, nunca como corte de volume. | Abaixo do piso: "sem tempo mensurável", fica no volume. Sensibilidade, só como ordem de grandeza: ≈ 5,5 s (3.600 ÷ 650). A SSI Schäfer mede **caixas por hora**, na estação goods-to-person, com pessoa **ou robô** separando. Não são coletas manuais. O piso vale para a média da linha ou da tarefa, nunca para um intervalo isolado de checkout ou colmeia. | Dematic (resumo de busca, inacessível); SSI Schäfer (verificada) | baixa | não |
| F5 | Qtde Endereços por linha | ≥ 1, sem máximo | **Confirmo.** Não é dado pessoal (NQ11). | Zero só em linha cancelada. Sem corte por valor: marcar a cauda por depositante e tipo de onda. Na colmeia e no checkout, a soma por pedido pode contar mais de uma vez a mesma visita física (3.6). | Senior; Bartholdi e Hackman; contrato | média | não |
| F6 | Qtde Produtos por linha (linha tarifável) | ≥ 1, sem máximo | **Confirmo.** | Marcar os dois sentidos da divergência com Endereços. Endereços maior que Produtos: o mesmo SKU sai de dois endereços (falta parcial, ou lote e validade: [●]). Produtos maior que Endereços: endereço com mais de um SKU ou outra regra do WMS. Muda a fatura: PQ02. | Senior; contrato | média | sim (PQ02) |
| F7 | Qtde Un por linha | ≥ 1, sem máximo | **Confirmo**, com ajuste A6. | Zero é corte, pulo ou cancelamento: não é produção. Palete ou caixa fechada (area_origem de palete ou Qtde CxG maior que zero) sai do UPH, do volume compatível com o robô (CR4, CR5) e da base tarifável do robô. | Senior; contrato (NQ10) | média | sim (carga do Kappabot: [●]) |
| F8 | Peças por linha | ≥ 1 | **Confirmo.** Para medir esforço, usar Qtde Un. | — | Senior; contrato | média | não |
| F9 | Qtde Un (ou Peças) por linha em onda de checkout | 1 a 1 | **Confirmo**, com ajuste A7. | Linha de checkout com mais de uma unidade vira subclasse marcada, não erro. | Senior, Checkout Express | alta | sim, se a subclasse for relevante |
| F10 | Embalagens / Hora | não usar | **Confirmo.** | Excluir da análise (NQ05). | 9fleet v1; contrato | média | não |
| F11 | Jornada ativa por operador-dia, M11 (h) | ≤ 12 | **Confirmo.** Sem mínimo setorial. | Acima de 12 h, ou amplitude acima de 14 h: marcar turnos fundidos ou login compartilhado. FTE com e sem esses dias. Com atividade de madrugada, separar o operador-dia por descanso de 11 h ou mais (art. 66), e não pela meia-noite. | CLT, arts. 59, 59-A, 66 e 71; CF, art. 7º, XIII; Senior | alta (texto da CLT não reconferido nesta rodada) | não |
| F12 | Intervalo entre atividades de tarefas diferentes do mesmo operador-dia, M10 (s) | 0 a 1.800 | **Confirmo** a faixa e os cenários, **corrigidos em A4**: base de 900 s, conservador de 300 s, intermediário de 600 s, limite superior de 1.800 s. | Âncora: a **distribuição medida**. O deck (slide 6) mede o intervalo humano entre pedidos-a-pedido consecutivos (ida ao packing, etiqueta e primeira coleta). Mediana e quartis ficam abaixo de 300 s, e 900 s reproduz a mediana (PAR02). Âncora também: PQ03. A CLT **não** diz se um intervalo de 15 min é trabalho ou pausa. Negativo vale zero. No pedido-a-pedido, medir a fração de sobreposição (H05). | deck, slide 6; contrato (PAR02, M10) | **baixa** até PQ03 | **sim (PQ03; decisão de Marcus no G2)** |
| F13 | Data/Hora Início e Fim | regras | **Confirmo.** | Fim ≥ Início, com tolerância de −1 s. Data é o dia do Fim; a jornada usa o dia do Início. Carimbos humanos iguais em série: captura em bloco (H06). | Suriadi et al. (2017); contrato | alta | não |

### Ajustes de tratamento (A1 a A10)

- **A1. Linha de um endereço.** Se o tempo dessas linhas cresce com as unidades, o coletor bipa unidade a unidade, e N−1 mistura deslocamento com bipagem. Se o Fim for "finalizar pedido", o tempo inclui uma etapa que não é coleta. Validar com a Social: como o coletor registra a coleta (pergunta 3 do perfil). O engenheiro já testou em agregado (resposta r1): no pedido-a-pedido da Royal Canin não há sinal de bipe por unidade. Na colmeia, a questão fica para a D3.
- **A2. Pausa dentro da linha ou da tarefa.** PAR01 se aplica à média por coleta. Numa linha ou tarefa com muitos endereços, uma refeição inteira cabe dentro da média.
  - Pedido-a-pedido: marcar as linhas com duração acima de PAR02 que passam em PAR01. Reportar com e sem elas.
  - Checkout e colmeia: cortar por intervalo entre confirmações consecutivas, e não pela média da tarefa.
  - O contrato r2 já faz isso por segmentos Início a Início.
  - Muda as horas do checkout e da colmeia (CR1, CR7): `validar com pessoa do setor`.
- **A3. Piso e linha de base limpa.**
  - O piso pega a confirmação em lote rápida. Não pega a confirmação humana de pedidos do robô feita no ritmo do bipe (H06). Essas linhas deixam o manual "mais rápido" e jogam contra a oferta.
  - Sensibilidade de M08 e M14: a linha de base do pedido-a-pedido da Royal Canin antes do início da operação do robô (PAR11).
  - Decisivo para CR3: `validar com pessoa do setor` (engenharia da Acta).
- **A4. Teto de intervalo (corrigido na r1).**
  - **Retiro a justificativa da versão anterior.** Ela usava PR16, que é o trajeto do **robô** ao faturamento medido no 9fleet (relatório 9fleet v1, p. 13), como se fosse parte do intervalo humano. O intervalo humano medido no deck (slide 6) já inclui a ida ao packing, a etiqueta e a primeira coleta, e a mediana e os quartis ficam abaixo de 300 s. Logo, 300 s não corta o ciclo típico documentado: corta só a cauda.
  - **Recomendação.** Base de 900 s, que reproduz a mediana do slide 6. **Conservador de 300 s** para CR1, CR3 e CR8: menos horas, menos economia, menos FTE e mais linhas por hora manuais. Intermediário de 600 s. Limite superior de 1.800 s.
  - O analista reporta os quatro, e a regra conservadora não favorece a oferta.
  - Também sugiro ao planejador um teto pela distribuição medida de M10, com o percentil **declarado antes** do resultado. Isso é só referência, não troca o conservador.
  - Mudar o conservador exige evidência que não favoreça a oferta e **decisão de Marcus no G2**, com validação da operação (PQ03).
- **A5. Crédito das pausas em M11.**
  - A versão anterior do contrato truncava cada pausa no teto (cada almoço contava PAR02 inteiro como trabalho). Já corrigido no contrato: a pausa sai da jornada.
  - S1 credita a mediana do intervalo. S2, a truncagem, fica só como limite superior.
  - Muda horas e FTE (CR1, CR8): `validar com pessoa do setor`.
- **A6. Palete e caixa fechada fora do escopo do robô.** Não são picking fracionado nem demanda de robô. Carga útil e volume por viagem do Kappabot: [●] (engenharia da Acta). Isso afeta PR07 se os itens da Royal Canin forem volumosos.
- **A7. Checkout com mais de uma unidade.** O Checkout Express do Senior só aceita pedido de uma peça. Reportar à parte em P3, PR03 e PR08. Se o checkout conferido no robô supõe uma peça por pedido: [●] (engenharia da Acta).
- **A8. Tarefas abertas por meses e fechadas no mesmo dia (NQ02).** Leitura sem fonte ([●], confiança baixa): parece encerramento administrativo de pendências. Ficam fora da produtividade e, até a Social confirmar que houve coleta (E10), fora da base tarifável. Ficam no volume físico, marcadas.
- **A9. Pedido em mais de uma tarefa ou segmento (NQ08).** Pode ser pedido reliberado depois de um corte ou confirmado em partes ([●]). A deduplicação por produto não é possível (sem código de produto). O contrato reporta dois limites (soma e máximo), e eu aceito.
- **A10. Calendário e carga.** Ver seção 2.

## 2. Dias sem registro, pós-pausa e dia parcial

| Dia sem registro (contrato) | Dia da semana | Leitura | Confiança |
|---|---|---|---|
| 04/06 | quinta | Corpus Christi: data calculada (Páscoa de 2026 em 05/04, mais 60 dias). Não sei se é feriado na cidade da Social nem se ela fechou: [●] (E4). | alta para a data; [●] baixa para o fechamento |
| 05/06 | sexta | Possível ponte de feriado: [●], sem fonte (E4). | baixa |
| 08/06 | segunda | **Sem explicação de calendário.** Com o fim de semana, são cinco dias corridos sem separação. Leitura sem fonte ([●], confiança baixa): uma parada desse tamanho seria atípica para um 3PL de e-commerce. Hipóteses a perguntar (E4): inventário geral aproveitando o feriado, parada ou migração do WMS, lacuna de extração. | baixa |
| 07/09 | segunda | Independência, feriado nacional (Lei 10.607/2002). | alta |
| 24/09 | quinta | **Sem explicação de calendário nacional.** Feriado municipal, parada ou lacuna de extração: [●] (E4). | baixa |

Consequências e regras:
1. **Pós-pausa** = 09/06, 08/09 e **25/09**. O dia 25/09 é o **último dia pleno da carga**. A taxa corrente (CR2) e o dia de pico (CR4) não podem depender só dele. Reportar com e sem os dias pós-pausa e com e sem a última semana incompleta.
2. **Pico de retomada: hipótese, não fato** ([●], confiança baixa). Depois de dias parados, a fila acumulada precisa ser separada de fato. Isso pode se repetir a cada feriado prolongado e, em menor grau, às segundas. Testar em H02 (M17, M18).
   - Para a frota (CR4), o p90 continua sendo a referência.
   - O máximo pós-pausa entra em H02, que mede robôs **e** pessoas na janela estendida. Não é argumento automático de mais robôs nem de dispensar temporário.
3. **Lacuna de extração muda a leitura.** Se 08/06 ou 24/09 forem falha de extração, o volume mensal fica subestimado e as taxas por dia com registro não mudam. Na mensalização, usar os dias de operação do mês de referência.
4. **Dia parcial 28/09: confirmo** que fica fora das taxas diárias e do p90 (PAR08).
   - O último carimbo indica extração na manhã de segunda, 28/09. A data de 02/10 é do upload. Confirmar em PQ01.
   - Tarefas em andamento na hora da extração não aparecem (censura à direita).
5. **Setembro é mês parcial**: comparar só normalizado (M20).
6. **Sábados com registro.** Se a Social trabalha em escala de seis dias, as horas de sábado entram na mensalização (3.1).

## 3. O que um gerente de 3PL estranharia

Cada item traz a explicação do setor, a alternativa óbvia, a consequência e o teste.

### 3.1 Jornada ativa muito abaixo de PR12
- **Explicação do setor.** Não estranho. O WMS registra só a separação. O separador também faz reabastecimento, apoio ao packing e à conferência, resolução de problemas e outras tarefas (pergunta 2 do perfil). M11 é limite inferior, não presença (relatório 9fleet v1, p. 12).
- **Alternativa óbvia.** Pode ser **espera por onda**, num quadro dimensionado para o pico da manhã. Pode ser pausa longa que é trabalho. Pode ser operador multifunção.
- **Por que importa.** Com outras atividades, liberar horas de separação só vira economia com realocação. Com espera por onda, o robô não elimina a espera.
- **PR12.** É igual à jornada semanal máxima de 44 h (CF, art. 7º, XIII; o art. 58 da CLT fixa 8 h por dia) dividida por seis dias. Muito provavelmente é jornada contratual de escala de seis dias, não "medida no WMS". É coerente com os sábados com registro. Confirmar em PQ05.
- **FTE.** Horas ativas por dia útil ÷ PR12 dão **presença necessária num dia útil**, não quadro. O quadro precisa de cobertura de férias e absenteísmo (Brasil: [●]; EUA, BLS, só como proxy e com a definição declarada). Sensibilidade: FTE semanal = horas ativas da semana com sábado ÷ jornada semanal contratual.
- **Teste.** H13.
- `validar com pessoa do setor`: decide CR1 e CR8.

### 3.2 Tempo zero em linha de um endereço
- **Explicação do setor.** Não estranho: Início e Fim são o mesmo bipe (NQ03).
- **O que estranharia.** Uma cauda de tempos altos (A1).
- **Consequência.** No pedido-a-pedido de uma linha, **todo o custo do pedido está fora do relógio**. M08 não o vê (PAR03); M14 o captura pelo intervalo.
- **Leitura.** Pedido de uma linha costuma ir para lote (Bartholdi e Hackman, 3.3). Se a Royal Canin tem muitos pedidos de um endereço no pedido-a-pedido, há ganho de processo **sem robô**. A oferta precisa tratar isso (H08).
- **Alternativa.** Esses pedidos têm várias unidades e não cabem no Checkout Express.

### 3.3 Checkout com uma peça por pedido
- **Explicação do setor.** Não estranho: é a regra do Checkout Express. Estranharia linha de checkout com mais de uma unidade (A7).
- **Lente 2 (confiança baixa).** A tarifa por pedido de uma peça (PR03) precisa caber no que a Social recebe da Royal Canin por pedido. Esse valor é [●] (pergunta 14 do perfil).

### 3.4 Dias sem registro
Ver seção 2.

### 3.5 Confirmação humana em lote (NQ04)
- **Explicação do setor.** Operador que separa e bipa tudo no fim, às vezes por meta no coletor: o Senior permite meta por hora (pergunta 4 do perfil). Ou coletor que envia as confirmações juntas ([●]).
- **Alternativa, a testar primeiro.** São **pedidos do robô com devolutiva não automática**, confirmados por um humano (H06).
- **Por que importa.** Se for o robô, as linhas são volume do robô e saem do tempo manual.
- `validar com pessoa do setor` (engenharia da Acta): decide P8 e CR3.

### 3.6 Definições do contrato que eu questionava (situação no contrato atual)
1. **M10 contra M11 (A5):** corrigido no contrato.
2. **M09 (A2):** corrigido por segmentos.
3. **M05 na colmeia e no checkout.**
   - Em lote, uma visita física serve vários pedidos. As "coletas por hora" da colmeia saem infladas frente ao pedido-a-pedido, e CR7 fica enviesado **a favor da exclusão da colmeia**.
   - O contrato aceitou como viés declarado.
   - Com 3.7, é decisivo para CR7: `validar com pessoa do setor`.
4. **M08, média de razões:** para benchmark, usar a razão ponderada.
5. **M16 e M19: a curva horária mede processamento, não demanda.**
   - Sem a hora de criação ou de liberação do pedido, a concentração matinal pode ser a fila da noite.
   - Dimensionar a frota por essa curva copia o dimensionamento atual de pessoal (PQ06, horário de corte).
   - Decisivo para CR4: `validar com pessoa do setor`.
6. **Sábado na mensalização:** tratado no contrato.
7. **M24, ativo com uma linha no dia:** o contrato manteve a regra, com a sensibilidade de uma hora. O limite de uma hora não tem fonte: [●].
8. **M25, novo login:**
   - um login novo não é necessariamente uma contratação;
   - há viés de sobrevivência e de alocação;
   - controlar por tipo de onda.
9. **M02, pedido-a-pedido:** pode misturar B2C e B2B. Segmentar (H07).

### 3.7 Colmeia
- **Explicação do setor.** A separação em lote fica no WMS. A distribuição no put wall pode ser feita por outra pessoa e não aparecer na planilha (pergunta 13 do perfil).
- **Alternativa.** A distribuição é registrada como outra tarefa ou destino.
- **Consequência.** Se a distribuição não aparece, CR7 sai otimista para o manual e tende a manter a exclusão do slide 14. Decisivo para CR7 e ALT5: `validar com pessoa do setor`.

### 3.8 Multipedido no pedido-a-pedido
- **Hipótese sem fonte** ([●], confiança baixa; não usar como premissa até E1). O separador pode levar vários pedidos-a-pedido por viagem, se o carrinho comportar. Não sei se a Social faz isso.
- **Consequência, se fizer.** Os tempos das linhas se sobrepõem. M08 mede o tempo de vários pedidos como se fosse de um, e o manual parece **mais lento**, o que favorece a oferta. A vantagem do robô de três pedidos por viagem (PR07) também encolhe.
- **Teste.** H05.
- Decisivo para CR3: `validar com pessoa do setor`.

## 4. Hipóteses do setor para o plano

Todas são exploratórias. Ficam sempre em agregado, sem operador individual, com PAR07.

| ID | Hipótese do setor | Alternativa óbvia | Teste no WMS (métricas) | Liga a | Decisiva |
|---|---|---|---|---|---|
| H01 | **Pico horário.** A concentração matinal é fila da noite e da véspera processada na chegada da equipe. Pode haver um segundo pico antes do corte. | Pedidos chegam mesmo de manhã. | M16 e M19 por depositante e tipo de onda. Primeira hora de segunda e do pós-feriado contra terça a sexta. Pedir a hora de liberação da onda (PQ06). | CR4, P11 | sim (3.6, item 5) |
| H02 | **Pico de retomada com robôs e pessoas (reescrita na r1).** O Kappabot é colaborativo: cada hora de robô na janela estendida exige separador na mesma hora (o deck, slide 17, conta FTE também no cenário com robôs). A hipótese é que, nos dias pós-pausa e p90, a frota em janela estendida com separadores em **escala escalonada** (entrada e saída deslocadas, dentro de 8 h por dia e 44 h por semana) cubra o excedente com **menos pessoas-hora**, menos hora extra e menos temporários do que hoje. Não "sem hora extra nem temporário": o deck mantém o temporário guiado pelo robô. | O ganho por pessoa-hora com robô não basta para o pico, e a Social continua precisando de hora extra ou temporário. Ou a escala escalonada já existe e não há o que absorver. | (1) Hoje: excedente em pessoas-hora do pós-pausa e do p90 sobre o típico (M23), e como a Social o cobre. Sinais: amplitude do armazém e jornada ativa por operador nos dias de pico (hora extra) e operadores ativos (reforço; H10, M24). (2) Com robô: pessoas-hora = volume do escopo ÷ produtividade com robô (PR05, premissa de baixa confiança, com sensibilidade) contra a manual (M14). Distribuir por hora na janela estendida. Separadores por hora; robôs por hora no máximo a frota (M22); robôs por separador na faixa da base Acta (baixa). (3) Comparar quatro arranjos: manual com hora extra, manual com temporário, robô com escala escalonada, robô com hora extra. Hora extra até 2 h por dia (CLT, art. 59) com adicional mínimo de 50% (CF, art. 7º, XVI). Janela após as 22 h tem adicional noturno (CLT, art. 73). Custos de hora extra e de temporário: [●] (E11). Concluir só depois do teste. | CR4, CR8, P11, P19 | sim (CR8): `validar com pessoa do setor` |
| H03 | **Pooling entre depositantes.** Os picos diários dos depositantes compatíveis não coincidem, e a frota compartilhada cobre o p90 do conjunto com menos robôs que a soma dos p90 individuais. Interpretação: a fonte fala de sazonalidade complementar no 3PL, não de frota; confiança baixa. | Picos sincronizados. | p90 da soma contra soma dos p90; correlação dos volumes diários; tendência semanal por depositante. Brinquedos antes do Dia das Crianças: [●], confiança baixa. | CR4, CR5, ALT6 | não |
| H04 | **Tempo fora do relógio.** No pedido-a-pedido, a parcela do intervalo no ciclo cresce quando o número de endereços cai. | O intervalo contém espera ou outras atividades. | M10 e M14 por faixa de endereços e por hora; histograma dos intervalos por hora. Checagem de ordem de grandeza: de Koster et al., Fig. 4 (separação com papel; aplicabilidade média). | CR3, P10 | não |
| H05 | **Multipedido no pedido-a-pedido** (3.8; [●]). | Um pedido por viagem. | Fração de linhas sobrepostas no mesmo operador-dia, por depositante. Se relevante, M08 sem elas. | CR3, P7 | sim |
| H06 | **Lote humano é devolutiva não automática do robô** (3.5). | Lote por meta ou por coletor. | Linhas humanas de dois ou mais endereços abaixo do piso: por depositante e tipo, antes e depois de PAR11, nas horas do robô. Pedidos com linha do robô e linha humana. | CR3, P8, M12, M26 | sim |
| H07 | **Perfil por depositante.** Interpretação (a fonte trata de método manual, não de AMR; confiança baixa): pedidos com várias linhas são o alvo natural do AMR em zona, e pedidos de uma linha vão melhor em lote. | O perfil muda com o canal mais que com o depositante. | Distribuição (não média) de endereços e unidades por pedido, por depositante e tipo de onda. Marcadores de palete e caixa. | CR5, P14 | não |
| H08 | **Pedido-a-pedido de um endereço na Royal Canin** poderia ir ao checkout ou a lote. | Tem várias unidades e não cabe no Checkout Express. | Tabela agregada de endereços por unidades no pedido-a-pedido da Royal Canin. | CR1, CR2, P9 | não, mas afeta a credibilidade da oferta |
| H09 | **Curva de proficiência manual (reescrita na r1).** Operadores novos levam semanas para chegar à mediana dos experientes. Treino e proficiência são métricas diferentes. Os casos de AMR (DHL; MD Logistics, depoimento de fornecedor) falam de **tempo de treino**. O tempo até a proficiência com AMR é [●]. | Login novo não é pessoa nova; vieses de alocação e sobrevivência (3.6, item 8). | M25 por tipo de onda, com a participação de cada tipo na primeira semana. Mede só a curva manual. Na oferta: "treino mais curto, segundo casos dos EUA, confiança baixa". Ganho de proficiência com robô, só depois do teste controlado. | CR8, P13 | não |
| H10 | **Reforço nos dias de pico.** Operadores ativos crescem com o volume: a Social flexiona com temporários ou remanejamento. | Equipe fixa com hora extra. | M24 contra volume diário; amplitude do armazém e jornada ativa nos dias p90 contra os típicos. | CR8, P15, P19 | não |
| H11 | **Colmeia sem distribuição no WMS** (3.7). | Distribuição em outra tarefa ou destino. | Fração de linhas sobrepostas na colmeia; tarefas e usuários por destino COLMEIA; pergunta à Social. | CR7, ALT5 | sim |
| H12 | **Checkout misto** (A7). | Todo o checkout é Checkout Express. | Fração de ondas de checkout com mais de uma unidade, por depositante. | P3, PR03, PR08 | não |
| H13 | **Jornada baixa por espera** (3.1). | Outras atividades fora do WMS. | Intervalos acima do teto por hora contra a demanda da hora (M16); jornada ativa nos dias típicos contra os p90. | CR1, CR8 | sim |

## 5. Perguntas, com resposta proposta

| # | Pergunta | Para quem | Resposta proposta |
|---|---|---|---|
| E1 | Os separadores levam vários pedidos-a-pedido por viagem? | operação da Social | Supor um por viagem e medir a sobreposição (H05). |
| E2 | As contas humanas que confirmam vários endereços em segundos fazem a devolutiva manual do robô? | engenharia da Acta | Testar H06. Até confirmar, saem do tempo manual pelo piso, com a base pré-robô como sensibilidade. |
| E3 | Quem faz a distribuição na colmeia, e ela aparece no WMS? | operação da Social | Supor que não aparece e declarar CR7 otimista para o manual. |
| E4 | O que houve em 04/06, 05/06, 08/06 e 24/09? Operação parada, feriado local, inventário ou falha de extração? | Social (via Marcus, PQ01) | Dias sem operação no cenário base e lacuna de extração no alternativo; taxas com e sem pós-pausa. |
| E5 | PR12 é a jornada contratual de escala de seis dias (44 h semanais, CF, art. 7º, XIII)? Os separadores trabalham aos sábados? | autor do deck e Social (PQ05) | Sim. FTE em presença num dia útil, com a sensibilidade semanal (3.1). |
| E6 | O Senior da Social registra a criação ou a liberação do pedido? Qual o horário de corte de cada depositante? | Social (PQ06) | Sem o dado, a curva horária é de processamento (H01), e o dimensionamento da frota declara isso. |
| E7 | O coletor bipa cada unidade ou informa a quantidade? O Fim é a última coleta ou "finalizar pedido"? | Social | Última coleta, com quantidade informada. O teste agregado do engenheiro (A1) é compatível com isso. |
| E8 | Até quantos minutos entre um pedido e o próximo a operação considera trabalho, e não pausa? | operação da Social (PQ03) | Base de 900 s (reproduz a mediana do slide 6), conservador de 300 s, intermediário de 600 s, limite superior de 1.800 s. **Marcus decide no G2.** |
| E9 | Qual a carga útil e o volume por viagem do Kappabot? O checkout conferido supõe uma peça por pedido? | engenharia da Acta | Palete e caixa fechada fora do escopo do robô (A6); checkout de uma peça (A7). |
| E10 | As tarefas abertas por meses e fechadas em lote tiveram coleta? | Social | Encerramento administrativo: fora da produtividade e da base tarifável (A8). |
| E11 | **Novo.** Quantas horas extras e quantos temporários a Social usa por mês e nos picos, e quanto custa cada um (hora extra, agência, treino)? | Social (via Marcus) | Sem o dado, H02 e CR8 saem em pessoas-hora e pessoas, sem valor em reais; custos [●]. |

## 6. Pendências sugeridas a outros nós (sem alterar os nós)

- **engenheiro de dados (contrato):**
  - Reverter o cenário conservador para 300 s em PAR02 (`cenario_conservador`; tirar `cenario_estresse` ou deixá-lo igual a 300 s), na nota de PAR02, em M11, M12, M28, PQ03 e nas pendências.
  - Na nota de PAR02, tirar a frase de que 300 s "fica abaixo do ciclo… documentado (PR16…)" e o "endosso" do especialista à base. A âncora passa a ser a reprodução do slide 6 e PQ03, com confiança baixa.
  - Em PAR09 e PQ05, trocar "jornada semanal da CLT" por "jornada semanal da CF, art. 7º, XIII".
  - Em PAR10, rebaixar para [●]/baixa a confiança do fechamento em 04/06 e da ponte em 05/06.
  - Em M18 e onde houver "o máximo pós-pausa é argumento de horário estendido, não de mais robôs (H02)", trocar por "o máximo pós-pausa entra em H02, que mede robôs e pessoas na janela estendida".
- **qualidade-privacidade:**
  - Em QD15 e em `limiares.PAR02_teto_intervalo_s`, conservador de 300 s e intermediário de 600 s.
  - Em `limiares.piso_s_por_coleta.fonte_sensibilidade`, declarar que 650 é caixas por hora na goods-to-person, com pessoa ou robô: só ordem de grandeza, confiança baixa.
  - Em QD06, a mesma troca de texto de H02.
- **planejador:**
  - Registrar H01 a H13. H05, H06, H11 e H13 são pré-requisitos de CR3, CR7, CR1 e CR8.
  - H02 com os quatro arranjos de pessoas e robôs.
  - Cenários de teto de 300, 600, 900 e 1.800 s, com o conservador de 300 s até Marcus decidir no G2.
  - Opcional: um teto pela distribuição de M10, com percentil declarado antes do resultado.
  - Linha de base pré-robô (A3).
  - Reconciliação do tempo manual do relatório 9fleet v1 com e sem a conta do robô.
- **analista de impacto:** FTE como presença, não quadro (3.1). Declarar que horas ativas podem incluir espera que o robô não elimina (H13). Em CR8, pessoas-hora e pessoas por arranjo (H02), não "sem temporário".
- **Nota para D3 e D4 (minha):** julgarei cada recomendação também por custo e prazo de implantação do lado da Social: layout e corredores, rede sem fio, integração com o Senior, treino, queda de produtividade no go-live, segurança do AMR com pessoas e ergonomia. Hoje esses temas são [●] no perfil (pendência do perfilador).

## Autoverificação
- [x] Parecer dentro do perfil aprovado. Afirmações sem fonte no perfil estão marcadas [●] com confiança baixa: fechamento em feriado, ponte, parada de cinco dias, pico de retomada, multipedido, encerramento administrativo, sazonalidade de brinquedos, bipe por unidade e carga do robô.
- [x] Explicação alternativa para cada achado (seção 3 e coluna "alternativa" da seção 4).
- [x] Interpretações decisivas marcadas `validar com pessoa do setor`: A2 a A5; 3.1, 3.5, 3.6 (itens 3 e 5), 3.7 e 3.8; H01, H02, H05, H06, H11 e H13. O teto de intervalo é decisão de Marcus no G2.
- [x] Nenhum número de análise digitado. Nenhum dado pessoal lido nem citado.
