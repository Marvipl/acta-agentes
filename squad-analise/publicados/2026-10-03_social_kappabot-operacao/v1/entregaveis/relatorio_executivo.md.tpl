# Relatório executivo — {{meta.tema}}

Objetivo: {{meta.objetivo}} · data-base {{meta.data_base}} · versão v{{meta.versao}}

**Aprovado por Marcus no G3 (03/10/2026):** {{fmt.n_aprovados}} de {{fmt.n_insights}} insights aprovados; auditoria de reprodutibilidade {{fmt.auditoria}}. Os insights abaixo foram aprovados no G3. Todos são descritivos; nenhum afirma causa.

## Resposta

Não apresentar o deck como está. A ALT1 (manter o piloto atual) vale só como portão: perguntar à Social quantos postos de conferência (PR11) deixam de existir por causa da Royal Canin, medido no relatório de conferência do Senior. Com a frota recomendada (necessária mais um robô de reserva), a ALT4 (deck recalibrado) passa a partir de {{fmt.imp_IMP_INV_PR11_CR1_ALT4_ALT3_COM_RESERVA_provavel}} sem custo de implementação e de {{fmt.imp_IMP_INV_PR11_CR1_ALT4_ALT3_COM_RESERVA_COM_IMPL_provavel}} com ele. O rateio por pedidos dá {{fmt.imp_IMP_PR11_RATEIO_POSTOS_provavel}}. O especialista setorial espera, com confiança média, que o portão não passe.

Se passar, a ALT4 é cotável (tabela abaixo). Se não passar, o caminho é um piloto pago a custo de servir ou encerrar o piloto gratuito. Essas duas opções estão fora da lista original de alternativas do nó de decisão e pedem o aceite de Marcus no G3.

Para a meta da Social (menos custo de mão de obra e menos dificuldade de contratação), os dados dizem três coisas. A separação na Royal Canin libera menos de uma vaga ({{fmt.imp_IMP_CR8_FTE_ALT3_SEM_AUT_provavel}} no limite superior). O custo que a oferta ataca está na conferência, que o WMS não registra. O argumento de contratação evitada é do pico do armazém, em pessoas-hora, não da Royal Canin isolada.

## Como ler

- **Nível e confiança.** Todos os insights são descritivos. A confiança vem do motor, insight a insight.
- **Intervalos.** São faixas de cenários ou bootstrap de dias. Nenhuma premissa tem faixa com fonte.
- **Fatos e estimativas.** Fato medido vem do WMS. Estimativa de modelo depende de premissas (capacidade do robô, custo de servir, custo de implementação) e está marcada como tal.
- **Códigos.** Glossário no fim do documento.

## Configuração recomendada da ALT4 e janela de preço

Frota recomendada: {{fmt.imp_IMP_REC_FROTA_TOTAL_provavel}} (necessária dia a dia mais um robô de reserva). Piso igual ao custo de servir da frota total. Tarifas proporcionais às do deck. Volume tarifável corrente: {{fmt.imp_IMP_REC_VOL_CHECKOUT_MES_provavel}} de checkout e {{fmt.imp_IMP_REC_VOL_LINHAS_MES_provavel}} no pedido-a-pedido. Cada linha abaixo é um cenário só: o mínimo e o teto da tarifa não se misturam entre cenários.

