# Parecer do especialista setorial · D3 · interpretação dos resultados (r1)

- Projeto: `projetos/2026-10-03_social_kappabot-operacao/v1` · 2026-10-03 · agente `dados-especialista-setorial`.
- **Revisão r1.** Responde a `revisoes/sup-negocio_D4_r1.json`. A resposta ponto a ponto está em `revisoes/especialista-setorial_resposta_r2.md`.
  - Cinco valores foram atualizados pelos resultados de 20:03 a 20:06 e por `saidas/impacto.json` de 20:06.
  - 1.7, 1.8, 1.9, 1.10, 1.12, a seção 2 (U1, U2, U4, U5 e N6, mais N13 e N14) e a seção 3 foram reescritos.
  - "A conta da Acta leva à ALT6" e "ALT6 desde a primeira fase" saíram.
  - O parecer de viabilidade está em `revisoes/especialista_D4.md`.
- Perfil assumido: gerente de operações e engenharia de armazém de 3PL no Brasil (`perfil_especialista.md`, `nos/especialista.json`). A lente 2 (comercial e RaaS) tem confiança baixa.
- Entradas lidas:
  - `nos/decisao.json` e `nos/plano.json`;
  - `saidas/analises/ANA-000` a `ANA-017` (`resultado.json`, valores e notas) e duas tabelas agregadas de resultado (`ANA-010/perfil_por_depositante_e_tipo_de_onda.csv` e `ANA-011/ponte_deck_wms.csv`);
  - `saidas/insights.json`, `saidas/impacto.json` (20:06) e `saidas/memo_decisao.md`;
  - `revisoes/orquestrador_decisao_semana_incidente.md`, `orquestrador_decisao_regime_colmeia.md` e `orquestrador_decisao_inversao_ANA-016.md`.
  - Não li linhas de dados.
- Números: cito só valores dos resultados (`ANA-xxx.chave`), dos modelos (`IMP-...`) ou dos insights, mais parâmetros da decisão e faixas do setor com fonte do perfil. Não fiz conta nova.
- Bases:
  - "Normal" é a base da oferta: as quatro semanas até 18/09.
  - "Estresse" é a janela do plano, com o incidente.
  - "Pós-colmeia" é a base de pico e frota da RC, por decisão do orquestrador, a confirmar por Marcus no G3.

## Conclusão

1. **O problema é escala.** O escopo da Royal Canin (RC) é pequeno demais para a oferta do deck: receita (INS-001), FTE (INS-011), frota (INS-055) e margem (INS-085) dizem o mesmo.
   - O valor que ainda pode existir está na **conferência** (PR11), que o WMS não mede.
   - Os modelos atuais mostram que só o volume agrupado não fecha a conta sem o checkout:
     - `IMP-ALT6-DEP-CHECKOUT` (0,79 da receita da ALT6 vem do checkout);
     - `IMP-MARGEM-ARM-PAP-POOL` (−464 R$/robô/mês);
     - `IMP-FOLGA-ALT6-SEM` (−4.697 R$/mês).
   - Concordo com o memorando: ALT1 como portão sobre PR11.
2. **As cerca de 50 coletas/h manuais são plausíveis como taxa em tarefa, não por hora paga** (1.2). O WMS não decide o dobro (INS-006). `validar com pessoa do setor`.
3. **O volume implícito do deck tem explicação provável:** a semana de retomada depois do incidente, multiplicada pelos dias do mês (1.3). `validar com pessoa do setor`.
4. **Os postos de conferência talvez não sejam só da RC, e também embalam** (1.5). O rateio por pedidos dá `IMP-PR11-RATEIO-POSTOS` (0,47 posto), abaixo do limiar `IMP-INV-PR11-CR1-ALT4-ALT3` (0,58). `validar com pessoa do setor`.
5. **No pedido-a-pedido, a RC é mais lenta que o conjunto dos outros depositantes** (PT-D1). Produto e layout são as explicações mais prováveis. No checkout, na colmeia e no tempo fora do relógio, as pistas não se confirmam: o grupo de comparação é heterogêneo (1.10). Não usar como crítica à Social.
6. **O incidente de 21 a 25/09 provavelmente não foi falta de mão de obra** (1.14). Não usar como argumento de venda.
7. **Argumentos:**
   - Usar, com as ressalvas da seção 2: elasticidade no pico do armazém (U1, com alívio parcial); ergonomia (U3); auditoria amostral (U8, condicionada ao checkout pronto e ao aceite da RC).
   - Rebaixados nesta revisão: frota compartilhada (U2) e integração (U4).
   - Não usar: N1 a N14.
