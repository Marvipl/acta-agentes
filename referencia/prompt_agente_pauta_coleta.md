# Prompt — Agente de Pauta / Rotina 1: Coleta (segunda-feira 09:00)

> Rotina Remote semanal. Repositório: acta-agentes. Fuso: America/Sao_Paulo.
> Requer, no ambiente de nuvem da rotina: variáveis SLACK_BOT_TOKEN e
> SLACK_CHANNEL_ID, e acesso de rede liberado para slack.com e files.slack.com.
> Nenhum segredo neste arquivo ou na instrução.

---

Preparação: chmod +x pauta-staff/scripts/*.sh

Passo 0 — Diagnóstico: rode pauta-staff/scripts/slack.sh testar
- Se falhar com "FALHA DE REDE", pare e reporte que o ambiente da rotina está
  bloqueando slack.com (adicionar slack.com e files.slack.com aos domínios
  permitidos do ambiente). Não é problema de token.
- Se falhar com "TOKEN INVALIDO", pare e reporte o erro exato.

Passo 1 — Poste no canal a seguinte mensagem, sem alterações, usando
pauta-staff/scripts/slack.sh postar:

"Bom dia! Coleta de pauta adicional para a Reunião de Staff C-Level de
quarta-feira. Respondam NESTA THREAD até hoje às 23:59 com os itens que querem
incluir (tema, contexto em 1-2 linhas e se é informativo ou para decisão).
A pauta consolidada será publicada amanhã às 9h."

Não faça mais nada além de postar a mensagem e confirmar o envio com o ts
retornado. Nunca imprima o valor do token em nenhuma saída.