| Cenário | Piso por mês | Mínimo (múltiplo das tarifas do deck) | Teto (múltiplo) | Folga | Preço recomendado | Economia da Social | Margem da Acta (antes do hardware) |
|---|---|---|---|---|---|---|---|
| Todos os postos saem, sem implementação | {{fmt.imp_IMP_REC_PISO_MES_SEM_IMPL_provavel}} | {{fmt.imp_IMP_REC_KMIN_SEM_IMPL_provavel}} | {{fmt.imp_IMP_REC_KMAX_INT_provavel}} | {{fmt.imp_IMP_REC_FOLGA_INT_SEM_IMPL_provavel}} | {{fmt.imp_IMP_REC_PRECO_MES_INT_SEM_IMPL_provavel}} | {{fmt.imp_IMP_REC_ECONOMIA_SOCIAL_MES_INT_SEM_IMPL_provavel}} | {{fmt.imp_IMP_REC_MARGEM_ACTA_MES_INT_SEM_IMPL_provavel}} |
| Todos os postos saem, com implementação (preço de tabela, limite superior) | {{fmt.imp_IMP_REC_PISO_MES_COM_IMPL_provavel}} | {{fmt.imp_IMP_REC_KMIN_COM_IMPL_provavel}} | {{fmt.imp_IMP_REC_KMAX_INT_provavel}} | {{fmt.imp_IMP_REC_FOLGA_INT_COM_IMPL_provavel}} | {{fmt.imp_IMP_REC_PRECO_MES_INT_COM_IMPL_provavel}} | {{fmt.imp_IMP_REC_ECONOMIA_SOCIAL_MES_INT_COM_IMPL_provavel}} | {{fmt.imp_IMP_REC_MARGEM_ACTA_MES_INT_COM_IMPL_provavel}} |
| Todos os postos saem, com implementação e desconto da implantação do robô que já opera | {{fmt.imp_IMP_REC_PISO_MES_COM_IMPL_DESCONTO_provavel}} | {{fmt.imp_IMP_REC_KMIN_COM_IMPL_DESCONTO_provavel}} | {{fmt.imp_IMP_REC_KMAX_INT_provavel}} | {{fmt.imp_IMP_REC_FOLGA_INT_COM_IMPL_DESCONTO_provavel}} | {{fmt.imp_IMP_REC_PRECO_MES_INT_COM_IMPL_DESCONTO_provavel}} | {{fmt.imp_IMP_REC_ECONOMIA_SOCIAL_MES_INT_COM_IMPL_DESCONTO_provavel}} | {{fmt.imp_IMP_REC_MARGEM_ACTA_MES_INT_COM_IMPL_DESCONTO_provavel}} |
| PR11 rateado, sem implementação | {{fmt.imp_IMP_REC_PISO_MES_SEM_IMPL_provavel}} | {{fmt.imp_IMP_REC_KMIN_SEM_IMPL_provavel}} | {{fmt.imp_IMP_REC_KMAX_RAT_provavel}} | {{fmt.imp_IMP_REC_FOLGA_RAT_SEM_IMPL_provavel}} | {{fmt.imp_IMP_REC_PRECO_MES_RAT_SEM_IMPL_provavel}} | {{fmt.imp_IMP_REC_ECONOMIA_SOCIAL_MES_RAT_SEM_IMPL_provavel}} | {{fmt.imp_IMP_REC_MARGEM_ACTA_MES_RAT_SEM_IMPL_provavel}} |
| PR11 rateado, com implementação | {{fmt.imp_IMP_REC_PISO_MES_COM_IMPL_provavel}} | {{fmt.imp_IMP_REC_KMIN_COM_IMPL_provavel}} | {{fmt.imp_IMP_REC_KMAX_RAT_provavel}} | {{fmt.imp_IMP_REC_FOLGA_RAT_COM_IMPL_provavel}} | {{fmt.imp_IMP_REC_PRECO_MES_RAT_COM_IMPL_provavel}} | {{fmt.imp_IMP_REC_ECONOMIA_SOCIAL_MES_RAT_COM_IMPL_provavel}} | {{fmt.imp_IMP_REC_MARGEM_ACTA_MES_RAT_COM_IMPL_provavel}} |

Com PR11 rateado o teto fica abaixo do mínimo: não há janela, o preço recomendado vira o piso (sem janela: margem zero por construção) e a Social não atinge a economia mínima; com implementação e desconto, a folga continua negativa ({{fmt.imp_IMP_REC_FOLGA_RAT_COM_IMPL_DESCONTO_provavel}}). A coluna de implementação sem desconto é o limite superior do custo; a margem da Acta é antes do hardware. Com um posto inteiro desmobilizado, o teto é {{fmt.imp_IMP_ALT4_KMAX_ALT3_UM_POSTO_provavel}} das tarifas do deck: há janela sem implementação, mas não com ela.

**Tarifas em reais, por cenário** (múltiplo aplicado às tarifas do deck de checkout e de linha):

| Tarifa | Por pedido de checkout | Por linha de pedido-a-pedido |
|---|---|---|
| Mínima, sem implementação | {{fmt.imp_IMP_REC_TARIFA_CHECKOUT_MIN_SEM_IMPL_provavel}} | {{fmt.imp_IMP_REC_TARIFA_LINHA_MIN_SEM_IMPL_provavel}} |
| Mínima, com implementação | {{fmt.imp_IMP_REC_TARIFA_CHECKOUT_MIN_COM_IMPL_provavel}} | {{fmt.imp_IMP_REC_TARIFA_LINHA_MIN_COM_IMPL_provavel}} |
| Teto, todos os postos saem | {{fmt.imp_IMP_REC_TARIFA_CHECKOUT_MAX_INT_provavel}} | {{fmt.imp_IMP_REC_TARIFA_LINHA_MAX_INT_provavel}} |
| Teto, PR11 rateado (sem janela) | {{fmt.imp_IMP_REC_TARIFA_CHECKOUT_MAX_RAT_provavel}} | {{fmt.imp_IMP_REC_TARIFA_LINHA_MAX_RAT_provavel}} |
| Recomendada, todos os postos, sem implementação | {{fmt.imp_IMP_REC_TARIFA_CHECKOUT_RECOMENDADA_INT_SEM_IMPL_provavel}} | {{fmt.imp_IMP_REC_TARIFA_LINHA_RECOMENDADA_INT_SEM_IMPL_provavel}} |
| Recomendada, todos os postos, com implementação | {{fmt.imp_IMP_REC_TARIFA_CHECKOUT_RECOMENDADA_INT_COM_IMPL_provavel}} | {{fmt.imp_IMP_REC_TARIFA_LINHA_RECOMENDADA_INT_COM_IMPL_provavel}} |