8. **Reformulação:** a do memorando (ALT1 como portão, depois ALT4, e ALT6 como fase seguinte e condicionada ao checkout).
   - O custo de implementação ainda não está no motor e pode mudar os limiares.
   - A viabilidade operacional dos dois ramos está em `revisoes/especialista_D4.md`.

## 1. Achados decisivos

Formato: o dado, a explicação do setor, a alternativa óbvia, o que um gerente de 3PL estranharia e a consequência.

### 1.1 A franquia fica muito acima da receita por transação (ANA-002; INS-001, INS-002)
- **Dado.** CR2 falha nas duas janelas (`ANA-002.classe_cr2_alt3_normal` = −1).
  - Cobertura na ALT3: `ANA-002.cobertura_franquia_alt3_normal` (`IMP-CR2-ALT3-NORMAL`, 0,384).
  - Para cobrir a franquia, o checkout teria de chegar a `IMP-CR2-VOLUME-CHECKOUT-ALT3` (3.236 pedidos/mês).
- **Explicação do setor (média).** A franquia foi desenhada para um volume que não é o corrente (1.3). Pela lente 2 (baixa), "assinatura base mais tarifa por transação acima de uma franquia incluída" é estrutura comum (Fulfill.com, 2026, EUA). Ali, a franquia cabe no volume.
- **Alternativa óbvia.** O volume vai crescer. O dado não sustenta isso:
  - a melhor previsão é a média de quatro semanas (INS-061);
  - a tendência é negativa ou nula (INS-004, INS-062);
  - a alta temporada não está nos dados.
- **O que um gerente de 3PL estranharia.**
  - A franquia vira custo fixo novo para a Social.
  - O volume elegível do pedido-a-pedido caiu por decisão de processo da própria Social (degrau da colmeia, `ANA-001.degrau_colmeia_part_pap_rc`; INS-003). Num contrato de PR14, o risco desse volume fica com a Social.
- **Consequência.** CR2 falha por estrutura. Confiança: alta para o fato, média para a leitura de risco.

### 1.2 A linha de base manual fica acima de PR06 (ANA-004; INS-005, INS-006, INS-007, INS-084)
- **Dado.**
  - Ritmo manual: `ANA-004.linhas_hora_pap_rc_t300` (50,59 coletas/h, teto conservador), `..._t900` (37,15) e `..._t1800` (31,16).
  - Tempo fora da conta no teto conservador: `ANA-004.fracao_tempo_descartado_pap_rc_t300` (0,6866).
  - Tempo por coleta: `ANA-004.t_coleta_manual_ponderada_s` (63,01 s) e mediana `..._mediana_s` (51 s).
  - Com truncamento das pausas (S2), a razão PR05 sobre o manual sobe para perto do dobro ou acima. O WMS não decide o dobro, nem a favor nem contra (INS-006).
- **50 coletas/h manuais são plausíveis?**
  - **Como taxa em tarefa, sim (média).** No teto de 300 s, M14 conta coletas por hora em tarefa de separação.
    - O tempo por coleta é coerente com separação com carrinho dominada por deslocamento: de 50% a 55% do tempo, segundo de Koster et al. (2007), para separação com papel (média).
  - **Como taxa por hora paga ou presente, não.** As referências por pessoa-hora ficam perto de PR06:
    - eixo de cerca de 15 a 25 em 36 armazéns dos EUA, sem denominador (Bartholdi e Hackman, Fig. 15.5; baixa);
    - TCC em São Paulo, de 28,3 para 38,4 linhas por homem-hora (inacessível; baixa).

    Não há contradição: o denominador é outro (armadilha 11 do perfil). O deck mediu "por hora presente", com teto folgado (INS-084).
- **O "dobro" depende do denominador.**
  - PR05 (66) é taxa em zona com 85% de ocupação, isto é, por hora presente. O método de medição é desconhecido (INS-006).
  - O ganho honesto depende do que existe no intervalo entre pedidos:
    - ida ao packing e etiqueta, que o robô tira;
    - outras tarefas e pausas, que o robô não tira.

    O WMS não separa um do outro (INS-073).
- **Ocupação (média).** O pedido-a-pedido inteiro da RC consome `ANA-003.horas_dia_escopo_alt2_t300_normal` (1,61 h por dia pleno). Um separador dedicado à zona da RC ficaria ocioso a maior parte do dia. Fontes: filas (Bartholdi e Hackman, 16.3; alta) e o modo swarm (RSM; média).
- **Robô contra manual (INS-007, INS-009).** As definições não são iguais.
  - A missão do robô inclui a primeira perna, o que pesa contra o robô.
  - A amostra do relatório só tem pedidos de dois ou mais endereços.
  - A conta do robô capta só as devolutivas automáticas.
  - Por escolha da operação, o robô recebe mais pedidos de um endereço: 68,6% contra 47,0% no manual (INS-009).

  Esses vieses puxam em sentidos opostos. Só um teste com pedidos sorteados resolve.
