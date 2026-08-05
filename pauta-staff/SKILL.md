---
name: pauta-staff
description: Gera a pauta semanal da Reunião de Staff C-Level da Acta Robotics no modelo oficial da empresa, a partir das pendências da reunião anterior e dos itens de pauta adicional coletados no Slack. Use sempre que a tarefa envolver criar, consolidar ou publicar a pauta de staff da Acta Robotics.
---

# Pauta de Staff C-Level — Acta Robotics

> Este agente vive inteiro em `pauta-staff/` dentro do repo `acta-agentes` e nao
> compartilha arquivos com os demais agentes. Todos os caminhos abaixo sao
> relativos a RAIZ do repositorio.

## O que este skill faz

Gera a pauta da reuniao de Staff C-Level (toda quarta-feira). A pauta e um
**esqueleto padrao** com apenas duas partes dinamicas:

1. **Pendencias da Semana Anterior** — acompanhadas na LISTA do Slack
   "Action Plan - Staff C-level", fonte unica das pendencias. A lista e
   localizada PELO NOME em tempo de execucao (nenhum ID fixo); o comando
   `lista_garantir` a cria e compartilha no canal se nao existir. Colunas: Pendencia, Responsavel, Data prevista, Status
   (Aberto/Fazendo/Concluido) e Comentario. O time cria as novas acoes e
   atualiza status e comentario DIRETO na lista (lembrete da rotina de
   segunda, ate segunda 23:59); a rotina de terca apenas LE a lista e poe na
   pauta um RESUMO com indicadores — a verificacao item a item e feita direto
   na lista, fora ou durante a reuniao. O agente nao baixa nem le arquivos de
   pauta/ata do canal e nunca altera itens existentes da lista.
2. **Pauta Adicional** — itens enviados pelo time na thread da mensagem de coleta
   de segunda-feira (cutoff segunda 23:59, America/Sao_Paulo).

As secoes Projetos, Comercial e Financeiro sao SEMPRE genericas — o detalhamento
e preenchido manualmente pelo time depois da reuniao. O agente NUNCA tenta
extrair ou redigir status de projetos, comercial ou financeiro.

O documento e um DOCX gerado por `pauta-staff/scripts/gerar_pauta.py` sobre o template real
da empresa (`pauta-staff/templates/Template_Ata_Staff.docx`) — logo, estilos, cabecalho e
rodape preservados. **Nunca escreva o DOCX manualmente nem use python-docx:
sempre use o script.**

## Estrutura obrigatoria do documento

Titulo "PAUTA DE REUNIÃO" + subtitulo "STAFF C-LEVEL", tabela de informacoes,
tabela de participantes e as secoes, nesta ordem:

