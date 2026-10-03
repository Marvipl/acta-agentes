# Resposta do arquiteto da decisão ao sup-negocio, rodada 1

Nó revisado: `nos/decisao.json`. Todos os pontos foram aceitos e corrigidos no nó. Não digitei contas novas: os valores do deck viraram premissas nomeadas (PR01 a PR19) com fonte, e o recálculo fica com o motor.

## Pontos

1. **Alta: base de volume do slide 15 e da franquia do slide 18.** Aceito.
   - O que mudou:
     - A restrição está registrada no item 1 de `restricoes`.
     - A economia do slide 15 virou PR19, "referência a reconciliar", com confiança baixa.
     - `impacto_esperado` passou a [●] até o motor recalcular.
     - A07 caiu para `parcial`.
     - Nova pergunta P5, ligada a CR2.
     - Pergunta a Marcus sobre a base usada: Q06(a). Resposta proposta: recalcular com o volume do WMS.

2. **Alta: o enquadramento só validava o deck.** Aceito.
   - O que mudou:
     - Nova alternativa ALT5, com a colmeia no escopo (deck, slide 8 contra slide 14).
     - Novo critério CR7 compara a produtividade da colmeia com PR05.
     - Nova pergunta P17.
     - Bloco `trilha_exploratoria` com P9, P10, P11, P13, P14 e P15. Delas, P10 (tempo fora do relógio por recorte) e P13 (curva de aprendizado por coorte, agregada) são novas.
     - Regra declarada: exploratório só sobe a insight aprovado com confirmação. Nada sai por operador individual.

3. **Alta: viabilidade para a Acta e frota.** Aceito.
   - O que mudou:
     - Novo critério CR6: receita mensal por robô de pelo menos PR13 (custo de servir, [●], a informar por Marcus). A referência de RaaS da Base de Conhecimento (seção 1.3) entra só como sensibilidade de baixa confiança.
     - CR4 ficou de mão dupla e é medido hora a hora no dia p90, na janela PR15, contra capacidade horária. Falta de frota leva a ALT4. Sobra só se justifica com CR6. As duas leituras de frota do deck (slides 12 e 14) estão em PR09.
     - Q07(a) agora pede o custo mensal por robô.

4. **Alta: Q04 errada (Onda é numérica).** Aceito.
   - O que mudou:
     - A nova Q05 confirma a regra verificada pelo orquestrador:
       - depositante = prefixo de Região Origem;
       - colmeia = Região Destino COLMEIA;
       - pedido-a-pedido = onda com um pedido;
       - checkout = onda com vários pedidos e uma coleta cada (relatório 9fleet v1, p. 4).
     - A regra já está como `premissa_adotada` de A05.
     - A restrição antiga ("aparentemente não tem coluna de depositante") foi substituída.

5. **Média: CR3 circular.** Aceito.
   - O que mudou:
     - CR3 agora testa só o que o WMS mede: a linha de base manual em ciclo completo, que precisa ficar em no máximo PR06.
     - PR05 está declarado como premissa de amostra pequena.
     - Com CR3 passando, o dobro só pode ser afirmado depois do teste controlado. Com CR3 falhando, a regra leva a ALT1 ou ALT4.

6. **Média: CR4 com hora de pico contra limites diários e sem capacidade no checkout.** Aceito.
   - O que mudou:
     - A métrica é hora a hora contra capacidade horária, com a janela de operação PR15 medida no WMS.
     - A capacidade no checkout virou PR08 ([●]), perguntada em Q07(b).

7. **Média: CR2 em "todos os meses" com o mix em mudança.** Aceito.
   - O que mudou:
     - A referência agora é a taxa corrente por dia útil das últimas semanas.
     - O mês completo mais recente serve de conferência, e meses parciais são normalizados.
     - A tendência do mix entra como sensibilidade no prazo do contrato (PR14).

8. **Média: falta uma regra que leve a cada alternativa.** Aceito.
   - O que mudou: novo bloco `regra_decisao`, com uma condição por alternativa (ALT1 a ALT6).
   - Concordo que ALT2, como estava, era inviável pelo slide 18. Ela foi redefinida como a oferta para quando a conferência não puder ser desmobilizada.

9. **Média: Q05 misturava cláusula comercial com definição técnica.** Aceito.
   - O que mudou:
     - A definição comercial de linha foi para Q06(b): Marcus decide, e CR2 é mostrado nas duas contagens.
     - O método de horas e FTE (jornada ativa com teto de intervalo, e não a soma de Tempo em Segundos) foi para Q05.

10. **Média: pedidos do robô no WMS.** Aceito.
    - O que mudou: nova pergunta P8 (CR3) e parte de Q04. Resposta proposta: a engenharia confirma; se os pedidos aparecerem, a comparação é descritiva. O tema também está em `restricoes`.

11. **Média: CR5 sem fonte.** Aceito.
    - O que mudou: o limite agora é ocupar ao menos um robô adicional (PR07 ou PR08, na janela PR15) e a receita desse volume cobrir o custo de servir (CR6). A comparação com a Royal Canin saiu.

12. **Baixa: Black Friday e Natal.** Aceito.
    - O que mudou: está registrado em `restricoes` que a série cobre de junho a setembro e que P11 não responde pela alta temporada.

13. **Baixa: Q03 com opções redundantes; Q07 ocupando vaga.** Aceito.
    - O que mudou:
      - As opções de Q04 (antiga Q03) foram reduzidas a duas.
      - A privacidade (antiga Q07) virou `premissa_adotada` de A06, com aceite pedido em Q03.
      - A vaga liberada foi usada em Q02 (o que a Social quer).

14. **Baixa: parâmetros digitados nos limites.** Aceito.
    - O que mudou: novo bloco `premissas` (PR01 a PR19), com valor, unidade, fonte e confiança. Os limites referenciam esses nomes, o que facilita montar o `impacto.json`.

15. **Média: Qtde Endereços mascarada.** Não cabe a este nó. Fica para a qualidade-privacidade, como o orquestrador indicou.

## Lacunas apontadas

- **O que a Social quer (principal):** entrou na nova Q02, com o status do deck, as objeções da Social e da Royal Canin, o decisor e o validador na Social, e com resposta proposta.
- **Custo de servir:** CR6, PR13 e Q07(a).
- **Colmeia:** ALT5, CR7 e P17.
- **Desmobilização da conferência e prontidão do checkout conferido:** Q02, Q07(c), `regra_decisao` (ALT2 e ALT3) e `restricoes`.
- **Pedidos do robô no WMS:** P8 e Q04.
- **Granularidade da planilha:** registrada em `restricoes` para o contrato do engenheiro de dados.
- **Alta temporada:** registrada em `restricoes`.

## Efeito na prontidão

A07 caiu de `premissa` para `parcial`, porque o impacto está em [●]. A nota cai um pouco e continua abaixo do mínimo até Marcus responder Q01 a Q07. Seguem 7 perguntas-chave abertas na rodada 1.
