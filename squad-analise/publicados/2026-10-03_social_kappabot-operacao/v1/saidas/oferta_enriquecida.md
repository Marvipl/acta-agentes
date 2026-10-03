# Oferta enriquecida — Social

> **USO INTERNO DA ACTA. Não encaminhar à Social nem à Royal Canin.** Rascunho pré-G3: 20 de 71 insights aprovados; auditoria aprovada. Todos os insights citados são descritivos.

Para Marcus Lima e Matheus Correa (comercial). Versão v1 · data-base 2026-10-03.

## Em uma frase

Não apresentar o deck como está. Primeiro o portão: a Social diz quantos postos de conferência (PR11) deixam de existir por causa do checkout da Royal Canin, medido no relatório de conferência do Senior. Se passar, cotar a ALT4 da tabela abaixo. Se não passar, propor um piloto pago ou encerrar o piloto gratuito (as duas opções estão fora da lista original de alternativas e pedem o aceite de Marcus no G3). O valor que os dados sustentam está na conferência desmobilizada e no pico do armazém, não na separação da Royal Canin isolada.

**Glossário.** ALT1: manter o piloto atual (aqui, só como portão). ALT2: pedido-a-pedido sem checkout. ALT3: oferta do deck. ALT4: oferta do deck recalibrada. ALT6: oferta ampliada a outros depositantes. CR1: economia mínima da Social. CR2: a receita por transação cobre a franquia. CR6: margem da Acta por robô. CR8: menor dependência de contratação. PR01: garantia mínima de economia do deck. PR05: linhas por hora por operador com robô. PR10: custo por operador. PR11: postos de conferência. PR13: custo de servir por robô, sem hardware. M23: leitura de CR8 (autônoma ou colaborativa).

## Proposta-modelo cotável (ALT4, se o portão passar)

ALT4 no escopo da ALT3 (checkout conferido mais pedido-a-pedido da Royal Canin). Depende do checkout conferido, que não está pronto, e da conferência desmobilizada. Frota de 3 robôs: a necessária dia a dia mais um robô de reserva. Piso igual ao custo de servir da frota total. Preço recomendado: ponto médio da janela (regra do analista; Marcus pode trocar). Volume tarifável corrente: 1.100 pedidos/mês de checkout e 1.595 linhas/mês no pedido-a-pedido.

**Cotar só nestes cenários (todos os postos de PR11 saem por causa da Royal Canin).** "Com implementação" é preço de tabela e a coluna sem desconto é o limite superior do custo; a coluna com desconto tira a implantação do robô que já opera na Social (a integração simples continua contada). A margem da Acta é antes do hardware.

| Item | Sem implementação | Com implementação (limite superior) | Com implementação e desconto |
|---|---|---|---|
| Frota | 3 robôs | 3 robôs | 3 robôs |
| Piso mensal (também a franquia recalibrada) | R$ 3.000/mês | R$ 6.500/mês | R$ 5.500/mês |
| Múltiplo mínimo das tarifas do deck | 1,32 x | 2,87 x | 2,42 x |
| Tarifa mínima por pedido de checkout | R$ 2,25/pedido | R$ 4,87/pedido | não calculada |
| Tarifa mínima por linha de pedido-a-pedido | R$ 0,33/linha | R$ 0,72/linha | não calculada |
| Tarifa teto por pedido de checkout (economia mínima da Social) | R$ 5,96/pedido | R$ 5,96/pedido | R$ 5,96/pedido |
| Tarifa teto por linha | R$ 0,88/linha | R$ 0,88/linha | R$ 0,88/linha |
| Tarifa recomendada por pedido de checkout | R$ 4,10/pedido | R$ 5,42/pedido | não calculada |
| Tarifa recomendada por linha | R$ 0,60/linha | R$ 0,80/linha | não calculada |
| Preço mensal recomendado | R$ 5.477/mês | R$ 7.227/mês | R$ 6.727/mês |
| Folga da janela de preço | R$ 4.954/mês | R$ 1.454/mês | R$ 2.454/mês |
| Economia da Social no preço recomendado | R$ 4.779/mês | R$ 3.029/mês | R$ 3.529/mês |
| Margem da Acta no preço recomendado (antes do hardware) | R$ 2.477/mês | R$ 727/mês | R$ 1.227/mês |
| Hardware máximo pagável por robô | R$ 19.816/robô (hardware, implantação, mapeamento e integração somados) | R$ 5.816/robô (só hardware, depois de recuperar a implementação) | não calculado |

