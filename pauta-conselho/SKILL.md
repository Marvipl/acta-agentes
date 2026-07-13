---
name: pauta-conselho
description: Gera a minuta mensal da pauta da Reunião do Conselho Consultivo da Acta Robotics, consolidando a última pauta/ata de conselho, as atas de Staff C-Level desde então e os itens adicionais coletados no Slack, e envia para validação humana. Use sempre que a tarefa envolver criar ou publicar a pauta do conselho da Acta Robotics.
---

# Pauta do Conselho Consultivo — Acta Robotics

> Este agente vive em `pauta-conselho/` dentro do repo `acta-agentes` e REUTILIZA
> a caixa de ferramentas de `pauta-staff/scripts/` (slack.sh, gerar_pauta.py,
> ler_docx.py, validar_pauta.py, achar_pauta_anterior.sh). Todos os caminhos
> abaixo sao relativos a RAIZ do repositorio.

## O que este skill faz

Gera a MINUTA da pauta da reuniao mensal do Conselho Consultivo e a publica no
canal do Slack **para validacao humana** — a pauta NAO e final: a mensagem de
publicacao pede explicitamente que o time confira e ajuste manualmente.

Fontes, em ordem de uso:

1. **Ultima pauta/ata de CONSELHO** consolidada no canal (validada pelo conteudo
   — titulo contendo CONSELHO + data interna) → alimenta a secao "Pendencias da
   Reuniao Anterior" (tabela de Proximos Passos + itens de deliberacao em aberto)
   e a lista de participantes.
2. **Todas as pautas/atas de STAFF C-Level** com data posterior a ultima reuniao
   de conselho → alimentam as secoes de Projetos, Comercial/Pipeline, Captacao,
   Parcerias e Financeiro, por consolidacao do que esta escrito nelas.
3. **Itens adicionais do Slack**: respostas na thread da mensagem de coleta de
   segunda-feira + mensagens do canal que mencionem "conselho" no periodo entre
   a ultima reuniao de conselho e segunda-feira 23:59 (America/Sao_Paulo).

## Estrutura obrigatoria do documento

Template: `pauta-conselho/templates/Template_Pauta_Conselho.docx` (rodape ja diz
"Conselho Consultivo"). Gere SEMPRE com `pauta-staff/scripts/gerar_pauta.py` —
nunca escreva o DOCX manualmente.

Titulo "PAUTA DE REUNIÃO" + subtitulo "CONSELHO CONSULTIVO".

Tabela de informacoes: Reuniao = "Reunião Ordinária do Conselho Consultivo";
Data = "[ __ ] / MM / AAAA" do mes corrente (placeholder — a data exata e
confirmada na validacao); Horario = "[15h às 17h]"; Local / Formato =
"(    ) Presencial    (    ) Remoto"; Secretariado por = "Diego Nunes".

Participantes (ordem fixa, salvo alteracao na ultima pauta de conselho):
Marcus Lima (CEO), Vinicius Bastos (CTO), Renato Correa (CFO), Diego Nunes
(Secretário), Menotti Franceschini (Conselheiro externo), Julio Oliveira
(Conselheiro externo), Erick Sighn (S2 Investimentos).

Secoes, nesta ordem:

1. **Pendencias da Reuniao Anterior (DD/MM/AAAA)** — data da ultima reuniao de
   conselho no titulo. Bullets, um por acao da tabela "Proximos Passos" da
   pauta/ata anterior, no formato `Acao (Responsavel): status.` O status vem
   das atas de staff quando localizavel; caso contrario, "status a reportar."
2. **Status dos Projetos** — blocos por projeto (FINEP/CPQD/Social/HBR,
   ANP/STREAM, Meta Industria, FAPEAM etc.), consolidando o que as atas de
   staff do periodo dizem. Bloco sem informacao no periodo nao entra.
3. **Pipeline Comercial** — funis (Acta e JV-S2) com os valores MAIS RECENTES
   encontrados nas atas de staff, ganhos/perdidos do periodo, oportunidades em
   andamento, eventos.
4. **Captacao e Estrutura Societaria** — investidores e estruturas em
   negociacao citados nas atas do periodo.
5. **Parcerias Estrategicas e Novos Negocios** — parcerias citadas no periodo.
6. **Financeiro e Caixa** — posicao mais recente citada nas atas do periodo;
   valores sem fonte viram "[a apresentar pelo CFO]".
7. **Pauta Adicional** — SOMENTE SE houver itens coletados (thread + mencoes a
   "conselho"). Um bullet por item: `[Nome]: item.` Sem itens, a secao nao
   aparece e Proximos Passos assume o numero 7.
8. **Proximos Passos** — tabela # | Acao | Responsavel | Prazo com 5 linhas
   vazias, com quebra de pagina antes.

Fecha com "Encerramento e Aprovacao" e assinaturas: Marcus Lima (CEO), Vinicius
Bastos (CTO), Renato Correa (CFO), Menotti Franceschini (Conselheiro externo),
Julio Oliveira (Conselheiro externo), Erick Sighn (S2 Investimentos).

Marque itens de deliberacao com prefixo em negrito "Deliberar: " APENAS quando a
ata de staff de origem sinalizar explicitamente uma decisao pendente
(ex.: "Deliberar", "decisao pendente", "a definir pelo conselho"). Nunca crie
itens de deliberacao por inferencia propria.

