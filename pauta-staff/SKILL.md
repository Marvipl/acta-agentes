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

1. **Pendencias da Semana Anterior** — extraidas do ultimo arquivo de pauta/ata
   disponivel no canal do Slack (tabela de pendencias + tabela de plano de acao).
   Este e o UNICO uso do arquivo anterior.
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

1. **Pendencias da Semana Anterior** — nota "Follow-up das acoes da reuniao
   anterior." + tabela Responsavel | Pendencia | Prazo. Conteudo: uniao das
   linhas da tabela de pendencias e da tabela de plano de acao do arquivo
   anterior (sem duplicatas; campo vazio vira "—"). Se nao houver arquivo
   anterior, uma linha unica: ["—", "[sem arquivo de referencia no canal]", "—"].
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

## Fluxo de execucao (rotina de terca-feira 9h)

Pre-requisitos no ambiente: `SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID`, `curl`,
`jq`, `python3`.

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
4. **Pendencias**: localize o arquivo da ULTIMA reuniao com
   `./pauta-staff/scripts/achar_pauta_anterior.sh <data_da_proxima_quarta_ISO> /tmp/anterior.docx`.
   O script baixa os .docx recentes do canal e valida cada um PELO CONTEUDO
   (titulo contendo Staff/C-Level + linha "Data" interpretavel, via
   `pauta-staff/scripts/validar_pauta.py`), escolhendo o de data interna mais recente
   anterior a proxima reuniao — nunca confie apenas no nome ou na ordem de
   upload. Depois `python3 pauta-staff/scripts/ler_docx.py /tmp/anterior.docx` e extraia
   APENAS as linhas das tabelas "Responsavel | Pendencia | Prazo" e
   "# | Acao | Responsavel | Prazo" (ignorando linhas vazias e cabecalhos).
   Nao leia nem use o restante do documento.
5. **Montagem**: escreva o JSON de conteudo seguindo `pauta-staff/exemplos/pauta_exemplo.json`
   (esquema completo no cabecalho de `pauta-staff/scripts/gerar_pauta.py`). Inclua
   `footer_data` com a data da reuniao (dd/mm/aaaa).
6. **Geracao**: `python3 pauta-staff/scripts/gerar_pauta.py --template
   pauta-staff/templates/Template_Ata_Staff.docx --json /tmp/conteudo.json --out
   /tmp/Pauta_Staff_AAAA-MM-DD.docx` (data da quarta-feira no nome).
7. **Verificacao antes de publicar**: rode `python3 pauta-staff/scripts/ler_docx.py` no
   arquivo gerado e confira: (a) toda resposta valida da thread virou item da
   Pauta Adicional, (b) as pendencias do arquivo anterior estao na tabela,
   (c) as secoes 2-4 contem apenas o texto generico fixo, (d) a data esta correta.
8. **Publicacao**: `./pauta-staff/scripts/slack.sh enviar_arquivo /tmp/Pauta_Staff_....docx
   "Pauta da reuniao de quarta-feira <data>. Itens de ultima hora podem ser
   levados diretamente na reuniao."`
9. **Sem respostas na thread**: gere a pauta sem a secao Pauta Adicional e
   informe no comentario de publicacao: "Nenhum item adicional foi enviado
   nesta semana."

## Pos-reuniao (fora do escopo do agente)

O detalhamento das secoes Projetos, Comercial e Financeiro e preenchido
manualmente pelo time com base no que foi discutido, e a ata final e enviada ao
canal pelo proprio time. O agente nao participa dessa etapa — mas o arquivo
enviado manualmente sera a fonte de pendencias da semana seguinte, desde que o
documento mantenha o titulo Staff C-Level e a linha "Data" no padrao atual
(a selecao e feita pelo conteudo do arquivo, nao pelo nome).

## Tratamento de erros

- Falha em chamada ao Slack: pare e reporte o erro exato (`ERRO Slack: <codigo>`).
- `achar_pauta_anterior.sh` com exit 3 (nenhum candidato valido): siga a regra
  da secao 1 (linha placeholder) e avise no comentario de publicacao. Os motivos
  de descarte de cada candidato saem no stderr do script — inclua-os no log.
- Nunca publique um arquivo que nao passou pela verificacao do passo 7.
