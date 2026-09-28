# Documentos de referência

Coloque aqui tudo que o agente deve usar para preencher o formulário. Ele lê a
pasta inteira e casa o conteúdo com os rótulos de cada tela.

Tudo nesta pasta é ignorado pelo git, menos este arquivo e o modelo. Dados
pessoais da equipe, valores de orçamento e o texto do projeto **não entram no
repositório** (regra 5 do SKILL.md da Acta).

## O que colocar

Formato livre — .docx, .xlsx, .pdf ou .md. Tipicamente três documentos:

**1. Texto do projeto.** Título, objetivo geral e específicos, justificativa,
estado da arte, inovação, metodologia, resultados esperados, impactos, prazo.
Mantenha as seções com nomes próximos aos do formulário; facilita o
casamento e reduz pendência.

**2. Planilha de orçamento.** Itens por rubrica (pessoal, material de consumo,
equipamentos, serviços de terceiros, viagens, obras), com valor unitário,
quantidade e total, mais o total geral. Deixe explícita a rubrica de cada
item: o agente não classifica despesa por conta própria, ele pergunta.

**3. Cronograma.** Metas e etapas, com mês de início e fim de cada uma, e o
cronograma de desembolso se o edital pedir. Diga se os meses são relativos ao
início do projeto ou datas de calendário.

**4. Equipe** (se for preencher essa aba). Um bloco por membro — ver
`equipe.exemplo.md`.

**5. Correções de uma proposta já preenchida.** Um arquivo `correcoes-*.md`
com a lista de alterações, cada uma com ID, onde fica, o que mudar e como
conferir. Com ele, o agente entra em modo correção: mexe só no que está listado
e deixa o resto como está. Quando houver arquivo de correções, deixe na pasta só
ele e a versão vigente do orçamento e cronograma — versões antigas geram
divergência e interrupção.

## O que ajuda de verdade

- **Campos de lista** (Sexo, Titulação, Vínculo, Função, Nível, rubrica):
  use a opção exata como aparece no formulário.
- **Dado que ainda não existe**: escreva "A DEFINIR" em vez de omitir. Assim
  o agente registra como pendência em vez de deixar passar despercebido.
- **Texto longo**: se você já sabe o limite de caracteres do campo, anote ao
  lado da seção. Quando o texto não couber, o agente condensa e te mostra a
  versão reduzida antes de escrever — nunca trunca no limite.
- **Números**: deixe o total geral explícito no documento. O agente soma as
  rubricas e compara com esse total e com o que o formulário calcula; os três
  têm que bater.
