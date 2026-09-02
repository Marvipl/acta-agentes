/*
 * FINEP (ZK) — PASSO 3: preenche os membros da equipe.
 * Requer, na mesma aba e nesta ordem: 02-helpers.js e depois dados-equipe.js
 * (que define window.EQUIPE_FINEP).
 *
 * PROVISORIO: a constante ORDEM abaixo foi inferida dos valores que ja estavam
 * no formulario, nao dos rotulos. Confirme com a saida do 01-mapear.js antes de
 * rodar com DRY_RUN = false.
 *
 * O script NAO clica em "Proximo Passo" nem em nada que submeta a proposta.
 */
(async () => {
  const F = window.__finep;
  if (!F) { console.error('Carregue antes o 02-helpers.js'); return; }

  // ------------------------------------------------------------------ ajustes
  const DRY_RUN = true;              // true = so simula e loga; nao escreve nada
  const ID_BOTAO_ADICIONAR = '';     // ex.: 'cXAQug' — confirmar qual das duas tabelas
  const ID_BOTAO_SALVAR = '';        // ex.: 'cXAQn2'
  const SALVAR_A_CADA = 1;           // salva a cada N membros (0 = nao salvar)

  // Ordem dos campos DENTRO de um bloco de membro, e o tipo de cada um.
  // 'texto' = input comum; 'combo' = dropdown ZK (id termina em -real).
  const ORDEM = [
    ['cpf',                'texto'],
    ['nome',               'texto'],
    ['sexo',               'combo'],
    ['titulacao',          'combo'],
    ['instituicaoTitulacao', 'texto'],
    ['anoTitulacao',       'texto'],
    ['areaFormacao',       'texto'],
    ['empresa',            'combo'],
    ['vinculo',            'combo'],
    ['funcaoNoProjeto',    'combo'],
    ['nivel',              'combo'],
    ['horas',              'texto'],
    ['meses',              'texto'],
    ['atividades',         'texto'],
    ['email',              'texto'],
    ['telefone',           'texto'],
    ['linkedin',           'texto']
  ];
  // ---------------------------------------------------------------------------

  const DADOS = window.EQUIPE_FINEP;
  if (!Array.isArray(DADOS) || !DADOS.length) {
    console.error('window.EQUIPE_FINEP vazio. Carregue o dados-equipe.js primeiro.');
    return;
  }
  if (!DRY_RUN && (!ID_BOTAO_ADICIONAR || !document.getElementById(ID_BOTAO_ADICIONAR))) {
    console.error('ID_BOTAO_ADICIONAR nao configurado ou nao encontrado na pagina.');
    return;
  }

  const log = (...a) => console.log('[finep]', ...a);

  // Cria um bloco novo e devolve os inputs que apareceram, em ordem de documento.
  const abrirBlocoNovo = async () => {
    const antes = new Set(F.inputsVisiveis().map(e => e.id));
    document.getElementById(ID_BOTAO_ADICIONAR).click();
    await F.esperar();
    let novos = F.inputsVisiveis().filter(e => !antes.has(e.id));
    if (novos.length === ORDEM.length) return novos;
    // O ZK pode re-renderizar a secao inteira e trocar todos os uuids.
    if (novos.length > ORDEM.length && novos.length % ORDEM.length === 0) {
      log('secao re-renderizada (' + novos.length + ' campos); usando o ultimo bloco');
      return novos.slice(-ORDEM.length);
    }
    throw new Error('esperava ' + ORDEM.length + ' campos novos, apareceram ' + novos.length +
      '. Ids: ' + JSON.stringify(novos.map(e => e.id)));
  };

  const preencherBloco = async (inputs, membro, rotulo) => {
    for (let i = 0; i < ORDEM.length; i++) {
      const [chave, tipo] = ORDEM[i];
      const valor = membro[chave];
      const el = inputs[i];
      if (valor === undefined || valor === null || valor === '') { log(rotulo, chave, '(vazio, pulado)'); continue; }
      if (!el) { log(rotulo, chave, 'SEM CAMPO na posicao ' + i); continue; }
      if (DRY_RUN) { log(rotulo, i, chave, '->', el.id, '=', valor, '(dry-run)'); continue; }
      try {
        const res = tipo === 'combo'
          ? await F.selecionarCombo(el.id, valor)
          : await F.escrever(el.id, valor);
        log(rotulo, chave, '=', res);
      } catch (e) {
        console.error('[finep]', rotulo, chave, 'FALHOU:', e.message);
        throw e;                                   // para na primeira falha
      }
      if (F.sessaoExpirada()) throw new Error('sessao do ZK expirou — recarregue e faca login de novo');
    }
  };

  F.monitorar();
  log(DRY_RUN ? 'MODO SIMULACAO — nada sera escrito' : 'preenchendo de verdade',
      '| membros:', DADOS.length);
  log('para interromper a qualquer momento: __finep.parar()');

  F.retomar();   // limpa um aborto anterior
  for (let m = 0; m < DADOS.length; m++) {
    F.checarAborto();
    const rotulo = 'membro ' + (m + 1) + '/' + DADOS.length +
      ' (' + (DADOS[m].nome || '?') + ')';
    let inputs;
    if (DRY_RUN) {
      log(rotulo, '- simulando: clicaria em #' + ID_BOTAO_ADICIONAR + ' e preencheria');
      inputs = ORDEM.map(() => null);
    } else {
      inputs = await abrirBlocoNovo();
    }
    await preencherBloco(inputs, DADOS[m], rotulo);
    if (!DRY_RUN && SALVAR_A_CADA && (m + 1) % SALVAR_A_CADA === 0 && ID_BOTAO_SALVAR) {
      document.getElementById(ID_BOTAO_SALVAR).click();
      await F.esperar();
      log('salvo apos', rotulo);
    }
  }
  log('fim. Confira na tela, rode "Verificar pendencias" e avance manualmente.');
})();