**Limiar de PR11 por configuração** (postos que precisam sair por causa da Royal Canin para a ALT4 passar a economia mínima da Social, com a margem da Acta em zero):

| Frota | Sem implementação | Com implementação (limite superior) | Com implementação e desconto do robô que já opera |
|---|---|---|---|
| Sem reserva | {{fmt.imp_IMP_INV_PR11_CR1_ALT4_ALT3_provavel}} | {{fmt.imp_IMP_INV_PR11_CR1_ALT4_ALT3_COM_IMPL_provavel}} | {{fmt.imp_IMP_INV_PR11_CR1_ALT4_ALT3_COM_IMPL_DESCONTO_provavel}} |
| Com reserva (recomendada) | {{fmt.imp_IMP_INV_PR11_CR1_ALT4_ALT3_COM_RESERVA_provavel}} | {{fmt.imp_IMP_INV_PR11_CR1_ALT4_ALT3_COM_RESERVA_COM_IMPL_provavel}} | {{fmt.imp_IMP_INV_PR11_CR1_ALT4_ALT3_COM_RESERVA_COM_IMPL_DESCONTO_provavel}} |

Uma vaga inteira liberada (CR8, leitura colaborativa) pede {{fmt.imp_IMP_INV_PR11_CR8_ALT3_COL_provavel}}. O rateio por pedidos atribui à Royal Canin {{fmt.imp_IMP_PR11_RATEIO_POSTOS_provavel}}.

**Custo de implementação (preço de tabela da Acta, limite superior).** Investimento da ALT4 sem reserva: {{fmt.imp_IMP_IMPL_INVESTIMENTO_ALT3_SEM_RESERVA_provavel}}; com reserva: {{fmt.imp_IMP_IMPL_INVESTIMENTO_ALT3_COM_RESERVA_provavel}}. Descontada a implantação do robô que já opera: {{fmt.imp_IMP_IMPL_INVESTIMENTO_ALT3_SEM_RESERVA_DESCONTO_provavel}} sem reserva e {{fmt.imp_IMP_IMPL_INVESTIMENTO_ALT3_COM_RESERVA_DESCONTO_provavel}} com reserva (a integração simples continua contada). Ficam fora da conta o mapeamento (área [●]), o desenvolvimento do checkout conferido ([●]) e a integração nova do checkout com o Senior. O custo real da Acta é [●]. O deck promete "tudo incluído"; o custo de servir informado cobre só a manutenção. Máximo pagável por robô para hardware, implantação, mapeamento e integração somados: {{fmt.imp_IMP_REC_HW_MAX_INT_SEM_IMPL_provavel}}, ou só para hardware depois de recuperar a implementação: {{fmt.imp_IMP_REC_HW_MAX_INT_COM_IMPL_provavel}} (compare com o custo de hardware, [●]).

**Custo de oportunidade do robô.** A receita mensal por robô na ALT4 é {{fmt.imp_IMP_CR6_ALT3_RECEITA_ROBO_SOBRE_LOCACAO_DECK_provavel}} da locação de tabela nas tarifas do deck e {{fmt.imp_IMP_CR6_ALT3_RECEITA_ROBO_SOBRE_LOCACAO_NO_TETO_provavel}} no teto de preço. É referência, não limite; Marcus decide.

## Se o portão não passar

