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
   "Pendências — Staff C-Level", fonte unica das pendencias. A lista e
   localizada PELO NOME em tempo de execucao (nenhum ID fixo); o comando
   `lista_garantir` a cria e compartilha no canal se nao existir. Colunas: Pendencia, Responsavel, Data prevista, Status
   (Aberto/Fazendo/Concluido) e Comentario. O time atualiza status e
   comentario direto na lista (lembrete da rotina de segunda, ate segunda
   23:59); a rotina de terca cria na lista os itens novos vindos do Plano de
   Acao da ultima ata e poe na pauta apenas um RESUMO — a verificacao item a
   item e feita direto na lista, fora ou durante a reuniao.
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
   lista 'Pendências — Staff C-Level' do Slack; verificacao item a item direto
   na lista." + dois bullets com dados REAIS lidos da lista no passo 5 do
   fluxo de terca:
   - "Resumo da lista: X em aberto, Y em andamento, Z concluidas."
   - "Sem atualizacao desde a semana passada: [Nome] (n itens), ..." — apenas
     se houver itens nao concluidos com comentario vazio; se todos tiverem
     comentario, omita este bullet.
   Sem tabela de pendencias no documento — a lista e a fonte unica.
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
`SLACK_DM_USER_IDS` para o envio por DM do passo 10 — IDs de usuario U...
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
4. **Sincronizacao do Plano de Acao com a lista**: localize o arquivo da
   ULTIMA reuniao com
   `./pauta-staff/scripts/achar_pauta_anterior.sh <data_da_proxima_quarta_ISO> /tmp/anterior.docx`.
   O script baixa os .docx recentes do canal e valida cada um PELO CONTEUDO
   (titulo contendo Staff/C-Level + linha "Data" interpretavel, via
   `pauta-staff/scripts/validar_pauta.py`), escolhendo o de data interna mais recente
   anterior a proxima reuniao — nunca confie apenas no nome ou na ordem de
   upload. Depois `python3 pauta-staff/scripts/ler_docx.py /tmp/anterior.docx` e extraia
   APENAS as linhas preenchidas da tabela de plano de acao
   ("# | Acao | Responsavel | Prazo"). Rode
   `./pauta-staff/scripts/slack.sh lista_garantir` antes de mexer na lista.
   Para cada acao que NAO exista na lista
   (compare o texto com o campo pendencia dos itens de
   `./pauta-staff/scripts/slack.sh lista_itens`, ignorando diferencas de
   caixa/espacos), crie o item com
   `./pauta-staff/scripts/slack.sh lista_criar_item "<acao>" "<IDs>" "<data>" aberto`
   — responsavel mapeado por nome via `usuarios_canal` (mais de um nome:
   IDs separados por virgula; sem correspondencia clara: deixe sem
   responsavel e registre no relato); prazo no formato dd/mm/aaaa vira data
   AAAA-MM-DD; prazo textual vai no 5º argumento como
   "Prazo original: <texto>". Nunca crie duplicatas nem apague/edite itens
   existentes. Se nao houver arquivo valido (exit 3), pule a sincronizacao e
   registre o aviso.
5. **Leitura da lista**: leia `./pauta-staff/scripts/slack.sh lista_itens`
   (ja com os itens recem-sincronizados) e calcule: contagem por status
   (aberto / fazendo / concluido) e, entre os itens nao concluidos, os
   responsaveis com comentario vazio (para o bullet "Sem atualizacao desde a
   semana passada", com nomes em texto — sem mencao dentro do DOCX).
6. **Montagem**: escreva o JSON de conteudo seguindo `pauta-staff/exemplos/pauta_exemplo.json`
   (esquema completo no cabecalho de `pauta-staff/scripts/gerar_pauta.py`).
   A secao 1 usa apenas bullets (resumo da lista, conforme "Estrutura
   obrigatoria"), sem tabela de pendencias. Inclua `footer_data` com a data
   da reuniao (dd/mm/aaaa).
7. **Geracao**: `python3 pauta-staff/scripts/gerar_pauta.py --template
   pauta-staff/templates/Template_Ata_Staff.docx --json /tmp/conteudo.json --out
   /tmp/Pauta_Staff_AAAA-MM-DD.docx` (data da quarta-feira no nome).
8. **Verificacao antes de publicar**: rode `python3 pauta-staff/scripts/ler_docx.py` no
   arquivo gerado e confira: (a) toda resposta valida da thread virou item da
   Pauta Adicional, (b) as contagens do resumo batem com a lista lida no
   passo 5, (c) as secoes 2-4 contem apenas o texto generico fixo, (d) a data
   esta correta.
9. **Publicacao**: `./pauta-staff/scripts/slack.sh enviar_arquivo /tmp/Pauta_Staff_....docx
   "Pauta da reuniao de quarta-feira <data>. Pendencias na lista: <url de
   lista_url> — revisem seus itens antes da reuniao. Itens de ultima hora
   podem ser levados diretamente na reuniao."`
10. **Copia por DM**: se `SLACK_DM_USER_IDS` estiver definida, envie o MESMO
   arquivo por mensagem individual a cada destinatario com
   `./pauta-staff/scripts/slack.sh dm_arquivo /tmp/Pauta_Staff_....docx
   "<mesmo comentario da publicacao>"`. Com o valor `canal`, o proprio script
   resolve os destinatarios na hora: membros atuais do canal, excluindo bots e
   contas desativadas. O comando continua nos demais destinatarios se um
   falhar — falha parcial de DM nao invalida a publicacao no canal; apenas
   registre os avisos no relato final. Se a variavel nao estiver definida,
   pule este passo.
11. **Sem respostas na thread**: gere a pauta sem a secao Pauta Adicional e
    informe no comentario de publicacao: "Nenhum item adicional foi enviado
    nesta semana."

## Pos-reuniao (fora do escopo do agente)

O detalhamento das secoes Projetos, Comercial e Financeiro e preenchido
manualmente pelo time com base no que foi discutido, e a ata final e enviada ao
canal pelo proprio time. O agente nao participa dessa etapa — mas o Plano de
Acao do arquivo enviado sera sincronizado com a lista de pendencias na terca
seguinte (passo 4), desde que o documento mantenha o titulo Staff C-Level e a
linha "Data" no padrao atual (a selecao e feita pelo conteudo do arquivo, nao
pelo nome). Status e comentario das pendencias sao atualizados pelo time
DIRETO na lista do Slack — o agente nunca altera itens existentes, apenas cria
os novos.

## Tratamento de erros

- Falha em chamada ao Slack: pare e reporte o erro exato (`ERRO Slack: <codigo>`).
- `achar_pauta_anterior.sh` com exit 3 (nenhum candidato valido): siga a regra
  da secao 1 (linha placeholder) e avise no comentario de publicacao. Os motivos
  de descarte de cada candidato saem no stderr do script — inclua-os no log.
- Nunca publique um arquivo que nao passou pela verificacao do passo 7.
