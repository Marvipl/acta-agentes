/*
 * FINEP (ZK) — PASSO 2: instala os helpers de escrita em window.__finep
 * e um monitor do trafego cliente->servidor do ZK.
 *
 * Por que nao basta "input.value = x": o ZK e um framework de estado no
 * SERVIDOR. Escrever no DOM muda so a tela; o servidor continua com o valor
 * antigo e o Salvar grava o antigo. O valor so viaja quando o ZK dispara o
 * evento onChange/onSelect — e isso acontece no blur (campo de texto) ou no
 * clique no item do dropdown (combobox). E o que estes helpers fazem.
 *
 * Uso: cole no console. Depois, para conferir o mecanismo em UM campo:
 *   __finep.monitorar()
 *   await __finep.escrever('cXAQpj', '2021')          // campo de texto
 *   await __finep.selecionarCombo('cXAQzi-real', 'Feminino')   // dropdown
 * Se o monitor logar "[ZK ->] onChange ..." o valor chegou ao servidor.
 */
(() => {
  const F = (window.__finep = window.__finep || {});

  F.pausa = ms => new Promise(r => setTimeout(r, ms));

  F.ocupado = () => {
    try {
      if (typeof zAu !== 'undefined' && typeof zAu.processing === 'function' && zAu.processing()) return true;
      if (typeof zk !== 'undefined' && zk.processing) return true;
      if (document.querySelector('#zk_showBusy, .z-loading, .z-apply-mask')) return true;
    } catch (e) { /* ignora */ }
    return false;
  };

  // Espera o ZK terminar o round-trip e o DOM re-renderizado assentar.
  F.esperar = async (limite = 20000) => {
    const t0 = Date.now();
    await F.pausa(200);                 // deixa o evento sair
    while (F.ocupado() && Date.now() - t0 < limite) await F.pausa(120);
    await F.pausa(350);                 // assenta o DOM
    if (Date.now() - t0 >= limite) console.warn('[finep] timeout esperando o ZK responder');
  };

  F.monitorar = () => {
    if (F._monitorAtivo) return 'monitor ja ativo';
    if (typeof zAu === 'undefined') return 'zAu nao existe nesta pagina';
    F._sendOriginal = zAu.send;
    zAu.send = function (evt) {
      try {
        console.log('[ZK ->]', evt && evt.name,
          evt && evt.target && evt.target.uuid, evt && evt.data);
      } catch (e) { /* ignora */ }
      return F._sendOriginal.apply(this, arguments);
    };
    F._monitorAtivo = true;
    return 'monitor ativo: todo evento enviado ao servidor sera logado';
  };

  F.pararMonitor = () => {
    if (F._sendOriginal) { zAu.send = F._sendOriginal; F._monitorAtivo = false; }
    return 'monitor desligado';
  };

  F.sessaoExpirada = () =>
    /sess[aã]o|session|timeout|expirad/i.test(
      (document.querySelector('.z-messagebox, .z-window-modal') || {}).innerText || ''
    );

  // Campo de texto (zul.inp.Textbox / Intbox / Decimalbox).
  F.escrever = async (id, valor) => {
    const el = document.getElementById(id);
    if (!el) throw new Error('campo nao encontrado: ' + id);
    if (el.readOnly || el.disabled) throw new Error('campo somente leitura: ' + id);
    el.scrollIntoView({ block: 'center' });
    el.focus();
    await F.pausa(80);
    el.value = String(valor);
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
    el.blur();                          // e o blur que faz o ZK mandar onChange
    await F.esperar();
    const depois = document.getElementById(id);
    return depois ? depois.value : '(campo re-renderizado pelo servidor)';
  };

  // Combobox do ZK: o input real e "<uuid>-real", o botao "<uuid>-btn".
  // Abrimos o dropdown (alguns carregam os itens so nesse momento), achamos
  // o item pelo rotulo e clicamos nele como um usuario faria.
  F.selecionarCombo = async (idReal, rotulo) => {
    const base = idReal.replace(/-real$/, '');
    const cb = (typeof zk !== 'undefined' && zk.Widget) ? zk.Widget.$('#' + base) : null;
    if (!cb) throw new Error('combobox nao encontrado: ' + base);

    const btn = document.getElementById(base + '-btn');
    if (btn) { btn.scrollIntoView({ block: 'center' }); btn.click(); await F.pausa(400); }

    const alvo = String(rotulo).trim().toLowerCase();
    const itens = [];
    for (let it = cb.firstChild; it; it = it.nextSibling) {
      if (typeof it.getLabel === 'function') itens.push(it);
    }
    const rotulos = itens.map(i => i.getLabel());
    let escolhido = itens.find(i => i.getLabel().trim().toLowerCase() === alvo)
                 || itens.find(i => i.getLabel().trim().toLowerCase().startsWith(alvo))
                 || itens.find(i => i.getLabel().trim().toLowerCase().includes(alvo));

    if (!escolhido) {
      if (btn) { btn.click(); await F.pausa(150); }   // fecha o dropdown
      throw new Error('opcao "' + rotulo + '" nao existe em ' + base +
        '. Disponiveis: ' + JSON.stringify(rotulos));
    }

    const no = escolhido.$n && escolhido.$n();
    if (no) {
      ['mousedown', 'mouseup', 'click'].forEach(t =>
        no.dispatchEvent(new MouseEvent(t, { bubbles: true, cancelable: true, view: window })));
    } else if (typeof cb.setSelectedItem === 'function') {
      cb.setSelectedItem(escolhido);
      cb.fire('onSelect', { items: [escolhido], reference: escolhido }, { toServer: true });
    } else {
      throw new Error('nao consegui selecionar em ' + base + ' (sem no DOM e sem setSelectedItem)');
    }
    await F.esperar();
    const real = document.getElementById(idReal);
    return real ? real.value : '(re-renderizado)';
  };

  // Lista os inputs preenchiveis na ordem do documento — base da deteccao de blocos.
  F.inputsVisiveis = () => [...document.querySelectorAll('input')]
    .filter(e => e.type !== 'hidden' && e.id && (e.offsetParent || e.getClientRects().length));

  console.log('helpers instalados em window.__finep:',
    'monitorar, pararMonitor, escrever, selecionarCombo, esperar, inputsVisiveis');
})();
