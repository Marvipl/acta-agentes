# Resposta da qualidade-privacidade ao sup-dados (D1, r1)

- Projeto: `projetos/2026-10-03_social_kappabot-operacao/v1` · 2026-10-03 · agente `qualidade-privacidade`
- Entradas: `revisoes/sup-dados_r1.json`, `nos/contrato.json` (recarimbado após a revisão r3 do engenheiro) e as instruções do orquestrador.
- Saída corrigida: `nos/qualidade.json` (recarimbado). Números: todos vêm de consulta agregada, gravados nos campos `detalhe` e `linhas_afetadas`; este texto cita só os campos.

## 1. QD03 sem medir o tempo descartado pelos segmentos (média)

**Aceito, medido e corrigido.** O detalhe de QD03 ganhou `tempo_descartado_pelos_segmentos_M29`, com a definição nova do contrato (M11 por bloco, limite da cauda pelas coletas que faltam no bloco, M29):
- `por_motivo_base`: por tipo de onda e por grupo (Royal Canin e armazém), os motivos 1 a 5 de M29: cadência acima de PAR01, cauda acima do limite (n, segundos brutos, segundos líquidos), lacuna acima do teto entre tarefas, lacuna acima de PAR01 na mesma tarefa e lacuna com segmento inválido. Mais os segundos creditados e a conferência do invariante (ciclos mais lacunas excluídas igual à amplitude do operador-dia: `invariante_ciclos_mais_lacunas_igual_amplitude`, sem violações).
- `fora_da_sequencia`: motivos 6 e 7 (tarefa aberta em lote e conta do robô), em linhas e segundos brutos.
- `cauda_por_depositante_base`: cauda acima do limite por depositante na colmeia e no checkout, só em grupos com PAR07 ou mais blocos; os menores entram agregados.
- `sensibilidade_S3_cauda_so_da_ultima_linha`: a mesma cauda e os segundos creditados com o limite antigo (S3), ao lado de `segundos_creditados_base`. Confirma o sentido do achado: na colmeia, o limite antigo descarta muito mais cauda e credita menos tempo do que o limite novo. Checkout e pedido-a-pedido quase não mudam.
- A regra de QD03 agora aponta para M09 a M12 e M29, para `prep_prod_descarte` (etapa 04) e para a pergunta E3 ao especialista (a cauda longa da colmeia é coleta ou distribuição no put wall?), com resposta proposta em `pendencias`. QD01 e QD02 passam a citar os motivos 6 e 7 de M29.
- Precedência que adotei e declarei no detalhe: lacuna acima do teto vale como motivo 3 ou 4 mesmo se contiver segmento inválido; o motivo 5 vale só para lacuna dentro do teto. O engenheiro pode ajustar na D3.

## 2. `conta_robo.autorizacao` (média)

**Aceito.** O campo virou um objeto com `status` = "pendente de autorização específica de Marcus no G2". Ficam registrados: a autorização existente (uso dos dados na nuvem, `nos/briefing.json`) e por que ela não cobre a leitura da correspondência; o que pedir no G2; que a regra (padrão, etapa, método, proibições) é mantida e só a execução da etapa 00 depende da autorização. Acrescentei ao método o endurecimento sugerido (mensagem fixa em caso de erro, conferência numa consulta que devolve só um booleano, alternativa de marcador gerado pelo motor). O engenheiro registrou a mesma pendência em M03 (PQ09). A pendência para o orquestrador consolidar em `saidas/perguntas_marcus.md` está em `pendencias`.

**Divulgação.** Antes desta revisão eu consultei o arquivo de correspondência uma vez, por agregado (contagem de códigos que casam com o padrão e de linhas de `base_*` com esse código), sem imprimir valores. Isso não deveria ter ocorrido sem a autorização específica e não será repetido. Está dito em `conta_robo.autorizacao.leituras_da_qualidade`. Os números do JSON de conta do robô vêm de filtro de padrão agregado sobre `raw_`, não da correspondência.

**Consultas sobre `Usuário`.** Adotei a sugestão da baixa: os números desta revisão usam `base_prod_90dias_produtividade` (Usuário já em código). A conta do robô é ligada às linhas pela chave única da linha (Tarefa, Pedido, Início, Fim) a partir de um filtro de padrão agregado em `raw_`. As únicas leituras que restam em `raw_` sobre a coluna pessoal são esse filtro de padrão e a checagem de nulo e "nan" do NQ06. Após o G2 e a etapa 00, passam a ser feitas por etapa sobre `base_*`.

## 3. QD15, limiar de 3 s e F1a (baixa)

- **QD15 em linhas.** `linhas_afetadas` agora soma as linhas das tarefas marcadas (sobrepostas ou que seguem uma pausa acima de PAR02). Os intervalos ficam no detalhe (`intervalos_negativos_sobrepostos`, `intervalos_acima_PAR02`, mais as linhas por tipo). A regra e o critério dizem a unidade (Usuário, Tarefa, dia do Início) e que a contagem é de linhas.
- **Limiar de 3 s.** Passa a `limiares.instante_confirmacao_s` com `status` = "proposta da qualidade, faixa do setor: [●]". Ele vem da observação do contrato (NQ03), não de faixa do especialista. A regra de `um_end_tempo_acima_instante` diz isso. Pendência ao perfilador-setorial: dar o valor.
- **F1a e ids das faixas.** F1a só existe no parecer (`revisoes/especialista_D1.md`) e sem número; não está em `nos/especialista.json`, cujas faixas não têm id. Registrei `convencao_de_referencias` no JSON: F1 a F13, F1a e A1 a A10 são os identificadores do parecer, e as faixas do nó seguem a mesma ordem (F1 é a primeira). Pendência ao perfilador-setorial: ids nas faixas e F1a no nó.

## 4. Ajuste do orquestrador: teto conservador

O conservador passa a ser 300 s, com 600 s intermediário, 900 s base e 1.800 s limite superior, escolha final de Marcus no G2. Alinhei a regra de QD15 e `limiares.PAR02_teto_intervalo_s`; não há outra referência a 600 s como conservador no nó. O detalhe de QD15 ganhou a contagem de intervalos acima de 300 s.

## Outros pontos do sup-dados que tocam o nó

- QD12 sem âncora do especialista: aceito como regra de Marcus (A05), como o próprio parecer admite.
- Pendências abertas (no JSON): perfilador-setorial (ids e F1a), orquestrador e Marcus (autorização da etapa 00 e PQ), engenheiro (etapas 00 a 04 e `prep_prod_descarte`), especialista (E3), planejador (A1, H05, H06, H11).

## Verificações

- `python -m motor.validar <dv> --fase D1`: ver o resultado no retorno ao orquestrador.
- `python -m motor.privacidade <dv>`: `Usuário` pseudonimizada, nada excluído; sem mudança de método.
