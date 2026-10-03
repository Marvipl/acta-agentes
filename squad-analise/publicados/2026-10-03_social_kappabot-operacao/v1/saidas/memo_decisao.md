# Memorando de decisão — Social

**Rascunho pré-G3:** 20 de 71 aprovados; auditoria aprovada.

**Decisão:** que oferta levar à Social, para reduzir custo de mão de obra e dependência de contratação, com viabilidade para a Acta.

**Recomendação:** não apresentar o deck como está. A ALT1 (manter o piloto atual) serve só de portão: perguntar à Social quantos postos de conferência (PR11) deixam de existir por causa da Royal Canin, medido no relatório de conferência do Senior. Com reserva, a ALT4 passa a partir de 0,76 postos (sem implementação), 1,64 postos (com, limite superior) ou 1,39 postos (com desconto do robô que já opera). Rateio por pedidos: 0,47 postos. O especialista espera que não passe.
- **Se passar:** ALT4 (deck recalibrado): 3 robôs com reserva, piso de R$ 3.000/mês (R$ 6.500/mês com implementação, limite superior) e, se todos os postos saem, tarifa de R$ 4,10/pedido e R$ 0,60/linha. Garantia de capacidade e da conferência medida.
- **Se não passar:** piloto pago no pedido-a-pedido do armazém a custo de servir (R$ 4.000/mês, 4 robôs, 3 meses), implantação de R$ 72.000 (custo total da Acta: R$ 84.000; quem paga, no G3); ou encerrar o piloto gratuito (R$ 1.000/mês). Fora da lista original: aceite de Marcus no G3.

**Evidência (fatos descritivos, medidos no WMS):**
- A receita por transação da Royal Canin cobre 38,4% da franquia do deck; o volume do deck não aparece no WMS (INS-001, INS-080).
- O WMS não registra a conferência; a separação do escopo equivale a, no máximo, 0,30 FTE (INS-012, INS-011).
- No pico, o excedente da Royal Canin é fração de jornada, mesmo no IC de bootstrap por dias; o armazém põe 2,83 pessoas a mais em atividade (INS-015, INS-048).

**Impacto (modelo; margem antes do hardware):** se todos os postos saem, a Social economiza R$ 4.779/mês e a Acta tem margem de R$ 2.477/mês; com implementação, R$ 3.029/mês e R$ 727/mês (limite superior) ou R$ 3.529/mês e R$ 1.227/mês (com desconto). A Acta só é viável se o hardware (PR20, [●]) custar até R$ 19.816/robô (sem implementação) ou R$ 5.816/robô (com).

**Confiança:** alta (INS-001), media (INS-012), baixa (INS-054), baixa (INS-089).

**Os dados não permitem concluir:** quantos postos saem, o ganho do robô, a alta temporada, o custo de implementação.

**Premissas:** PR11 sai com o checkout; o checkout ganha prazo; há reserva. Marcus confirma no G3: janela, regime, CR8.

**Riscos (red team):** integração nova do checkout com o Senior; instalar antes do go-live (a Acta paga o piso sem receita); realocação dos postos (transição, acordo coletivo, segurança [●]); erro de conferência na conta da Acta.

**Próximo passo, até [●]:** Marcus Lima, PR11 via Social (Royal Canin, pela Social); Vinicius Bastos, checkout; Renato Correa, implementação e hardware (HBR); Matheus Correa, cotação.
