# pauta-staff — Agente de Pauta do Staff C-Level

> Pasta autocontida dentro do repo `acta-agentes`, seguindo a filosofia do repositório: aqui fica só conteúdo estável (playbook, scripts e template); dados que mudam toda semana (pauta gerada, itens coletados) vivem no Slack, nunca aqui. Os prompts das duas rotinas estão em `referencia/prompt_agente_pauta_coleta.md` e `referencia/prompt_agente_pauta_consolida.md`, no padrão dos demais agentes.
> Não conflita com os demais agentes: nenhum arquivo fora de `pauta-staff/` é lido ou modificado, não há instalação de dependências e nada é gravado em configuração global do repositório.

Automação semanal via **Claude Code Routines**:

As pendências vivem numa **lista do Slack** ("Pendências — Staff C-Level", colunas Pendência / Responsável / Data prevista / Status / Comentário) — fonte única, atualizada pelo próprio time direto na lista. Na reunião, a verificação item a item é feita na lista, não na pauta.

- **Segunda 09:00** — o agente posta no canal pedindo itens de pauta adicional (respostas na thread até 23:59) e um lembrete com o link da lista, mencionando os responsáveis por itens não concluídos para atualizarem status e comentário até 23:59.
- **Terça 09:00** — o agente coleta as respostas da thread (cutoff segunda 23:59), sincroniza o Plano de Ação da última ata do canal com a lista (cria os itens novos, status Aberto), lê a lista e gera a pauta da reunião de quarta com os indicadores das pendências — total não finalizado (aberto + fazendo) com comparação vs. semana passada, contagem por responsável e concluídas —, publicando o DOCX no canal (e por DM, se configurado).

A pauta gerada é um esqueleto padrão: Pendências da Semana Anterior (indicadores da lista, sem tabela — para a reunião abrir com a visão de se o volume está crescendo ou caindo), Projetos / Comercial / Financeiro com texto genérico fixo ("Apresentação de status..."), Pauta Adicional (somente se houver itens no Slack) e Plano de Ação em branco. O detalhamento das seções é preenchido manualmente pelo time após a reunião e enviado ao canal — o Plano de Ação desse arquivo vira itens novos na lista na terça seguinte.

## Estrutura

```
pauta-staff/
  SKILL.md                           Modelo da pauta Acta + fluxo do agente (leitura obrigatória da rotina)
  README.md                          Este arquivo
  templates/Template_Ata_Staff.docx  Template real (logo, estilos, rodapé) — o corpo é regenerado
  scripts/gerar_pauta.py             Gera o DOCX a partir de um JSON de conteúdo (stdlib apenas)
  scripts/ler_docx.py                Extrai texto/tabelas de um DOCX (stdlib apenas)
  scripts/slack.sh                   postar | historico | respostas | listar_arquivos_docx | baixar | enviar_arquivo | dm_arquivo | lista_itens | lista_criar_item | lista_url | ts
  scripts/validar_pauta.py           Valida um DOCX pelo conteúdo: título Staff/C-Level + data interna (stdlib apenas)
  scripts/achar_pauta_anterior.sh    Baixa os .docx do canal, valida cada um e escolhe o da última reunião
  exemplos/pauta_exemplo.json        Exemplo funcional do esquema de conteúdo
```

## Pré-requisitos

1. **App do Slack** (já feito na Etapa 1): bot scopes `chat:write`, `channels:history`, `files:read`, `files:write`, `lists:read`, `lists:write` (`groups:history` se o canal for privado; `im:write` para o envio da pauta por DM; `channels:read` + `users:read` para o modo `canal` das DMs e para as menções — `groups:read` no lugar de `channels:read` se o canal for privado); bot convidado ao canal.
2. **Lista de pendências**: totalmente automática — os comandos `lista_*` localizam a lista **pelo nome** ("Pendências — Staff C-Level") em tempo de execução, e `lista_garantir` a cria (colunas pendencia/responsavel/data_prevista/status/comentario) e a compartilha no canal se não existir. Nenhum ID configurado; se a lista for recriada, nada precisa mudar. Overrides opcionais: `SLACK_LIST_NAME` (outro nome) ou `SLACK_LIST_ID` (ID fixo).
3. **Ambiente de nuvem das rotinas**: variáveis `SLACK_BOT_TOKEN` (xoxb-...) e `SLACK_CHANNEL_ID`; opcionalmente `SLACK_DM_USER_IDS` — quem recebe a pauta também por mensagem individual: IDs de usuário U... separados por vírgula, ou o valor especial `canal` para enviar a todos os membros humanos do canal (a lista de destinatários é resolvida a cada envio); vazio/ausente desliga as DMs; acesso de rede Custom com `slack.com` e `files.slack.com` nos domínios permitidos (mantendo a lista padrão de gerenciadores de pacotes); script de configuração vazio. Nenhum segredo na instrução ou no repo.
4. Ferramentas no ambiente de execução: `curl`, `jq`, `python3` (padrão nas sessões do Claude Code).

## Teste local (faça antes de agendar)

