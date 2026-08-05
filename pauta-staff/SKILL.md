---
name: pauta-staff
description: Mantém a dash (canvas de canal) da Reunião de Staff C-Level da Acta Robotics no Slack — analytics das atividades do Action Plan, espelho dos action items e lembretes de vencimento — a partir da lista "Action Plan - Staff C-level". Use sempre que a tarefa envolver a dash, a pauta ou as pendências do staff da Acta Robotics.
---

# Dash de Staff C-Level — Acta Robotics

> Este agente vive inteiro em `pauta-staff/` dentro do repo `acta-agentes` e nao
> compartilha arquivos com os demais agentes. Todos os caminhos abaixo sao
> relativos a RAIZ do repositorio.

## O que este skill faz

Mantem a DASH da reuniao semanal de Staff C-Level (toda quarta-feira): o
canvas de canal do canal principal do staff no Slack. A dash concentra
analytics das atividades, resumo da ultima reuniao, action items, lembretes e
pauta — o acompanhamento e feito nela (nao ha mais documento Word).

Fontes e papeis:

1. **Lista "Action Plan - Staff C-level"** — fonte unica das atividades
   (colunas: pendencia, responsavel, data_prevista, status
   aberto/fazendo/concluido, comentario). Localizada PELO NOME em tempo de
   execucao (`lista_garantir` cria e compartilha se nao existir; override:
   `SLACK_LIST_NAME`/`SLACK_LIST_ID`). O time cria as acoes e atualiza
   status/comentario DIRETO na lista; o agente so cria itens quando
   explicitamente pedido e NUNCA altera itens existentes.
2. **Dash (canvas de canal)** — atualizada pelo agente na terca 9h (blocos de
   analytics e espelho de action items) e editada manualmente pelo time nas
   secoes marcadas com ✍️. O historico semanal vive na propria dash (tabela
   que o agente acrescenta linha a linha) — nao ha armazenamento externo.
3. **Rotinas**: segunda 9h (lembrete), terca 9h (atualizacao da dash) e
   diaria 9h (lembretes de vencimento — DM em D-3 e aviso no canal
   #avisos-action-items 1 dia apos vencer).

## Estrutura da dash (canvas de canal)

Secoes, nesta ordem. As marcadas com ✍️ sao MANUAIS — o agente NUNCA as edita.

1. **📊 Analytics** — tres blocos do agente, cada um localizavel por
   `canvas_substituir` com um texto de busca ESTAVEL:
   - Bloco de indicadores (busca: `Não finalizadas (aberto + fazendo):`):
     "🔢 Não finalizadas (aberto + fazendo): N — semana passada: M."
   - Tabela de desempenho individual (busca: `Vencidas`):
     colunas `Pessoa | Abertas | Vencidas | Concluídas`, ordenada por abertas
     desc. Abertas = aberto+fazendo; Vencidas = nao concluidas com data <
     hoje; Concluidas = status concluido. Item multi-responsavel conta para
     cada um; sem responsavel entra como "sem responsável".
   - Tabela de historico (busca: `Concluídas (acum.)`):
     colunas `Semana | Não finalizadas | Concluídas (acum.)` — uma linha por
     terca; o agente ACRESCENTA a linha da semana ao final, preservando as
     anteriores. O "semana passada: M" dos indicadores vem da ULTIMA linha
     existente antes da atualizacao.
2. **📝 Resumo da última reunião** ✍️
3. **✅ Action items** — nota fixa com o link da lista (o espelho e somente
   leitura; edicao ao vivo e na lista) + tabela do agente (busca:
   `Atividade`): colunas `Atividade | Responsável | Data | Status`, apenas
   itens NAO concluidos, ordenados por data prevista crescente (sem data ao
   final); Status como `🔴 Aberto` ou `🟡 Fazendo`; datas dd/mm. Atualizada
   DIARIAMENTE pela rotina de lembretes e na terca pela rotina da dash.
4. **📌 Lembretes** ✍️ — tracking de itens importantes que nao sao action
   items, em tabela manual `Descrição | Responsável | Observações | Data`
   editada livremente pelo time (o agente nao a toca).
5. **📋 Pauta padrão** — estatica (Projetos, Comercial, Financeiro). O agente
   nao edita.
6. **➕ Pauta adicional** ✍️ — o time adiciona itens direto na dash; limpa
   apos a reuniao.

Se um bloco do agente nao for encontrado (alguem apagou), recrie-o com
`canvas_inserir_apos` a partir do titulo da secao correspondente (ex.:
inserir apos o bloco que contem "Analytics") e registre o ocorrido no relato.

## Regras inviolaveis

- **Nunca invente dados, valores, nomes ou prazos** — tudo vem da lista, do
  historico da dash ou do historico de mensagens.
- **Nunca edite as secoes manuais (✍️) nem a Pauta padrão** da dash; nunca
  remova secoes; nunca sobrescreva o historico (apenas acrescente).
- Nunca altere ou apague itens existentes da lista.
- Nomes comerciais: **9fleet** (nunca K.FLEET) e **Roboteazy** (nunca
  K.CONCEPT). Nunca cite "Corsight". Nunca cite Venturus ou SiDi como
  parceiros.
- Portugues do Brasil. Fuso de referencia: America/Sao_Paulo.
- Nunca imprima o valor do token em nenhuma saida.

## Fluxo de execucao (rotina de segunda-feira 9h — lembrete)

Pre-requisitos: `SLACK_BOT_TOKEN` e `SLACK_CHANNEL_ID` exportadas;
ferramentas `curl`, `jq`, `python3`. Rode `pauta-staff/scripts/slack.sh testar`
antes de qualquer outro passo.

1. Rode `./pauta-staff/scripts/slack.sh lista_garantir` e leia a lista com
   `./pauta-staff/scripts/slack.sh lista_itens`. Identifique os responsaveis
   (IDs U...) dos itens com status DIFERENTE de "concluido". Pegue tambem
   `lista_url` e `dash_url`.
2. Poste UMA mensagem avulsa no canal:
   "Bom dia! Preparacao para a reuniao de quarta: (1) atualizem o status e o
   comentario dos seus itens na lista ate hoje as 23:59 — <url da lista>;
   (2) itens de pauta adicional vao direto na secao ➕ da dash — <url da
   dash>. Itens em aberto de: <@ID1> <@ID2> ..." (cada responsavel unico
   mencionado uma vez; item sem responsavel nao gera mencao; se nao houver
   itens abertos, omita a parte "Itens em aberto de:").