A viabilidade para a Acta depende de o custo de hardware (PR20, [●]) ficar abaixo do máximo pagável do cenário.

**Não cotar** se a Social confirmar só o rateio de PR11 (a parte da Royal Canin no checkout do armazém): o teto da tarifa fica em R$ 1,39/pedido e R$ 0,20/linha, abaixo do mínimo (0,82 x das tarifas do deck contra 1,32 x necessário). A folga é -R$ 1.151/mês sem implementação e -R$ 4.651/mês com ela; no piso, a margem da Acta é zero por construção (sem janela) e a economia da Social é -R$ 375/mês sem implementação; com implementação e desconto a folga continua negativa (-R$ 3.651/mês). Com um posto inteiro desmobilizado, o teto é 1,74 x das tarifas do deck: há janela sem implementação (mínimo de 1,32 x), mas não com ela (mínimo de 2,87 x).

**Limiar de PR11 (postos que precisam sair para a ALT4 passar, com margem da Acta zero):**

| Frota | Sem implementação | Com implementação (limite superior) | Com implementação e desconto |
|---|---|---|---|
| Sem reserva | 0,58 postos | 1,14 postos | 0,89 postos |
| Com reserva (recomendada) | 0,76 postos | 1,64 postos | 1,39 postos |

Uma vaga inteira liberada (CR8, leitura colaborativa) pede 0,95 postos. O rateio por pedidos atribui à Royal Canin 0,47 postos.

**Implementação.** Preço de tabela da Acta, limite superior: R$ 60.000 sem reserva e R$ 84.000 com reserva; descontada a implantação do robô que já opera, R$ 36.000 e R$ 60.000. Fora da conta: mapeamento (área [●]), desenvolvimento do checkout conferido ([●]) e integração nova do checkout com o Senior. O custo real da Acta é [●]. O deck promete "tudo incluído"; o custo de servir informado cobre só a manutenção. Duas formas de cobrar, equivalentes para a Social: tudo incluído, amortizado nas tarifas, ou taxa de implantação e mapeamento à parte. Máximo pagável por robô para hardware, implantação, mapeamento e integração somados: R$ 19.816/robô; só para hardware, depois de recuperar a implementação: R$ 5.816/robô (compare com o custo de hardware, [●]).

## O que retirar do deck

| Item do deck | O que os dados mostram | Base |
|---|---|---|
| Franquia do slide 18 | A receita por transação da Royal Canin é R$ 2.268/mês, a maior franquia que o volume cobre. Para cobrir a franquia do deck, o checkout teria de chegar a 3.236 pedidos/mês. | INS-001, INS-002 |
| Economia do slide 15 e a base de volume | O volume implícito não aparece no WMS. Hipótese a confirmar com o autor do deck: taxa diária de uma semana de retomada vezes os dias do mês. | INS-080 |
| FTE e vagas do slide 14 | A separação do escopo libera no máximo 0,30 FTE (limite superior), menos de uma vaga. O método do deck é desconhecido. | INS-083, INS-011 |
| Frota maior do slide 14 | A frota necessária é menor. Prometer a do deck deixaria de R$ 2.000/mês a R$ 3.000/mês de custo de servir com a Acta (estimativa de modelo). Margem por robô sem piso com a frota do deck: -R$ 546/robô/mês. | INS-055, INS-085 |
| Dobro de produtividade, e o teste curto do slide 19 como prova | A razão depende do teto de intervalo e do denominador. O WMS não decide o dobro. O teste do dobro não decide a Royal Canin. | INS-006 |
| "Pico sem temporário" na Royal Canin | O excedente do dia de pico é 1,20 pessoas-hora/dia, fração de jornada. O robô poupa 0,05 pessoas-hora/dia na leitura colaborativa. O IC de bootstrap por dias do excedente está na nota de INS-015, abaixo. | INS-015, INS-056, INS-059 |
| Garantia de percentual de economia sobre um custo que inclui a conferência | A conferência não está no WMS e é decisão de processo da Social. A Acta não controla PR11. | INS-089, INS-012 |
| Margem com piso, ou hardware máximo com piso, como prova de viabilidade | Vem de uma franquia que o volume não cobre. Não usar como referência de custo de hardware. | INS-086 |
| Margem da ALT6 nas tarifas do deck como a "melhor" | Nessas tarifas a economia da Social na ALT6 fica em 10,9%, abaixo da garantia mínima. | INS-088 |

