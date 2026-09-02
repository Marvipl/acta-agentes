/*
 * FINEP (credito.finep.gov.br, framework ZK) — PASSO 1: mapear o formulario.
 * SOMENTE LEITURA: nao escreve, nao clica, nao salva nada.
 *
 * Uso: abra a tela da equipe, F12 > Console, cole e execute.
 *      Na primeira vez o Chrome bloqueia colar: digite "allow pasting" + Enter.
 * Saida: objeto no console + JSON copiado para a area de transferencia.
 */
(() => {
  const zkOk = typeof zk !== 'undefined' && !!zk.Widget;
  const limpar = s => (s || '').replace(/\s+/g, ' ').trim();
  const visivel = el => !!(el.offsetParent || el.getClientRects().length);

  const widgetDe = (el) => {
    if (!zkOk || !el.id) return null;
    try {
      return zk.Widget.$('#' + el.id.replace(/-real$/, '')) || zk.Widget.$(el) || null;
    } catch (e) { return null; }
  };

  // Le as opcoes de um combobox sem abri-lo. Comboboxes com modelo carregado
  // sob demanda podem devolver lista vazia — nesse caso abra o dropdown na mao
  // uma vez e rode o mapa de novo.
  const opcoesDe = (wgt) => {
    if (!wgt) return undefined;
    const ops = [];
    try {
      for (let it = wgt.firstChild; it; it = it.nextSibling) {
        if (typeof it.getLabel === 'function') ops.push(it.getLabel());
      }
    } catch (e) { return ['<erro ao ler opcoes: ' + e.message + '>']; }
    return ops.length ? ops : undefined;
  };

  // Percorre o DOM em ordem de documento guardando o ultimo texto visto.
  // No ZK o <label> nao esta associado ao <input>, entao o texto imediatamente
  // anterior e a melhor aproximacao do rotulo do campo.
  const campos = [];
  let ultimoTexto = '';
  let ordem = 0;
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT);
  while (tw.nextNode()) {
    const n = tw.currentNode;
    if (n.nodeType === Node.TEXT_NODE) {
      const t = limpar(n.textContent);
      if (t) ultimoTexto = t;
      continue;
    }
    if (!/^(INPUT|SELECT|TEXTAREA)$/.test(n.tagName) || n.type === 'hidden') continue;
    const wgt = widgetDe(n);
    campos.push({
      ordem: ordem++,
      id: n.id || '(sem id)',
      tag: n.tagName.toLowerCase(),
      tipo: n.type || '',
      widgetZK: wgt ? (wgt.className || wgt.widgetName || '?') : '(sem widget ZK)',
      rotuloProvavel: ultimoTexto,
      valorAtual: limpar(n.value).slice(0, 60),
      somenteLeitura: !!(n.readOnly || n.disabled),
      visivel: visivel(n),
      maxlength: n.maxLength > 0 ? n.maxLength : undefined,
      opcoes: opcoesDe(wgt)
    });
  }

  const botoes = [...document.querySelectorAll(
    'button, .z-button, .z-toolbarbutton, input[type=button], input[type=submit], a[onclick]'
  )].map(b => ({ id: b.id || '', texto: limpar(b.innerText || b.value), visivel: visivel(b) }))
    .filter(b => b.texto);

  const saida = {
    url: location.href,
    zk: zkOk
      ? { versao: zk.version, desktop: (zk.Desktop && zk.Desktop.$() ? zk.Desktop.$().id : '?') }
      : '(ZK nao detectado nesta pagina)',
    totalCampos: campos.length,
    campos,
    botoes
  };
  console.log(saida);
  try {
    copy(JSON.stringify(saida, null, 2));
    console.log('Mapa copiado para a area de transferencia. Campos: ' + campos.length);
  } catch (e) {
    console.log('Nao consegui copiar; copie o objeto acima com botao direito > Copy object.');
  }
})();