3. Nao faca mais nada; encerre reportando o ts da mensagem e quantos
   responsaveis foram mencionados.

## Fluxo de execucao (rotina de terca-feira 9h — atualizacao da dash)

Pre-requisitos: os mesmos de segunda. Rode `pauta-staff/scripts/slack.sh testar`
antes de qualquer outro passo.

1. **Dados**: rode `lista_garantir`; leia `lista_itens` e `usuarios_canal`
   (mapa ID -> primeiro nome). Calcule HOJE (America/Sao_Paulo).
2. **Indicadores**: total de nao finalizadas (aberto + fazendo); por pessoa:
   abertas, vencidas (data_prevista < HOJE e nao concluida), concluidas;
   total de concluidas.
3. **Historico**: `id=$(dash_canvas_id)`; leia
   `./pauta-staff/scripts/slack.sh canvas_conteudo $id` e extraia da tabela de
   historico (a que contem "Concluídas (acum.)") as linhas existentes e o
   numero de nao finalizadas da ULTIMA linha — esse e o M de "semana
   passada". Sem tabela ou sem linhas: M = "sem registro". Nunca calcule M
   por conta propria.
4. **Atualizacao dos 4 blocos** com
   `./pauta-staff/scripts/slack.sh canvas_substituir $id "<busca>" "<markdown>"`:
   (a) indicadores — busca `Não finalizadas (aberto + fazendo):`, novo texto
   com N desta semana e o M do passo 3;
   (b) tabela de desempenho — busca `Vencidas`;
   (c) tabela de historico — busca `Concluídas (acum.)`, TODAS as linhas
   antigas + a linha nova `dd/mm/aaaa | N | concluidas` ao final (se ja
   existir linha com a data de hoje, substitua apenas essa linha em vez de
   duplicar);
   (d) tabela de action items — busca `Atividade`, itens nao concluidos
   conforme "Estrutura da dash".
   Blocos de tabela: o markdown deve ser a tabela COMPLETA (cabecalho +
   linhas). Bloco nao encontrado: recrie conforme "Estrutura da dash".
