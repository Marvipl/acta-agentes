# Planejador analítico: registro das pistas de ANA-012 em ANA-016 e na F2 (D3, r3)

- Projeto: `projetos/2026-10-03_social_kappabot-operacao/v1` · 2026-10-03 · agente `planejador-analitico`
- Entradas lidas: `revisoes/pistas_ANA-012.md`, `saidas/analises/ANA-012/pistas_propostas.csv`, os nomes das chaves de `saidas/analises/ANA-012/limiares_descoberta.csv` e `revisoes/orquestrador_decisao_semana_incidente.md`. Todos esses arquivos vêm só da descoberta (semanas ímpares).
- Não li nenhum dado nem resultado das semanas pares. ANA-016 ainda não foi registrada.
- Saída: `nos/plano.json` (ANA-016, `familias_holm.F2`, ANA-000, `definicoes.janela_taxa_corrente`, pendências), recarimbado.
- Números: nenhum resultado digitado. Limiares e pesos são citados pelo nome da chave e lidos do arquivo registrado.

## Conclusão

A F2 passa a ter seis testes, com Holm sobre os seis:
- PT-H04, PT-H09 e PT-H10, as três pistas a priori;
- PT-D1, PT-D3 e PT-D4, as pistas novas.

PT-D2 fica fora da F2: é reportada só como descritiva.

## Decisão por pista

| Pista | Decisão | Motivo (só descoberta) |
|---|---|---|
| PT-D1: M14 padronizado do pedido-a-pedido, Royal Canin menor que os outros (P9; CR3, CR5) | Entra | IC fora do zero. Muda o que se promete em ALT6: a linha de base da Royal Canin não vale como base do armazém. |
| PT-D2: M14 do armazém maior no pico que no típico (P19; CR8) | Fora da F2, descritiva | O IC cruza o zero no tratamento primário. O sinal depende da semana do incidente. Há poucos dias de pico nas semanas pares, abaixo do mínimo de 10 unidades. Seria inconclusiva por desenho e gastaria alfa das demais. Fica como hipótese do teste controlado para M23. |
| PT-D3: mediana de M10(a) da Royal Canin maior que nos outros (P10; CR3) | Entra | IC fora do zero. É a pista do tempo fora do relógio, de leitura descritiva. |
| PT-D4: M14 padronizado de checkout e colmeia, Royal Canin menor (P9; CR3, CR7) | Entra | IC fora do zero, com 10 a 19 operadores: o IC sai com aviso. Junto com PT-D1, separa produto e layout de processo. Não muda a regra de CR7. |

Para cada pista nova, o plano registra:
- hipótese, recorte e métrica;
- estatística, direção, nulo e variante primária (teto base e pesos fixos);
- limiares fixos, pelo nome da chave em `limiares_descoberta`;
- unidade (operador, bloco de semana e dia; vale o IC mais largo), robustez, efeito relevante e leitura comercial.

A regra de leitura é comum às seis pistas (`ANA-016.regra_leitura_pistas`):
- sinal, IC 95% fora do nulo, p ajustado na F2 abaixo de alfa e sem inversão;
- regra `sem_poder` e aviso de magnitude;
- o memorando usa só a estimativa das semanas pares.

## Incidente da Royal Canin

- A semana de 21 a 25/09 é ímpar. ANA-016 não filtra incidente nas semanas pares.
- Antes dos testes, ANA-016 confere em agregado o volume da Royal Canin em cada semana par. A referência é a mediana semanal das semanas ímpares sem o incidente.
- Uma semana par abaixo da metade dessa mediana é marcada. As pistas com a Royal Canin rodam sem ela (primário) e com ela (robustez). A regra foi fixada sem olhar as semanas pares.
- Registrei também em `definicoes.janela_taxa_corrente` o desvio declarado pelo orquestrador: a base da oferta são as quatro semanas até 2026-09-18, e a janela original vira cenário de estresse.

## Próximos passos

- Estatístico: estender ANA-000 para PT-D1, PT-D3 e PT-D4 (alfa ÷ 6 no pior caso) e registrá-la de novo antes de ANA-016. Os valores das F1 devem sair iguais.
- Red team: conferir que este recarimbo é anterior ao campo `em` de ANA-016.