```bash
export SLACK_BOT_TOKEN=xoxb-...
export SLACK_CHANNEL_ID=C...
chmod +x pauta-staff/scripts/*.sh

# 1) gerador funciona?
python3 pauta-staff/scripts/gerar_pauta.py \
  --template pauta-staff/templates/Template_Ata_Staff.docx \
  --json pauta-staff/exemplos/pauta_exemplo.json \
  --out /tmp/teste.docx
python3 pauta-staff/scripts/ler_docx.py /tmp/teste.docx

# 2) validador funciona? (usa o próprio arquivo gerado no passo 1)
python3 pauta-staff/scripts/validar_pauta.py /tmp/teste.docx

# 3) Slack funciona?
pauta-staff/scripts/slack.sh postar "teste do agente de pauta — pode ignorar"
pauta-staff/scripts/slack.sh enviar_arquivo /tmp/teste.docx "teste de upload — pode ignorar"
pauta-staff/scripts/achar_pauta_anterior.sh   # deve encontrar e validar o arquivo recém-enviado

# 4) DM funciona? (opcional — requer scope im:write; use seu próprio ID U...)
pauta-staff/scripts/slack.sh dm_arquivo /tmp/teste.docx "teste de DM — pode ignorar" U0SEUID

# 5) modo canal funciona? (opcional — requer channels:read + users:read;
#    só lista os destinatários, não envia nada)
pauta-staff/scripts/slack.sh membros_canal

# 6) lista de pendências funciona? (resolução pelo nome — nenhum ID necessário)
pauta-staff/scripts/slack.sh lista_garantir   # cria e compartilha se não existir
pauta-staff/scripts/slack.sh lista_itens | jq 'group_by(.status) | map({status: .[0].status, n: length})'
```

Depois, rode o prompt da Rotina 2 (abaixo) numa sessão interativa do Claude Code
apontada para este repo e valide o DOCX gerado antes de agendar de verdade.

## Rotinas (claude.ai/code/routines, ou /schedule no CLI, ou Desktop → Schedule → New Remote Task)

Ambas apontam para este repositório, com as duas variáveis de ambiente configuradas.
Horários no fuso local (America/Sao_Paulo).

### Rotina 1 — `pauta-coleta` — semanal, segunda 09:00

```
Leia pauta-staff/SKILL.md e siga exatamente o "Fluxo de execucao (rotina de
segunda-feira 9h — coleta)" descrito nele. Resumo: postar a mensagem padrão de
coleta de pauta adicional (texto fixo no prompt) e, em seguida, um lembrete
com o link da lista de pendências (slack.sh lista_url), mencionando (<@ID>)
os responsáveis por itens não concluídos para atualizarem status e comentário
na lista até 23:59. Nunca mencionar por palpite. Prompt completo em
referencia/prompt_agente_pauta_coleta.md.
```

### Rotina 2 — `pauta-consolida` — semanal, terça 09:00

```
Leia pauta-staff/SKILL.md e siga exatamente o "Fluxo de execução" descrito
nele para gerar e publicar a pauta da Reunião de Staff C-Level de quarta-feira.
Resumo: coletar as respostas da thread de coleta de ontem (apenas mensagens
até segunda-feira 23:59, America/Sao_Paulo), localizar o arquivo da última
reunião com pauta-staff/scripts/achar_pauta_anterior.sh (validação pelo conteúdo: título
Staff/C-Level + data interna — não pelo nome do arquivo), sincronizar o Plano
de Ação dele com a lista de pendências (slack.sh lista_criar_item, sem
duplicar nem alterar itens existentes), ler a lista (slack.sh lista_itens) e
gerar o DOCX com pauta-staff/scripts/gerar_pauta.py sobre o template oficial
(seção 1 apenas com o resumo da lista; seções Projetos, Comercial e
Financeiro sempre com o texto genérico fixo; Pauta Adicional somente se houver
itens) e publicar no canal com o link da lista no comentário. Se a variável
SLACK_DM_USER_IDS estiver definida, enviar em seguida o mesmo arquivo por
mensagem individual a cada ID com pauta-staff/scripts/slack.sh dm_arquivo.
Respeite todas as regras invioláveis do SKILL.md — em especial: nunca inventar
dados e nunca publicar sem a verificação final.
```

## Notas operacionais

- Routines está em research preview; cada execução consome os limites de uso do
  plano (2 execuções/semana é irrisório). As rotinas pertencem à conta que as criou.
- O cutoff de segunda 23:59 é aplicado por filtro de timestamp na coleta — por isso
  não existe uma terceira rotina às 23:59.
- Se o Slack retornar `not_in_channel`, o bot não foi convidado ao canal (`/invite @bot`).
- Para obter o ID de usuário (U...) de alguém: perfil da pessoa no Slack → menu
  "⋮" → "Copiar ID do membro". A DM chega pela aba de mensagens do app do bot —
  se alguém não estiver recebendo, confira se não silenciou o app.
- No modo `SLACK_DM_USER_IDS=canal`, TODO membro humano do canal recebe a DM.
  Se o canal tiver gente além do C-Level (assistentes, convidados), prefira a
  lista explícita de IDs — ou mantenha o canal restrito ao staff.
- O compartilhamento da lista com o canal é automático (`lista_garantir`).
  Para facilitar ainda mais o acesso, fixe a mensagem com o link da lista no
  canal ("Fixar no canal"). O agente nunca edita nem apaga itens existentes da
  lista — só cria os novos a partir do Plano de Ação; status e comentário são
  sempre do time.
- Não renomeie a lista no Slack: a localização é pelo nome exato "Pendências —
  Staff C-Level". Se precisar renomear, defina SLACK_LIST_NAME (ou
  SLACK_LIST_ID) no ambiente das rotinas com o novo nome/ID.
- Se o download do arquivo vier como HTML (erro "download nao parece um DOCX"),
  confira o scope `files:read` e se o arquivo está no mesmo workspace.
- Para mudar o modelo do documento, edite o SKILL.md (estrutura/regras) e, se for
  mudança visual, troque `templates/Template_Ata_Staff.docx` por uma ata mais recente
  — o gerador se adapta sozinho (extrai logo, estilos e numeração do template).
