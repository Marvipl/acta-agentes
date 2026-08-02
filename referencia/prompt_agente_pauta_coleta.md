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

Tarefa: leia pauta-staff/SKILL.md e siga exatamente o "Fluxo de execucao
(rotina de segunda-feira 9h — coleta)" descrito nele.

Resumo do fluxo (a referência completa é o SKILL.md):

1. Poste no canal a seguinte mensagem, sem alterações, usando
   pauta-staff/scripts/slack.sh postar:

"Bom dia! Coleta de pauta adicional para a Reunião de Staff C-Level de
quarta-feira. Respondam NESTA THREAD até hoje às 23:59 com os itens que querem
incluir (tema, contexto em 1-2 linhas e se é informativo ou para decisão).
Logo abaixo posto as pendências da última reunião — cada responsável responda
na thread da sua pendência com um update até 23:59, para todos lerem antes da
reunião. A pauta consolidada será publicada amanhã às 9h."

2. Localize o arquivo da última reunião com
   pauta-staff/scripts/achar_pauta_anterior.sh (data da próxima quarta-feira
   como limite) e extraia a união das tabelas de pendências e de plano de ação
   (apenas colunas Responsável, Pendência e Prazo — ignore a coluna Update se
   existir).

3. Poste UMA mensagem avulsa no canal por pendência (nunca dentro de thread),
   no formato exato do SKILL.md, começando com "Update de pendencia (i/N)" —
   é por esse prefixo que a rotina de terça encontra as mensagens. Mencione o
   responsável com a sintaxe <@ID> (IDs via pauta-staff/scripts/slack.sh
   usuarios_canal, associados pelo nome; sem correspondência clara e única,
   use o nome em texto — nunca mencione por palpite). Cada mensagem tem a
   própria thread, para o responsável responder individualmente.

4. Se não houver arquivo anterior válido ou nenhuma pendência, poste apenas a
   mensagem de coleta e encerre reportando o motivo.

Não faça mais nada além disso; confirme o envio com o ts da mensagem de coleta
e a quantidade de mensagens de pendência postadas. Nunca invente pendências —
somente as extraídas do arquivo. Nunca imprima o valor do token em nenhuma
saída.
