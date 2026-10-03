# Pistas propostas por ANA-012 para confirmação em ANA-016

Autor: analista-exploratorio. Origem: ANA-012, recorte de descoberta (semanas ISO ímpares). Nenhuma semana par foi lida para chegar a estas pistas (o script filtra `semana_impar` no SQL e confere por assert; única exceção declarada: o painel de novatos de PT-H09, por operador).

Valores: nenhum número está digitado aqui. Estimativas de descoberta, limiares, pesos e efeitos relevantes estão em `saidas/analises/ANA-012/pistas_propostas.csv` e `saidas/analises/ANA-012/limiares_descoberta.csv` (gravados pelo motor). O texto abaixo só define o que medir e como ler.

## Como ler este arquivo

- Pistas a priori já no plano: PT-H04, PT-H09, PT-H10 (ANA-012 as calculou na descoberta; ver `poder_pistas_a_priori.csv`). Aqui entram só as **novas**.
- Ordem = valor comercial para a decisão (primeiro o que muda o que se promete à Social), não força do sinal.
- Cada pista usa **só** limiares e pesos da tabela `limiares_descoberta`, sem recálculo nas semanas pares.
- Pista não confirmada fica exploratória, não vira insight aprovado e não vai ao memorando como número; pode entrar como hipótese a medir no teste controlado.

## Regras comuns de leitura (valem para as quatro)

1. Estimativa, IC de 95% de percentis por bootstrap e p unilateral, **só nas semanas pares**. A estimativa da descoberta não vai ao memorando.
2. Unidades de reamostragem: operador, bloco de semana e dia pleno; **vale o IC mais largo**. O mesmo sorteio vale nos dois grupos comparados. Para PT-D2 os dias são reamostrados dentro do tipo (pico e típico).
3. Mínimo de unidades (definicoes.poder.minimo_clusters): vinte ou mais operadores, IC por operador; de dez a dezenove, IC com aviso e comparado ao de bloco de semana; menos de dez, só descritivo (inconclusivo por desenho).
4. Pista confirmada = mesmo sinal da direção declarada, IC 95% inteiro fora do nulo, p unilateral ajustado por Holm na F2 abaixo de alfa e sem inversão de sinal na robustez.
5. Efeito relevante: 10% do valor de referência (a média ou a mediana do grupo de comparação nas semanas pares). Se o MDE de ANA-000 passar do efeito relevante, vale a regra `sem_poder` do plano: inconclusivo por desenho não se lê como "sem efeito"; confirmada com MDE acima do efeito relevante leva o aviso de magnitude.
6. Teto: variante primária no teto base; o teto conservador do G2 entra como robustez (mesmo sinal exigido). A leitura de CR1, CR3 e CR8 no teto conservador continua sendo do plano.
7. Robustez sem valor de confirmação: semanas pares da janela base; deixar um operador de fora por vez; por segmento (faixa, tipo de onda) com `comum.robustez_segmentos`.

## Incidente da Royal Canin (recorte atípico, declarado)

A semana ISO de 21 a 25/09 (`incidente_rc_inicio` e `incidente_rc_fim` em `limiares_descoberta`) é ímpar e está na descoberta. A queda da Royal Canin nessa semana é real (decisão em `revisoes/orquestrador_decisao_semana_incidente.md`). Tratamento em ANA-012:

- tratamento primário (operação normal): as poucas linhas da Royal Canin desses dias saem dos conjuntos de linhas e de tempo; onde o volume ou a hora do dia do armazém inteiro entra num limiar ou numa variável (quartis e p90 do volume, janela observada, faixa de refeição, H10), os dias saem inteiros;
- sensibilidades gravadas: `*_com_incidente` (tudo como extraído, limiares recalculados com a semana) e `*_dia_incidente_fora` (dias inteiros fora do conjunto de linhas);
- os limiares de `limiares_descoberta` são os do tratamento primário; os recalculados com a semana têm sufixo `_com_incidente` nas chaves de ANA-012.

Nas semanas pares da confirmação o incidente não existe (a semana dele é ímpar). O estatístico confere em ANA-016 que a Royal Canin tem volume normal em todas as semanas pares antes de rodar, e **não** aplica filtro de incidente nelas.

