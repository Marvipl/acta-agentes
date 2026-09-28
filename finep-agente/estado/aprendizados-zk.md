# Aprendizados do formulário FINEP (ZK)

Arquivo vivo: cada erro que custou uma rodada vira uma linha aqui, para não
custar a segunda. Escrito durante o preenchimento, não depois.

## Como dirigir o navegador quando o MCP não carrega

O MCP do navegador (playwright) só entra no registro na **inicialização** do
`claude`. Se ele não estiver carregado, não é preciso parar a sessão: o Edge/Chrome
aberto por `abrir-edge.cmd` / `abrir-chrome.cmd` expõe CDP na porta 9222, e
`finep-agente/ferramentas/cdp.ps1` fala esse protocolo direto.

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File finep-agente/ferramentas/cdp.ps1 -Plan plano.json
```

`plano.json` é uma lista de ações executadas em sequência:

| op | campos | o que faz |
|---|---|---|
| `eval` | `js` | roda JS, devolve o valor |
| `evalfile` | `file`, `out?` | roda JS de arquivo (sem inferno de escape); `out` grava o retorno em UTF-8 |
| `click` | `x`, `y` | clique real de mouse (CDP `Input`) |
| `clickSel` | `sel` | rola até o elemento e clica no centro dele |
| `type` / `typefile` | `text` / `file` | `Input.insertText` — um texto de 2000 chars numa tacada |
| `clear` | — | ctrl+a + Delete |
| `key` | `key` | Tab, Enter, Escape, Down, Up, Home |
| `zkidle` | `ms?` | espera `zAu.processing()` zerar — o assentamento do ZK |
| `screenshot` | `file` | PNG da viewport |
| `wait` | `ms` | pausa |

**Por que eventos reais de CDP e não `element.value = ...`:** o ZK escuta eventos
de teclado/mouse do navegador. Valor atribuído por script costuma não disparar o
`onChange` que manda o dado ao servidor — fica na tela e some no round-trip
seguinte. `Input.insertText` + `Tab` (blur) grava de verdade.

## Armadilhas já pagas

- **Caminho de projeto com caixa diferente derruba o MCP.** O servidor estava
  registrado sob `C:/dev/acta-agentes` e a sessão rodava em `C:\Dev\acta-agentes`.
  O Claude Code indexa config por string literal: não enxerga. Corrigir com
  `claude mcp add` a partir do diretório certo, e reiniciar.
- **Caminho com `\` dentro de JSON quebra o `ConvertFrom-Json`.** Usar `/` nos
  caminhos do plano — Windows aceita.
- **`\n` dentro de JS embutido em JSON**: usar `String.fromCharCode(10)` ou
  carregar o JS por `evalfile`. Foi a primeira coisa a falhar.
- **Console do PowerShell mangla acento** (cp850). Para ler texto com acento,
  gravar com `out` e ler o arquivo pelo bash, não pela saída do console.
- **Coordenada de aba envelhece.** Depois de trocar de aba uma vez, as posições
  mudam. Nunca reaproveitar `x,y` entre passos: marcar o elemento por texto
  (`data-alvo`) e usar `clickSel`.

## Como o ZK sinaliza erro (o caminho rápido)

1. `Validar` **troca sozinho para a aba que tem erro** e põe um `!` vermelho no
   cabeçalho dessa aba. Olhar o cabeçalho das abas é mais rápido que caçar
   `errbox` no DOM.
2. O balão laranja ("Verifique os erros marcados na tela") é genérico e some;
   não traz o campo. O `!` da aba traz.
3. Os `errbox` podem não estar no DOM no instante seguinte ao `Validar` —
   não confiar neles como única fonte.

## Fatos do formulário desta chamada

- Limite real do campo **Aderência** é **4000** caracteres, e não 2000 como o
  documento de referência supõe. Conferir o rótulo `(máximo: N caracteres)` na
  tela antes de cortar texto.
- Passo 1 (**Dados Gerais**) tem 3 abas: *Introdução* (só orientações, sem
  campo), *Linha temática/grupo de concorrência* (2 campos) e *Instituições
  participantes* (proponente já preenchido do cadastro, lista de coexecutoras e
  uma caixa de declaração).
- **Os dados do passo 1 travam depois do `Próximo Passo`.** A própria aba avisa:
  alteração posterior só pela opção "Alteração dos dados gerais da proposta" no
  menu lateral. Confirmar com o usuário antes de avançar.
- O submit final chama-se **`Enviar`** (item 10 das orientações). Nunca clicar.
- Etapas depois do passo 1: Dados cadastrais dos partícipes · Descrição do
  Projeto e Equipe Executora · Custos · Cronogramas.

## Extração do .docx de referência

Sem Python na máquina. `finep-agente/ferramentas/` não guarda extrator; o
caminho usado foi descompactar o .docx com `System.IO.Compression.ZipFile` e
percorrer `word/document.xml` em PowerShell.

Quebra de parágrafo dentro de célula sai como ` /  / ` no texto extraído.
Ao preencher, converter: ` /  / ` → linha em branco, ` / ` → quebra simples.
A contagem de caracteres do documento (`[1866/2000 caracteres]`) bateu exatamente
com o que o campo registrou — bom sinal de que a conversão está correta.

## Âncoras: o que é estável e o que não é

- **`title` NÃO é estável entre renderizações.** O mesmo campo apareceu como
  `title="Valor:"` e, depois de um round-trip, como `title="Valor"`. Idem
  `Nome:` / `Nome`. Sempre comparar normalizando: tirar `:` final, NBSP e caixa.
  `ferramentas/js/marca-campo.tpl.js` já faz isso.
- **`title` se repete fora do grid.** O cabeçalho "Nome:" da seção tem o mesmo
  `title` das células "Nome" das linhas. Indexar por ordem de DOM entre títulos
  diferentes desalinha. Ou parear dentro da linha, ou percorrer em ordem de DOM
  usando um campo âncora (`Nº`) para abrir cada linha.
- **`closest('tr')` não sobrevive a re-render**: a árvore muda. Percorrer em
  ordem de DOM com um campo âncora é mais robusto que subir na árvore.
- O marcador de erro do ZK é `.err-ind` (visível). Os `error-box-*` são classes
  de layout, presentes em tudo — não servem para achar erro.

## O overlay "Processando..."

Trocar de passo mostra uma página quase vazia com "Processando...".
`zAu.processing()` já voltou 0 nesse instante — não basta. O `zkidle` do driver
também espera esse texto sumir. Sem isso, o dump seguinte pega a página vazia.

## Navegação entre passos

Existe **`Passo Anterior`**, e ele preserva o que foi digitado: voltei do passo 3
ao passo 2 e os valores continuavam lá. Serve para conferir um passo já deixado
para trás sem risco.

## O erro que mais custou: clique que não foca o campo

Sintoma: `Input.insertText` não escreve nada e o campo continua vazio, sem erro.
Causa: **o clique não deu foco**. Conferir sempre com
`document.activeElement` depois do clique — se voltar `BODY`, o clique errou o alvo.

Duas causas distintas, ambas corrigidas no `cdp.ps1`:

1. **Medir a posição no mesmo `eval` do `scrollIntoView`.** A rolagem pode ser
   animada; a coordenada medida antes dela envelhece e o clique cai noutro lugar.
   Rolar e medir têm de ser chamadas separadas, com espera entre elas.
2. **Balões de ajuda cobrindo o centro do campo.** O formulário tem popups
   (`.z-popup-content`) que ficam por cima do meio dos `textarea`. Clicar no centro
   acerta o balão. O `clickSel` agora varre 9 pontos dentro do retângulo do alvo e
   usa `document.elementFromPoint` para escolher um que realmente pertença ao alvo.

Antes da correção, 6 textos longos "entraram" e sumiram sem aviso. Depois dela,
os 6 gravaram na primeira tentativa. **Conferir o comprimento do campo depois de
escrever** é o que separou um caso do outro.

## Três widgets de seleção, três comportamentos

| Widget | Como reconhecer | Como selecionar |
|---|---|---|
| **Combobox** | `zul.inp.Combobox`, opções `.z-comboitem` no popup `#<id>-pp` | abrir por `#<id>-btn` e **clicar na opção**. Funciona. |
| **Listbox inline** | opções são `.z-listitem` soltas na página (ex.: "Produto/Processo") | **clicar no `.z-listitem`**. Funciona; confirmar pela classe `z-listitem-selected`. |
| **Bandbox** | `zul.inp.Bandbox`, popup `.z-bandpopup` com um `.z-listbox` dentro | **não consegui gravar**. Clique simples, duplo, Enter e até `zAu.send` de `onSelect` marcam a linha (`selectedIndex` muda) mas o valor do campo continua vazio. |