- **Piloto pago.** Pedido-a-pedido de dois ou mais endereços da Royal Canin e de um ou dois depositantes compatíveis (armazém), com frota agrupada e pedidos sorteados entre robô e manual. Preço igual ao custo de servir da frota correta do escopo agrupado: {{fmt.imp_IMP_PILOTO_PRECO_MES_CUSTO_DE_SERVIR_provavel}}, para {{fmt.imp_IMP_PILOTO_FROTA_provavel}} de referência (a frota exata é [●]), por {{fmt.imp_IMP_PILOTO_DURACAO_MESES_provavel}} (duração proposta pelo red team, a confirmar por Marcus). Implantação dos robôs extras, a preço de tabela: {{fmt.imp_IMP_PILOTO_INVESTIMENTO_IMPLANTACAO_provavel}}; quem paga é decisão de Marcus no G3 ([●]). Se fosse recuperada dentro do piloto, amortizada em {{fmt.imp_IMP_PILOTO_DURACAO_MESES_provavel}}, o preço subiria a {{fmt.imp_IMP_PILOTO_PRECO_MES_COM_IMPLANTACAO_provavel}}. Custo total para a Acta se ela absorver a implantação: {{fmt.imp_IMP_PILOTO_CUSTO_TOTAL_ACTA_provavel}}. A Social fica no negativo durante o piloto (folga de {{fmt.imp_IMP_FOLGA_ARM_PAP_POOL_provavel}} no teto conservador, {{fmt.imp_IMP_FOLGA_ARM_PAP_POOL_ALTO_provavel}} no mais folgado): vende-se como investimento em informação, com crédito no contrato se a fase seguinte for contratada. O aceite dos depositantes, clientes da Social, depende da Social via Marcus.
- **Meta de sucesso do piloto, fixada antes (mesma regra da oferta).** Meta de ritmo do robô no piloto, em linhas por hora, fixada antes e lida em cada teto de intervalo, com o ritmo manual medido no mesmo teto e a frota do próprio piloto (pedido-a-pedido do armazém, sem checkout e sem PR11). Teto conservador: {{fmt.imp_IMP_PILOTO_META_PR05_T300_provavel}}; folga contra o teto de manuseio do deck (limite físico do robô): {{fmt.imp_IMP_PILOTO_META_FOLGA_FISICA_T300_provavel}}, negativa: a meta é inatingível e não pode ser critério de sucesso. Teto base: {{fmt.imp_IMP_PILOTO_META_PR05_T900_provavel}}; folga {{fmt.imp_IMP_PILOTO_META_FOLGA_FISICA_T900_provavel}}, inconclusiva (a faixa cruza o limite físico). Teto mais folgado: {{fmt.imp_IMP_PILOTO_META_PR05_T1800_provavel}}; folga {{fmt.imp_IMP_PILOTO_META_FOLGA_FISICA_T1800_provavel}}, atingível. Só a leitura do teto mais folgado pode valer como critério de sucesso, e vencê-la não prova viabilidade nos outros tetos: o relatório do piloto mostra as três leituras. O armazém inteiro é o teto do escopo, então a meta real é igual ou maior. Medição pelo mesmo método do WMS, com sorteio de pedidos, espera do robô e pessoas-hora por mil linhas no pico. Marcus e o planejador confirmam no G3.
- **Encerrar o piloto gratuito.** Custo de manter: {{fmt.imp_IMP_ALT1_CUSTO_MES_PILOTO_GRATUITO_provavel}}, vezes os meses de espera pelas respostas de PR11 e do prazo do checkout. O valor que se perde (parceria e operação de referência) é [●]. Gatilhos: a Social confirma conferência abaixo do limiar com reserva e implementação; a Royal Canin não aceita conferência na coleta; sem prazo do checkout dentro do que Marcus aceita esperar; o piloto pago não é aceito ou não atinge a meta. A relação segue depois, com uma oferta de pico, quando houver dados de alta temporada.

## Insights aprovados no G3

### Franquia, volume e o que o deck afirma

**INS-001 · franquia na ALT3.** Descritivo · confiança {{fmt.ins_INS_001_confianca}}.
{{fmt.ins_INS_001}}
Para a oferta: a franquia do deck sai da mesa. A maior franquia que o volume corrente cobre é a receita por transação, {{fmt.imp_IMP_CR2_RECEITA_ALT3_provavel}}, e a maior parte dela vem do checkout, que não está pronto.

**INS-002 · franquia na ALT2.** Descritivo · confiança {{fmt.ins_INS_002_confianca}}.
{{fmt.ins_INS_002}}
Para a oferta: sem o checkout, a ALT2 não fecha para a Acta. Margem por robô sem piso: {{fmt.imp_IMP_CR6_ALT2_SEM_PISO_provavel}}.

**INS-080 · volume implícito do deck.** Descritivo · confiança {{fmt.ins_INS_080_confianca}}.
Resumo: o volume que sustenta a economia do slide 15 e a franquia do slide 18 não aparece no WMS. A hipótese é que o deck multiplicou a taxa diária de uma semana de retomada pelos dias do mês, a confirmar com o autor do deck.
Para a oferta: para cobrir a franquia, o checkout teria de chegar a {{fmt.imp_IMP_CR2_VOLUME_CHECKOUT_ALT3_provavel}}. Um comprador com o WMS refaz essa conta; corrigir antes de apresentar é condição.

### Conferência, mão de obra e produtividade

**INS-012 · o WMS não registra a conferência.** Descritivo · confiança {{fmt.ins_INS_012_confianca}}.
{{fmt.ins_INS_012}}
Para a oferta: é o insight que decide. Os limiares estão na tabela acima. O relatório do módulo de conferência do Senior é a fonte para medir; a pergunta certa é quanto do tempo de cada posto é conferência, não quantos postos saem, porque a bancada também embala.

**INS-089 · custo atual de mão de obra no escopo.** Descritivo · confiança {{fmt.ins_INS_089_confianca}}.
Resumo: o custo atual é estimativa, não medida do WMS. A maior parte vem dos postos de conferência (PR11), e a parte de separação é limite inferior.
Para a oferta: o que se vende é a conferência desmobilizada. O custo mensal da conferência atribuível à Royal Canin pelo rateio é {{fmt.imp_IMP_PR11_ATRIBUIVEL_RC_provavel}}. Não garantir economia sobre PR11 enquanto não for medida.

**INS-083 · FTE do slide 14.** Descritivo · confiança {{fmt.ins_INS_083_confianca}}.
Resumo: os FTE do slide 14 não se reproduzem pelas horas ativas do WMS. Parte da diferença é de definição (presença paga contra tempo de coleta creditado), e o método do deck é desconhecido.
Para a oferta: sem a conferência, nenhuma cobrança cabe na economia mínima da Social. A cobrança máxima compatível é {{fmt.imp_IMP_PMAX_ALT3_SEM_provavel}} no teto conservador e {{fmt.imp_IMP_PMAX_ALT3_SEM_ALTO_provavel}} no mais folgado, abaixo do custo de servir da frota.