- **O que um gerente de 3PL estranharia.** O manual da RC caiu ao longo do período:
  - de `ANA-004.linhas_hora_pap_rc_mes_2026_06` (54,68) para `..._mes_2026_09` (41,84);
  - de `ANA-004.linhas_hora_pap_rc_pre_robo` (53,85) para `..._pos_robo` (44,69).

  A colmeia entrou na semana ISO 28 (`ANA-001.semana_primeira_colmeia`) e o robô em PAR11 (20/07), e os efeitos estão confundidos.
  - Leitura do setor: o pedido-a-pedido virou fluxo residual depois da colmeia.
  - Alternativa: o robô interfere ou exige atendimento do separador.
- **Consequência.** A promessa de dobro sai. O ganho se mede no teste controlado, com o método do WMS (M14 nos tetos de 300 e 900 s) e pedidos sorteados.
- `validar com pessoa do setor`:
  - operação da Social: o que o separador faz entre um pedido e o próximo;
  - engenharia da Acta: a regra que manda pedidos ao robô (E17).

### 1.3 O volume implícito do deck não aparece no WMS (ANA-011; INS-080, INS-081)
- **Dado.**
  - Nenhuma base testada reproduz franquia e economia ao mesmo tempo (`ANA-011.n_bases_que_reproduzem_os_dois_normal` = 0).
  - O implícito equivale a `ANA-011.razao_implicito_corrente_normal` (6,28) nas linhas e `..._checkout_normal` (3,47) no checkout.
  - O checkout implícito é `ANA-011.vol_implicito_checkout_em_dias_do_slide10` (30,05) vezes a taxa diária do slide 10.
  - Na tabela `ponte_deck_wms`, as taxas diárias do deck vêm do 9fleet na "última semana" (25/09 a 02/10), fora da extração do WMS: linha S8c (248 pedidos por dia) e linha S10d (127 pedidos de checkout por dia).
  - Pelo WMS, a RC tem `ANA-013.rc_pedidos_por_dia_pleno_sem_incidente` (147,4 pedidos por dia).
- **Explicação do setor (média).** É a semana logo depois do incidente. Depois de uma parada, o 3PL separa a fila acumulada: é semana de retomada, não taxa corrente.
  - O WMS mostra o mesmo fenômeno em escala menor (INS-026, INS-028).
  - Multiplicar uma semana de retomada pelos dias do mês infla o volume duas vezes, pelo nível e pelos dias.
- **Alternativas.** A RC cresceu de fato. Ou o 9fleet conta outra coisa (as linhas R05 e R06 da ponte já mostram diferença de recorte).
- **Consequência.** Isso decide a franquia e a frota do deck.
- `validar com pessoa do setor` (autor do deck e Social): E12 e E13.

### 1.4 O FTE do escopo fica muito abaixo do slide 14 (ANA-003, ANA-011; INS-010, INS-011, INS-083)
- **Dado.**
  - Escopo da ALT3: `ANA-003.fte_escopo_alt3_t300_normal` (0,30 FTE) contra 1,86 no slide 14.
  - Jornada ativa por operador-dia em dia típico: `ANA-003.h13a_media_jornada_tipicos_h` (2,08 h).
  - Armazém: de `ANA-003.fte_armazem_t300` (1,81) a `..._t1800` (2,67) FTE de separação ativa.
  - Operadores por dia: `ANA-013.ativos_dia_media` (7,95, corte de uma linha) e `..._1h` (4,59, corte de uma hora).
- **Explicação do setor (média).** O separador de um 3PL deste porte é polivalente, e o WMS registra só a separação. H13b não acha espera relevante (INS-014): o tempo fora do WMS parece outras atividades.
- **Leitura provável do slide 14.** Conta pessoas que tocam a RC no dia (`ANA-013.ativos_dia_media_rc_sem_incidente`, 2,93), não horas de separação.
- **Alternativa.** A RC tem equipe dedicada (E18).
- **Consequência.** Corte de quadro não é argumento. O argumento é absorver pico e crescimento.
- `validar com pessoa do setor` (Social).

### 1.5 A conferência não está nesta exportação do WMS, e PR11 pesa no custo (INS-012, INS-089)
- **Dado.**
  - A exportação de produtividade não traz conferência. O módulo de conferência do Senior é outro relatório e pode registrar o que falta (INS-012).
  - Do custo atual da ALT3, `ANA-015.fracao_custo_atual_alt3_vinda_de_pr11` vem de PR11 (0,90).
  - Pelo rateio de pedidos de checkout, a parte da RC é `IMP-PR11-RATEIO-POSTOS` (0,47 posto).
