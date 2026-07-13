# Prompt — Agente de Pauta / Rotina 1: Coleta (segunda-feira 09:00)

> Rotina Remote semanal. Repositório: acta-agentes. Fuso: America/Sao_Paulo.
>
> ATENÇÃO — este arquivo commitado contém PLACEHOLDERS. Ao criar a rotina no
> claude.ai, cole o texto abaixo no campo de instrução e SUBSTITUA os
> placeholders pelos valores reais. Nunca commite o token neste repositório.

---

Configuração (execute antes de qualquer outra coisa):

    export SLACK_BOT_TOKEN="<COLE_AQUI_O_TOKEN_XOXB>"
    export SLACK_CHANNEL_ID="<COLE_AQUI_O_ID_DO_CANAL>"
    chmod +x pauta-staff/scripts/*.sh

Passo 0 — Diagnóstico: rode `pauta-staff/scripts/slack.sh testar`.
- Se falhar com "FALHA DE REDE", pare imediatamente e reporte que o ambiente
  da rotina está bloqueando slack.com (não é problema de token).
- Se falhar com "TOKEN INVALIDO", pare e reporte o erro exato.

Passo 1 — Poste no canal a seguinte mensagem, sem alterações, usando
`pauta-staff/scripts/slack.sh postar`:

"Bom dia! Coleta de pauta adicional para a Reunião de Staff C-Level de
quarta-feira. Respondam NESTA THREAD até hoje às 23:59 com os itens que querem
incluir (tema, contexto em 1-2 linhas e se é informativo ou para decisão).
A pauta consolidada será publicada amanhã às 9h."

Não faça mais nada além de postar a mensagem e confirmar o envio com o ts
retornado. Nunca imprima o valor do token em nenhuma saída.