**INS-011 · FTE liberados.** Descritivo · confiança {{fmt.ins_INS_011_confianca}}.
{{fmt.ins_INS_011}}
Para a oferta: a separação libera no máximo {{fmt.imp_IMP_CR8_FTE_ALT3_SEM_AUT_provavel}} na leitura autônoma e {{fmt.imp_IMP_CR8_FTE_ALT3_SEM_COL_provavel}} na colaborativa; com a conferência integral, {{fmt.imp_IMP_CR8_FTE_ALT3_INT_COL_provavel}}. Trocar "vagas liberadas" por "absorver crescimento e pico sem contratar". FTE fracionário só vira economia se a Social realocar as pessoas.

**INS-006 · o dobro de produtividade.** Descritivo · confiança {{fmt.ins_INS_006_confianca}}.
Resumo: a razão entre o ritmo do deck e o manual medido depende do teto de intervalo e do denominador. O WMS não decide o dobro, nem a favor nem contra.
Para a oferta: o teste do dobro não decide a Royal Canin. Mesmo com PR05 no teto de manuseio do deck, a folga de preço da ALT2 é {{fmt.imp_IMP_FOLGA_ALT2_PR05_TETO_provavel}} (teto conservador) e {{fmt.imp_IMP_FOLGA_ALT2_PR05_TETO_ALTO_provavel}} (mais folgado). Decide só o armazém sem conferência, medido no piloto pago (meta do piloto na seção "Se o portão não passar").

### Frota, margem e preço

**INS-054 · frota necessária da Royal Canin.** Descritivo · confiança {{fmt.ins_INS_054_confianca}}.
Resumo: a frota necessária no dia de pico, calculada dia a dia, é pequena e fica abaixo da do deck em toda a grade. A leitura pelo perfil médio é otimista e não tem reserva. As premissas de capacidade do robô têm confiança baixa.
Para a oferta: frota recomendada de {{fmt.imp_IMP_REC_FROTA_TOTAL_provavel}} (um de reserva), com piso de {{fmt.imp_IMP_REC_PISO_MES_SEM_IMPL_provavel}} ({{fmt.imp_IMP_REC_PISO_MES_COM_IMPL_provavel}} com implementação). A reserva se decide antes do preço.

**INS-055 · sobra de frota contra o slide 14.** Descritivo · confiança {{fmt.ins_INS_055_confianca}}.
Resumo: contra a frota do deck, a frota necessária deixa sobra. É sobra condicionada às premissas, não ociosidade medida: a frota do deck pode embutir reserva e crescimento.
Para a oferta: prometer a frota do deck deixaria de {{fmt.imp_IMP_CR4_SOBRA_FROTA_DECK_INF_provavel}} a {{fmt.imp_IMP_CR4_SOBRA_FROTA_DECK_SUP_provavel}} de custo de servir com a Acta. Propor frota inicial menor, revisão trimestral e robôs extras no pico com preço próprio.

**INS-085 · margem sem piso, frota do deck.** Descritivo · confiança {{fmt.ins_INS_085_confianca}}.
Resumo: com a frota do deck, a receita por transação sozinha não paga o custo de servir do robô. A saída é frota menor ou preço maior, não a franquia do deck.
Para a oferta: margem por robô sem piso com a frota do deck: {{fmt.imp_IMP_CR6_ALT3_DECK5_SEM_PISO_provavel}}.

**INS-086 · margem com o piso da franquia.** Descritivo · confiança {{fmt.ins_INS_086_confianca}}.
Resumo: com a franquia do deck como piso a margem fica não negativa, mas vem de uma franquia que o volume não cobre e que seria custo extra da Social.
Para a oferta: margem com a frota do deck e piso: {{fmt.imp_IMP_CR6_ALT3_DECK5_COM_PISO_provavel}}. Não usar como prova de viabilidade nem como referência de hardware.

**INS-087 · margem sem piso, frota necessária.** Descritivo · confiança {{fmt.ins_INS_087_confianca}}.
Resumo: com a frota necessária, a margem sem piso é positiva e pequena, e o sinal depende da frota, da janela e da reserva.
Para a oferta: sem reserva, {{fmt.imp_IMP_CR6_ALT3_SEM_PISO_provavel}}. Com um robô de reserva, {{fmt.imp_IMP_CR6_ALT3_SEM_PISO_COM_RESERVA_provavel}}; com reserva e implementação, {{fmt.imp_IMP_CR6_ALT3_SEM_PISO_COM_RESERVA_COM_IMPL_provavel}}. Ressalva do red team: com reserva, ou com o custo de servir pouco acima do informado, a margem sem piso fica negativa; é preciso subir as tarifas.

### Pico e contratação

