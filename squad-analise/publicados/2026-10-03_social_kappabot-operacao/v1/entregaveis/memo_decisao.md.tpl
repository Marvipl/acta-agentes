# Memorando de decisão — {{meta.tema}}

**Aprovado por Marcus no G3 (03/10/2026):** {{fmt.n_aprovados}} de {{fmt.n_insights}} aprovados; auditoria {{fmt.auditoria}}.

**Decisão:** que oferta levar à Social, para reduzir custo de mão de obra e dependência de contratação, com viabilidade para a Acta.

**Recomendação:** não apresentar o deck como está. A ALT1 (manter o piloto atual) serve só de portão: perguntar à Social quantos postos de conferência (PR11) deixam de existir por causa da Royal Canin, medido no relatório de conferência do Senior. Com reserva, a ALT4 passa a partir de {{fmt.imp_IMP_INV_PR11_CR1_ALT4_ALT3_COM_RESERVA_provavel}} (sem implementação), {{fmt.imp_IMP_INV_PR11_CR1_ALT4_ALT3_COM_RESERVA_COM_IMPL_provavel}} (com, limite superior) ou {{fmt.imp_IMP_INV_PR11_CR1_ALT4_ALT3_COM_RESERVA_COM_IMPL_DESCONTO_provavel}} (com desconto do robô que já opera). Rateio por pedidos: {{fmt.imp_IMP_PR11_RATEIO_POSTOS_provavel}}. O especialista espera que não passe.
- **Se passar:** ALT4 (deck recalibrado): {{fmt.imp_IMP_REC_FROTA_TOTAL_provavel}} com reserva, piso de {{fmt.imp_IMP_REC_PISO_MES_SEM_IMPL_provavel}} ({{fmt.imp_IMP_REC_PISO_MES_COM_IMPL_provavel}} com implementação, limite superior) e, se todos os postos saem, tarifa de {{fmt.imp_IMP_REC_TARIFA_CHECKOUT_RECOMENDADA_INT_SEM_IMPL_provavel}} e {{fmt.imp_IMP_REC_TARIFA_LINHA_RECOMENDADA_INT_SEM_IMPL_provavel}}. Garantia de capacidade e da conferência medida.
- **Se não passar:** piloto pago no pedido-a-pedido do armazém a custo de servir ({{fmt.imp_IMP_PILOTO_PRECO_MES_CUSTO_DE_SERVIR_provavel}}, {{fmt.imp_IMP_PILOTO_FROTA_provavel}}, {{fmt.imp_IMP_PILOTO_DURACAO_MESES_provavel}}), implantação de {{fmt.imp_IMP_PILOTO_INVESTIMENTO_IMPLANTACAO_provavel}} (custo total da Acta: {{fmt.imp_IMP_PILOTO_CUSTO_TOTAL_ACTA_provavel}}; quem paga, no G3); ou encerrar o piloto gratuito ({{fmt.imp_IMP_ALT1_CUSTO_MES_PILOTO_GRATUITO_provavel}}). Fora da lista original: aceite de Marcus no G3.

**Evidência (fatos descritivos, medidos no WMS):**
- A receita por transação da Royal Canin cobre {{fmt.imp_IMP_CR2_ALT3_NORMAL_provavel}} da franquia do deck; o volume do deck não aparece no WMS (INS-001, INS-080).
- O WMS não registra a conferência; a separação do escopo equivale a, no máximo, {{fmt.imp_IMP_CR8_FTE_ALT3_SEM_AUT_provavel}} (INS-012, INS-011).
- No pico, o excedente da Royal Canin é fração de jornada, mesmo no IC de bootstrap por dias; o armazém põe {{fmt.imp_IMP_CR8_PICO_ARM_PESSOAS_provavel}} a mais em atividade (INS-015, INS-048).

**Impacto (modelo; margem antes do hardware):** se todos os postos saem, a Social economiza {{fmt.imp_IMP_REC_ECONOMIA_SOCIAL_MES_INT_SEM_IMPL_provavel}} e a Acta tem margem de {{fmt.imp_IMP_REC_MARGEM_ACTA_MES_INT_SEM_IMPL_provavel}}; com implementação, {{fmt.imp_IMP_REC_ECONOMIA_SOCIAL_MES_INT_COM_IMPL_provavel}} e {{fmt.imp_IMP_REC_MARGEM_ACTA_MES_INT_COM_IMPL_provavel}} (limite superior) ou {{fmt.imp_IMP_REC_ECONOMIA_SOCIAL_MES_INT_COM_IMPL_DESCONTO_provavel}} e {{fmt.imp_IMP_REC_MARGEM_ACTA_MES_INT_COM_IMPL_DESCONTO_provavel}} (com desconto). A Acta só é viável se o hardware (PR20, [●]) custar até {{fmt.imp_IMP_REC_HW_MAX_INT_SEM_IMPL_provavel}} (sem implementação) ou {{fmt.imp_IMP_REC_HW_MAX_INT_COM_IMPL_provavel}} (com).

**Confiança:** {{fmt.ins_INS_001_confianca}} (INS-001), {{fmt.ins_INS_012_confianca}} (INS-012), {{fmt.ins_INS_054_confianca}} (INS-054), {{fmt.ins_INS_089_confianca}} (INS-089).

**Os dados não permitem concluir:** quantos postos saem, o ganho do robô, a alta temporada, o custo de implementação.

**Premissas:** PR11 sai com o checkout; o checkout ganha prazo; há reserva. Marcus confirma no G3: janela, regime, CR8.

**Riscos (red team):** integração nova do checkout com o Senior; instalar antes do go-live (a Acta paga o piso sem receita); realocação dos postos (transição, acordo coletivo, segurança [●]); erro de conferência na conta da Acta.

**Próximo passo, até [●]:** Marcus Lima, PR11 via Social (Royal Canin, pela Social); Vinicius Bastos, checkout; Renato Correa, implementação e hardware (HBR); Matheus Correa, cotação.