- **Explicação do setor.** No Checkout Express, a conferência é um bipe em bancada (Senior 8.12; alta). Na prática, a mesma bancada embala e etiqueta (média). O checkout conferido no robô tira o bipe, não a embalagem.
- **O que um gerente de 3PL estranharia (decisivo).**
  - São dois postos para o checkout da RC, que tem `ANA-002.taxa_pedidos_checkout_rc_dia_normal` (52,4 pedidos por dia).
  - O checkout dos outros depositantes é maior (`ANA-010.taxa_pedidos_checkout_outros_dia`, 158,1).
  - Leitura provável: os postos são compartilhados.
- **Alternativa.** A RC exige conferência própria (SLA, kit), com postos dedicados.
- **Referência.** A GEODIS passou a auditoria de 100% para 10% com AMR (média). Isso vale só se a RC aceitar bipe na coleta.
- **Consequência.** É o portão do memorando. A resposta da Social precisa ser medida, não declarada (ver D4).
- `validar com pessoa do setor` (Social): E15 e E20.

### 1.6 A colmeia fica inconclusiva em CR7 (ANA-007; INS-023, INS-024)
- **Dado.** `ANA-007.linhas_hora_colmeia_rc` (70,28, teto base), com IC que cruza PR05 (`ANA-007.classe_cr7` = 0). Sobreposição `ANA-007.fracao_sobreposicao_colmeia` (0,971).
- **Explicação.** O lote dilui a caminhada (Bartholdi e Hackman, 3.3; alta), e M05 conta a mesma visita várias vezes. A distribuição no put wall não aparece (E3).
- **Alternativa.** A distribuição é registrada em outro lugar ou feita por outra pessoa.
- **Robô na colmeia (interpretação, baixa).** O ganho sobre lote tende a ser menor que sobre pedido-a-pedido.
- **Consequência.** ALT5 entra como teste de prioridade baixa, depois de E3. `validar com pessoa do setor`.

### 1.7 Outros depositantes e frota compartilhada (ANA-010; INS-029 a INS-033, INS-088) — reescrito na r1
- **Dado.**
  - CR5 em linhas fica inconclusivo depois da robustez (`ANA-010.classe_cr5_linhas_apos_robustez` = 0).
  - Sem o maior depositante, a razão cai para `ANA-010.razao_demanda_pr07_outros_sem_maior` (0,55).
  - **Frota agrupada, calculada dia a dia (INS-031):**
    - entre os dois depositantes relevantes, o pooling poupa robôs: 4 agrupados contra 6 individuais;
    - mas a correlação diária entre esses dois é positiva (0,36 na janela longa), então **os picos não se compensam**;
    - a média de pares perto de zero (`ANA-010.correlacao_media_volume_dia_maiores_depositantes`) não descreve esse par.
  - **Margem do robô adicional:** `ANA-010.margem_robo_adicional_mes_normal` (554 R$/robô/mês; o valor de 1.590 era a leitura pela banda, superestimada), com hardware máximo de 13.260 R$/robô (INS-032).
- **Explicação do setor.** Um 3PL multi-cliente ganha com escala e sazonalidade complementar (Bartholdi e Hackman, cap. 1; alta para a fonte, baixa para frota).
  - Os dados de junho a setembro não mostram complementaridade entre os dois depositantes que pesam. Pode haver no quarto trimestre: brinquedos concentraram 64% do movimento de agosto a dezembro (ABRINQ, 2017; média). Pet food e cosméticos: [●].
- **O que um gerente de 3PL estranharia.**
  1. Os outros têm, em geral, pedidos pequenos e leves (tabela de ANA-010). O concorrente do robô é o lote manual com carrinho, sem investimento (Bartholdi e Hackman, 3.3; alta).
  2. No manual, eles já separam mais rápido que a RC (INS-070).
  3. A receita da ALT6 vem quase toda do checkout (`IMP-ALT6-DEP-CHECKOUT`, 0,79), que não está desenvolvido.
  4. A receita supõe que todo o volume compatível dos clientes da Social vá ao robô na tarifa da RC (INS-032).
- **Consequência.** A ALT6 não é a saída sem o checkout. Fica como fase seguinte, condicionada ao checkout e à adesão.
- `validar com pessoa do setor` (Social): processo e estabilidade dos dois depositantes relevantes.