## PT-D1 (ordem 1) — a Royal Canin é mais lenta que os outros depositantes no pedido-a-pedido

- Pergunta e critério: P9; CR3 e CR5 (ALT6).
- Hipótese: no pedido-a-pedido manual em ciclo completo, o M14 padronizado por faixa de endereços da Royal Canin é menor que o dos outros depositantes. A base de produtividade da Royal Canin pode não valer para os outros depositantes (ALT6) e o ganho do robô tende a ser maior onde o manual rende menos.
- Recorte: `prep_prod_ciclos`, `tipo_onda = 'pedido_a_pedido'`, filtros de M14 (`comum.FILTRO_TEMPO`: sem CANCELADO, sem `linha_palete`, sem dia parcial), semanas pares. Grupo A = depositante Royal Canin; grupo B = todos os outros depositantes (inclui MULTI).
- Estatística: M14 padronizado de A menos o de B. Padronização com `comum.taxa_padronizada` por faixa de endereços (1, 2, 3, 4-5, 6+) com os pesos `peso_faixa_pap_rc_*` de `limiares_descoberta` (fixos). Ciclo = `ciclo_t900` (base); `coalesce(ciclo, 0)`.
- Direção: menor que zero. Nulo: zero.
- Unidade: operador, bloco de semana e dia (vale o mais largo).
- Robustez: ciclo no teto conservador do G2; sinal por faixa (sem inversão); retirar um operador por vez; semanas pares da janela base; versão sem os dias pós-pausa.
- Efeito relevante: 10% do M14 padronizado do grupo B nas semanas pares.
- Leitura comercial: confirmada, o argumento "a linha de base da Royal Canin vale para o armazém" sai da oferta e CR5 passa a ser lido com a produtividade dos outros depositantes. Não confirmada, nada muda.
- Implementação de referência: função `contraste_pad` de `analises/ANA-012.py` (copiar, não importar; não há recorte nela).

## PT-D2 (ordem 2) — no dia de pico o ciclo tem menos espera (apoio fraco na descoberta)

- Pergunta e critério: P19; CR8 (M23).
- Hipótese: nos dias de pico o M14 padronizado do armazém é maior que nos dias típicos. Se for, converter o excedente de linhas do dia p90 em horas com o M14 típico superestima as horas excedentes.
- Recorte: `prep_prod_ciclos`, todos os tipos de onda, manual, filtros de M14, **dias plenos** das semanas pares. Dia de pico = volume diário do armazém (`comum.volume_diario`, M05) maior ou igual a `volume_p90`; dia típico = volume entre `volume_q1` e `volume_q3`. Os três limiares vêm de `limiares_descoberta` e **não** são recalculados nas semanas pares.
- Estatística: M14 padronizado dos dias de pico menos o dos dias típicos; células tipo de onda e faixa de endereços com os pesos `peso_celula_*` (fixos); ciclo `ciclo_t900`.
- Direção: maior que zero. Nulo: zero.
- Unidade: operador, bloco de semana e dia (dias reamostrados dentro do tipo de dia); vale o mais largo.
- Robustez: ciclo no teto conservador do G2; sinal por tipo de onda; retirar um operador por vez.
- Efeito relevante: 10% do M14 padronizado dos dias típicos nas semanas pares.
- Aviso de desenho: na descoberta o IC do tratamento primário cruza o zero (apoio fraco), e o resultado muda com a semana do incidente dentro (`dif_m14_pico_tipico_pad_com_incidente`). São poucos dias de pico por recorte; o poder tende a ser baixo. É a pista de menor apoio; o planejador decide se vale um teste a mais na F2.
- Implementação de referência: `contraste_pad` com `estrato_dia`.

## PT-D3 (ordem 3) — mais tempo fora do relógio na Royal Canin

