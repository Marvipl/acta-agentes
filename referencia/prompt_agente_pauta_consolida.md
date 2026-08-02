# Prompt — Agente de Pauta / Rotina 2: Consolidação (terça-feira 09:00)

> Rotina Remote semanal. Repositório: acta-agentes. Fuso: America/Sao_Paulo.
> Requer, no ambiente de nuvem da rotina: variáveis SLACK_BOT_TOKEN e
> SLACK_CHANNEL_ID; opcional SLACK_DM_USER_IDS — IDs U... separados por
> vírgula, ou "canal" para todos os membros humanos do canal — para envio da
> pauta também por DM. A lista de pendências é localizada pelo nome em tempo
> de execução — nenhum ID de lista é configurado. Acesso de rede liberado
> para slack.com e files.slack.com. Nenhum segredo neste arquivo ou na
> instrução.

---

Preparação: chmod +x pauta-staff/scripts/*.sh

Passo 0 — Diagnóstico: rode pauta-staff/scripts/slack.sh testar
- Se falhar com "FALHA DE REDE", pare e reporte que o ambiente da rotina está
  bloqueando slack.com (adicionar slack.com e files.slack.com aos domínios
  permitidos do ambiente). Não é problema de token.
- Se falhar com "TOKEN INVALIDO", pare e reporte o erro exato.

Tarefa: leia pauta-staff/SKILL.md e siga exatamente o "Fluxo de execucao"
descrito nele para gerar e publicar a pauta da Reunião de Staff C-Level de
quarta-feira.

Resumo do fluxo (a referência completa é o SKILL.md):
1. Coletar as respostas da thread de coleta postada ontem, considerando apenas
   mensagens até segunda-feira 23:59 (America/Sao_Paulo).
2. Localizar o arquivo da última reunião com
   pauta-staff/scripts/achar_pauta_anterior.sh (validação pelo CONTEÚDO —
   título Staff/C-Level + data interna — nunca pelo nome do arquivo), passando
   a data da próxima quarta-feira como limite.
3. Sincronizar o Plano de Ação da última ata com a lista de pendências
   (antes, rode slack.sh lista_garantir): criar na lista (slack.sh
   lista_criar_item, status aberto) as ações que ainda não existem nela.
   Nunca duplicar nem alterar itens existentes.
4. Ler a lista (slack.sh lista_itens) e montar o resumo da seção 1 da pauta:
   contagens por status e responsáveis sem atualização — sem tabela de
   pendências no documento; a lista é a fonte única.
5. Gerar o DOCX com pauta-staff/scripts/gerar_pauta.py sobre o template oficial.
   Seções Projetos, Comercial e Financeiro sempre com o texto genérico fixo;
   seção Pauta Adicional somente se houver itens coletados.
6. Verificar o arquivo gerado com pauta-staff/scripts/ler_docx.py antes de
   publicar. Nunca publicar sem essa verificação.
7. Publicar no canal com pauta-staff/scripts/slack.sh enviar_arquivo, com o
   link da lista (slack.sh lista_url) no comentário.
8. Se SLACK_DM_USER_IDS estiver definida, enviar o mesmo arquivo por mensagem
   individual a cada ID com pauta-staff/scripts/slack.sh dm_arquivo (mesmo
   comentário da publicação). Falha em uma DM não invalida a publicação no
   canal — apenas relate os avisos.

Regras inegociáveis (detalhadas no SKILL.md): nunca inventar dados; pendência
sem prazo vira "—"; sem emojis no documento; nomes comerciais 9fleet e
Roboteazy; nunca citar Corsight, Venturus ou SiDi. Nunca imprima o valor do
token em nenhuma saída.