Rádios Sim/Não: o `input[type=radio]` real costuma estar oculto; clicar no
**wrapper `.z-radio`** (id = id do input sem o sufixo `-real`).

## Casar pergunta com controle: não confie em texto

Procurar "o elemento cujo `innerText` contém a pergunta" pega um `div` embrulho
que contém a página inteira — `children.length > 1` não basta como filtro, porque
um wrapper de um filho só carrega todo o texto. Resultado real: as 7 perguntas
Sim/Não foram para o mesmo par de rádios.

O que funciona: percorrer os `input[type=radio]`, subir de cada um até a linha
que tem texto próprio maior que ~25 caracteres (tirando "Sim"/"Não"), e montar a
lista pergunta → ids. Depois clicar por id. Está em `ferramentas/js/pares.js`.

## Campos que aparecem depois

Responder "Sim" a "Há previsão de participação de ICTs?" **abre um bloco inteiro
de campos obrigatórios** (nome, CNPJ, departamento, histórico, infraestrutura,
contato, telefone, e-mail e nº de pesquisadores por titulação). Rodar `Validar`
de novo depois de cada resposta que possa revelar seção nova.

## Marcadores editoriais do documento

O .docx traz notas do autor entre colchetes (`[Confirmar com o HBR...]`,
`[inserir]`). São instruções para o redator, não conteúdo da proposta — remover
antes de colar, e registrar em pendências que o trecho vinha marcado.