- Pergunta e critério: P10; CR3.
- Hipótese: no pedido-a-pedido, a mediana do intervalo entre tarefas do mesmo operador (M10 a) é maior na Royal Canin que nos outros depositantes. Mostra onde a ida ao packing e a troca de etiqueta pesam mais e quanto do ciclo da Royal Canin é espera fora do alcance do robô.
- Recorte: `prep_prod_ciclos`, `tipo_onda = 'pedido_a_pedido'`, dias plenos das semanas pares, sem dia parcial, sem CANCELADO, `intervalo_entre_tarefas_s` não nulo e entre zero e o teto base. A hora e o depositante são os da linha que termina antes do intervalo (como em `comum.intervalos_dia_hora`). Grupo A = Royal Canin; grupo B = demais.
- Estatística: mediana do intervalo de A menos a de B (linhas agrupadas, sem ponderar por operador).
- Direção: maior que zero. Nulo: zero.
- Unidade: operador, bloco de semana e dia (vale o mais largo).
- Robustez: teto conservador do G2; retirar um operador por vez; sem os dias pós-pausa.
- Efeito relevante: 10% da mediana do grupo B nas semanas pares.
- Leitura: descritiva da estrutura do tempo fora do relógio; não prova que o robô elimina esse tempo.
- Implementação de referência: `dif_intervalo` em `analises/ANA-012.py`.

## PT-D4 (ordem 4) — a lentidão da Royal Canin também aparece no checkout e na colmeia

- Pergunta e critério: P9; CR3 e CR7.
- Hipótese: no checkout e na colmeia, o M14 padronizado da Royal Canin é menor que o dos outros depositantes. Se vale nos três tipos de onda, a causa tende a ser produto e layout; se só vale no pedido-a-pedido, é processo. Muda o que se pode prometer ao usar a produtividade da colmeia (CR7).
- Recorte: `prep_prod_ciclos`, `tipo_onda in ('checkout', 'colmeia')`, filtros de M14, semanas pares. Grupo A = Royal Canin; grupo B = demais.
- Estatística: M14 padronizado de A menos o de B, células tipo de onda e faixa de endereços com os pesos `peso_celula_rc_cc_*` (fixos); ciclo `ciclo_t900`.
- Direção: menor que zero. Nulo: zero.
- Unidade: operador, bloco de semana e dia (vale o mais largo). Na descoberta há poucos operadores nesses tipos (faixa de dez a dezenove): IC com aviso e comparado ao de bloco de semana.
- Robustez: teto conservador do G2; sinal por tipo de onda (checkout e colmeia separados); retirar um operador por vez.
- Atenção: o viés declarado de M05 (visita contada várias vezes no checkout e na colmeia) vale para os dois grupos; a diferença entre grupos não o remove, só o torna comum.
- Efeito relevante: 10% do M14 padronizado do grupo B nas semanas pares.

## Olhado e não proposto (para registro dos caminhos percorridos)

- M14 antes contra depois da faixa de refeição: com o tratamento do incidente e o IC por dia, o IC cruza o zero nos dois tetos (gravado como `dif_m14_antes_depois_refeicao_pad*`, descritivo).
- Razão do M14 do novato sobre o dos experientes por semana desde a entrada (PT-H09): painel pequeno, razões extremas; fica como pista a priori já no plano, com leitura descritiva.
- Tempo por coleta (M08) da Royal Canin contra os outros: sinal na mesma direção de PT-D1, mas o IC de cada grupo se sobrepõe; seria um segundo teste do mesmo fenômeno e foi deixado de fora para não gastar alfa da F2.

## O que o planejador e o estatístico precisam fazer antes de ANA-016

1. Registrar as pistas aceitas em ANA-016 (campo `pistas`) e em F2, com recarimbo do plano. O carimbo precisa ser anterior ao campo `em` de ANA-016 em `saidas/registro.json`.
2. Estender `analises/ANA-000.py`: hoje ele levanta erro para pista fora de `PISTAS_IMPLEMENTADAS`; é preciso EP e MDE de PT-D1 a PT-D4 (só poder, sem efeito) e registrar ANA-000 de novo. O alfa da família passa a ser o do novo número de testes em F2.
3. Implementar PT-D1 a PT-D4 em `ANA-016.py` com os limiares de `limiares_descoberta.csv` lidos do arquivo registrado, sem recálculo.
4. Conferir em `incidente_rc_por_semana_impar.csv` e nos dados das semanas pares que o incidente da Royal Canin não aparece nelas.
