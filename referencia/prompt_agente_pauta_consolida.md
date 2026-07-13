# Prompt — Agente de Pauta / Rotina 2: Consolidação (terça-feira 09:00)

> Rotina Remote semanal. Repositório: acta-agentes. Variáveis de ambiente da
> rotina: SLACK_BOT_TOKEN, SLACK_CHANNEL_ID. Fuso: America/Sao_Paulo.

Leia pauta-staff/SKILL.md e siga exatamente o "Fluxo de execucao" descrito nele
para gerar e publicar a pauta da Reunião de Staff C-Level de quarta-feira.

Resumo do fluxo (a referência completa é o SKILL.md):
1. Coletar as respostas da thread de coleta postada ontem, considerando apenas
   mensagens até segunda-feira 23:59 (America/Sao_Paulo).
2. Localizar o arquivo da última reunião com
   pauta-staff/scripts/achar_pauta_anterior.sh (validação pelo CONTEÚDO —
   título Staff/C-Level + data interna — nunca pelo nome do arquivo), passando
   a data da próxima quarta-feira como limite.
3. Extrair do arquivo APENAS as tabelas de pendências e de plano de ação.
4. Gerar o DOCX com pauta-staff/scripts/gerar_pauta.py sobre o template oficial.
   Seções Projetos, Comercial e Financeiro sempre com o texto genérico fixo;
   seção Pauta Adicional somente se houver itens coletados.
5. Verificar o arquivo gerado com pauta-staff/scripts/ler_docx.py antes de
   publicar. Nunca publicar sem essa verificação.
6. Publicar no canal com pauta-staff/scripts/slack.sh enviar_arquivo.

Regras inegociáveis (detalhadas no SKILL.md): nunca inventar dados; pendência
sem prazo vira "—"; sem emojis no documento; nomes comerciais 9fleet e
Roboteazy; nunca citar Corsight, Venturus ou SiDi.