5. **Verificacao**: releia `canvas_conteudo $id` e confira que (a) os numeros
   dos indicadores batem com a lista, (b) o historico ganhou exatamente uma
   linha (ou substituiu a de hoje), (c) as secoes manuais continuam
   intactas (presenca dos titulos ✍️ e da Pauta padrão).
6. **Aviso no canal**: poste "📊 Dash atualizada para a reuniao de amanha:
   <url da dash>. Nao finalizadas: N (semana passada: M). Pauta adicional e
   resumo: direto na dash."
7. Este fluxo NAO gera arquivos, NAO baixa documentos do canal e NAO envia
   DMs.

## Fluxo de execucao (rotina diaria 9h — lembretes de vencimento)

Pre-requisitos: `SLACK_BOT_TOKEN` e `SLACK_CHANNEL_ID` exportadas; scope
`im:write` (DMs); bot convidado ao canal privado de avisos
"avisos-action-items" (o ID e resolvido em tempo de execucao com
`./pauta-staff/scripts/slack.sh canal_por_nome avisos-action-items`). Rode
`pauta-staff/scripts/slack.sh testar` antes de qualquer outro passo. Esta
rotina roda TODOS os dias, inclusive fins de semana.

1. **Datas**: calcule HOJE, HOJE+3 e ONTEM no fuso America/Sao_Paulo
   (AAAA-MM-DD).
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
   data_prevista == ONTEM (venceram ha 1 dia e continuam nao concluidos),
   poste UMA mensagem consolidada no canal de avisos com
   `./pauta-staff/scripts/slack.sh postar_em <id_do_canal> "<texto>"`:
   "⚠️ Atividades vencidas ontem (dd/mm/aaaa) e ainda nao concluidas:
   • <pendencia> — <@ID> <@ID2>
   Atualizem o status na lista: <url>"
   Item sem responsavel: escreva "sem responsavel" em texto no lugar da
   mencao. Item concluido ate a data da checagem NAO entra no aviso. NAO
   poste no canal principal neste fluxo.
5. **Espelho diario de action items na dash**: independentemente das janelas
   de lembrete, atualize a tabela de action items da dash —
   `id=$(dash_canvas_id)` e
   `./pauta-staff/scripts/slack.sh canvas_substituir $id "Atividade" "<tabela>"`
   com TODOS os itens nao concluidos, no formato definido em "Estrutura da
   dash". Falha aqui nao cancela os lembretes (partes independentes).
6. **Nada nas janelas de lembrete**: nao poste mensagens nem DMs e reporte
   "nada a lembrar hoje" (o espelho do passo 5 e atualizado mesmo assim).
7. As partes sao independentes: se o canal de avisos nao for encontrado
   (bot nao convidado), envie mesmo assim as DMs do passo 3 e o espelho do
   passo 5, e reporte o erro do canal no relato final.
8. Nunca altere a lista. Itens vencidos ha mais de 1 dia (data < ONTEM) NAO
   geram novo aviso — o alerta de vencimento e unico, no dia seguinte ao
   vencimento.

## Pos-reuniao (fora do escopo do agente)

Apos a reuniao de quarta, o time: cola o resumo na secao 📝 da dash; cria as
novas acoes DIRETO na lista (com responsavel e data prevista); atualiza a
secao 📌 Lembretes se preciso; e limpa a secao ➕ Pauta adicional. O agente
nao participa — a dash reflete tudo na terca seguinte. Nao ha mais geracao de
documento Word para o staff; os scripts de DOCX no repo sao legado/uso do
fluxo do conselho.

## Tratamento de erros

- Falha em chamada ao Slack: pare e reporte o erro exato
  (`ERRO Slack: <codigo>`).
- Bloco do agente ausente na dash (lookup vazio): recrie com
  `canvas_inserir_apos` conforme "Estrutura da dash" e registre no relato.
- Historico sem linhas (primeira execucao): use "semana passada: sem
  registro" — nunca invente o numero.
- Dash inexistente (canal sem canvas): pare e reporte — a criacao da dash e
  um ato unico feito fora das rotinas, nao recrie automaticamente.
