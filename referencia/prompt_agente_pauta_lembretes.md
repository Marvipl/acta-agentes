# Prompt — Rotina 3: Lembretes de vencimento (staff)

> Rotina Remote diária. Repositório: acta-agentes. Fuso: America/Sao_Paulo.
> Agendamento: todos os dias às 09:00 (America/Sao_Paulo) — cron UTC `0 12 * * *`.
> Requer, no ambiente de nuvem da rotina: variáveis SLACK_BOT_TOKEN e
> SLACK_CHANNEL_ID, acesso de rede liberado para slack.com e files.slack.com,
> scope im:write no app do Slack e o bot convidado ao canal privado
> #avisos-action-items. Nenhum segredo neste arquivo ou na instrução.

Leia pauta-staff/SKILL.md e siga exatamente o "Fluxo de execucao (rotina
diaria 9h — lembretes de vencimento)" descrito nele.

Resumo do fluxo:

1. Calcular HOJE e HOJE+3 (America/Sao_Paulo).
2. Ler a lista (pauta-staff/scripts/slack.sh lista_itens) e considerar apenas
   itens não concluídos com data prevista preenchida.
3. Itens que vencem em HOJE+3: enviar UMA mensagem privada por responsável
   (slack.sh dm_texto) listando as atividades dele que vencem em 3 dias, com
   o link da lista (slack.sh lista_url).
4. Itens que vencem HOJE: postar UMA mensagem consolidada no canal
   #avisos-action-items (id via slack.sh canal_por_nome avisos-action-items;
   postagem via slack.sh postar_em), mencionando os responsáveis (<@ID>).
5. Sem itens nas duas janelas: encerrar sem postar nada.

Nunca alterar a lista, nunca postar no canal principal neste fluxo, nunca
inventar atividades ou datas, e nunca imprimir o valor do token. Itens já
vencidos em dias anteriores não geram novo aviso.