1. **Pendencias da Semana Anterior** — nota "As pendencias sao acompanhadas na
   lista 'Action Plan - Staff C-level' do Slack; verificacao item a item direto
   na lista." + tres bullets de INDICADORES com dados reais calculados no
   passo 4 do fluxo de terca (sem tabela de pendencias — a lista e a fonte
   unica):
   - "Nao finalizadas (aberto + fazendo): N — semana passada: M." — M e o
     numero registrado no comentario de publicacao da pauta anterior
     (mensagem do bot no canal, passo 4); sem registro anterior, escreva
     "semana passada: sem registro".
   - "Por responsavel: Nome N, Nome N, ..." — contagem de nao finalizadas por
     responsavel, em ordem decrescente; acrescente "sem responsavel: N"
     apenas se houver itens sem responsavel.
   - "Concluidas na lista: N."
   (No DOCX, com acentuacao correta: "Não finalizadas...", "Por
   responsável...", "Concluídas...".)
2. **Projetos** — bullet unico e fixo: "Apresentacao de status semanal de projetos."
3. **Comercial** — bullet unico e fixo: "Apresentacao de status das acoes comerciais."
4. **Financeiro** — bullet unico e fixo: "Apresentacao de status do financeiro."
5. **Pauta Adicional** — SOMENTE SE houver itens coletados no Slack. Nota
   "Itens enviados pelo time na thread de coleta." + um bullet por item no
   formato `[Nome]: item.` (nome de quem enviou a mensagem). Se nao houver
   itens, a secao NAO aparece e o Plano de Acao assume o numero 5.
6. **Plano de Acao** (5 se nao houver Pauta Adicional) — nota "Proximos passos
   definidos na reuniao, com responsaveis e prazos." + tabela # | Acao |
   Responsavel | Prazo com 5 linhas vazias.

Fecha com "Encerramento e Aprovacao" e assinaturas.

## Dados fixos

Participantes padrao (ordem fixa):

| Participante | Cargo |
|---|---|
| Marcus Lima | CEO |
| Renato Correa | CFO |
| Vinicius Bastos | CTO |
| Diego Nunes | Gestor de Financas |

Tabela de informacoes: Reuniao = "Reuniao de Staff C-Level"; Data = data da
proxima quarta-feira por extenso (ex.: "15 de julho de 2026"); Formato =
"Staff — alinhamento semanal"; Secretariado por = "[a definir]".

Encerramento: "Nada mais havendo a tratar, a reuniao foi encerrada e a presente
ata lavrada para registro e aprovacao do Staff C-Level da Acta Robotics."

Assinaturas: os 4 participantes padrao.

Use acentuacao correta em todo o texto do documento (este arquivo esta sem
acentos apenas por seguranca de encoding; o DOCX final deve estar em portugues
correto, ex.: "Pendências da Semana Anterior", "Apresentação de status semanal
de projetos").

## Regras inviolaveis de conteudo

- **Nunca invente dados, valores, nomes ou prazos.** Pendencia sem prazo no
  arquivo anterior fica com "—". Item de pauta adicional entra com o texto que
  a pessoa escreveu (resumido se longo, sem adicionar informacao).
- Nomes comerciais: **9fleet** (nunca K.FLEET) e **Roboteazy** (nunca K.CONCEPT).
  Nunca cite "Corsight". Nunca cite Venturus ou SiDi como parceiros.
- Sem emojis no documento.
- Portugues do Brasil, tom de registro de ata (impessoal).
- Fuso horario de referencia: America/Sao_Paulo.

## Fluxo de execucao (rotina de segunda-feira 9h — coleta)

Pre-requisitos: os mesmos do fluxo de terca (sem necessidade de
`SLACK_DM_USER_IDS`). Rode `pauta-staff/scripts/slack.sh testar` antes de
qualquer outro passo. Nunca imprima o valor do token.

1. **Mensagem de coleta**: poste com `./pauta-staff/scripts/slack.sh postar` a
   mensagem padrao de coleta de pauta adicional (texto fixo no prompt da
   rotina), sem alteracoes.
2. **Lembrete da lista de pendencias**: rode
   `./pauta-staff/scripts/slack.sh lista_garantir` (localiza a lista pelo
   nome, cria e compartilha no canal se nao existir; imprime id e url) e leia
   a lista com `./pauta-staff/scripts/slack.sh lista_itens`. Identifique os responsaveis
   (IDs U... da coluna responsavel) dos itens com status DIFERENTE de
   "concluido". Poste UMA mensagem avulsa no canal:
   "Lembrete das pendencias: atualizem o status e o comentario dos seus itens
   na lista ate hoje as 23:59 — <url da lista>. Itens em aberto de:
   <@ID1> <@ID2> ..." (cada responsavel unico mencionado uma vez, via
   `<@ID>`; item sem responsavel nao gera mencao). Se todos os itens
   estiverem concluidos ou a lista estiver vazia, poste o lembrete sem a
   parte "Itens em aberto de:".
3. Nao faca mais nada alem disso; encerre reportando o ts da mensagem de
   coleta e quantos responsaveis foram lembrados.

## Fluxo de execucao (rotina de terca-feira 9h)

Pre-requisitos: variaveis `SLACK_BOT_TOKEN` e `SLACK_CHANNEL_ID` exportadas
(a instrucao da rotina faz o export antes de chamar este fluxo) e, opcional,
`SLACK_DM_USER_IDS` para o envio por DM do passo 9 — IDs de usuario U...
separados por virgula, ou o valor especial `canal` para enviar a todos os
membros humanos do canal. A lista de pendencias e localizada pelo nome em
tempo de execucao (`lista_garantir`) — nenhum ID de lista e configurado.
Ferramentas: `curl`, `jq`, `python3`. Rode `pauta-staff/scripts/slack.sh testar`
antes de qualquer outro passo. Nunca imprima o valor do token.

1. **Janela de coleta**: calcule segunda-feira desta semana 09:00 e 23:59
   (America/Sao_Paulo) e converta para epoch com
   `./pauta-staff/scripts/slack.sh ts "YYYY-MM-DD HH:MM"`.
2. **Mensagem de coleta**: busque no historico
   (`./pauta-staff/scripts/slack.sh historico <oldest> <latest>`) a mensagem do bot pedindo
   pauta adicional (contem "Coleta de pauta adicional"). Guarde o `ts`.
3. **Itens adicionais**: leia a thread com `./pauta-staff/scripts/slack.sh respostas <ts>`.
   **Descarte qualquer mensagem com ts posterior a segunda 23:59.** Ignore
   mensagens do proprio bot. Cada resposta valida vira um item de Pauta
   Adicional com o nome de quem enviou.
4. **Leitura da lista e indicadores**: rode
   `./pauta-staff/scripts/slack.sh lista_garantir`, depois leia
   `./pauta-staff/scripts/slack.sh lista_itens` e calcule: (a) total de NAO
   finalizadas — status aberto + fazendo; (b) contagem de nao finalizadas por
   responsavel, com nomes resolvidos via `usuarios_canal` (item com mais de
   um responsavel conta para cada um; sem responsavel entra em "sem
   responsavel"); (c) total de concluidas. Para a comparacao semanal, busque
   no historico dos ultimos 8 dias
   (`./pauta-staff/scripts/slack.sh historico <epoch_8_dias_atras>`) a
   mensagem MAIS RECENTE do bot que contenha "finalizadas na lista:"
   (comentario da publicacao da pauta anterior; a busca ignora o "Não"
   inicial para nao depender de acento) e extraia o PRIMEIRO numero apos essa
   expressao — esse e o M de "semana passada". Se nao houver tal
   mensagem, use "sem registro". Nunca calcule o numero anterior por conta
   propria — apenas o que esta registrado na mensagem. O agente NAO baixa nem
   le arquivos de pauta/ata do canal neste fluxo — a lista e o historico de
   mensagens sao as unicas fontes.
5. **Montagem**: escreva o JSON de conteudo seguindo `pauta-staff/exemplos/pauta_exemplo.json`
   (esquema completo no cabecalho de `pauta-staff/scripts/gerar_pauta.py`).
   A secao 1 usa apenas bullets (resumo da lista, conforme "Estrutura
   obrigatoria"), sem tabela de pendencias. Inclua `footer_data` com a data
   da reuniao (dd/mm/aaaa).
6. **Geracao**: `python3 pauta-staff/scripts/gerar_pauta.py --template
   pauta-staff/templates/Template_Ata_Staff.docx --json /tmp/conteudo.json --out
   /tmp/Pauta_Staff_AAAA-MM-DD.docx` (data da quarta-feira no nome).
7. **Verificacao antes de publicar**: rode `python3 pauta-staff/scripts/ler_docx.py` no
   arquivo gerado e confira: (a) toda resposta valida da thread virou item da
   Pauta Adicional, (b) as contagens do resumo batem com a lista lida no
   passo 4, (c) as secoes 2-4 contem apenas o texto generico fixo, (d) a data
   esta correta.
8. **Publicacao**: `./pauta-staff/scripts/slack.sh enviar_arquivo /tmp/Pauta_Staff_....docx
   "Pauta da reuniao de quarta-feira <data>. Nao finalizadas na lista: <N>
   (semana passada: <M ou sem registro>). Pendencias: <url de lista_url> —
   revisem seus itens antes da reuniao. Itens de ultima hora podem ser
   levados diretamente na reuniao."` — no comentario real, use acentuacao
   correta ("Não finalizadas na lista: 19"). A expressao
   "finalizadas na lista:" seguida do numero N e OBRIGATORIA e com esta
   grafia: e dela que a rotina da proxima semana extrai o M da comparacao.
9. **Copia por DM**: se `SLACK_DM_USER_IDS` estiver definida, envie o MESMO
   arquivo por mensagem individual a cada destinatario com
   `./pauta-staff/scripts/slack.sh dm_arquivo /tmp/Pauta_Staff_....docx
   "<mesmo comentario da publicacao>"`. Com o valor `canal`, o proprio script
   resolve os destinatarios na hora: membros atuais do canal, excluindo bots e
   contas desativadas. O comando continua nos demais destinatarios se um
   falhar — falha parcial de DM nao invalida a publicacao no canal; apenas
   registre os avisos no relato final. Se a variavel nao estiver definida,
   pule este passo.
10. **Sem respostas na thread**: gere a pauta sem a secao Pauta Adicional e
    informe no comentario de publicacao: "Nenhum item adicional foi enviado
    nesta semana."

## Fluxo de execucao (rotina diaria 9h — lembretes de vencimento)

Pre-requisitos: `SLACK_BOT_TOKEN` e `SLACK_CHANNEL_ID` exportadas; scope
`im:write` (DMs); bot convidado ao canal privado de avisos
"avisos-action-items" (o ID e resolvido em tempo de execucao com
`./pauta-staff/scripts/slack.sh canal_por_nome avisos-action-items`). Rode
`pauta-staff/scripts/slack.sh testar` antes de qualquer outro passo. Nunca
imprima o valor do token. Esta rotina roda TODOS os dias, inclusive fins de
semana.

1. **Datas**: calcule HOJE e HOJE+3 no fuso America/Sao_Paulo (AAAA-MM-DD).
2. **Itens ativos**: leia `./pauta-staff/scripts/slack.sh lista_itens` e
   considere apenas itens com status DIFERENTE de "concluido" E data_prevista
   preenchida. Guarde tambem a url da lista (`lista_url`).
3. **Lembrete D-3 (privado)**: para os itens com data_prevista == HOJE+3,
   agrupe por responsavel (item com mais de um responsavel: cada um recebe) e
   envie UMA DM por responsavel com
   `./pauta-staff/scripts/slack.sh dm_texto <ID> "<texto>"`, no formato:
   "⏰ Lembrete: sua(s) atividade(s) na lista Action Plan - Staff C-level
   vence(m) em 3 dias (dd/mm/aaaa):
   • <pendencia>
   Atualize o status e o comentario na lista: <url>"
   Item sem responsavel nao gera DM (aparecera no aviso de vencimento).
4. **Aviso de vencimento (canal de avisos)**: para os itens com
   data_prevista == HOJE, poste UMA mensagem consolidada no canal de avisos
   com `./pauta-staff/scripts/slack.sh postar_em <id_do_canal> "<texto>"`:
   "⚠️ Atividades vencendo hoje (dd/mm/aaaa):
   • <pendencia> — <@ID> <@ID2>
   Atualizem o status na lista: <url>"
   Item sem responsavel: escreva "sem responsavel" em texto no lugar da
   mencao. NAO poste no canal principal neste fluxo.
5. **Nada nas duas janelas**: encerre sem postar nada e reporte "nada a
   lembrar hoje".
6. As duas partes sao independentes: se o canal de avisos nao for encontrado
   (bot nao convidado), envie mesmo assim as DMs do passo 3 e reporte o erro
   do canal no relato final.
7. Nunca altere a lista. Itens ja vencidos em dias anteriores (data < HOJE)
   NAO geram novo aviso — o alerta de vencimento e unico, no proprio dia.

## Pos-reuniao (fora do escopo do agente)

Com a lista como fonte unica, o ciclo das pendencias NAO depende de ata: apos
a reuniao, o time cria as novas acoes DIRETO na lista e atualiza
status/comentario la. O agente nao busca, baixa nem le arquivos de pauta/ata
do canal — atas editadas que o time eventualmente enviar sao apenas registro
formal, sem efeito no ciclo. A comparacao semanal vem do comentario de
publicacao da pauta anterior (mensagem do bot no canal). O agente nunca
altera itens existentes da lista.

## Tratamento de erros

- Falha em chamada ao Slack: pare e reporte o erro exato (`ERRO Slack: <codigo>`).
- Sem mensagem de publicacao anterior no historico (primeira execucao ou
  intervalo maior que 8 dias): use "semana passada: sem registro" — nunca
  invente o numero.
- Nunca publique um arquivo que nao passou pela verificacao do passo 7.
