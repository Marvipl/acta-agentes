# Resposta do planejador analítico à revisão do sup-metodologia (D2, r2)

- Projeto: `projetos/2026-10-03_social_kappabot-operacao/v1` · 2026-10-03 · agente `planejador-analitico`
- Entrada: `revisoes/sup-metodologia_r2.json`. Veredito: aprovado com ressalvas, com duas condições para o carimbo.
- Saída corrigida: `nos/plano.json`, agora com 17 análises: entrou a ANA-000.
- Números: nenhum resultado de análise. O único valor citado é o efeito relevante de CR3, aritmética das premissas PR05 e PR06 de `nos/decisao.json`, levado à QP6 a pedido do supervisor.

## Condições para o carimbo

**1. Alcance de `sem_poder` (alta).** Aceito, com a redação sugerida.
- "Inconclusivo por desenho" vale só na não rejeição: o IC cruza o limite ou contém o nulo. Nesse caso é proibido ler o resultado como "sem efeito" ou como falha.
- Com o IC inteiro de um lado, a classificação vale no nível nominal. Se o MDE passar do efeito relevante, o resultado leva o aviso de magnitude possivelmente exagerada (erro tipo M).
- CR3, e portanto ALT3, e CR7 ficam alcançáveis.
- A QP6 diz a Marcus que o efeito relevante de CR3 é pequeno: PR05 ÷ 2 − PR06.

**2. Direção de CR7 (alta).** Aceito.
- A variante primária de H-P17 usa o teto de 900 s com a cauda base.
- CR7 só passa se o IC inteiro ficar em PR05 ou acima também em S2 e no teto de 1.800 s. Essas são as variantes desfavoráveis à exclusão, como manda M14.exclusoes do contrato.
- S3 e o teto de 300 s são o limite favorável e só são reportados.
- Atualizados: `cenarios_teto.uso_nos_testes` (exceção para CR7), a linha de H-P17 em F1a, e a hipótese, o método, a robustez e as chaves de ANA-007.
- A regra de H11 passou a declarar como otimista um "passa" de CR7 enquanto E3 não vier.

## Pontos médios

**3. Portões de H06 (ANA-005).** Aceito.
- O portão agora é a diferença-em-diferenças ajustada pela tendência prévia linear, com IC acima de zero.
- A inferência é por operador, com unidade operador-semana. Exige pelo menos 10 operadores por grupo; com menos, H06 é inconclusiva.
- A tendência prévia e o placebo, com 7 semanas, ficam descritivos e declarados insuficientes.
- Em ANA-004, no período anterior a PAR11: o IC primário é por operador, com aviso se houver 10 a 19 operadores. O bloco de semana serve só de comparação.

**4. PT-H10 (ANA-016).** Aceito. Unidade = dia pleno (39 dias pares), com erro HAC. O bloco de semana fica como comparação, declarado como exceção ao mínimo de clusters.

**5. H13a.** Aceito. Entra a amplitude dentro do operador.
- A folga só é sustentada se a jornada ativa sobe e a amplitude fica estável: IC que contém zero e fica abaixo do efeito relevante.
- Se a amplitude sobe junto, a leitura é hora extra, e H13a não confirma folga.

**6. Intervalo de previsão de ANA-014.** Aceito.
- Usa o erro agregado de quatro semanas, um valor por origem.
- A faixa vai do mínimo ao máximo das origens, com cobertura nominal (n − 1) ÷ (n + 1) declarada.
- Não usa percentis de erros diários.

## Pontos baixos

- **ANA-008:** a primeira hora passa a ser a primeira hora do dia que alcança PAR06 do volume do dia.
- **P13:** o insight declara o viés de sobrevivência até K e a referência comum de experientes. O script grava quantos novatos saíram antes de K.
- **PT-H04:** mantida, mas lida como verificação (positiva quase por construção), não como evidência nova.

## Lacuna principal: ordem MDE antes do efeito

Aceito, com uma análise separada, a **ANA-000**:
- Grava só `n_*`, `ep_*` e `mde_*` de cada teste com p-valor ou margem (F1a, F1b, F2 e a equivalência de ANA-006).
- O EP sai de permutação ou de réplicas centradas. Nenhuma estimativa pontual, diferença ou p é gravada nem impressa.
- O orquestrador roda e registra a ANA-000 sozinha, antes das demais. O horário fica no campo `em` de `resultado.json` e o hash em `registro.json`.
- As outras análises leem esses valores e não recalculam. As chaves `mde_*` saíram delas.
- Quando entrarem as pistas de ANA-012, a ANA-000 é registrada de novo antes de ANA-016. As F1 devem sair iguais, e o red team confere.

## Mantidos

QP1 a QP6 (a QP6 atualizada) e as pendências de recarimbo das pistas. Nova pendência: o orquestrador roda a ANA-000 primeiro.
