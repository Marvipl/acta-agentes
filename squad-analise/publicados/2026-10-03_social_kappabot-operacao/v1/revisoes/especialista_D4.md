# Parecer do especialista setorial · D4 · viabilidade operacional da recomendação

- Projeto: `projetos/2026-10-03_social_kappabot-operacao/v1` · 2026-10-03 · agente `dados-especialista-setorial`.
- Perfil: gerente de operações e engenharia de armazém de 3PL no Brasil. A lente 2 (comercial) tem confiança baixa.
- Entradas lidas: `saidas/memo_decisao.md`, `saidas/impacto.json` (20:06), `revisoes/sup-negocio_D4_r1.json` e o parecer D3 (r1).
- O custo de implementação (implantação, mapeamento, integração e checkout) **ainda não está no motor**: o `impacto.json` de 20:06 não tem esses modelos. Trato o tema como [●] e não digito valores.

## Conclusão

1. **O portão (ALT1) é viável e barato, se a resposta for medida e não declarada.**
   - Na leitura do setor (média), a resposta mais provável é uma fração de posto, porque a bancada também embala. Isso leva ao ramo "não passa".
   - O limiar atual (`IMP-INV-PR11-CR1-ALT4-ALT3`, 0,58 posto) não tem reserva nem implementação. Vale como **piso** do limiar até o motor recalcular.
2. **Ramo "passa" (ALT4).** O risco operacional maior é a **integração do checkout conferido, que ainda não existe**. Em seguida vêm a contingência da bancada, a disponibilidade de uma frota pequena e uma garantia de capacidade que depende de gente da Social.
3. **Ramo "não passa".** Encerrar o piloto gratuito é simples para a operação. O piloto pago no pedido-a-pedido agrupado só se sustenta como aprendizado pago, com critério fixado antes. Ele não se paga para a Social (`IMP-PILOTO-ECONOMIA-SOBRE-CUSTO-ROBO`, 0,26) nem para a Acta nas tarifas do deck (`IMP-MARGEM-ARM-PAP-POOL`).

## 1. Portão: o que pode dar errado

| Risco | Por que acontece | Mitigação | Validar |
|---|---|---|---|
| A Social responde "dois postos" sem medir | A pergunta é hipotética, e a bancada também embala (D3 1.5). O checkout conferido tira o bipe, não a embalagem. | Medir o tempo de conferência por posto e por depositante no relatório de conferência ou de packing do Senior (E20), mais um dia de cronometragem na bancada. Perguntar "quanto do posto é bipe da RC", e não "quantos postos saem". | `validar com pessoa do setor` (operação da Social) |
| A RC não aceita conferência na coleta | Pode haver SLA de acurácia, kits ou brindes ([●]). Sem o aceite, a bancada continua. | A pergunta vai à RC via Social, antes de qualquer desenvolvimento. Proposta de auditoria amostral (GEODIS: de 100% para 10%; média). | `validar com pessoa do setor` (Social e RC) |
| O limiar sobe com reserva e implementação | Os modelos ainda não incluem a reserva no limiar nem a implementação (sup-negocio). | Decidir só com o limiar recalculado no motor. Até lá, 0,58 posto é o mínimo. | analista e Marcus |
| A expectativa do setor (média) já aponta "não passa" | A parte da RC no checkout do armazém é pequena (`IMP-PR11-RATEIO-FRACAO`, 0,24). Um posto inteiro sair só por causa da RC é improvável. | Preparar desde já a mensagem do ramo "não passa". | `validar com pessoa do setor` |

## 2. Ramo "passa": ALT4 com frota mais reserva, piso no custo de servir e garantia de capacidade

1. **Integração do checkout conferido (decisivo).**
   - Hoje roda só a importação de ondas e a devolutiva automática. A conta do robô capta só as devolutivas automáticas (INS-009).
   - O checkout conferido exige integração nova com o Senior: confirmação de conferência por item, fechamento de volume e etiqueta, e a liberação de faturamento em trânsito do slide 10 (sup-negocio).
   - Quem altera o Senior (a Senior, um integrador ou a TI da Social), com qual prazo e qual custo: [●] (E19).
   - O risco de TI é alto. Envolve um terceiro, homologação com a nota fiscal da RC e modos de falha novos.
   - **Não desenvolver antes do portão.**
   - `validar com pessoa do setor` (engenharia da Acta e TI da Social).
2. **Contingência.**
   - Se o robô, a rede ou a integração param, a conferência volta para a bancada. A Social vai manter capacidade de bancada, então o posto não some por inteiro.
   - A garantia de economia deve valer só para a parte da conferência que a Social de fato deixa de pagar, medida depois da estabilização.
3. **Disponibilidade.**
   - A frota necessária é `ANA-009.frota_necessaria_alt3_pos_colmeia` (2; de 1 a 2). Uma parada derruba metade ou toda a capacidade.
   - A reserva é obrigatória, com custo no piso (`IMP-KMIN-ALT4-ALT3-COM-RESERVA`).
   - O SLA de suporte precisa caber numa equipe da Acta pequena (memorando).
