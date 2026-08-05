# Prompt — Rotina 1: Lembrete de segunda (staff)

> Rotina Remote semanal. Repositório: acta-agentes. Fuso: America/Sao_Paulo.
> Agendamento: segundas às 09:00 (America/Sao_Paulo) — cron UTC `0 12 * * 1`.
> Requer, no ambiente de nuvem da rotina: variáveis SLACK_BOT_TOKEN e
> SLACK_CHANNEL_ID, e acesso de rede liberado para slack.com e
> files.slack.com. A lista e a dash são localizadas em tempo de execução —
> nenhum ID em configuração. Nenhum segredo neste arquivo ou na instrução.

Leia pauta-staff/SKILL.md e siga exatamente o "Fluxo de execucao (rotina de
segunda-feira 9h — lembrete)" descrito nele.

Resumo do fluxo:

1. Ler a lista "Action Plan - Staff C-level"
   (pauta-staff/scripts/slack.sh lista_garantir e lista_itens) e identificar
   os responsáveis por itens não concluídos.
2. Postar UMA mensagem no canal com os dois lembretes da semana: atualizar
   status e comentário dos itens na lista até 23:59 (link via slack.sh
   lista_url) e adicionar itens de pauta adicional direto na seção ➕ da
   dash (link via slack.sh dash_url), mencionando (<@ID>) uma única vez cada
   responsável por item em aberto. Nunca mencionar por palpite.

Não fazer mais nada além disso. Nunca imprimir o valor do token.