**INS-015 · excedente do dia de pico na Royal Canin.** Descritivo · confiança {{fmt.ins_INS_015_confianca}}.
Resumo: o excedente de horas do dia de pico sobre o dia típico, no escopo da Royal Canin, é fração de jornada, não vaga inteira. A conclusão vale nos intervalos de bootstrap de dias e de cenários.
Para a oferta: excedente de {{fmt.imp_IMP_CR8_P90_RC_EXCEDENTE_provavel}}, com o IC de bootstrap por dias no texto integral abaixo (chave excedente_h_p90_escopo_poscolmeia_ic_dias, de ANA-003). "Pico sem temporário" sai da oferta da Royal Canin.
Texto integral, com o IC de bootstrap por dias: {{fmt.ins_INS_015}}

**INS-056 · CR8 no dia de pico, duas leituras de M23.** Descritivo · confiança {{fmt.ins_INS_056_confianca}}.
Resumo: na leitura colaborativa, a que descreve o Kappabot, a frota absorve só uma fração do excedente e CR8 falha. Na autônoma, registrada no plano e limite superior, CR8 passa. Marcus decide a leitura no G3.
Para a oferta: fração absorvida de {{fmt.imp_IMP_CR8_P90_RC_PCT_COL_provavel}} na colaborativa e {{fmt.imp_IMP_CR8_P90_RC_PCT_AUT_provavel}} na autônoma.

**INS-059 · vantagem do robô no pico, pela mesma regra.** Descritivo · confiança {{fmt.ins_INS_059_confianca}}.
Resumo: medido pela mesma regra no manual e no robô, o robô quase não reduz o excedente do dia de pico da Royal Canin. Os custos de hora extra e de temporário da Social ainda faltam, então não há reais aqui.
Para a oferta: o robô poupa {{fmt.imp_IMP_CR8_P90_RC_POUPA_COL_provavel}} na leitura colaborativa.

**INS-048 · pico no armazém inteiro.** Descritivo · confiança {{fmt.ins_INS_048_confianca}}.
Resumo: nos dias de pico o armazém põe mais gente e mais horas em atividade. É censo descritivo: não diz como a Social cobre o pico (hora extra, temporário, remanejamento) e não prova contratação.
Para a oferta: {{fmt.imp_IMP_CR8_PICO_ARM_PESSOAS_provavel}} a mais em atividade e {{fmt.imp_IMP_CR8_PICO_ARM_EXCEDENTE_provavel}} de excedente. Na leitura colaborativa, a frota alivia no máximo {{fmt.imp_IMP_CR8_PICO_ARM_ALIVIO_COL_provavel}}. Dizer em pessoas e pessoas-hora, não em reais.

### Outros depositantes e frota agrupada (ALT6)

**INS-032 · receita adicional dos outros depositantes.** Descritivo · confiança {{fmt.ins_INS_032_confianca}}.
Resumo: os outros depositantes compatíveis trariam receita adicional por transação e margem positiva por robô adicional na frota agrupada dia a dia. A maior parte da receita da ALT6 vem do checkout, e a adesão é incerta.
Para a oferta: receita por transação da ALT6 de {{fmt.imp_IMP_CR2_RECEITA_ALT6_provavel}}, dos quais {{fmt.imp_IMP_ALT6_DEP_CHECKOUT_provavel}} vêm do checkout conferido.

**INS-058 · frota agrupada da ALT6.** Descritivo · confiança {{fmt.ins_INS_058_confianca}}.
Resumo: a frota agrupada, calculada dia a dia, é maior que a da Royal Canin sozinha, e a sobra do slide 14 deixa de existir se a oferta incluir os outros depositantes.
Para a oferta: piso da ALT6 de {{fmt.imp_IMP_ALT4_PMIN_ALT6_provavel}} sem reserva. Com PR11 integral, a folga de preço é {{fmt.imp_IMP_ALT4_FOLGA_ALT6_INT_provavel}} sem reserva e sem implementação; {{fmt.imp_IMP_ALT4_FOLGA_ALT6_INT_COM_RESERVA_provavel}} com reserva; {{fmt.imp_IMP_ALT4_FOLGA_ALT6_INT_COM_IMPL_provavel}} com implementação; {{fmt.imp_IMP_ALT4_FOLGA_ALT6_INT_COM_RESERVA_COM_IMPL_provavel}} com os dois. Sem PR11, {{fmt.imp_IMP_FOLGA_ALT6_SEM_provavel}}. A ALT6 não pode ser a primeira fase: depende do checkout, da adesão e de postos desmobilizados.

**INS-088 · margem do robô adicional na ALT6.** Descritivo · confiança {{fmt.ins_INS_088_confianca}}.
Resumo: nas tarifas do deck, o robô adicional que atende os outros depositantes tem margem positiva. Com essas tarifas, porém, a economia da Social na ALT6 fica abaixo da garantia mínima.
Para a oferta: economia da Social na ALT6 nas tarifas do deck: {{fmt.imp_IMP_CR1_ALT6_DECK_INT_provavel}}. No teto de preço compatível com a economia mínima, a margem por robô é {{fmt.imp_IMP_CR6_ALT6_NO_TETO_INT_provavel}} sem implementação e {{fmt.imp_IMP_CR6_ALT6_NO_TETO_INT_COM_IMPL_provavel}} com implementação (limite superior, com o armazém inteiro como teto). Nas tarifas do deck a margem seria {{fmt.imp_IMP_CR6_ALT6_TOTAL_provavel}}, mas esse preço a Social não aceitaria pelo próprio critério de compra.