4. **Erro de conferência.**
   - Em ração há muitas variações de sabor e tamanho ([●]). Um erro vira devolução para a RC.
   - Definir no contrato a auditoria amostral, o critério de aceite e o limite de responsabilidade da Acta.
5. **Garantia de capacidade depende de gente.**
   - O Kappabot é colaborativo: `ANA-009.separadores_pico_p90_com_robo` = 1.
   - A garantia precisa ser condicionada à Social pôr o separador na zona nos horários combinados. A medição é no WMS, pelo mesmo método (M14).
   - Sem isso, a Acta garante o que não controla.
   - `validar com pessoa do setor`.
6. **Layout e segurança.**
   - A área da RC (porta-palete, circulação de empilhadeira) e a cobertura da rede sem fio são [●] (E16, E21).
   - A ISO 3691-4 trata da preparação da zona de operação. A avaliação do Kappabot por essa norma é [●] (pergunta 21 do perfil).
   - `validar com pessoa do setor` (Social e engenharia da Acta).
7. **Go-live e treino.**
   - A queda de produtividade inicial é [●].
   - Manter o fluxo manual em paralelo nas primeiras semanas. Não medir a garantia no primeiro mês.
8. **Transição da Social.**
   - Desmobilizar posto por desligamento tem custo legal: aviso prévio proporcional e multa de 40% do FGTS (Lei 12.506/2011; Lei 8.036/1990, art. 18; alta).
   - O caminho mais barato é realocar a pessoa ou não repor quem sair.
   - Acordo coletivo sobre automação: [●].
9. **Implementação.**
   - O "tudo incluído" do slide 18 põe implantação, mapeamento e integração no custo da Acta. Num escopo de dois ou três robôs, esse custo fixo pesa muito por transação (média).
   - Cobrar setup à parte ou amortizar de forma explícita. Valores: [●] até o analista registrar.
10. **Volume.** A RC pode zerar o volume por uma semana (incidente). O piso no custo de servir é justo para os dois lados. Incluir cláusula de queda de volume de um depositante.

## 3. Ramo "não passa"

### 3.1 Piloto pago no pedido-a-pedido agrupado
- **Economia.**
  - A folga é negativa no teto conservador (`IMP-FOLGA-ARM-PAP-POOL`) e só fica positiva no teto mais folgado (`IMP-FOLGA-ARM-PAP-POOL-ALTO`).
  - A tarifa teria de subir para `IMP-KMIN-ARM-PAP-POOL` (1,87 vezes PR04).
  - A Social paga para aprender, não para economizar.
- **Operação.**
  - Exige mapear e implantar nas áreas de outros depositantes. Quem paga é [●].
  - Os pedidos desses depositantes são pequenos e leves. O concorrente é o lote manual (D3 1.7), e o piloto pode mostrar pouco ganho e virar uma referência negativa.
  - O preço precisa ser o da frota agrupada, não o da frota da RC (sup-negocio).
- **Depositantes.**
  - Leitura do setor sem fonte ([●]): mudar o equipamento de separação costuma ser decisão interna do 3PL. Contratos com SLA de acurácia ou de dados podem exigir aviso ou aceite.
  - `validar com pessoa do setor` (Social: contratos com os depositantes relevantes).
- **Condições mínimas.** Critério de sucesso fixado antes, pedidos sorteados, duração fechada e crédito no contrato se a fase seguinte vier.

### 3.2 Encerrar o piloto gratuito
- **Para a Social, a operação é simples.** O robô atende uma parte pequena do pedido-a-pedido da RC (piso de 12,3%, INS-009), e o manual absorve.
- **Riscos para a Acta.**
  - Perde o local de referência ([●]).
  - Reabrir depois exige remapear.
  - Continuar de graça custa PR13 por robô por mês, o que ainda não está modelado.
- **Como encerrar.** Com mensagem clara e um gatilho para reabrir: checkout pronto, PR11 confirmado por medição ou volume novo.

## 4. Perguntas (detalhe em D3, seção 4)
- E15 e E20: medir PR11.
- E19: integração do checkout.
- E21: área e rede.
- E16: layout da RC.
- E11: hora extra e temporários.

## Autoverificação
- [x] **Dentro do perfil.** O que não tem fonte está em [●]: custos de implementação, SLA da RC, segurança do Kappabot, acordo coletivo e contratos com depositantes.
- [x] **Decisivos com `validar com pessoa do setor`:**
  - medição de PR11;
  - aceite da RC;
  - integração do checkout;
  - condição de pessoal da garantia;
  - layout e segurança;
  - contratos com depositantes.
- [x] **Nenhum número novo.** Só chaves e modelos do motor e referências legais com fonte do perfil.
