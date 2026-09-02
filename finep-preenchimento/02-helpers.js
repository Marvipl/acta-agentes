/*
 * FINEP (ZK) — PASSO 2: helpers de escrita em window.__finep, com verificação.
 *
 * Por que não basta "input.value = x": o ZK guarda o estado no SERVIDOR.
 * Escrever no DOM muda só a tela; o Salvar grava o valor antigo. O valor só
 * sobe quando o ZK dispara onChange (campo de texto) ou onSelect (combobox).
 *
 * Estes helpers tentam três caminhos, nessa ordem, e param no primeiro que
 * comprovadamente colocou um evento no fio:
 *   1. updateChange_() do próprio widget ZK  (o que o ZK faz no blur)
 *   2. blur real no elemento
 *   3. zAu.send explícito de onChange/onSelect
 * A confirmação vem do monitor: só conta como sucesso se um evento com o uuid
 * do campo tiver sido enviado ao servidor.
 *
 * Uso:
 *   __finep.monitorar()
 *   await __finep.diagnosticar('cXAQpj', '1999')   // escreve, verifica, restaura
 */
(() => {
  const F = (window.__finep = window.__finep || {});
  F.eventos = [];

  F.pausa = ms => new Promise(r => setTimeout(r, ms));

  F.ocupado = () => {
    try {
      if (typeof zAu !== 'undefined' && typeof zAu.processing === 'function' && zAu.processing()) return true;
      if (typeof zk !== 'undefined' && zk.processing) return true;
      if (document.querySelector('#zk_showBusy, .z-loading, .z-apply-mask')) return true;
    } catch (e) { /* ignora */ }
    return false;
  };

  F.esperar = async (limite = 20000) => {
    const t0 = Date.now();
    await F.pausa(200);
    while (F.ocupado() && Date.now() - t0 < limite) await F.pausa(120);
    await F.pausa(350);
  };

  F.monitorar = () => {
    if (F._monitorAtivo) return 'monitor já ativo';
    if (typeof zAu === 'undefined') return 'zAu não existe neste contexto (confira o seletor de frame do console)';
    F._sendOriginal = zAu.send;
    zAu.send = function (evt) {
      try {
        const reg = {
          nome: evt && evt.name,
          uuid: evt && evt.target && evt.target.uuid,
          dados: evt && evt.data,
          t: Date.now()
        };
        F.eventos.push(reg);
        if (reg.nome !== 'dummy') console.log('[ZK ->]', reg.nome, reg.uuid, reg.dados);
      } catch (e) { /* ignora */ }
      return F._sendOriginal.apply(this, arguments);
    };
    F._monitorAtivo = true;
    return 'monitor ativo (eventos "dummy" são no-op do ZK e ficam fora do log)';
  };

  F.pararMonitor = () => {
    if (F._sendOriginal) { zAu.send = F._sendOriginal; F._monitorAtivo = false; }
    return 'monitor desligado';
  };

  F.widget = (id) => {
    if (typeof zk === 'undefined' || !zk.Widget) return null;
    try { return zk.Widget.$('#' + String(id).replace(/-real$/, '')) || null; } catch (e) { return null; }
  };

  F.sessaoExpirada = () =>
    /sess[aã]o|session|timeout|expirad/i.test(
      (document.querySelector('.z-messagebox, .z-window-modal') || {}).innerText || ''
    );

  // Eventos relevantes (não-dummy) do uuid dado, enviados depois da marca.
  const relevantes = (marca, uuid) => F.eventos.slice(marca)
    .filter(e => e.nome && e.nome !== 'dummy' && (!uuid || e.uuid === uuid));

  // ---------------------------------------------------------------- texto
  F.escrever = async (id, valor) => {
    const el = document.getElementById(id);
    if (!el) throw new Error('campo não encontrado: ' + id);
    if (el.readOnly || el.disabled) throw new Error('campo somente leitura: ' + id);
    if (!F._monitorAtivo) F.monitorar();

    const wgt = F.widget(id);
    const uuid = wgt && wgt.uuid;
    const original = el.value;
    if (String(valor) === original) {
      return { ok: true, via: 'sem alteração (valor já era esse)', valor: original };
    }

    const marca = F.eventos.length;
    el.scrollIntoView({ block: 'center' });
    el.focus();
    await F.pausa(80);
    el.value = String(valor);
    el.dispatchEvent(new Event('input', { bubbles: true }));

    // caminho 1: o próprio ZK
    if (wgt && typeof wgt.updateChange_ === 'function') {
      try { wgt.updateChange_(); } catch (e) { console.warn('[finep] updateChange_ falhou:', e.message); }
    }
    // caminho 2: blur real
    el.dispatchEvent(new Event('change', { bubbles: true }));
    el.blur();
    await F.esperar();

    let evs = relevantes(marca, uuid);
    let via = evs.length ? 'evento do ZK (' + evs.map(e => e.nome).join(', ') + ')' : null;

    // caminho 3: manda o onChange na unha
    if (!via && wgt && typeof zAu !== 'undefined' && zk.Event) {
      try {
        zAu.send(new zk.Event(wgt, 'onChange', { value: String(valor) }, { toServer: true }));
        await F.esperar();
        evs = relevantes(marca, uuid);
        if (evs.length) via = 'zAu.send explícito';
      } catch (e) { console.warn('[finep] zAu.send explícito falhou:', e.message); }
    }

    const agora = document.getElementById(id);
    return {
      ok: !!via,
      via: via || 'NENHUM evento chegou ao servidor',
      valorNaTela: agora ? agora.value : '(re-renderizado)',
      valorNoWidget: wgt ? wgt._value : undefined,
      eventos: evs.map(e => e.nome)
    };
  };

  // -------------------------------------------------------------- combobox
  F.selecionarCombo = async (idReal, rotulo) => {
    const base = String(idReal).replace(/-real$/, '');
    const cb = F.widget(base);
    if (!cb) throw new Error('combobox não encontrado: ' + base);
    if (!F._monitorAtivo) F.monitorar();

    const btn = document.getElementById(base + '-btn');
    if (btn) { btn.scrollIntoView({ block: 'center' }); btn.click(); await F.pausa(400); }

    const alvo = String(rotulo).trim().toLowerCase();
    const itens = [];
    for (let it = cb.firstChild; it; it = it.nextSibling) {
      if (typeof it.getLabel === 'function') itens.push(it);
    }
    const rotulos = itens.map(i => i.getLabel());
    const escolhido = itens.find(i => i.getLabel().trim().toLowerCase() === alvo)
                   || itens.find(i => i.getLabel().trim().toLowerCase().startsWith(alvo))
                   || itens.find(i => i.getLabel().trim().toLowerCase().includes(alvo));
    if (!escolhido) {
      if (btn) { btn.click(); await F.pausa(150); }
      throw new Error('opção "' + rotulo + '" não existe em ' + base +
        '. Disponíveis: ' + JSON.stringify(rotulos));
    }

    const marca = F.eventos.length;
    const no = escolhido.$n && escolhido.$n();
    if (no) {
      ['mousedown', 'mouseup', 'click'].forEach(t =>
        no.dispatchEvent(new MouseEvent(t, { bubbles: true, cancelable: true, view: window })));
    }
    await F.esperar();

    let evs = relevantes(marca, cb.uuid);
    let via = evs.length ? 'clique no item (' + evs.map(e => e.nome).join(', ') + ')' : null;

    if (!via && typeof cb.setSelectedItem === 'function') {
      try {
        cb.setSelectedItem(escolhido);
        cb.fire('onSelect', { items: [escolhido], reference: escolhido }, { toServer: true });
        await F.esperar();
        evs = relevantes(marca, cb.uuid);
        if (evs.length) via = 'setSelectedItem + fire onSelect';
      } catch (e) { console.warn('[finep] fire onSelect falhou:', e.message); }
    }

    const real = document.getElementById(idReal);
    return {
      ok: !!via,
      via: via || 'NENHUM evento chegou ao servidor',
      valorNaTela: real ? real.value : '(re-renderizado)',
      opcoes: rotulos.length,
      eventos: evs.map(e => e.nome)
    };
  };

  // ------------------------------------------------------------ diagnóstico
  // Escreve um valor DIFERENTE, verifica se o evento subiu, e restaura.
  F.diagnosticar = async (id, valorTeste) => {
    const el = document.getElementById(id);
    if (!el) throw new Error('campo não encontrado: ' + id);
    const combo = /-real$/.test(id);
    const original = el.value;
    if (String(valorTeste) === original) {
      throw new Error('escolha um valor DIFERENTE do atual ("' + original + '"), senão o ZK não dispara nada');
    }
    console.log('[finep] valor original de', id, '=', JSON.stringify(original));
    const ida = combo ? await F.selecionarCombo(id, valorTeste) : await F.escrever(id, valorTeste);
    console.log('[finep] escrita:', ida);

    const elDepois = document.getElementById(id);
    if (elDepois && elDepois.value !== original) {
      const volta = combo ? await F.selecionarCombo(id, original) : await F.escrever(id, original);
      console.log('[finep] restaurado:', volta);
    } else {
      console.warn('[finep] não restaurei automaticamente — confira o campo na tela');
    }
    console.log(ida.ok
      ? '[finep] VEREDITO: o mecanismo funciona (via ' + ida.via + ')'
      : '[finep] VEREDITO: nada chegou ao servidor — precisamos de Playwright');
    return ida;
  };

  F.inputsVisiveis = () => [...document.querySelectorAll('input')]
    .filter(e => e.type !== 'hidden' && e.id && (e.offsetParent || e.getClientRects().length));

  console.log('helpers em window.__finep: monitorar, diagnosticar, escrever, selecionarCombo, esperar, inputsVisiveis');
})();