## Regras inviolaveis de conteudo

- **Nunca invente dados, valores, nomes, prazos ou conclusoes.** Toda afirmacao
  das secoes 2-6 precisa existir em alguma ata de staff do periodo ou na pauta
  de conselho anterior. Informacao ausente vira placeholder entre colchetes.
- Em conflito entre atas de staff, prevalece a de data mais recente; se o
  conflito for relevante (ex.: valores diferentes de funil), registre apenas o
  mais recente.
- Nomes comerciais: **9fleet** (nunca K.FLEET) e **Roboteazy** (nunca
  K.CONCEPT). Nunca cite "Corsight". Nunca cite Venturus ou SiDi como parceiros.
- Sem emojis no documento. Portugues do Brasil, tom de registro impessoal.
- Acentuacao correta no DOCX final (este arquivo esta sem acentos apenas por
  seguranca de encoding).
- Fuso de referencia: America/Sao_Paulo.

## Fluxo de execucao (rotina de terca-feira apos a 1a segunda do mes)

Pre-requisitos: variaveis `SLACK_BOT_TOKEN` e `SLACK_CHANNEL_ID` no ambiente da
rotina; rede liberada para slack.com e files.slack.com; `curl`, `jq`, `python3`.
Rode `pauta-staff/scripts/slack.sh testar` antes de qualquer outro passo.
Nunca imprima o valor do token.

1. **Janela de coleta**: calcule segunda-feira (ontem) 09:00 e 23:59
   (America/Sao_Paulo) com `pauta-staff/scripts/slack.sh ts "YYYY-MM-DD HH:MM"`.
2. **Fontes**: rode `pauta-conselho/scripts/coletar_fontes.sh <hoje_ISO>`.
   O script devolve JSON com a ultima pauta/ata de conselho
   (/tmp/conselho_anterior.docx) e a lista de atas de staff do periodo
   (/tmp/staff_fonte_*.docx). Leia cada arquivo com
   `python3 pauta-staff/scripts/ler_docx.py <arquivo>`.
3. **Itens adicionais**: (a) localize no historico a mensagem do bot de ontem
   contendo "pauta adicional para a Reunião do Conselho" e leia a thread com
   `slack.sh respostas <ts>`; (b) leia o historico do canal desde a data da
   ultima reuniao de conselho ate segunda 23:59 e selecione mensagens humanas
   que mencionem "conselho" (ignore mensagens do proprio bot e as pautas
   publicadas). Descarte qualquer mensagem apos segunda 23:59.
4. **Montagem**: escreva o JSON de conteudo (esquema no cabecalho de
   `pauta-staff/scripts/gerar_pauta.py`; exemplo em
   `pauta-conselho/exemplos/pauta_conselho_exemplo.json`). `footer_data` =
   "[__]/MM/AAAA" nao e aceito pelo rodape — use a data placeholder do primeiro
   dia util previsto ou omita `footer_data` para manter o rodape do template.
5. **Geracao**: `python3 pauta-staff/scripts/gerar_pauta.py --template
   pauta-conselho/templates/Template_Pauta_Conselho.docx --json /tmp/conteudo.json
   --out /tmp/Pauta_Conselho_AAAA-MM.docx` (ano-mes da reuniao no nome).
6. **Verificacao antes de publicar**: `ler_docx.py` no arquivo gerado e confira:
   (a) toda resposta valida da thread e toda mencao a "conselho" virou item da
   Pauta Adicional ou de uma secao tematica; (b) cada afirmacao das secoes 2-6
   tem origem nas fontes; (c) as pendencias da reuniao anterior estao completas;
   (d) `validar_pauta.py --tipo conselho` retorna `titulo_ok: true` — a data
   pode (e deve) estar como placeholder na minuta. Isso e intencional: a minuta
   nao validada fica com `valido: false` por falta de data real e, por isso,
   NUNCA sera escolhida pelo coletar_fontes.sh do mes seguinte como pauta de
   conselho oficial; apenas a versao final, com a data preenchida pelo time,
   vira referencia.
7. **Publicacao**: `slack.sh enviar_arquivo` com o comentario:
   "Minuta da pauta do Conselho de <mês>. Por favor, validem as informações e
   ajustem manualmente o que for necessário antes do envio aos conselheiros —
   em especial a data da reunião e os valores marcados entre colchetes.
   Respondam nesta thread com correções."
8. **Sem pauta de conselho anterior no canal** (exit 3 do coletar_fontes.sh):
   gere a minuta apenas com as atas de staff dos ultimos 45 dias e os itens
   coletados, com a secao 1 contendo a linha "[sem pauta de conselho anterior
   no canal]", e avise no comentario de publicacao.

## Pos-publicacao (fora do escopo do agente)

O time valida, edita manualmente e publica a versao final no canal. Essa versao
final (mantendo o titulo CONSELHO CONSULTIVO e a linha "Data" com a DATA REAL
preenchida) sera a referencia de pendencias do mes seguinte — sem data real, o
arquivo e ignorado pelo coletor.

## Tratamento de erros

- Falha em chamada ao Slack: pare e reporte o erro exato.
- Nunca publique um arquivo que nao passou pela verificacao do passo 6.
- Motivos de descarte de candidatos saem no stderr do coletar_fontes.sh —
  inclua-os no log da execucao.
