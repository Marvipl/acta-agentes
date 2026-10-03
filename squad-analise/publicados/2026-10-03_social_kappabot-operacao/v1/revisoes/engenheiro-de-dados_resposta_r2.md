# Resposta do engenheiro de dados às pendências da qualidade-privacidade (D1, r2)

- Projeto: `projetos/2026-10-03_social_kappabot-operacao/v1` · 2026-10-03 · agente `engenheiro-de-dados`
- Entradas: `nos/qualidade.json` (problemas QD01 a QD22, `conta_robo`, `limiares`, `pendencias`). Saída corrigida: `nos/contrato.json` (recarimbado).
- Números: o contrato só traz parâmetros (PAR01 a PAR13). As consultas de apoio foram agregadas e preliminares; a análise registrada as refaz.

## 1. Fim em bloco: M09, M10, M11 e M12 (QD03)

**Aceito e verificado.** Em checkout e colmeia as linhas da mesma tarefa e do mesmo usuário repetem o Fim e o Início é o primeiro bipe do pedido. "Início da próxima menos Fim da anterior" fica negativo quase sempre na colmeia. Em consulta agregada, o Início a Início consecutivo nunca é negativo, nem no checkout nem na colmeia.
- **Passo 1 comum (M11):** segmentos de atividade por unidade (Usuário, Tarefa). Cadência_i = [Início_i, Início_(i+1)] e cauda = [Início_n, Fim comum]. No pedido-a-pedido a unidade tem só a cauda, a linha [Início, Fim]. Segmento acima do limite (PAR01 na cadência; max(1, endereços da última linha − 1) × PAR01 na cauda) é pausa e não conta.
- **M09:** usa as cadências Início a Início, com PAR01 em cada uma. Tempo por pedido, por coleta e por unidade saem da soma das cadências válidas. A fórmula por extensão da tarefa (união dos intervalos [Início, Fim], com os trechos acima de PAR01 descontados) é variante. A cauda não entra em M09 e fica só no crédito de M11.
- **M11:** jornada ativa = união dos segmentos válidos do operador-dia, com lacunas acima do teto excluídas (PAR01 dentro da tarefa, PAR02 entre tarefas), sem dupla contagem de linhas sobrepostas. S1 e S2 valem também para segmentos inválidos.
- **M10:** usa a mesma linha do tempo. Mede só lacunas entre tarefas diferentes, com sobreposição valendo zero e marcada `sobreposicao_tarefa`.
- **M12:** o ciclo é atribuído à linha dona do segmento. A soma dos recortes de um operador-dia fecha com M11.
- **Efeito preliminar:** as horas totais caem frente à redação anterior, porque segmentos acima do limite deixam de ser creditados e as linhas sobrepostas não contam duas vezes.
- A coerência M09/M10/M11/M12 está dita na nota de M11. Também ficaram registrados `fim_em_bloco` e `tarefa_aberta_lote` e a nota nas colunas Fim e Tempo em Segundos (não somar nem tirar a média por linha em checkout e colmeia).

## 2. `linha_palete` e `un_extremas` (QD13, QD14)

**Aceito.**
- **`linha_palete`:** qualquer token de área da Região Origem igual a PALLET ALTO, PORTA PALET ALTO ou PORTA PALLET ALTO (grafias com uma e duas letras L, normalizadas), inclusive em linha de região mista, ou Qtde CxG maior que zero. Entra nas colunas derivadas (com a lista de áreas por token) e em M05. Segue fora de M14, de M22 (CR4, CR5) e da base tarifável do robô (M06).
- **`un_extremas`:** marca separada, só marcação, sem corte por valor. PAR13 registra o limiar de revisão proposto pela qualidade (`limiares.un_extremas`) e a sensibilidade, com a ressalva "sem fonte setorial: [●]". M07, M14 e M22 reportam essas linhas à parte e as tiram das comparações de unidades por hora com referência de picking fracionado. Se a Social confirmar que são caixa fechada ou palete, `linha_palete` absorve a marca.

## 3. Chave do pedido em M04 (QD18)

**Aceito, com uma ressalva.** Pedido = (depositante, Pedido) em M04, M06, M20 e M26, com a marca `pedido_em_mais_de_um_depositante` e a pergunta PQ07 à Social. Em consulta agregada, o mesmo número aparece em mais de um depositante em poucos casos, alguns com a linha MULTI (um pedido com regiões de dois depositantes).
- **Ressalva:** em M02, `pedidos_na_onda` continua contando pelo número do Pedido. Pelo `pedido_id`, esse pedido viraria dois dentro da onda e mudaria o tipo de poucas ondas de pedido-a-pedido. No total do armazém, o efeito em M04 é mínimo; por depositante nada se duplica.

## 4. Conta do robô (conta_robo)

**Registrado em M03.** Regra: login original, sem acento e em minúsculas, contendo "acta" e "robo".
- **Etapa:** `etapas/00_conta_robo.py` roda antes de qualquer etapa que marque executor. Obtém o caminho de `dados/privado` por `pragma database_list`, lê a correspondência de Usuário por `read_parquet` em SQL e cria `prep_conta_robo` só com o código. Exige exatamente uma linha e confere a contagem agregada de `base_*` contra a de `raw_*`; se falhar, aborta sem mostrar nomes.
- **Proibido:** imprimir ou gravar o login original, carregar a coluna original em pandas ou numpy, e gravar a correspondência fora de `dados/privado`.
- **Marcação:** `executor` = robo quando o Usuário pseudonimizado é igual ao código; `robo_pre_inicio` pela data de PAR11. A nota de identificação na pseudonimização foi atualizada.

## Pendências
- **D3 (engenheiro):** escrever as etapas 00 a 04, com 03 e 04 usando os segmentos de M11.
- **Marcus (via Social):** PQ07 (pedido repetido entre depositantes) e a confirmação de que as linhas de milhares de unidades são caixa fechada ou palete (junto de PQ02).
