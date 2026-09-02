# Preenchimento assistido do formulário da FINEP (equipe)

Scripts de console para preencher a seção de equipe do formulário eletrônico da
FINEP (`credito.finep.gov.br/credito/externo/privado/formRender.zul`).

## O que o sistema é, e por que isso importa

O formulário é **ZK Framework** (`.zul`). Duas consequências práticas:

1. **O estado vive no servidor.** Escrever `input.value = 'x'` muda só a tela; o
   servidor continua com o valor antigo e o "Salvar" grava o antigo. O valor só
   sobe quando o ZK dispara `onChange` (no *blur* de um campo de texto) ou
   `onSelect` (no clique num item do dropdown). Os helpers do passo 2 fazem
   exatamente isso.
2. **Os ids são gerados a cada renderização.** `cXAQhi`, `cXAQqi` etc. são uuids
   do ZK e mudam a cada recarga da página e a cada "Adicionar". Nenhum script
   pode fixar ids: o passo 3 descobre os campos do bloco novo por diferença de
   DOM depois de cada clique em "Adicionar".

Campos cujo id termina em `-real` são **comboboxes** (dropdown), não texto livre:
`Sexo`, `Titulação`, `Empresa/CNPJ`, `Vínculo`, `Função no projeto`, `Nível`.

## Ordem de uso

1. Abra a tela da equipe, já logado. F12 > Console. Se o Chrome bloquear o colar,
   digite `allow pasting` + Enter uma vez.
2. Cole **`01-mapear.js`**. Ele não altera nada. Guarde o JSON gerado.
3. Cole **`02-helpers.js`** e rode o diagnóstico. O valor de teste tem de ser
   **diferente** do que está no campo: o ZK compara o valor novo com o que já
   tem e não dispara nada se forem iguais. O helper escreve, verifica e
   restaura o valor original sozinho.

   ```js
   __finep.monitorar()
   await __finep.diagnosticar('<id de um campo de texto>', 'valor diferente')
   await __finep.diagnosticar('<id terminado em -real>', 'Outra opção da lista')
   ```

   O veredito sai no console. `ok: true` significa que um evento com o uuid do
   campo foi de fato enviado ao servidor — o campo `via` diz por qual dos três
   caminhos. `ok: false` significa que nada subiu, e aí a rota é Playwright
   acoplado ao Chrome, que emula teclado e mouse de verdade.

   Eventos `dummy` no monitor são round-trips no-op do ZK e ficam fora do log.
4. Copie `dados-equipe.exemplo.js` para `dados-equipe.js` (ignorado pelo git),
   preencha com os membros e cole no console.
5. Cole **`03-preencher.js`** com `DRY_RUN = true`. Confira o log.
6. Rode com `DRY_RUN = false` **para um único membro** primeiro. Confira na tela.
7. Só então rode a lista completa.

## Limites deliberados

- O script nunca clica em "Próximo Passo" nem em nada que submeta a proposta.
  "Salvar" é opcional e só grava rascunho.
- Ele para na primeira falha, em vez de seguir e deixar dados pela metade.
- Detecta expiração de sessão do ZK e aborta.
- Se houver captcha, assinatura ou validação externa de CPF, o script para ali.

## Dados pessoais

CPF, telefone e e-mail da equipe **não entram neste repositório**.
`dados-equipe.js` está no `.gitignore`. Só o código é versionado.