## `Próximo Passo` é bloqueado por qualquer erro pendente

Tentar avançar com um único campo obrigatório vazio devolve
*"Erro ao tentar enviar o formulário."* e **não troca de passo** — a tela
continua onde estava. A mensagem fala em "enviar", mas é só a validação da
etapa; não tem nada a ver com o `Enviar` final da proposta.

Ou seja: o `Validar` tem de estar limpo **antes** de clicar em `Próximo Passo`.
Não adianta deixar pendência para depois e seguir.

## O passo 5 não é ZK: é dhtmlxGantt

O Cronograma de Execução usa **dhtmlxGantt 4.1.0**, com `window.gantt` exposto.

- **Calendário sintético: `01/01/2000` = mês 1**, um mês por unidade, `end_date`
  exclusivo. Então mês N ↔ `new Date(2000,0,1)` + (N−1) meses, e
  `duração = fim − início + 1`.
- O editor (lightbox) só tem Título, Detalhe, Indicador e **duração** — o mês de
  início não está lá. Pela interface, só arrastando a barra.
- **O caminho que funciona é a API**: `gantt.addTask({text, detail, indicador,
  start_date, duration}, idDoPai)` e `gantt.updateTask(id)`. Os campos
  personalizados desta chamada chamam-se **`detail`** e **`indicador`** —
  descobertos em `gantt.config.lightbox.sections` (cada seção tem um `map_to`).
- Isso **persiste**: o `Salvar` do ZK grava e as tarefas voltam depois do
  round-trip. Foram 49 atividades criadas assim, em 4 lotes.
- `t.parent` volta como **string**: comparar com `String(t.parent)==='100000'`,
  não `===100000`. Comparação estrita silenciosa custou uma rodada.
- **Só dois níveis: raiz (id 100000, a meta física) → atividades.** Em 27/09
  foram criadas 8 "metas" sob a raiz e 49 atividades sob elas (3 níveis). O
  `Salvar` respondeu sucesso e o gantt local mostrava tudo, mas na sessão
  seguinte as 49 do 3º nível **tinham sumido**. Para indicar a meta, o título
  da atividade leva o prefixo `(Meta N) ` (limite de 100 caracteres no título).
- **Salvar com sucesso não prova persistência no gantt.** Prova é sair e voltar
  (`Passo Anterior` → `Próximo Passo`) e conferir `gantt.eachTask` de novo.
  Ao substituir estrutura: criar → salvar → vaivém → conferir → só então
  `gantt.deleteTask` das antigas → salvar → vaivém de novo.
