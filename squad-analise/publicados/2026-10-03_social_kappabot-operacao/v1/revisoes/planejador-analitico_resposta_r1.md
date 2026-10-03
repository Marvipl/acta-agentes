# Resposta do planejador analítico à revisão do sup-metodologia (D2, r1)

- Projeto: `projetos/2026-10-03_social_kappabot-operacao/v1` · 2026-10-03 · agente `planejador-analitico`
- Entrada: `revisoes/sup-metodologia_r1.json` (veredito revisar; 22 pontos, 7 altos; 8 lacunas) e o contrato recarimbado na r3 (M29, S3, M21/M23/M27/M28, PAR13, PAR14, conservador provisório de 300 s).
- Saída corrigida: `nos/plano.json`. Não está carimbado: o carimbo do plano é o último, depois do ajuste textual do contrato e da qualidade (pedido do orquestrador).
- `python -m motor.validar <dv> --fase D2`: o único bloqueio é "nó plano: nao_carimbado".
- Números: não há resultado de análise. Aparecem só parâmetros de desenho: datas, semanas, alfa, contagens de calendário e convenções a aceitar no G2.

## Conclusão

Aceitei os 22 pontos e as 8 lacunas. Nenhum foi recusado. Em cinco casos a solução difere da sugerida:

- **CR2:** passa a ser lido por envelope, fora do Holm.
- **H-P14b:** vira contagem de robôs poupados.
- **P13:** divisão por operador, e não por período.
- **ANA-013:** reaproveitada como censo confirmatório.
- **ANA-001:** sai das famílias como verificação do deck.

## Pontos altos

**1. Confirmação das exploratórias vaza (ANA-016).** Aceito.
- A confirmação usa só as semanas ISO pares. As semanas pares da janela base (36 e 38) ficaram como robustez, sem valor de confirmação.
- Os limiares e cortes são calculados só nas semanas ímpares. ANA-012 os grava em `limiares_descoberta`, e ANA-016 os lê sem recalcular. As faixas de endereços estão fixadas no plano desde já.
- Robustez nova: deixar um operador de fora por vez, e recortes por tipo de onda e por depositante.
- O memorando usa só a estimativa da confirmação.
- `pistas` e F2 já têm três pistas a priori, vindas das hipóteses H04, H09 e H10 do especialista. As outras pistas, até cinco, saem de `pistas_propostas` de ANA-012. Elas entram no plano com recarimbo antes de ANA-016 rodar.
- Integridade: um assert no SQL proíbe semana par nos scripts exploratórios. O red team confere que o carimbo é anterior ao campo `em` de `saidas/registro.json`.

**2. H13 não separa espera de outras explicações.** Aceito.
- **H13a:** comparação dentro do mesmo operador pseudonimizado (pico contra típico, só operadores com os dois tipos de dia). Bootstrap por operador; robustez sem dias pós-pausa.
- **H13b:** unidade (dia, hora), com efeitos fixos de hora e de dia da semana. A faixa de refeição sai, por regra fixada agora. A exposição é o volume do dia, e não o processamento da hora (PQ06). Inferência por bloco de semana e por dia; vale o intervalo mais largo.
- **Consequência registrada:** se H13 confirmar, CR1 e CR8 em horas ativas viram limite superior e são lidos no teto conservador. O argumento de CR8 muda de "vagas liberadas" para "absorver crescimento e pico sem contratar".

**3. Diferença-em-diferenças de ANA-005 sem desenho.** Aceito.
- Estudo de evento semanal, com antecipações e defasagens.
- Checagem de tendência prévia.
- Placebo em 2026-06-29, só com as semanas anteriores a PAR11.
- Reponderação por faixa de endereços.
- Inferência por semana e por operador; incerteza declarada como bootstrap.
- Robustez: sem as semanas de entrada da colmeia, e controle só com operadores que não separam Royal Canin.
- **Regra para CR3:** se H06 confirmar, CR3 lê M14 do período anterior a PAR11, padronizado ao mix da janela base.

**4. Variante primária e famílias.** Aceito.
- **F1a (critério):** H-P7, H-P17 e H-P14a.
- **F1b (apoio):** H06, H13a, H13b e H01.
- **F2:** pistas exploratórias.
- Cada teste tem uma linha com recorte, métrica, variante, direção e unidade. O resto vira robustez.
- CR3 e CR7 são testados no teto conservador fixado no G2.
- A regra declara os dois papéis: o IC 95% sem ajuste classifica o critério; o p ajustado por Holm sustenta a afirmação do insight. "Passam juntos" é teste de interseção, sem ajuste.

**5. IC de CR2 com dias insuficientes.** Aceito; vale a opção de faixa_cenarios, declarada.
- CR2 é lido pelo envelope das variantes de janela (2, 4, 6 e 8 semanas; sem pós-pausa; sem a última semana) com M06 inferior. O IC de bootstrap entra como uma componente do envelope.
- O resultado traz os dias por estrato. Bloco de semana fica só como sensibilidade.
- Réplicas e inclinação de ANA-001 em nível de M06 vão ao impacto (PR14).
- H-P4a e H-P4b saem do Holm.

**6. ANA-014: horizonte validado contra projetado.** Aceito.
- Intervalo de previsão só no mês 1 (horizonte validado de 4 semanas). Meses 2 e 3 entram como faixa_cenarios, entre volume constante e tendência.
- O IP vem dos quantis empíricos dos erros fora da amostra.
- Quatro candidatos fixados agora.
- Regra de vitória: menor MAE em todas as séries e na maioria das origens; com menos de cinco origens, não há troca. O número de origens é reportado.
- A marca de dia especial cobre só feriados de calendário. Os dias sem explicação não entram como marca.