**Nota sobre INS-015 (excedente do dia de pico, com o IC de bootstrap por dias, chave excedente_h_p90_escopo_poscolmeia_ic_dias de ANA-003):** O excedente de horas ativas do escopo da ALT3 no dia p90 sobre o dia típico depende do regime. Na base pós-colmeia (dias plenos desde a entrada da colmeia, sem o incidente de 21 a 25/09) é de 1,20 horas por dia (faixa de cenários de 1,20 a 2,34), ou 0,16 FTE (faixa de cenários de 0,16 a 0,32): uma fração de jornada, não uma vaga inteira. A banda do p90 pós-colmeia tem só o mínimo de dias (5 dias plenos na banda PAR05 do volume diário), então o IC de bootstrap de dias, largo, deve acompanhar o número: 1,20 horas por dia (IC bootstrap 0,56 a 2,15), ou 0,16 FTE (IC bootstrap 0,08 a 0,29); a conclusão (fração de jornada) vale nas duas incertezas (a faixa de cenários citada é dos tetos e de S1 a S3, não é intervalo de confiança). Na variante do plano, que inclui o regime pré-colmeia, é de 2,32 horas por dia (faixa de cenários de 2,32 a 5,15), ou 0,32 FTE (faixa de cenários de 0,32 a 0,70), porque a banda do p90 do período inteiro tem 8 dias plenos, dos quais 8 dias plenos anteriores à colmeia, quando o pedido-a-pedido era bem maior. Na janela normal de 24/08 a 18/09 a leitura é só descritiva (0,82 horas por dia (faixa de cenários de 0,60 a 0,87), poucos dias na banda do p90). Na retomada (segundas e dias pós-pausa) o excedente pós-colmeia é 1,27 horas por dia (faixa de cenários de 1,27 a 2,68). A regra de teto inteiro de M23 transformaria qualquer fração em um operador adicional, mas esse número não sustenta o argumento 'pico sem temporário': o reforço é uma fração de jornada. No armazém inteiro, sem quebra de regime, o excedente do dia p90 é 5,12 horas por dia (faixa de cenários de 4,77 a 9,16) (0,70 FTE (faixa de cenários de 0,65 a 1,25)). O dia máximo fica só como limite superior. A base pós-colmeia é decisão do orquestrador a confirmar por Marcus no G3.

## O que manter e o que mudar

**Manter a estrutura, não o nível.** Tarifa por transação (checkout e pedido-a-pedido), com a proporção do deck entre as duas. O nível sobe para o da tabela de cotação acima. Manter o checkout conferido como peça central (é onde está o valor), condicional à resposta da Social e a um prazo de desenvolvimento ainda sem estimativa. Manter a integração com o WMS como argumento qualitativo.

| Componente | No deck | Na oferta recalibrada | Base |
|---|---|---|---|
| Sequência | Checkout e pedido-a-pedido da Royal Canin, de uma vez | Portão (pergunta de PR11), depois ALT4 no escopo da ALT3, depois armazém (ALT6) como fase seguinte | INS-058, INS-032 |
| Frota | Frota maior, que acompanha o pico sem custo fixo | Frota necessária mais reserva, revisão trimestral e pool de pico com preço próprio | INS-054, INS-055 |
| Franquia | Fração do volume atual | Piso igual ao custo de servir da frota total, da tabela de cotação | INS-054, INS-058 |
| Tarifas | Tarifas do deck | Dentro da janela do cenário confirmado; sem janela, não cotar. Limitar pelo custo da alternativa sem robô ([●]) | INS-054, INS-089 |
| Garantia | Percentual de economia sobre o custo atual | Garantia de capacidade, medida no primeiro trimestre. Economia em reais só sobre a conferência efetivamente desmobilizada e medida | INS-089, INS-012 |
| Mensagem | Corte de quadro e vagas liberadas | Pico e contratação evitada no armazém, em pessoas e pessoas-hora; conferência desmobilizada | INS-048, INS-011 |
| Implantação | Tudo incluído | Taxa à parte ou amortização explícita nas tarifas | IMP-IMPL |
| Armazém | Não há | Fase seguinte, só depois do portão, do checkout e do teste de adesão dos depositantes compatíveis (CR5) | INS-058, INS-088 |

