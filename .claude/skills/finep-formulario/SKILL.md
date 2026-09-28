---
name: finep-formulario
description: Preenche o formulário eletrônico da FINEP (credito.finep.gov.br, framework ZK) a partir de um documento de referência local, tela por tela, até o fim — sem nunca submeter a proposta. Use quando o usuário pedir para preencher, continuar, retomar ou conferir a proposta no sistema da FINEP.
---

# Preenchimento do formulário da FINEP

Você opera o navegador do usuário, que já está logado no sistema da FINEP, e
preenche o formulário a partir de um documento de referência local. O usuário
não deve precisar colar código nem descrever cada tela.

## Limite absoluto

**Nunca clique em nada que submeta, envie, finalize ou encerre a proposta.**
Rótulos proibidos, em qualquer variação: Enviar, Submeter, Finalizar,
Concluir proposta, Assinar, Transmitir, Enviar para análise. Se a tela só
avançar por um botão assim, **pare e devolva o controle ao usuário**.

Permitidos: `Salvar`, `Validar`, `Verificar pendências`, `Passo Anterior`,
`Próximo Passo`, `Adicionar`, `Exportar PDF`. Antes do **primeiro**
`Próximo Passo` da sessão, confirme com o usuário; depois disso siga sozinho.

Nesta chamada, o botão **`Enviar`** só aparece na barra inferior a partir do
**passo 5**, ao lado do `Salvar`. Cuidado redobrado ali: são botões vizinhos.
(O item "Enviar Proposta" do menu superior existe desde o início e também não
se toca.)

**As caixas de declaração da aba "Aprovação e Envio da Proposta" não se marcam.**
São a assinatura da proposta — "Concordo, integralmente, com o conteúdo da
proposta e com sua subscrição à Finep..." — e quem subscreve é o dirigente.
Deixe as duas vazias e entregue.

