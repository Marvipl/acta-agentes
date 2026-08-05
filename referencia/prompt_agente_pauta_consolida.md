# Prompt — Rotina 2: Atualização da dash (staff)

> Rotina Remote semanal. Repositório: acta-agentes. Fuso: America/Sao_Paulo.
> Agendamento: terças às 09:00 (America/Sao_Paulo) — cron UTC `0 12 * * 2`.
> Requer, no ambiente de nuvem da rotina: variáveis SLACK_BOT_TOKEN e
> SLACK_CHANNEL_ID, e acesso de rede liberado para slack.com e
> files.slack.com. A lista e a dash são localizadas em tempo de execução —
> nenhum ID em configuração. Nenhum segredo neste arquivo ou na instrução.

Leia pauta-staff/SKILL.md e siga exatamente o "Fluxo de execucao (rotina de
terca-feira 9h — atualizacao da dash)" descrito nele.

Resumo do fluxo:

1. Ler a lista "Action Plan - Staff C-level" (slack.sh lista_garantir,
   lista_itens, usuarios_canal) e calcular os indicadores: não finalizadas
   (aberto + fazendo) no total e por pessoa, vencidas por pessoa, concluídas.
2. Ler a dash (slack.sh dash_canvas_id + canvas_conteudo) e extrair da tabela
   de histórico o número da semana passada (última linha) — nunca calcular
   por conta própria.
3. Atualizar os 4 blocos do bot na dash (slack.sh canvas_substituir):
   indicadores, tabela de desempenho individual, tabela de histórico (linhas
   antigas + a linha desta semana ao final) e tabela de action items não
   concluídos. NUNCA editar as seções manuais (✍️ Resumo, Lembretes, Pauta
   adicional) nem a Pauta padrão.
4. Verificar relendo o canvas: números batem com a lista, histórico ganhou
   exatamente uma linha, seções manuais intactas.
5. Postar no canal: "📊 Dash atualizada para a reunião de amanhã: <url da
   dash>. Não finalizadas: N (semana passada: M). Pauta adicional e resumo:
   direto na dash."

Este fluxo não gera arquivos nem envia DMs. Respeitar as regras invioláveis
do SKILL.md — em especial: nunca inventar dados e nunca tocar nas seções
manuais. Nunca imprimir o valor do token.
