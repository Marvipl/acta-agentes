# Prompt — Agente de Pauta do Conselho / Rotina 1: Coleta (1ª segunda do mês, 09:00)

> Rotina Remote com gatilho SEMANAL (toda segunda 09:00, America/Sao_Paulo) e
> guarda de data na instrução. Repositório: acta-agentes. Ambiente: o mesmo do
> agente de pauta de staff (SLACK_BOT_TOKEN, SLACK_CHANNEL_ID, rede liberada
> para slack.com e files.slack.com). Nenhum segredo na instrução.

---

Guarda de data — execute primeiro:

    python3 -c "import datetime,zoneinfo;d=datetime.datetime.now(zoneinfo.ZoneInfo('America/Sao_Paulo'));print(d.isoweekday(),d.day)"

Prossiga SOMENTE se o resultado for dia da semana 1 (segunda) E dia do mês
entre 1 e 7 (primeira segunda-feira do mês). Caso contrário, encerre
imediatamente reportando "fora da janela mensal — nada a fazer".

Preparação: chmod +x pauta-staff/scripts/*.sh

Passo 0 — Diagnóstico: rode pauta-staff/scripts/slack.sh testar
- "FALHA DE REDE": pare e reporte bloqueio de slack.com no ambiente.
- "TOKEN INVALIDO": pare e reporte o erro exato.

Passo 1 — Poste no canal a seguinte mensagem, sem alterações, usando
pauta-staff/scripts/slack.sh postar:

"Bom dia! Coleta de pauta adicional para a Reunião do Conselho Consultivo deste
mês. Respondam NESTA THREAD até hoje às 23:59 com os itens que querem levar ao
Conselho (tema, contexto em 1-2 linhas e se é informativo ou para deliberação).
Mensagens no canal que mencionem 'conselho' desde a última reunião também serão
consideradas. A minuta da pauta será publicada amanhã às 9h para validação."

Não faça mais nada além de postar a mensagem e confirmar o envio com o ts
retornado. Nunca imprima o valor do token em nenhuma saída.