## Ressalvas do red team da decisão

- **Premissa crítica.** PR11 lida como postos atribuíveis à Royal Canin e efetivamente desmobilizados. A atribuição e a desmobilização não têm fonte; os limiares acima são a forma de testá-la.
- **Instalar antes do go-live do checkout.** A cobrança do deck só começa no go-live. Se a frota for instalada antes, a Acta paga o piso ({{fmt.imp_IMP_REC_PISO_MES_SEM_IMPL_provavel}}) sem a receita principal. Não desenvolver nem instalar antes da resposta do portão.
- **Realocação dos postos.** FTE fracionário só vira economia se a Social realocar as pessoas. Custos de transição (rescisão ou realocação, queda de produtividade no go-live, estações fixas) são da Social e não estão nos modelos. Acordo coletivo e avaliação de segurança do Kappabot estão em aberto [●].
- **Reserva.** Uma parada do robô devolve a conferência à bancada, a Social mantém o posto e PR11 se desfaz. A reserva é parte da configuração, não opção.
- **Erro de conferência.** Vira responsabilidade da Acta perante a Royal Canin; o contrato precisa de auditoria amostral, critério de aceite e limite de responsabilidade.
- **Concorrência.** A Social pode conferir na coleta, com bipe e auditoria amostral, sem robô; o preço fica limitado ao custo dessa alternativa [●]. Nos depositantes de pedido leve, o lote manual com carrinho concorre sem investimento. No pico, um fornecedor de robôs por locação pode ofertar só na alta temporada.
- **Incoerências do deck.** Franquia acima do volume e FTE do slide 14 dariam a um comprador o argumento de que a Acta superestima. Corrigir antes de apresentar é condição.
- **Equipe.** A equipe da Acta não comporta, ao mesmo tempo, o checkout, a frota com reserva e a abertura de outros depositantes.

## O que estes dados não permitem concluir

- **Causa.** Não há afirmação causal. O ganho do robô sobre o manual não foi testado com sorteio de pedidos. O dobro de produtividade não se confirma nem se refuta.
- **Quantos postos de conferência saem.** O WMS não registra a conferência. Atribuição à Royal Canin e desmobilização são premissa da Social, não dado.
- **Economia garantida em reais.** Falta o custo de hora extra e de temporário e a medição da conferência.
- **Alta temporada e crescimento.** A série cobre de junho a setembro, sem Black Friday nem Natal. O dia de pico vale para o período, e os modelos de crescimento são pontos de equilíbrio, não previsões.
- **Custo real de implementação.** Os valores são preço de tabela, limite superior. Mapeamento, desenvolvimento do checkout e integração com o Senior estão fora da conta.
- **Payback do hardware.** O custo de hardware por robô não foi informado. Os modelos entregam só o máximo pagável.
- **Disponibilidade do robô.** Não há reserva medida, e a capacidade do robô no checkout é desconhecida.
- **Adesão dos outros depositantes.** CR5 está inconclusivo. O valor para eles pode ser menor, porque já rendem mais no manual.
- **Colmeia.** CR7 está inconclusivo: a colmeia segue como candidata a teste, sem tarifa nem capacidade de robô no deck.
- **Incidente de setembro e comparação de ritmo entre depositantes.** Não usar como argumento de venda nem como crítica; o dado é associativo e não separa produto, layout e processo.

## Qualidade e limites dos dados

- **Fonte única de campo.** A exportação de produtividade do WMS cobre separação. Não traz conferência, pré-conferência, deslocamento ao packing, etiqueta nem reabastecimento. A jornada ativa é limite inferior da presença e não é hora paga.
- **Robô só por agregados.** O banco 9fleet não foi usado, por decisão de Marcus. O lado do robô entra pelas premissas do relatório 9fleet v1, de amostra preliminar e baixa confiança. No WMS o robô aparece só como uma conta de integração. O banco 9fleet fica para a v2.
- **Linha tarifável e linha operacional** são definições distintas. Trocar uma pela outra muda o volume tarifável e a frota.
- **Tarefas abertas em lote, colmeia e checkout** foram marcadas, não apagadas. Colmeia e checkout sobrepõem linhas, então o tempo é por tarefa e operador.
- **Privacidade.** Usuário foi pseudonimizado. Nenhum resultado sai por operador.
- **Incidente operacional da Royal Canin, no fim de setembro.** Confirmado por Marcus como queda real, não falha de extração. É desvio declarado: a base da oferta é a janela normal; a janela do plano, com o incidente, é cenário de estresse.
- **Regime da colmeia.** Pico, frota e excedente usam a base pós-colmeia (decisão do orquestrador, a confirmar por Marcus). A variante do plano, com o regime pré-colmeia, segue reportada com esse rótulo.
- **Premissas.** Todas têm fonte, mas nenhuma tem faixa com fonte. A incerteza entra por cenários nomeados: PR11 integral, rateado e fora; reserva sem e com; implementação sem e com; teto de intervalo conservador e superior; leitura autônoma e colaborativa de M23; frota dia a dia e frota do deck. O extremo desfavorável das premissas de custo é lido pelos pontos de inversão de PR13 e PR10.
- **Reserva e preço recomendado** são regras declaradas pelo analista de impacto, a confirmar com Vinicius Bastos (reserva) e Marcus (regra de preço: ponto médio da janela).
- **Auditoria.** Reprodutibilidade: {{fmt.auditoria}}.

