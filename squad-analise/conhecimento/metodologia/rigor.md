# Rigor analítico

## Tipo de análise
- **Confirmatória:** hipótese e teste registrados no plano antes de rodar. Pode sustentar decisão.
- **Exploratória:** surgiu depois ou não tinha hipótese. Gera pista; só vira insight aprovado se for confirmada em outra análise (outro período ou recorte).

## Nível da afirmação
- **Descritivo:** o que aconteceu ("a duração média foi X").
- **Associativo:** o que anda junto ("missões da noite duram mais"). Não diz por quê.
- **Causal:** o que provoca ("trocar o turno reduz a duração"). Só com desenho: experimento, antes e depois com grupo de controle, pareamento ou descontinuidade, descrito no plano.

## Incerteza adequada ao método
| Situação | Tipo |
|---|---|
| Contagem ou soma de todos os registros do período | nenhuma |
| Média, proporção ou diferença estimada de uma amostra | intervalo_confianca |
| Distribuição estranha ou estatística sem fórmula simples | bootstrap |
| Previsão de valor futuro | intervalo_previsao |
| Valor que depende de premissas (impacto financeiro) | faixa_cenarios (o motor simula) |

## Barreiras
- Efeito e incerteza sempre; valor-p sozinho não decide.
- Vários testes ao mesmo tempo: correção (Holm por padrão).
- Robustez: o efeito em pelo menos dois recortes; inversão de sinal entre segmentos invalida a leitura agregada.
- Modelos: validação fora da amostra, por tempo quando houver data, contra uma referência simples.
- Amostra pequena (menos de 30 por grupo): sinalizar; grupos com menos de 5 registros não vão ao relatório.

## Estados do insight
descoberto → quantificado → validado → acionável → aprovado. O motor (`python -m motor.insights`) confere o que cada estado exige.