**7. Coortes de P13.** Aceito, com outro desenho.
- Painel balanceado com K = 4 semanas nos dois lados.
- A divisão é por operador: novatos que entraram em semana ímpar formam a descoberta; os de semana par, a confirmação. Os dois grupos têm operadores distintos e acompanhamento completo. Isso evita comparar coortes antes e depois do robô.
- A medida é a razão do novato contra os experientes, na mesma semana-calendário e tipo de onda.
- PAR07 passa a ser contado em operadores distintos, para todo grupo definido por operadores (`definicoes.privacidade`).

## Pontos médios

8. **M14 sem padronização (ANA-004).** Aceito. Há regra transversal de padronização por faixa de endereços e tipo de onda, com o mix da janela base e `ctx.estat.robustez` por faixa. Ficou registrado para o G2 que a escolha do teto segue a validação operacional, não o resultado de CR3.
9. **"Dentro do IC" em ANA-006.** Aceito. Agora é teste de equivalência: IC 90% dentro de ±10% do valor do slide 10 (convenção, QP6). Reamostragem por operador, com tarefa e usuário como sensibilidade, harmonizada com ANA-007.
10. **H-P14a e H-P14b.** Aceito.
    - H-P14a: o p fica só na parte de linhas (PR07), na janela longa de 38 dias. A parte do checkout (PR08) é faixa sem p.
    - H-P14b: passa a ser "robôs poupados pelo pooling", pela regra de M22 nos perfis horários do p90. É determinístico e fica fora do Holm.
11. **ANA-001: OLS iid.** Aceito.
    - Erro HAC, mais bloco de semana.
    - Degrau na entrada da colmeia e pesos por dias plenos.
    - p unilateral com checagem de sinal.
    - Rotulada como verificação do deck e retirada das famílias.
    - Inclinação em nível de M06 vai ao impacto.
12. **ANA-008.** Aceito.
    - Só segundas contra terça a sexta; os pós-pausa ficam descritivos.
    - Primeira hora = a hora da primeira linha do dia.
    - Robustez por metades do período.
    - Incerteza alinhada para intervalo_confianca.
13. **Poucos clusters e bootstrap iid.** Aceito. Há um módulo comum (estratificado, por cluster e por bloco de semana). Cada estimativa reporta o n de clusters e usa o mais largo dos dois IC. Abaixo de 10 clusters, só descritivo.
14. **Inconclusivo em CR4–CR7, e M29/S3 fora do plano.** Aceito. Há destino do inconclusivo para cada CR, de CR1 a CR8, e para os argumentos de venda. Em CR7, inconclusivo mantém a colmeia como candidata. ANA-003, ANA-004 e ANA-007 trazem os quatro tetos, S1 a S3 e M29.
15. **Censo preso nas exploratórias.** Aceito. ANA-013 virou um censo confirmatório descritivo do período inteiro, com lista fechada:
    - operadores ativos;
    - horas do armazém;
    - proxy de rotatividade;
    - H08;
    - M29;
    - abandono;
    - intervalo mediano por tipo de onda.

    As associações de P15 e P13 foram para ANA-012.
16. **Tolerância da ponte (ANA-011).** Aceito. Diferença relativa de até 2%, ou o arredondamento do próprio número quando o deck é aproximado. Desempate fixado: mais números reproduzidos, depois o método do slide 12, depois o mais recente.
17. **Hipóteses formadas com os mesmos dados.** Aceito. ANA-001, ANA-003 H-P1, ANA-006, a parte descritiva de ANA-008 e ANA-011 levam o rótulo de verificação do deck. Nesses insights a linguagem é descritiva, sem "significativo".

## Pontos baixos

18. **Incerteza por chave.** Aceito: `definicoes.incerteza_por_chave`.
19. **H04 por construção.** Aceito: a estatística principal é o intervalo absoluto por faixa de endereços; a parcela fica descritiva.
20. **Correlação entre ativos e volume.** Aceito: desvios da média da semana, dia da semana e mês controlados, e corte de uma hora.
21. **Dia máximo.** Aceito: a referência de retomada é a média dos dias pós-pausa e das segundas; o máximo só como limite superior (ANA-003, ANA-009).
22. **Extremos de vários IC combinados.** Aceito: as réplicas do bootstrap vão ao impacto, e a grade de frota inclui os limites do IC do p90.

## Lacunas

- **Poder e tamanho mínimo.** Feito. Cada análise tem o campo `poder`, com unidade, n esperado pelo calendário e efeito relevante. Há regra de mínimo de clusters (20 ou mais / 10 a 19 / menos de 10). O MDE é calculado antes do efeito e gravado como `mde_*`. MDE maior que o efeito relevante dá inconclusivo por desenho.
  - Efeito relevante: convenção de 10%, exceto CR3 = PR05 ÷ 2 − PR06 (QP6, a aceitar no G2).
- **Padronização por mix.** Feito: `definicoes.padronizacao_mix`.
- **Consequência dos pré-requisitos.** Feito: H05, H06, H11 e H13, cada um com sua regra.
- **M29 e S3.** Feito.
- **Proxy de rotatividade para CR8.** Feito: ANA-013, item 4.
- **Tendência do mix e H06 no impacto.** Feito: `entradas_impacto` liga ANA-001 e ANA-014 ao PR14, e ANA-005 a CR3.
- **Revisão dos executores.** Fica para a D3.
- **Especialista e qualidade desatualizados.** É com o orquestrador; está em `pendencias`.

## Perguntas novas ao G2

- **QP5:** teto conservador de 300 s ou de 600 s. Escolher sem olhar CR3.
- **QP6:** convenção de efeito relevante e margens de equivalência e de reprodução.