- O botão "+" de cada linha tem **tamanho zero até o mouse passar por cima**.
  Por isso o `cdp.ps1` ganhou a op `hoverSel`. Ainda assim, criar pela API saiu
  mais confiável que caçar o "+".

## Ler a mensagem de erro de verdade

O balão "Verifique os erros marcados na tela" não diz nada. As mensagens úteis
estão em popups escondidos no DOM: varrer `.z-errbox,.z-popup,[class*=tooltip]`
e ler o `innerText` **mesmo dos invisíveis** devolveu, de uma vez:

- "Verifique a(s) atividade(s) abaixo: Linha 2: Você deve preencher a 'Descrição'
  e o 'Indicador Físico'..." → eram as metas sem indicador;
- "Algumas células da tabela estão inválidas... linha(s): 3" + "Campo obrigatório!"
  → a contrapartida 0,00 da parcela 3.

Sem isso eu estaria adivinhando.

## O campo pode mostrar o valor e não ter gravado

A contrapartida da parcela 2 estava visível no campo (`207.630,00`) e **não havia
chegado ao servidor**: o total da coluna, que o servidor calcula, estava
R$ 207.630,00 menor. Reescrever resolveu.

**Regra:** em tabela com totalizador, conferir o **total calculado pelo servidor**,
nunca o `value` do campo. O `value` prova digitação, não gravação. Foi assim que
as 11 linhas de pessoal e as 38 da relação de itens foram validadas — cada soma
bateu ao centavo com o documento.

## Modo correção (sessão de 28/09)

- **`Exportar PDF` exporta só o passo corrente** (4–6 páginas). A cópia
  integral da proposta é o "Dados Preenchidos na Proposta", em *Resumo* no menu
  lateral — peça ao usuário ou gere por lá antes de mexer.
- **Limite de texto longo**: os `textarea` do passo 3 não têm `maxlength` no DOM
  (`-1`). O limite real está no widget: `zk.Widget.$(ta).getMaxlength()` →
  100000 nesses campos.
- **Troca cirúrgica de texto que funcionou**: ler o `value` inteiro, aplicar as
  trocas em node exigindo **exatamente 1 ocorrência** de cada trecho, gravar o
  texto novo em arquivo, marcar o `textarea` pelo prefixo **e** comprimento
  originais (dois campos podem começar igual), `clear` + `typefile` + `Tab`, e
  depois do `Salvar` comparar caractere a caractere com o esperado — e conferir
  que nenhum outro campo mudou.
- **Relação de itens, colunas**: Categoria de despesa de pessoal (`N/A` fora
  da Equipe Própria) · **Qtde** · Qtde total de horas por pessoa (só para quem
  vem da Equipe Executora) · Valor unitário. Lançar horas da ICT em **Qtde**
  (11.520 × 107,00) faz o avaliador ler "11.520 h de uma pessoa". Solução
  adotada: uma linha da ICT, Qtde 1 × valor total, e o detalhamento por pessoa
  no texto da ICT. Ler o cabeçalho da tabela (screenshot) antes de concluir
  o que um campo é — `title` vazio não diz nada.
- **Relação de itens não tem coluna de fonte nem de parcela.** Fonte e parcela
  só existem no Cronograma Financeiro, por totais.
- **Dados dos Responsáveis** (passo 2) é uma grade única "Dirigentes"; não há
  tipo Dirigente/Coordenador.
- Linha de orçamento: o botão da lixeira é `button.btn-danger` com
  `i.z-icon-trash-o` dentro, na altura do `textarea` da linha; pede "Sim/Não".
- **Conferir as caixas da aba "Aprovação e Envio" no início da sessão.** Em
  28/09 elas estavam marcadas sem que o agente tivesse tocado nelas. Não mexer;
  relatar.
- No plano JSON do `cdp.ps1`, `\(` dentro de `js` inline quebra o
  `ConvertFrom-Json`. Regex com barra invertida vai por `evalfile`.

## Onde o agente para

A aba "Aprovação e Envio da Proposta" (passo 5) tem duas caixas de declaração e o
botão `Enviar`. O texto da própria tela: *"Após confirmar as declarações abaixo e
clicar no botão 'Enviar', a proposta será submetida à Finep."*

As caixas são a **assinatura** da proposta. Não marcar, não clicar em `Enviar`.
Preencher tudo, validar, salvar, e entregar a assinatura ao usuário.
