# Prompt — Assistente Estratégico, Rotina 2: leitura estratégica semanal

> Rotina Remote semanal. Repositório: acta-agentes. Fuso: America/Sao_Paulo.
> Agendamento: sextas 08:00 (America/Sao_Paulo) — cron UTC `0 11 * * 5`.
> Requer, no ambiente de nuvem da rotina: variáveis SLACK_BOT_TOKEN,
> SLACK_CHANNEL_ID (canal #estrategia) e SLACK_STAFF_CHANNEL_ID (canal do
> staff); acesso de rede liberado para slack.com e files.slack.com; conector
> Google Drive ativo; bot convidado aos dois canais. Nenhum segredo neste
> arquivo ou na instrução.

Leia assistente-estrategico/SKILL.md e siga exatamente o "Fluxo de execução
(rotina semanal — leitura estratégica)" descrito nele.

Resumo do fluxo:

1. Rodar `assistente-estrategico/scripts/estrategia.sh testar`.
2. EXECUÇÃO: ler a lista "Action Plan - Staff C-level" e a dash do staff
   (indicadores, desempenho por pessoa, últimas ~8 linhas do histórico) via
   pauta-staff/scripts/slack.sh, somente leitura.
3. REUNIÕES: ler as 2 entradas mais recentes do canvas "Resumos de reuniões —
   Staff C-Level".
4. MERCADO: ler os briefings dos últimos 7 dias na pasta Acta/Briefings do
   Drive e selecionar os 3 a 5 movimentos com maior implicação para a Acta.
5. CRUZAMENTO: identificar onde execução e mercado se tocam (ação vencida em
   tema que o mercado acelera, edital com prazo próximo sem ação na lista,
   decisão de reunião contradita por fato novo).
6. Postar no canal #estrategia (`estrategia.sh postar`) a leitura no formato
   do SKILL: Execução / Mercado (com links) / Cruzamentos e alertas /
   Pergunta da semana. Encerrar reportando o ts e as fontes consultadas.

Se todas as fontes falharem, não postar leitura pela metade — reportar o erro
e encerrar. Nunca inventar dados ou números; tendências vêm do histórico da
dash, nunca de memória. Nunca alterar lista/dash/canvas do staff. Nunca
imprimir o valor do token. Nomes comerciais: 9fleet e Roboteazy.