### 1.8 A frota necessária no p90 fica abaixo da do deck (ANA-009; INS-054, INS-055, INS-058) — atualizado na r1
- **Dado.**
  - ALT3 na base pós-colmeia, dia a dia: `ANA-009.frota_necessaria_alt3_pos_colmeia` (2; de 1 a 2), contra PR09 de 4 a 5. No dia típico sobram `ANA-009.sobra_dia_tipico_alt3_pos_colmeia` (3).
  - ALT6: `ANA-009.frota_necessaria_alt6_pos_colmeia` (5; de 3 a 5). Pela banda, a frota seria 4, o que subestima o pico.
  - Armazém sem filtro: `ANA-009.frota_armazem_p90_so_linhas` (9) contra `ANA-009.slide12_robos_armazem` (7).
  - Nenhuma frota inclui reserva de disponibilidade.
- **Explicação do setor (média).** O deck dimensionou pelo volume implícito (1.3).
- **Alternativa.** O deck dimensionou para crescimento ou para a alta temporada.
- **Ressalvas.**
  - A curva horária é de processamento, não de chegada (INS-027).
  - O robô é colaborativo: `ANA-009.separadores_pico_p90_com_robo` = `..._sem_robo` = 1. No escopo da RC, o robô não muda o número de pessoas na hora de pico.
- **Consequência (setor; média).** Com frota de um ou dois robôs, uma parada derruba metade ou toda a capacidade. Reserva não é opcional (D4).

### 1.9 A margem por robô depende da franquia e do checkout (ANA-015; INS-085 a INS-088) — reescrito na r1
- **Dado.**
  - Frota do slide 14, sem piso: `ANA-015.margem_robo_alt3_pr09_sem_piso_normal` (−546).
  - Frota necessária, sem piso: `IMP-CR6-ALT3-SEM-PISO` (134), sem reserva. Hardware máximo: `IMP-CR6-ALT3-HW-SEM-PISO` (3.219 R$/robô).
  - ALT6 total: `IMP-CR6-ALT6-TOTAL` (`ANA-015.margem_robo_alt6_total_normal`, 1.007 R$/robô/mês), com hardware de `IMP-CR6-ALT6-HW` (24.177 R$/robô). **Essa margem usa as tarifas do deck, com as quais a economia da Social na ALT6 fica abaixo de PR01** (`IMP-CR1-ALT6-DECK-INT`, 0,109).
  - Com o preço no teto de CR1, o hardware máximo cai para `IMP-ALT4-HW-ALT6-PMAX` (15.856 R$/robô), e só existe com PR11 integral.
  - Sem PR11, a ALT6 não tem janela (`IMP-FOLGA-ALT6-SEM`, −4.697 R$/mês).
  - Pedido-a-pedido do armazém agrupado, sem checkout: `IMP-MARGEM-ARM-PAP-POOL` (−464) e `IMP-FOLGA-ARM-PAP-POOL` (−3.697). Fica positivo só no teto mais folgado (`IMP-FOLGA-ARM-PAP-POOL-ALTO`, 378).
- **Lente 2 (baixa).** RaaS para 3PL usa mensalidade por robô ou cobrança por transação, com pool de pico (Cleverence).
- **Leitura revista.**
  - A conta da Acta **não** leva à ALT6 por si só. Ela depende da mesma conferência que decide a ALT4 (`IMP-INV-PR11-ALT6-REC`, 1,17 posto).
  - Volume agrupado ajuda, mas não substitui o checkout.
  - Os modelos ainda não incluem implantação, mapeamento nem integração (`saidas/impacto.json` de 20:06 não tem esses modelos). Os hardwares máximos acima são, na prática, o teto de hardware **mais** implementação.
- **Consequência.** Todas as margens são provisórias até o analista registrar o custo de implementação.

### 1.10 RC mais lenta (ANA-016; INS-070, INS-071, INS-072, INS-077) — atualizado na r1
- **Dado.**
  - **PT-D1 se confirma** no pedido-a-pedido: `ANA-016.pt_d1_dif_m14_pad` (−19,47 coletas/h). A confirmação depende do critério de inversão fixado depois dos sinais. Pelo critério só de sinal, a pista cairia.
  - **PT-D3 e PT-D4 não se confirmam** (`ANA-016.pt_d3_confirmada` = 0; `..._d4_confirmada` = 0). Contra um depositante o sinal se inverte: no checkout e na colmeia, a RC roda mais coletas por hora que ele (INS-071), e o tempo fora do relógio dela é menor (INS-072).
