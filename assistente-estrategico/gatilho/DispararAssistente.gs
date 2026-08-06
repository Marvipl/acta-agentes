/**
 * DispararAssistente.gs — gatilho do Assistente Estratégico SEM SERVIDOR.
 *
 * Roda no Google Apps Script (script.google.com) com acionador temporizado a
 * cada 1 minuto. A cada tique, verifica se há mensagem humana nova no canal
 * #estrategia (inclusive follow-up em thread); havendo, dispara via API a
 * rotina de perguntas & respostas do Claude Code (gatilho de API da rotina).
 * A rotina é idempotente (só responde o que ainda não foi respondido), então
 * um disparo a mais não gera resposta duplicada.
 *
 * Configuração — Propriedades do Script (Configurações do projeto):
 *   SLACK_BOT_TOKEN     token do bot (xoxb-...)
 *   SLACK_CHANNEL_ID    ID do canal #estrategia (C...)
 *   ROUTINE_FIRE_URL    URL do gatilho de API da rotina
 *                       (claude.ai/code/routines -> rotina -> Add API trigger)
 *   ROUTINE_FIRE_TOKEN  bearer token gerado junto com o gatilho de API
 *
 * Acionador: Editor > Acionadores > adicionar > dispararSeHouverNovidade,
 * baseado em tempo, a cada 1 minuto.
 *
 * Observação: o gatilho de API de rotinas é BETA (header
 * anthropic-beta: experimental-cc-routine-2026-04-01) — se o disparo passar a
 * falhar, confira o formato atual em code.claude.com/docs/en/routines.
 */

function dispararSeHouverNovidade() {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(5000)) return; // tique anterior ainda rodando

  try {
    var props = PropertiesService.getScriptProperties();
    var slackToken = props.getProperty('SLACK_BOT_TOKEN');
    var canal = props.getProperty('SLACK_CHANNEL_ID');
    var fireUrl = props.getProperty('ROUTINE_FIRE_URL');
    var fireToken = props.getProperty('ROUTINE_FIRE_TOKEN');
    if (!slackToken || !canal || !fireUrl || !fireToken) {
      throw new Error('Propriedades do script faltando (SLACK_BOT_TOKEN, SLACK_CHANNEL_ID, ROUTINE_FIRE_URL, ROUTINE_FIRE_TOKEN)');
    }

    // cursor: último ts (de mensagem ou reply) já considerado
    var ultimo = props.getProperty('ULTIMO_TS') ||
      String(Math.floor(Date.now() / 1000) - 300) + '.000000';

    var resp = UrlFetchApp.fetch(
      'https://slack.com/api/conversations.history?channel=' + canal +
        '&oldest=' + ultimo + '&limit=100',
      { headers: { Authorization: 'Bearer ' + slackToken } }
    );
    var dados = JSON.parse(resp.getContentText());
    if (!dados.ok) throw new Error('Slack: ' + dados.error);

    var maisRecente = ultimo;
    var temNovidade = false;
    var msgs = dados.messages || [];

    for (var i = 0; i < msgs.length; i++) {
      var m = msgs[i];
      var efetivo = (m.latest_reply && m.latest_reply > m.ts) ? m.latest_reply : m.ts;
      if (efetivo > maisRecente) maisRecente = efetivo;

      // mensagem nova de humano no canal
      if (!m.bot_id && !m.subtype && m.ts > ultimo) {
        temNovidade = true;
      }
      // reply nova em thread: só conta se a ÚLTIMA mensagem da thread é humana
      // (reply do próprio bot também avança latest_reply e não deve redisparar)
      if (!temNovidade && m.latest_reply && m.latest_reply > ultimo &&
          _ultimaDaThreadEhHumana(slackToken, canal, m.ts)) {
        temNovidade = true;
      }
    }

    // conversations.history não devolve o pai quando só a reply é nova e o pai
    // é anterior à janela — cobre-se com oldest curto o suficiente (o cursor
    // avança a cada tique, então a janela é de ~1 minuto na prática)

    if (temNovidade) {
      UrlFetchApp.fetch(fireUrl, {
        method: 'post',
        contentType: 'application/json',
        headers: {
          Authorization: 'Bearer ' + fireToken,
          'anthropic-beta': 'experimental-cc-routine-2026-04-01'
        },
        payload: JSON.stringify({
          text: 'Atividade nova no canal de estrategia. Rode o fluxo de pendencias.'
        })
      });
      Logger.log('Rotina disparada (novidade até ' + maisRecente + ')');
    }

    // avança o cursor SEMPRE (disparo único por lote; se a execução da rotina
    // falhar, a varredura horária agendada cobre)
    props.setProperty('ULTIMO_TS', maisRecente);
  } finally {
    lock.releaseLock();
  }
}

function _ultimaDaThreadEhHumana(slackToken, canal, threadTs) {
  var resp = UrlFetchApp.fetch(
    'https://slack.com/api/conversations.replies?channel=' + canal +
      '&ts=' + threadTs + '&limit=200',
    { headers: { Authorization: 'Bearer ' + slackToken } }
  );
  var dados = JSON.parse(resp.getContentText());
  if (!dados.ok || !dados.messages || !dados.messages.length) return false;
  var ult = dados.messages[dados.messages.length - 1];
  return !ult.bot_id && !ult.subtype;
}