### Critérios com leituras alternativas no G3

Cada linha é uma escolha de Marcus. A leitura registrada no plano e o desvio declarado aparecem lado a lado nas análises.

- **CR2, franquia.** Janela normal (base da oferta) ou janela do plano, com o incidente. Falha nas duas, nas alternativas ALT2 e ALT3.
- **CR3, linha de base manual.** Os tetos de intervalo e a variante que trunca pausas. O resultado muda de falha para inconclusivo ou passa. O WMS não decide o dobro.
- **CR4, frota.** Dia a dia pós-colmeia (base, leitura desfavorável) ou perfil médio da banda (otimista, sem reserva). O número de robôs muda entre as duas.
- **CR5, outros depositantes.** Inconclusivo após a robustez por mês. Passa se "compatível" for lido como todo o pedido-a-pedido.
- **CR8, reforço no dia de pico.** Leitura colaborativa (Kappabot, falha) ou autônoma (registrada no plano, passa).
- **Regra de preço recomendado e reserva.** Ponto médio da janela e um robô de reserva: regras do analista, que Marcus pode trocar.
- **Pistas exploratórias por depositante.** O plano não fixava o critério de inversão; o adotado foi fixado depois de ver os sinais. Ficam fora deste relatório até Marcus decidir.

## Próximos passos

- **Marcus Lima, com a Social.** Levar a pergunta de PR11 com os limiares da tabela. Pedir o relatório de conferência do Senior e perguntar quanto do tempo de cada posto é conferência. Pedir à Social que pergunte à Royal Canin se aceita conferência na coleta, com bipe e auditoria amostral (a Royal Canin só é contatada pela Social). Pedir os custos de hora extra e de temporário e como o pico é coberto hoje. Prazo: até [●], antes da reunião.
- **Marcus Lima, no deck.** Confirmar com o autor do deck o volume que alimentou a franquia e a economia. Refazer franquia, economia e frota com o volume do WMS. Aceitar, ou não, as duas opções fora da lista original (piloto pago e encerrar o piloto gratuito).
- **Vinicius Bastos.** Prazo, esforço e custo do checkout conferido e da integração nova com o Senior; reserva; capacidade do robô no checkout. Não começar o desenvolvimento antes da resposta de PR11.
- **Renato Correa.** Custo real de implantação, integração e mapeamento (e o que o "tudo incluído" cobre), custo de hardware (HBR), custo de servir e custo por operador.
- **Matheus Correa.** Cotar a ALT4 e o piloto pago a partir de `oferta_enriquecida`.
- **Dados a coletar.** Área a mapear. Volume diário da Royal Canin depois do incidente. Horas de separação dos depositantes compatíveis. Dados de alta temporada. Banco 9fleet para a v2.
- **Experimento que prova causa.** Piloto pago com operador dedicado, pedidos sorteados entre robô e manual, o mesmo método do WMS nos tetos de intervalo, tempo fora do relógio e espera do robô, e meta de ritmo por teto de intervalo fixada antes por planejador e Marcus (três leituras, critério no teto mais folgado).

## Glossário

- **ALT1:** manter o piloto atual e perguntar antes (aqui, só como portão). **ALT2:** pedido-a-pedido sem checkout. **ALT3:** oferta do deck. **ALT4:** oferta do deck recalibrada. **ALT6:** oferta ampliada a outros depositantes.
- **CR1:** economia mínima da Social. **CR2:** a receita por transação cobre a franquia. **CR3:** linha de base manual. **CR4:** frota do tamanho do pico. **CR5:** oportunidade além da Royal Canin. **CR6:** margem da Acta por robô. **CR7:** espaço na colmeia. **CR8:** menor dependência de contratação.
- **PR01:** garantia mínima de economia do deck. **PR05:** linhas por hora por operador com robô. **PR10:** custo por operador. **PR11:** postos de conferência. **PR13:** custo de servir por robô, sem hardware. **M23:** leitura de CR8 (autônoma ou colaborativa).
- **Teto conservador e teto mais folgado:** limites do intervalo entre tarefas usado para medir o ritmo manual.
- **Portão:** a pergunta a fazer antes de qualquer desenvolvimento.

Aprovado no G3 · auditoria de reprodutibilidade: {{fmt.auditoria}}.