- **Explicações do setor (média para a ordem; [●] para os fatos).**
  1. **Produto.** A RC tem `unidades_por_linha_p50` = 3 e `_p90` = 31 no pedido-a-pedido (tabela de ANA-010), contra 2 e 6 na HIVE. M14 não padroniza unidades nem peso. Peso por item: [●].
  2. **Layout.** Item volumoso em porta-palete, longe do packing ([●]).
  3. **Validade.** FEFO por lote e validade ([●]).

  A heterogeneidade em PT-D3 e PT-D4 é coerente com produto: um depositante de itens mais pesados ou volumosos que os da RC seria mais lento que ela.
- **Alternativas.** Composição da equipe. Efeito do robô e da colmeia no pedido-a-pedido (1.2).
- **Consequência.**
  - Há argumento de ergonomia (U3) se for peso: NR-17 (média) e retenção (Manhattan e Vanson Bourne, 2024; média). Depende da carga útil do Kappabot ([●], E9).
  - "A RC é lenta" não vai para a Social (N10).
  - Sem PT-D3 confirmada, "o desperdício está entre pedidos" (U5) perde força.
- `validar com pessoa do setor` (Social, E16; engenharia da Acta, E9).

### 1.11 Os operadores ativos sobem com o volume (PT-H10; INS-074, INS-048)
- **Dado.**
  - `ANA-016.pt_h10_coef` (2,24 operadores por mil linhas). Parte disso é mecânica (INS-074).
  - Dias de pico contra típicos: `IMP-CR8-PICO-ARM-PESSOAS` (2,83 pessoas a mais) e `IMP-CR8-PICO-ARM-EXCEDENTE` (5,12 pessoas-hora/dia).
  - A frota alivia no máximo `IMP-CR8-PICO-ARM-ALIVIO-COL` (1,20 pessoas-hora/dia) na leitura colaborativa.
- **Explicação do setor (média).** A Social puxa gente de outras funções no pico.
- **Alternativa.** Remanejamento sem contratação, temporário ou a folga da própria equipe (INS-048).
- **Consequência.** U1 vale, mas o robô alivia só uma parte do excedente. Valor em reais só com E11.

### 1.12 A jornada ativa é maior nos dias de pico (H13a; INS-013, INS-015) — atualizado na r1
- **Dado.**
  - Armazém: `ANA-003.h13a_dif_jornada_operador_h` (0,87 h). No escopo da RC, o IC contém zero (`ANA-003.h13a_dif_jornada_escopo_rc_h`).
  - Excedente do p90 da RC na base pós-colmeia: `ANA-003.excedente_h_p90_escopo_poscolmeia` (`IMP-CR8-P90-RC-EXCEDENTE`, 1,20 h por dia).
  - Na janela normal: `ANA-003.excedente_h_p90_escopo_normal` (0,82 h, só descritivo).
  - A frota absorve `IMP-CR8-P90-RC-PCT-COL` (0,04) desse excedente na leitura colaborativa.
- **Explicação do setor.** É folga redistribuída. Pode ser hora extra (indeterminado).
- **Consequência.** "Pico sem temporário" na RC não se sustenta (N6). O argumento de pico vive no armazém.

### 1.13 Previsão de volume (ANA-014; INS-060 a INS-062)
- **Dado.** A média de quatro semanas ganha (`ANA-014.mae_janela_4s`, 21,69, contra `mae_historia`, 76,96). A alta temporada não está modelada.
- **Explicação do setor.** O mix mudou por decisão de processo.
- **Alternativa.** O período é curto e sem sazonalidade.
- **Consequência.** Revisão trimestral de piso e frota. Pedir Black Friday e dezembro (QP4).

### 1.14 O incidente da RC de 21 a 25/09 (INS-060, INS-078)
- **Dado.** Na semana, a RC variou −99,0% e os demais −7,3% (INS-060).
- **Explicação do setor (média).** Com equipe compartilhada, falta de pessoal derrubaria todos os depositantes. A causa provável é da RC ([●]): fluxo de pedidos, estoque ou inventário.
- **Alternativa.** Uma equipe dedicada à RC (E18).
- **Consequência.**
  - Não usar como argumento de mão de obra (N9).
  - Usar para desenhar o preço: cláusula de queda de volume de um depositante.
- `validar com pessoa do setor` (Social, E14).

### 1.15 Pedidos de um endereço no pedido-a-pedido da RC (INS-051)
- **Dado.** 45,3% dos pedidos-a-pedido da RC têm um só endereço.
- **Explicação.** Esse perfil rende mais em lote (Bartholdi e Hackman, 3.3; alta), ou no Checkout Express, se tiver uma unidade.
- **Alternativa.** Pedido urgente ou com várias unidades.
- **Consequência.** Há ganho de processo sem robô. A Acta deve apontá-lo.