## Cláusulas a prever

- **Go-live do checkout.** Instalação de frota e cobrança só a partir do go-live do checkout conferido. Se a frota for instalada antes, a Acta paga o piso (R$ 3.000/mês) sem a receita principal.
- **Erro de conferência.** Auditoria amostral, critério de aceite e limite de responsabilidade da Acta perante a Royal Canin, definidos em contrato.
- **Reserva.** Robô de reserva e nível de suporte. Uma parada devolve a conferência à bancada e desfaz PR11; por isso a reserva está no piso.
- **Garantia de capacidade.** Nível: linhas por hora no pico com a frota contratada, medidas no WMS pelo mesmo método, mais pessoas-hora por mil linhas. Condicionada à Social pôr o separador na zona nos horários combinados (o Kappabot é colaborativo). Não medir no primeiro mês de operação. Nível medido no primeiro trimestre da ALT4, sem o primeiro mês, ou no piloto, se houver; o valor numérico é [●].
- **Economia garantida.** Só sobre a conferência efetivamente desmobilizada e medida depois da estabilização.
- **Realocação dos postos.** A cargo da Social, com os custos de transição (rescisão ou realocação, queda de produtividade no go-live, estações fixas) e o acordo coletivo ([●]).
- **Queda de volume.** Cláusula para queda de volume de um depositante; o piso é no custo de servir, justo para os dois lados.
- **Revisão trimestral** de frota e piso, com robôs extras no pico a preço próprio.

## Argumentos de venda sustentados pelos dados

| Rótulo | Argumento | Força | Base (insight e modelo) | Como dizer, e a condição |
|---|---|---|---|---|
| V1 | A conferência desmobilizada é onde a Social economiza | Condicional | INS-089, INS-012. Economia da Social no preço recomendado, se todos os postos saem: R$ 4.779/mês sem implementação | Afirmar só depois de a Social confirmar, por medida, os postos acima do limiar. Garantia só sobre o medido. Confiança de INS-089: baixa |
| V2 | No pico, o armazém põe mais gente e mais horas em atividade | Média (fato medido) | INS-048. Pessoas a mais: 2,83 pessoas. Excedente: 5,12 pessoas-hora/dia. Alívio estimado pelo modelo colaborativo, no máximo: 1,20 pessoas-hora/dia | Dizer o que foi medido, em pessoas e pessoas-hora. O dado não mostra como a Social cobre o pico nem prova contratação. Não dizer que o robô evita temporário. Confiança: media |
| V3 | Frota dimensionada pelo pico medido, sem os robôs a mais do deck | Média a baixa | INS-054, INS-055, INS-087. Frota recomendada: 3 robôs, com reserva. Margem sem piso: R$ 134/robô/mês sem reserva, -R$ 244/robô/mês com reserva | O preço cobre o piso fixo da frota e a reserva; a economia vem de não pagar robôs que o pico não pede. Ressalva do red team: com reserva, ou com custo de servir pouco acima do informado, a margem sem piso é negativa e as tarifas precisam subir. Confiança: baixa |
| V4 | Garantia de capacidade no pico, no lugar de percentual de economia | Média | INS-054, INS-089 | Depende do robô, que a Acta controla, e do separador presente. Medir no primeiro trimestre. Nível numérico: [●] |
| V5 | A Acta chega com a conta refeita no WMS da própria Social | Alta para o fato | INS-080, INS-083, INS-001 | Um comprador com o WMS refaz a conta. Corrigir o deck antes de apresentar é condição. Confiança de INS-001: alta |
| V6 | Frota compartilhada entre depositantes, paga por transação | Baixa; só como fase seguinte | INS-088, INS-058, INS-032. Piso da ALT6: R$ 5.000/mês | Depende do checkout (a maior parte da receita da ALT6 vem dele), da adesão (CR5 inconclusivo) e de dados de alta temporada que não temos. Com implementação, sem reserva, a folga de preço da ALT6 é -R$ 2.197/mês. Confiança: baixa |

