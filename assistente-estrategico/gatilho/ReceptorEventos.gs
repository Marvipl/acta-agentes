/**
 * ReceptorEventos.gs — disparo em TEMPO REAL, sem servidor (Modo A2).
 *
 * Vive no MESMO projeto Apps Script de DispararAssistente.gs. Publicado como
 * WEB APP, vira a Request URL da Events API do Slack: quando uma mensagem é
 * postada no canal #estrategia, o Slack chama esta URL na hora (push, sem
 * polling) e o script dispara a rotina de perguntas & respostas pelo gatilho
 * de API. Detecção em segundos; o Google hospeda a URL gratuitamente.
 *
 * Configuração (além das Propriedades do Script já usadas pelo poller —
 * SLACK_CHANNEL_ID, ROUTINE_FIRE_URL, ROUTINE_FIRE_TOKEN):
 *
 * 1. Implantar > Nova implantação > App da Web:
 *    "Executar como: eu" e "Quem pode acessar: Qualquer pessoa".
 *    Copie a URL /exec gerada.
 * 2. No app do Slack (api.slack.com/apps -> actabot):
 *    - Socket Mode DESATIVADO (com ele ligado, os eventos não vão para URL);
 *    - Event Subscriptions -> Enable Events -> Request URL = URL do web app
 *      (o Slack envia um desafio url_verification; este doPost responde);
 *    - Subscribe to bot events: message.groups (canal privado) e
 *      message.channels. Reinstalar o app.
 * 3. Com o A2 ativo, mude o acionador do poller (DispararAssistente.gs) de
 *    1 minuto para 10 minutos — ele vira reserva caso o Slack desative a
 *    entrega de eventos (faz isso se a URL falhar com frequência).
 *
 * Notas:
 * - O Slack exige resposta em ~3s; este handler faz uma única chamada HTTP
 *   (o fire) e responde — normalmente 1-2s. Retries do Slack são deduplicados
 *   por event_id (CacheService).
 * - "Freio" de 45s entre disparos: mensagens em rajada não geram uma execução
 *   da rotina cada — a sessão disparada lê as pendências depois de subir e
 *   cobre o lote inteiro (fluxo idempotente). O que escapar cai no poller.
 * - Eventos de outros canais (o bot está no canal do staff) são ignorados.
 */

function doPost(e) {
  var corpo;
  try {
    corpo = JSON.parse(e.postData.contents);
  } catch (err) {
    return _resposta('bad request');
  }

  // desafio de verificação da Request URL
  if (corpo.type === 'url_verification') {
    return _resposta(corpo.challenge);
  }
  if (corpo.type !== 'event_callback' || !corpo.event) {
    return _resposta('ok');
  }

  var props = PropertiesService.getScriptProperties();
  var canal = props.getProperty('SLACK_CHANNEL_ID');
  var ev = corpo.event;

  // só mensagem humana nova (ou reply humana em thread) no canal de estratégia
  if (ev.type !== 'message' || ev.channel !== canal) return _resposta('ok');
  if (ev.bot_id || ev.subtype) return _resposta('ok');

  var cache = CacheService.getScriptCache();
  if (corpo.event_id) {
    if (cache.get('ev_' + corpo.event_id)) return _resposta('ok'); // retry do Slack
    cache.put('ev_' + corpo.event_id, '1', 600);
  }
  if (cache.get('freio_disparo')) return _resposta('ok'); // rajada: rotina em voo cobre
  cache.put('freio_disparo', '1', 45);

  UrlFetchApp.fetch(props.getProperty('ROUTINE_FIRE_URL'), {
    method: 'post',
    contentType: 'application/json',
    headers: {
      Authorization: 'Bearer ' + props.getProperty('ROUTINE_FIRE_TOKEN'),
      'anthropic-beta': 'experimental-cc-routine-2026-04-01'
    },
    payload: JSON.stringify({
      text: 'Mensagem nova no canal de estrategia. Rode o fluxo de pendencias.'
    }),
    muteHttpExceptions: true // falha do fire não pode virar retry-loop do Slack
  });
  return _resposta('ok');
}

function _resposta(texto) {
  return ContentService.createTextOutput(texto);
}