## 2. Argumentos de venda (os rótulos U e N continuam; a r1 revê U1, U2, U4, U5 e N6 e cria N13 e N14)

### Usar, com as condições indicadas

| # | Argumento | Base | Força | Condição |
|---|---|---|---|---|
| U1 | No pico, a separação puxa gente de outras áreas; o robô reduz **parte** desse puxão | INS-074, INS-048; `IMP-CR8-PICO-ARM-EXCEDENTE`, `IMP-CR8-PICO-ARM-ALIVIO-COL` | média a baixa | Falar em pessoas e pessoas-hora. O alívio é parcial. Robô colaborativo exige gente na mesma hora. E11 para reais. |
| U2 | Uma frota compartilhada entre depositantes, paga por transação | INS-031, INS-058, INS-088 | **baixa** (rebaixada) | Só como fase seguinte. O pooling poupa robôs, mas os picos dos dois depositantes relevantes andam juntos. Depende do checkout (`IMP-ALT6-DEP-CHECKOUT`) e da adesão. |
| U3 | Menos transporte de carga pelo separador na RC | tabela de ANA-010; NR-17; Manhattan e Vanson Bourne | média a baixa | Peso por item [●]; carga útil do Kappabot [●]. |
| U4 | Pedidos do robô identificáveis no WMS | INS-009 | **média** (rebaixada) | A integração que existe (importação de ondas e devolutiva automática) já roda. Mas a conta do robô capta só as devolutivas automáticas: para a Social conferir a cobrança por transação, toda transação do robô precisa ser marcada. **O checkout conferido é integração nova** (D4). |
| U5 | O desperdício na RC está entre pedidos (ida ao packing, etiqueta) | INS-072, INS-073 | **baixa** (rebaixada) | PT-D3 não se confirmou (inversão contra um depositante). Só como hipótese do teste. |
| U6 | Crescer contratando menos | Manhattan e Vanson Bourne; DIEESE (proxy) | baixa a média | Só qualitativo (E11). |
| U7 | Treino mais curto | DHL; MD Logistics | baixa | Dizer "casos dos EUA". Nunca proficiência. |
| U8 | Auditoria amostral em vez de conferência total | GEODIS | média | Só com checkout pronto e aceite da RC (E15). |

### Não usar

| # | Argumento | Por quê |
|---|---|---|
| N1 | "Dobra a produtividade" | O WMS não decide o dobro, e PR05 tem método desconhecido (INS-006). |
| N2 | FTE do slide 14 e "libera vagas" na RC | Não se reproduz e fica abaixo de uma vaga (INS-010, INS-011, INS-083). |
| N3 | Economia garantida de PR01 sobre um custo com PR11 | Não medido, talvez compartilhado, depende de desenvolvimento (1.5). |
| N4 | Economia do slide 15 e franquia de "dois terços" | O volume implícito não aparece no WMS (1.3). |
| N5 | Frota de quatro a cinco robôs para a RC | Sobra (INS-055). |
| N6 | "Pico sem temporário" na RC | O excedente é uma fração de jornada (`IMP-CR8-P90-RC-EXCEDENTE`). O robô absorve pouco na leitura colaborativa (`IMP-CR8-P90-RC-PCT-COL`). O arranjo "temporário" (`ANA-009.h02_regraB_manual_temporario_pessoas_hora_p90`) contrata um dia inteiro para poucas horas. |
| N7 | "O robô coleta mais rápido" | As definições diferem, e a comparação tem baixa confiança (INS-007). |
| N8 | Curva do novato e rotatividade por login | Inconclusivo; login não é pessoa (INS-045, INS-050, INS-075). |
| N9 | O incidente como dependência de pessoas | A causa é provavelmente da RC (1.14). |
| N10 | "A RC é lenta" como crítica | Associativo e heterogêneo (1.10). |
| N11 | Ganhos de UPH dos EUA como promessa | Só ordem de grandeza. |
| N12 | Horário estendido sem custo | Não há operadores depois da janela (INS-057). Adicional mínimo de 50% (CF, art. 7º, XVI) ou noturno (CLT, art. 73). |
| N13 | **Novo.** A margem da ALT6 (`IMP-CR6-ALT6-TOTAL`) como prova de viabilidade | Usa tarifas com as quais CR1 da ALT6 falha (`IMP-CR1-ALT6-DECK-INT`). Não inclui implementação. |
| N14 | **Novo.** "Integração pronta" para o checkout conferido | Só a importação de ondas e a devolutiva automática rodam. O checkout conferido é integração nova com o Senior (D4). |

## 3. Como reformular a oferta (reescrito na r1; alinhado ao memorando)

