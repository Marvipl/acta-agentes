# Resposta do engenheiro de dados à revisão do sup-dados (D1, r3)

- Projeto: `projetos/2026-10-03_social_kappabot-operacao/v1` · 2026-10-03 · agente `engenheiro-de-dados`
- Entrada: `revisoes/sup-dados_r1.json` (veredito revisar) e o ajuste do especialista sobre o teto conservador. Saída corrigida: `nos/contrato.json` (recarimbado).
- Números: o contrato só traz parâmetros (PAR01 a PAR14) e, no bloco `invariantes_prep`, contagens de referência de consulta agregada, que não são análise registrada.

## 1. Cauda de M11 (alta)

**Aceito e verificado.** Na colmeia o Início da linha é o primeiro bipe do pedido e o Fim é comum, então depois do último primeiro bipe ainda faltam coletas de outros pedidos. O limite só do último pedido descartava a cauda.
- **M11, passo 1, reescrito por bloco** (mesma unidade e mesmo Fim corrigido). Cadência entre linhas do bloco e cauda até o Fim do bloco. O limite da cauda passa a ser max(1, soma dos endereços do bloco − m) × PAR01, com m linhas no bloco: as coletas que ainda faltam depois do último primeiro bipe. Para m = 1 vale o limite antigo, então pedido-a-pedido não muda.
- **S3 (sensibilidade obrigatória):** limite só com os endereços da última linha (a redação anterior), que dá o limite inferior de horas na colmeia. Em M12 e M14 a colmeia sai com a base e com S3.
- **Simulação própria, em agregado:** com o limite novo, as horas da colmeia da Royal Canin sobem 15%, e as do armazém sobem em ordem parecida. Checkout e pedido-a-pedido quase não mudam. Confirma o achado do sup-dados e o sentido do viés (favorecia manter a exclusão da colmeia em CR7 e ALT5).
- **Validação:** regra marcada para a pessoa do setor (A2, E3: a cauda longa é coleta ou distribuição no put wall). Registrada em `verificacoes`.
- **Granularidade (baixa):** texto corrigido. No pedido-a-pedido há poucas tarefas com 2 ou mais linhas, e cada linha é um bloco próprio com segmento [Início, fim_corrigido]. A cadência só vale em blocos com Fim repetido. A lacuna que contém um segmento inválido também sai, para o tempo inválido não voltar como lacuna.

## 2. Tempo descartado sem registro (média)

**Aceito.** Nova métrica **M29** e tabela `prep_prod_descarte`, por motivo, tipo de onda, depositante e mês. Motivos: cadência acima de PAR01, cauda acima do limite, lacuna acima do teto, lacuna acima de PAR01 dentro da tarefa, lacuna com segmento inválido, e linhas fora da sequência (tarefa aberta em lote e conta do robô). Traz n, segundos brutos e segundos líquidos. Invariante: soma dos ciclos + lacunas excluídas = amplitude do operador-dia. M09 a M12 apontam para M29. A qualidade acrescenta o detalhe de cauda em QD03 (pendência registrada).

## 3. Fórmulas que faltavam (média)

**Aceito.**
- **CR5, margem do robô adicional:** M21 ganhou a variante receita adicional do depositante d (receita com o volume de d somado ao do escopo, menos a do escopo, pelas mesmas faixas). M27 ganhou robôs adicionais (M22 sobre a demanda de d), receita e margem por robô adicional (menos PR13) e o hardware máximo, sem franquia adicional.
- **CR8, absorção do excedente:** M23 agora converte capacidade de robô em horas humanas. Absorvido por hora = min(excedente em linhas, frota × capacidade por robô); horas absorvidas = soma ÷ M14; residual = excedente − absorvidas; reforço = ceil(residual ÷ PR12). CR8 passa se o reforço for zero no dia p90.
- **Faixa de tarifa (M21, PAR14):** fórmula por faixa com os limites e as tarifas reduzidas do slide 18. Base marginal (a reduzida só acima do limite, pela leitura literal de "acima de"); a retroativa fica como sensibilidade. O deck não esclarece: [●], PQ08.
- **PR01 trimestral (M28):** a comparação usa a economia do trimestre (soma de três meses de economia ÷ soma de três meses de custo atual), e o mensal fica como referência. Base com volume constante; sensibilidade com três meses reais normalizados. Crédito da garantia = max(0, PR01 × custo do trimestre − economia do trimestre).

## 4. Etapa 00_conta_robo (média) e invariantes da D3

**Aceito.** Em M03:
- **Fora do padrão:** a etapa lê `dados/privado` e `raw_`, e `estado/README.md` prevê etapas que criam `prep_*` a partir de `base_*`. A autorização registrada (Marcus, 2026-10-03) é de uso dos dados na nuvem, não da correspondência. A autorização específica será pedida a Marcus no G2 (PQ09 nova) e registrada em `conta_robo.autorizacao` ou em `controle.json`.
- **Erro:** a etapa captura qualquer exceção e levanta erro de mensagem fixa e genérica, sem o texto do DuckDB (o motor imprime a exceção).
- **Conferência:** uma única consulta agregada devolve só um booleano. É a única leitura de `raw_`. Alternativa para o motor: marcador de conta de sistema gerado na pseudonimização.
- **Invariantes:** novo bloco `invariantes_prep`, com igualdades (sem número) e contagens de referência por tabela e por tipo de onda: linhas, pedidos, tarefas, ciclos, calendário e a conta do robô. Os pedidos distintos por `pedido_id` conferem com o número do sup-dados.

## 5. Teto conservador (ajuste do especialista)

**Aceito, corrigido em PAR02, M11, M12, M13, M14, M28, PQ03 e pendências.**
- O conservador é 300 s, provisório (teto menor = menos horas manuais = menos economia). 600 s é intermediário, 900 s é a base e 1.800 s é o limite superior. Os quatro tetos são reportados.
- M28 e M13 reportam os quatro. M28 usa 300 s como conservador.
- Ressalva mantida na nota de PAR02: 300 s fica abaixo do ciclo documentado no deck (PR16 mais etiqueta e primeiro endereço) e pode cortar trabalho legítimo; por isso é provisório. A escolha final é de Marcus no G2, com a validação da operação da Social (PQ03).

## Pendências
- **Marcus (G2):** autorização da etapa 00 (PQ09), cláusula da faixa de tarifa (PQ08) e escolha do teto conservador (PQ03).
- **Qualidade-privacidade:** detalhe de cauda em QD03 e pergunta E3 ao especialista.
- **D3:** etapas 00 a 04 e `prep_prod_descarte`, com os asserts de `invariantes_prep`.
- **Orquestrador:** consolidar PQ01 a PQ09 em `saidas/perguntas_marcus.md` antes do G2.
