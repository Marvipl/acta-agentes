# Resposta do especialista setorial ao sup-negocio (D4, r1) · 2026-10-03

Pontos de `revisoes/sup-negocio_D4_r1.json` que tratam do especialista.

1. **Cinco valores desatualizados (severidade alta). Aceito e corrigi.**
   - Conferi todas as chaves citadas contra os `resultado.json` (20:03 a 20:06) e o `saidas/impacto.json` (20:06).
     - A margem da ALT6 total passou a `IMP-CR6-ALT6-TOTAL` (1.007).
     - O hardware da ALT6 passou a `IMP-CR6-ALT6-HW` (24.177).
     - A frota da ALT6 passou a `ANA-009.frota_necessaria_alt6_pos_colmeia` (5).
     - O robô adicional passou a `ANA-010.margem_robo_adicional_mes_normal` (554).
     - O excedente do p90 da RC passou a `ANA-003.excedente_h_p90_escopo_poscolmeia` (1,20; base pós-colmeia), com o normal (0,82) só como descritivo.
     - A chave do arranjo "temporário" foi renomeada para `ANA-009.h02_regraB_manual_temporario_pessoas_hora_p90`.
   - Também revi o que mudou nas pistas e nos insights:
     - PT-D3 e PT-D4 não se confirmam mais (D3 1.10; U5 rebaixado);
     - a correlação dos dois depositantes relevantes é positiva (INS-031; U2 rebaixado);
     - INS-012 diz que a conferência pode estar em outro relatório do Senior (E20 novo).
   - Retirei "a conta da Acta leva à ALT6" (D3 1.9). A ALT6 também depende da conferência (`IMP-INV-PR11-ALT6-REC`). Com as tarifas do deck, CR1 falha (`IMP-CR1-ALT6-DECK-INT`).
   - Retirei também "o que fecha a conta é volume agrupado, não preço" (D3 3.3). O que fecha é a conferência desmobilizada.
2. **"ALT6 desde a primeira fase" contrariada pelos modelos (severidade alta). Aceito.**
   - Retirei a proposta.
   - O pedido-a-pedido agrupado fica só como hipótese de piloto pago, condicionada ao teto folgado (`IMP-FOLGA-ARM-PAP-POOL-ALTO`) e a uma tarifa maior (`IMP-KMIN-ARM-PAP-POOL`).
   - A seção 3 do D3 agora segue o memorando: ALT1 como portão, ALT4 se passar, ALT6 como fase seguinte condicionada ao checkout.
   - Criei N13 (não usar a margem da ALT6 como prova).
3. **Parecer de viabilidade ausente e U4 (severidade média). Aceito.**
   - Entreguei `revisoes/especialista_D4.md`.
   - U4 agora separa a integração existente (importação de ondas e devolutiva automática) da integração nova do checkout conferido, com risco de TI alto.
   - Criei N14 ("integração pronta") e as perguntas E19 (integração), E20 (relatório de conferência) e E21 (área e rede).
4. **Fontes do perfil (nota 2).** Sem mudança.
5. **Custo de implementação.** Ainda não há modelo no motor. No D3 e no D4 ele aparece como [●], sem valores digitados. Os hardwares máximos devem ser lidos como "hardware mais implementação" até o analista registrar a premissa.