1. **Retiro a proposta "ALT6 desde a primeira fase, com pedido-a-pedido do armazém primeiro".** Os modelos a contrariam: `IMP-MARGEM-ARM-PAP-POOL`, `IMP-FOLGA-ARM-PAP-POOL` e `IMP-ALT6-DEP-CHECKOUT`. O pedido-a-pedido agrupado só aparece como **hipótese de um piloto pago**: no teto mais folgado a folga é positiva (`IMP-FOLGA-ARM-PAP-POOL-ALTO`), mas a tarifa teria de subir (`IMP-KMIN-ARM-PAP-POOL`, 1,87 vezes PR04).
2. **Sequência:**
   - ALT1 como portão sobre PR11, medido (D4);
   - se passar, ALT4 no escopo da ALT3, com frota necessária mais reserva;
   - ALT6 como fase seguinte, condicionada ao checkout e à adesão dos depositantes.
3. **Preço.**
   - Piso igual ao custo de servir da frota contratada, com reserva (`IMP-KMIN-ALT4-ALT3-COM-RESERVA`).
   - Cláusula de queda de volume de um depositante e revisão trimestral (lente 2; baixa).
   - **Corrijo a r0:** "o que fecha a conta é volume agrupado, não preço" não se sustenta. O que fecha a conta é a conferência desmobilizada. Volume agrupado sem checkout não fecha (1.9).
   - Implantação, mapeamento e integração: cobrar à parte ou amortizar explicitamente. O "tudo incluído" do slide 18 transfere esse custo para a Acta. Valores: [●] até o analista registrar.
4. **Garantia.** Garantia de capacidade, condicionada ao separador presente (D4). Economia só sobre a conferência medida.
5. **Teste controlado** com pedidos sorteados e critério fixado antes.
6. **Ganhos de processo sem robô** (INS-051), ditos pela Acta.

## 4. Perguntas, com resposta proposta

A numeração continua a do D1. E1 a E11 seguem abertas.

| # | Pergunta | Para quem | Resposta proposta |
|---|---|---|---|
| E12 | As taxas dos slides 8 e 10 (linhas S8c e S10d) são da semana de 25/09 a 02/10? O mês foi feito com dias corridos? | autor do deck | Sim às duas. |
| E13 | Qual foi o volume diário da RC de 28/09 em diante? | Social | Retomada acima do normal e depois volta à média. |
| E14 | Qual foi a causa do incidente de 21 a 25/09? | Social | Do lado da RC. |
| E15 | Os dois postos de PR11 atendem só a RC? Também embalam? A RC aceita conferência na coleta? | Social e RC (via Marcus) | São compartilhados e embalam. |
| E16 | Layout da RC, peso por item, FEFO? | Social | Porta-palete e itens pesados. |
| E17 | Quem escolhe os pedidos do robô? | engenharia da Acta | A operação, por limite de carga. |
| E18 | Existe equipe dedicada à RC? | Social | Não. |
| E19 | **Novo.** Qual o escopo, o prazo e o esforço da integração do checkout conferido com o Senior? Quem altera o Senior: a Social, a Senior ou um integrador? | engenharia da Acta e TI da Social | Integração nova, caso a caso. Prazo e custo [●]. Não começar antes do portão. |
| E20 | **Novo.** O relatório de conferência ou de packing do Senior registra a conferência por posto e por depositante? | Social | Sim. Usar esse relatório para medir PR11 no portão. |
| E21 | **Novo.** Qual área precisa ser mapeada e como está a cobertura da rede sem fio na área da RC e nas dos outros depositantes? | Social | Área [●]. Rede a confirmar na visita. |

## 5. Pendências sugeridas (sem alterar nós)
- **Analista de impacto.**
  - Custo de implementação, como já está em curso.
  - Recalcular os hardwares máximos como "hardware mais implementação".
  - Margem da ALT6 no teto de CR1, como modelo primário de INS-088.
- **Cientista de dados.** PT-D1 antes de PAR11. M14 da RC por unidades por linha.
- **Comunicação.** A oferta deve trocar U2, U4 e U5 pela força revista e incluir N13 e N14. V3 da oferta não deve citar `IMP-CR6-ALT6-TOTAL` como prova.
- **Orquestrador.** Levar E12 a E21 para `saidas/perguntas_terceiros.md`.

## Autoverificação
- [x] **Dentro do perfil.** O que não tem fonte está em [●], e a lente 2 aparece com confiança baixa.
- [x] **Alternativa para cada achado** (de 1.1 a 1.15).
- [x] **Decisivos com `validar com pessoa do setor`:** 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.10 e 1.14.
- [x] **Nenhum número novo.** Todos os valores foram conferidos contra os resultados e modelos de 20:03 a 20:06.
