# Prompt — Agente de Pauta / Rotina 1: Coleta (segunda-feira 09:00)

> Rotina Remote semanal. Repositório: acta-agentes. Fuso: America/Sao_Paulo.
> Requer, no ambiente de nuvem da rotina: variáveis SLACK_BOT_TOKEN,
> SLACK_CHANNEL_ID e SLACK_LIST_ID (lista de pendências), e acesso de rede
> liberado para slack.com e files.slack.com. Nenhum segredo neste arquivo ou
> na instrução.

---

Preparação: chmod +x pauta-staff/scripts/*.sh

Passo 0 — Diagnóstico: rode pauta-staff/scripts/slack.sh testar
- Se falhar com "FALHA DE REDE", pare e reporte que o ambiente da rotina está
  bloqueando slack.com (adicionar slack.com e files.slack.com aos domínios
  permitidos do ambiente). Não é problema de token.
- Se falhar com "TOKEN INVALIDO", pare e reporte o erro exato.

Tarefa: leia pauta-staff/SKILL.md e siga exatamente o "Fluxo de execucao
(rotina de segunda-feira 9h — coleta)" descrito nele.

Resumo do fluxo (a referência completa é o SKILL.md):

1. Poste no canal a seguinte mensagem, sem alterações, usando
   pauta-staff/scripts/slack.sh postar:

"Bom dia! Coleta de pauta adicional para a Reunião de Staff C-Level de
quarta-feira. Respondam NESTA THREAD até hoje às 23:59 com os itens que querem
incluir (tema, contexto em 1-2 linhas e se é informativo ou para decisão).
A pauta consolidada será publicada amanhã às 9h."

2. Leia a lista de pendências (pauta-staff/scripts/slack.sh lista_itens) e o
   link dela (slack.sh lista_url). Poste UMA mensagem avulsa de lembrete no
   formato do SKILL.md: atualizar status e comentário dos itens na lista até
   23:59, com o link, mencionando (<@ID>) uma única vez cada responsável de
   item não concluído. Sem itens pendentes, poste o lembrete sem menções.

Não faça mais nada além disso; confirme o ts da mensagem de coleta e quantos
responsáveis foram lembrados. Nunca imprima o valor do token em nenhuma saída.