Caixas de declaração **em outras telas** (por exemplo "Declaro que os dados
cadastrais estão corretos", no passo 1) são diferentes: pergunte ao usuário
antes de marcar, e marque só com autorização expressa dele na conversa.

## Nunca invente dado

Campo sem correspondência no documento de referência fica **vazio**. Não
deduza CPF, data, valor, título nem sigla. Anote em pendências e siga. É um
documento oficial: um dado inventado é pior do que um campo em branco.

## Antes de começar

1. Confirme que as ferramentas de navegador estão disponíveis. Se não
   estiverem, **não pare ainda**: veja se há algo escutando na porta 9222
   (`http://127.0.0.1:9222/json/version`). Se houver, use
   `finep-agente/ferramentas/cdp.ps1` e siga normalmente. Se não houver, mande
   o usuário rodar `finep-agente\abrir-chrome.cmd` (ou `abrir-edge.cmd`) e pare.
2. Leia `finep-agente/estado/progresso.md` **e**
   `finep-agente/estado/aprendizados-zk.md`. O primeiro diz onde o trabalho
   parou; o segundo, quais armadilhas já foram pagas. Se houver trabalho
   anterior, retome de onde parou em vez de recomeçar — e **confira se o
   documento de referência em `dados/` ainda é o mesmo** do registro anterior:
   já aconteceu de a proposta inteira ter mudado entre sessões.
3. Leia **todos** os documentos de referência em `finep-agente/dados/` —
   tipicamente o texto do projeto, a planilha de orçamento e o cronograma.
   `.md` e `.pdf` se leem direto; `.docx` e `.xlsx` exigem a skill
   correspondente. Se o mesmo dado aparecer em dois arquivos com valores
   diferentes, pergunte qual manda — não escolha. Monte uma tabela: campo →
   valor → de qual documento e de qual trecho veio. Essa procedência entra no
   registro de progresso.
4. Tire um snapshot da página e confirme com o usuário em que passo do
   formulário vocês estão.

## Modo correção

Quando a proposta **já está preenchida** e o usuário traz uma lista de
alterações (tipicamente um arquivo `correcoes-*.md` em `dados/`, vindo de uma
auditoria), o trabalho muda de natureza: não se percorre o formulário inteiro,
vai-se a cada item.

- **Altere só o que está listado.** Não reescreva, não "melhore" e não
  reorganize o resto. Problema novo encontrado no caminho vai para o
  relatório, não para a plataforma.
- **O arquivo de correções é a fonte da sessão.** Se outro arquivo de `dados/`
  divergir dele, siga o de correções e registre a divergência. Itens marcados
  como decididos não se perguntam de novo.
- **Cópia antes de mexer.** `Exportar PDF` do estado atual antes da primeira
  alteração, e anote os totais que a plataforma mostra. É o que permite
  comparar e desfazer.
- **Troca de texto é cirúrgica.** Substitua só o trecho indicado; o resto do
  campo fica idêntico. Registre o trecho antes e depois.
- **Substituir estrutura: crie antes de apagar.** Linha de orçamento, meta do
  cronograma ou bloco repetido que será trocado: crie o novo, confira somas e
  contagens, e só então apague o antigo.
- **Totais que a correção declara invariantes são invariantes.** Confira pelo
  valor do servidor depois de cada tela de orçamento; se mudou, pare.
- **Registre por ID de item**: `feito`, `aguardando usuário`, `bloqueado` (com a
  mensagem da plataforma) ou `não se aplica` (com o motivo). O relatório final
  cobre todos os IDs, sem exceção.

## Ciclo por tela

Repita até o formulário acabar:

1. **Snapshot** da página. Leia os rótulos visíveis, não os ids.
2. **Case** cada campo com o documento de referência. O que não casar entra
   na lista de pendências, não em suposição.
3. **Preencha um campo por vez**, respeitando o tipo (ver regras do ZK).
   Depois de cada campo que provoque recarga, tire snapshot novo.
4. **Confira** o que foi escrito no snapshot seguinte. Valor que não fixou é
   erro, não detalhe — resolva antes de seguir.
5. Clique **Validar** e depois **Verificar pendências**. Leia a resposta e
   corrija o que for do seu escopo.
6. Clique **Salvar**.
7. **Registre** em `finep-agente/estado/progresso.md`.
8. Clique **Próximo Passo**.

## Tipos de campo além de texto curto

### Texto longo com limite de caracteres

Telas de caracterização do projeto (objetivo, justificativa, estado da arte,
inovação, metodologia, resultados esperados) quase sempre limitam o tamanho.

- **Leia o limite antes de escrever**: atributo `maxlength`, contador na tela
  ou instrução do tipo "máximo N caracteres".
- **Coube: escreva literal.** O texto é do usuário; não "melhore", não
  reescreva, não corrija estilo.
- **Não coube: nunca trunque.** Cortar no limite decepa a conclusão do
  parágrafo e o avaliador lê um texto sem fim. Condense preservando o conteúdo
  técnico e os números, **mostre a versão condensada ao usuário** e só escreva
  depois do aval dele. Registre no progresso que aquele campo foi condensado.
- Campo que pede algo que o documento não traz (uma seção que o projeto não
  tem) fica vazio e vira pendência — não se escreve um parágrafo novo.

### Orçamento e valores

- **Valores vão exatos como na planilha.** Não arredonde, não converta
  unidade, não redistribua "para fechar" — a menos que o usuário decida isso
  na conversa. Quando decidir, registre como divergência (ver Encerramento).
- **Confira o formato da tela** antes do primeiro valor: separador decimal,
  presença ou não de símbolo de moeda, milhar. Escreva no padrão que a tela
  usa nos campos já preenchidos.
- **Antes de sair da tela**, some as rubricas e compare com o total da
  planilha **e** com o total que o servidor calcula (armadilha 2, abaixo: o
  `value` do campo não prova gravação). Divergência é erro de entrada até
  prova em contrário: pare, mostre os três números e não avance.
- Rubrica da tela sem correspondência óbvia na planilha (ou item que caberia
  em duas rubricas): **pergunte**. Classificação de despesa muda análise e
  prestação de contas — não é escolha sua.

### Cronograma, metas e etapas

- São blocos repetidos: uma meta ou etapa por vez, com `Adicionar` →
  preencher → conferir → `Salvar` → próxima.
- **Confirme a convenção de tempo antes do primeiro bloco.** Nesta chamada o
  cronograma do passo 5 é um Gantt com mês relativo (ver "O passo 5 não é
  ZK"); em outras telas ou chamadas, se não estiver claro, pergunte.
- Ao fechar a tela, verifique que nenhuma etapa ultrapassa o último mês do
  projeto e que a duração total bate com o prazo declarado.

### Coerência entre telas

Antes de encerrar, confira os cruzamentos que o avaliador vai olhar:

- total do orçamento = soma das rubricas = soma do cronograma de desembolso;
- duração do cronograma = prazo do projeto declarado na caracterização;
- meses de dedicação da equipe compatíveis com a duração do projeto.

Divergência aqui vira relatório para o usuário, não correção por conta
própria: mexer num número para fazer fechar é inventar dado.

## Regras do ZK (aprendidas neste sistema)

O formulário é ZK (`formRender.zul`). Isso não é detalhe cosmético:

- **Os ids são descartáveis.** `cXAQhi` e afins são uuids regerados a cada
  renderização e a cada `Adicionar`. Nunca guarde um seletor entre passos:
  localize o campo pelo rótulo, no snapshot atual.
- **O `title` também não é estável.** O mesmo campo aparece como `"Valor:"` e,
  depois de um round-trip, como `"Valor"`. Comparar sempre normalizando: sem
  `:` final, sem NBSP, sem caixa.
- **Campo com id terminado em `-real` é widget, não texto livre** — pode ser
  combobox, bandbox, rádio ou checkbox, e **cada um se preenche diferente**:
  - *Combobox* (opções `.z-comboitem` no popup `#<id>-pp`): abrir por
    `#<id>-btn` e **clicar na opção**. Funciona.
  - *Listbox inline* (opções `.z-listitem` soltas na página): **clicar no item**;
    confirmar pela classe `z-listitem-selected`.
  - *Bandbox* (`.z-bandpopup` com `.z-listbox` dentro): clique, duplo clique,
    Enter e `zAu.send` de `onSelect` marcam a linha mas **não gravam o valor**.
    Se o `Validar` não exigir o campo, registre como pendência e siga.
  - *Rádio*: o `input` real costuma estar oculto; clicar no **wrapper `.z-radio`**
    (id do input sem o sufixo `-real`).
- **O estado vive no servidor.** Toda escrita dispara um round-trip. Espere a
  página assentar antes da ação seguinte; não encadeie cliques às cegas.
- **Blocos repetidos** (equipe, atividades, orçamento) nascem de `Adicionar`,
  que renderiza um bloco novo e pode trocar os ids da seção inteira. Faça um
  membro por vez: Adicionar, preencher, conferir, Salvar, próximo.
- **Sessão expira.** Diálogo falando em sessão ou timeout significa parar,
  avisar o usuário e registrar o progresso — não tente relogar.

## As três armadilhas que mais custam tempo

1. **Clique que não dá foco.** `insertText` não escreve nada e o campo fica
   vazio, sem erro nenhum. Duas causas: medir a posição no mesmo `eval` do
   `scrollIntoView` (a rolagem pode ser animada e a coordenada envelhece), e
   balões de ajuda (`.z-popup-content`) cobrindo o **centro** do campo.
   **Conferir `document.activeElement` depois de cada clique**: se voltar
   `BODY`, o clique errou o alvo.
2. **O campo mostra o valor e não gravou.** Em tabela com totalizador, conferir
   o **total calculado pelo servidor**, nunca o `value` do campo — o `value`
   prova digitação, não gravação.
3. **`Próximo Passo` é bloqueado por qualquer erro pendente**, devolvendo
   *"Erro ao tentar enviar o formulário."* sem trocar de passo. (A palavra
   "enviar" aí é só a validação da etapa; nada a ver com o `Enviar` final.)
   O `Validar` tem de estar limpo **antes** de avançar.

Para ler o erro de verdade: o balão "Verifique os erros marcados na tela" não
diz nada. Varrer `.z-errbox, .z-popup, [class*=tooltip]` e ler o `innerText`
**mesmo dos invisíveis** devolve a mensagem específica, com linha e campo.
O marcador de erro na tela é `.err-ind`; `error-box-*` é classe de layout.

## O passo 5 não é ZK

O Cronograma de Execução usa **dhtmlxGantt**, com `window.gantt` exposto.
Calendário sintético: **01/01/2000 = mês 1**, um mês por unidade, `end_date`
exclusivo. O editor só tem duração — o mês de início, não. O caminho que
funciona é a API: `gantt.addTask({text, detail, indicador, start_date,
duration}, idDoPai)`, e isso **persiste** no `Salvar` do ZK.

**O Gantt só aceita dois níveis**: a raiz (meta física, id 100000) e atividades
diretamente sob ela. Sub-atividade some no servidor mesmo com "salvo com
sucesso". Cada atividade vai direto sob a raiz, com a meta no título:
`(Meta 1) Gestão técnica e financeira do projeto` (título ≤ 100 caracteres).
Persistência só se prova saindo do passo e voltando.

## Ferramentas prontas

Se o MCP do navegador não carregar, não pare a sessão: o Chrome/Edge aberto
pelos lançadores expõe CDP na porta 9222 e
**`finep-agente/ferramentas/cdp.ps1`** fala esse protocolo direto (ops: `eval`,
`evalfile`, `click`, `clickSel`, `hoverSel`, `type`, `typefile`, `clear`, `key`,
`zkidle`, `screenshot`). Os localizadores reutilizáveis estão em
`finep-agente/ferramentas/js/`.

**Leia `finep-agente/estado/aprendizados-zk.md` antes de começar.** É o registro
vivo do que já custou uma rodada — e acrescente a ele o que aprender.

## Versionamento

Melhorar esta skill, `estado/aprendizados-zk.md` e `ferramentas/` é bem-vindo:
é assim que a próxima sessão começa sabendo mais.

- **No início da sessão**, rode `git pull`. Editar sobre uma versão velha gera
  conflito com o que foi alterado em outro lugar.
- **Ao terminar**, faça commit **só** desses caminhos, com mensagem que diga o
  que se aprendeu. Peça autorização ao usuário antes do `git push`.
- **Nunca versione** `estado/progresso.md` nem nada de `dados/`: têm CPF,
  telefone, valores e o texto da proposta.

## Registro do progresso

Mantenha `finep-agente/estado/progresso.md` atualizado a cada tela:

```markdown
## <nome do passo/aba>   — <data e hora>
Estado: preenchido | parcial | pendente
Campos preenchidos: <rótulo> = <valor>   (fonte: <onde no documento>)
Pendências: <rótulo> — <por que ficou vazio>
Observações: <o que o Validar reclamou, o que exigiu decisão>
```

É o que permite retomar depois de uma sessão expirada, e é o registro que o
usuário confere no fim.

## Encerramento

O fim do trabalho do agente é a aba **"Aprovação e Envio da Proposta"**, no
passo 5, com as duas caixas de declaração **vazias** e o `Enviar` intocado.
Chegar lá com tudo o mais validado é o sucesso, não um preenchimento parcial.

Entregue ao usuário:

- os passos preenchidos e o que o `Validar` ainda acusa, aba por aba;
- a lista de pendências com o **motivo** de cada uma — distinguindo *dado que
  não existe no documento* de *decisão que é do usuário*;
- o que **divergiu** do documento de referência e por quê (mapeamento de opção
  que não existia na lista, valor redistribuído a pedido dele, arredondamento);
- a instrução explícita de que assinar e enviar é manual, feito por ele.

Se alguma decisão sua mudou um número que o documento de referência também
traz, diga isso: os dois passam a divergir, e o usuário precisa saber qual
atualizar.