### Apoio qualitativo: hipóteses sem número, a validar

Vêm do parecer do especialista D3, de confiança baixa a média, e não de insight desta lista. Usar como hipótese, nunca como promessa.

- **Puxão sobre outras áreas no pico (U1).** Hipótese de que a separação puxa gente de outras áreas e de que o robô reduz parte disso. O dado mostra mais gente em atividade no pico, mas não diz de onde vem. Validar com a Social.
- **Ergonomia e retenção (U3).** Menos transporte de carga pelo separador. Falta peso por item e carga útil do Kappabot.
- **Integração e rastreabilidade (U4).** Os pedidos do robô já aparecem no WMS numa conta própria. Cuidado: a integração atual cobre importação de ondas e devolutiva automática; o checkout conferido é integração nova com o Senior.
- **Tempo entre pedidos (U5).** O trecho entre pedidos (ida ao packing, etiqueta) é o que o robô ataca. É hipótese do teste; o dado não prova que o robô o reduza.
- **Crescer contratando menos (U6).** Só qualitativo.
- **Treino mais curto (U7).** Dizer "casos dos EUA". Nunca falar em proficiência.
- **Auditoria amostral em vez de conferência total (U8).** Só com o checkout pronto e o aceite da Royal Canin.
- **Ganhos de processo sem robô, ditos pela própria Acta.** Mandar pedidos de um endereço para lote ou checkout.

### Defesa contra a conferência sem robô

A Social pode conferir na coleta, com bipe e auditoria amostral, sem robô. Se isso for viável no Senior ([●]), o maior valor da oferta não é exclusivo, e o preço fica limitado ao custo dessa alternativa. Nos depositantes de pedido leve, o lote manual com carrinho também concorre sem investimento. A oferta precisa juntar o que um coletor não faz: levar o pedido ao packing, a integração que já roda e a frota para o pico.

## Argumentos a NÃO usar

| Rótulo | Não usar | Por quê | Base |
|---|---|---|---|
| N1 | "Dobra a produtividade" | O WMS não decide o dobro; PR05 vem de amostra pequena e de método desconhecido | INS-006 |
| N2 | FTE do slide 14 e "libera vagas" na Royal Canin | Não se reproduz e fica abaixo de uma vaga | INS-083, INS-011 |
| N3 | Economia garantida de percentual sobre um custo que tem PR11 | PR11 não é medido e depende de desenvolvimento. Sem a conferência, a cobrança máxima compatível com a economia mínima é -R$ 45,89/mês, abaixo do custo de servir | INS-089, INS-012 |
| N4 | Economia do slide 15 e franquia de fração do volume | O volume implícito não aparece no WMS | INS-080, INS-001 |
| N5 | Frota maior do slide 14 para a Royal Canin | A sobra vira custo da Acta | INS-055, INS-085 |
| N6 | "Pico sem temporário" na Royal Canin | O excedente é fração de jornada e o robô alivia pouco na leitura colaborativa | INS-015, INS-056, INS-059 |
| N7 | "O robô coleta mais rápido que o operador" | O tempo produtivo é parecido, e com espera o robô leva mais | parecer D3 |
| N8 | Curva do novato, temporário guiado pelo robô, rotatividade por login | Inconclusivo por desenho; login não é pessoa | parecer D3 |
| N9 | O incidente operacional de setembro como argumento de venda | Causa não explicada; não usar | parecer D3 |
| N10 | Comparar o ritmo da Royal Canin com o de outros depositantes | Associativo e heterogêneo; não usar como crítica à operação | parecer D3 |
| N11 | Ganhos de produtividade dos EUA como promessa | Servem só como ordem de grandeza | parecer D3 |
| N12 | Horário estendido sem custo | Exige escala nova, hora extra ou adicional noturno | parecer D3 |
| N13 | A margem da ALT6 como prova de viabilidade | Usa tarifas com as quais a economia da Social na ALT6 não atinge a garantia mínima | INS-088 |
| N14 | "Integração pronta" para o checkout conferido | Só a importação de ondas e a devolutiva automática rodam; o checkout é integração nova | parecer D3 |

