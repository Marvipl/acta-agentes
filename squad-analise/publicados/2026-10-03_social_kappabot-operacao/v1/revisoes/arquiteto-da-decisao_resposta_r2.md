# Resposta do arquiteto da decisão ao sup-negocio, rodada 2

O veredito da rodada 2 foi aprovado com ressalvas. As ressalvas foram tratadas junto com a incorporação das respostas de Marcus ao G1, em 2026-10-03.

1. **Alta: sem PR13, a regra levava sempre a ALT1.** Resolvido.
   - Marcus informou PR13 (custo de servir sem hardware).
   - CR6 virou margem de contribuição por robô de pelo menos zero, avaliável sem o custo de hardware.
   - O motor reporta o custo máximo de hardware que se paga no prazo PR14. O hardware é PR20, [●].
   - A condição "CR6 não avaliável" saiu da regra de ALT1.

2. **Média: falta rastro da verificação do orquestrador.** Resolvido. A05 cita `revisoes/orquestrador_verificacao_regioes.md` nas evidências e na premissa.

3. **Média: Onda ou Id Onda.** Tratado.
   - A coluna que define a onda é fixada pelo engenheiro de dados no contrato e validada contra os totais por tipo de onda do slide 8.
   - Está registrado em A05 e em `restricoes`, e foi confirmado na resposta a Q05.

4. **Média: ALT5 não avaliável (sem tarifa nem capacidade para colmeia).** Aceito.
   - ALT5 virou "colmeia como teste da fase seguinte, sem preço nem frota nesta versão".
   - A regra de ALT5 foi ajustada. CR7 declara que PR05 serve só de referência de ordem de grandeza.

5. **Média: a regra de ALT2 não exigia CR1.** Aceito.
   - ALT2 agora exige CR1 como meta declarada, porque fica sem garantia ligada à conferência.
   - ALT2 também passou a ser o caminho enquanto o checkout conferido não estiver pronto, conforme Q07(c).

6. **Baixa: CR3 desalinhado da regra de ALT4.** Aceito.
   - Falha em CR3 leva a ALT4, sem a promessa de dobro.
   - Se CR3 não puder ser medido, leva a ALT1. A regra de ALT4 cita CR3.

7. **Baixa: Q03 com aceite único.** Sem efeito agora: Marcus já respondeu "aceito". As premissas de baixa confiança seguem marcadas no bloco `premissas`. PR10 e PR11 passaram a ter confiança alta, com fonte na Social.

8. **Baixa: ocupação em CR5 indefinida.** Aceito. Ocupação = demanda média na janela PR15 do dia típico de pelo menos uma capacidade de robô (PR07 ou PR08), com margem de contribuição não negativa (CR6).

Fica com a qualidade-privacidade, não com este nó: a coluna Qtde Endereços está mascarada no perfil.