## Perguntas a levar

| Rótulo | Pergunta | Para quem | Resposta proposta | Por que importa |
|---|---|---|---|---|
| Q1 | Quanto do tempo de cada posto é conferência e quantos postos deixam de existir por causa do checkout da Royal Canin? Medir no relatório de conferência do Senior. | Social, via Marcus Lima | Até a resposta, usar o rateio (0,47 postos), abaixo do limiar. A regra aponta ALT1 | A ALT4 passa a partir de 0,76 postos (sem implementação) ou 1,64 postos (com). A vaga inteira pede 0,95 postos |
| Q2 | A Royal Canin aceita conferência na coleta, com auditoria amostral? A Social conferiria na coleta, com coletor e sem robô? | Social, via Marcus Lima | [●]. Tratar como risco competitivo: o preço fica limitado ao custo dessa alternativa | Define o valor exclusivo da oferta (INS-012) |
| Q3 | Quanto a Social paga por hora extra e por temporário, e como cobre o pico hoje? | Social, via Marcus Lima | Sem resposta, o pico segue em pessoas-hora, sem reais | Transforma V2 em reais (INS-048, INS-059) |
| Q4 | O custo por operador (PR10) inclui encargos e benefícios? | Social, via Marcus Lima | Sim, como custo total | Com PR11 rateado e sem reserva, a janela abre acima de R$ 64.888/ano |
| Q5 | Qual o volume diário normal depois de setembro? | Marcus Lima, em conversa reservada com a Social | Nova extração; sem juízo sobre a causa do incidente | Refaz franquia e frota com o volume normal (INS-080) |
| Q6 | Quais depositantes são compatíveis, quantas horas de separação consomem, quais aderiam e qual a área a mapear? | Social, via Marcus Lima | Nova extração por depositante e tipo de onda. Até lá, o armazém inteiro é o teto | CR5 inconclusivo (INS-032, INS-088); a área entra no custo de mapeamento |
| Q7 | Quais custos de transição a Social teria (realocação ou rescisão, queda de produtividade, estações fixas) e há acordo coletivo sobre automação? | Social, via Marcus Lima | [●]. A transição é custo da Social; garantir economia só sobre a conferência medida | Realocação dos postos e CR1 |
| Q8 | Qual volume mensal alimentou a franquia e a economia do deck? | Autor do deck (Marcus Lima) | Taxa diária da semana de retomada vezes os dias do mês | INS-080 |
| Q9 | Qual o prazo, o esforço e o custo do checkout conferido e da integração nova com o Senior? A reserva é obrigatória? Qual a capacidade do robô no checkout? | Vinicius Bastos | A reserva é obrigatória. Sem prazo, a ALT4 não entra. Não desenvolver antes de Q1 | INS-054, INS-032 |
| Q10 | O custo de servir (PR13) inclui suporte em campo e reserva? Qual o custo real de implantação, integração, mapeamento e hardware (HBR), e o que o "tudo incluído" cobre? | Renato Correa | Manter PR13 como provável e a tabela como limite superior | A janela inverte abaixo de R$ 925/robô/mês (PR11 rateado, sem reserva) e a margem sem piso fica negativa acima de R$ 1.134/robô/mês (tarifas do deck, sem reserva) |
| Q11 | A Acta aceita propor piloto pago ou encerrar o piloto gratuito, e quem paga a implantação dos robôs extras do piloto? | Marcus Lima | Aceite no G3. Piloto pago só no pedido-a-pedido agrupado, com crédito no contrato | Ver o desenho abaixo |

## Piloto pago (se o portão não passar) e encerrar o piloto gratuito

As duas opções estão fora da lista original de alternativas; Marcus decide no G3.

- **Escopo.** Pedido-a-pedido de dois ou mais endereços da Royal Canin e de um ou dois depositantes compatíveis, com frota agrupada e pedidos sorteados entre robô e manual. Sem checkout. Se houver protótipo, medir o tempo da conferência.
- **Preço.** Valor fixo igual ao custo de servir da frota correta do escopo agrupado: R$ 4.000/mês, para 4 robôs de referência (a frota exata é [●]), por 3 meses (duração proposta pelo red team, a confirmar por Marcus). Não por linha. Crédito no contrato se a fase seguinte for contratada.
- **Implantação dos robôs extras.** A preço de tabela: R$ 72.000. Quem paga é decisão de Marcus ([●]). Se recuperada dentro do piloto, amortizada em 3 meses, o preço sobe a R$ 28.000/mês; se a Acta a absorve, o custo total para ela é R$ 84.000.
- **Por que só se vende como investimento em informação.** A economia de separação da Social no pedido-a-pedido da Royal Canin é R$ 256/mês, 0,26 x o custo de servir de um robô. No armazém, só pedido-a-pedido, a folga é -R$ 3.697/mês no teto conservador e R$ 378/mês no mais folgado; a tarifa mínima seria 1,86 x a do deck. Candidata a teste, não a oferta.
- **Meta de sucesso do piloto, fixada antes (mesma regra do relatório).** Meta de ritmo do robô no piloto, em linhas por hora, fixada antes e lida em cada teto de intervalo, com o ritmo manual medido no mesmo teto e a frota do próprio piloto (pedido-a-pedido do armazém, sem checkout e sem PR11). Teto conservador: 141 linhas/h; folga contra o teto de manuseio do deck (limite físico do robô): -63,1 linhas/h, negativa: a meta é inatingível e não pode ser critério de sucesso. Teto base: 83,7 linhas/h; folga -5,71 linhas/h, inconclusiva (a faixa cruza o limite físico). Teto mais folgado: 62,3 linhas/h; folga 15,7 linhas/h, atingível. Só a leitura do teto mais folgado pode valer como critério de sucesso, e vencê-la não prova viabilidade nos outros tetos: o relatório do piloto mostra as três leituras. O armazém inteiro é o teto do escopo, então a meta real é igual ou maior. Medição pelo mesmo método do WMS, com sorteio de pedidos, espera do robô e pessoas-hora por mil linhas no pico. Marcus e o planejador confirmam no G3.
- **Quem decide e quem paga.** O aceite dos depositantes, clientes da Social, depende da Social via Marcus. Preço e contrato: Matheus Correa. Frota e medição: Vinicius Bastos. Custo real e implantação: Renato Correa.
- **O que o piloto não decide.** A Royal Canin isolada: PR05 não a inverte (INS-006).
- **Encerrar o piloto gratuito.** Custo de manter: R$ 1.000/mês, vezes os meses de espera pelas respostas de PR11 e do prazo do checkout. O valor que se perde (parceria e operação de referência) é [●]. Gatilhos: a Social confirma conferência abaixo do limiar com reserva e implementação; a Royal Canin não aceita conferência na coleta; sem prazo do checkout dentro do que Marcus aceita esperar; o piloto pago não é aceito ou não atinge a meta. Voltar depois com uma oferta de pico, quando houver dados de alta temporada.

## Sequência e donos

- **Marcus Lima.** Q1, Q2, Q5 e Q8 primeiro, em conversa reservada. Decide no G3 as leituras que mudam número (janela normal ou do plano; regime pós-colmeia ou período inteiro; CR8 colaborativa ou autônoma; regra de preço) e aceita ou não piloto pago e encerrar. Prazo: até [●], antes da reunião com a Social.
- **Vinicius Bastos.** Q9. Desenho técnico do piloto, com o planejador.
- **Renato Correa.** Q10. Margem, implantação, hardware e cláusulas.
- **Matheus Correa.** Monta a cotação da ALT4 (dois cenários) e a do piloto pago a partir das tabelas acima. Só envia depois de Q1.

## Limites deste documento

- Todos os insights citados são descritivos, com a confiança junto de cada um. Nada aqui afirma causa.
- O WMS não registra a conferência. O robô entra só por agregados, sem o banco 9fleet.
- Os valores de implementação são preço de tabela, limite superior; o custo real é [●].
- O incidente operacional de setembro e o regime da colmeia são desvios declarados; Marcus os confirma no G3.
- Os dados não cobrem alta temporada. Os valores em reais são do volume corrente.
- Os argumentos U1, U3 a U8 e N7 a N14 vêm do parecer do especialista, não de insight desta lista, e não levam número.
