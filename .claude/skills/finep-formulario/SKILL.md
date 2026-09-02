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

## Nunca invente dado

Campo sem correspondência no documento de referência fica **vazio**. Não
deduza CPF, data, valor, título nem sigla. Anote em pendências e siga. É um
documento oficial: um dado inventado é pior do que um campo em branco.

## Antes de começar

1. Confirme que as ferramentas de navegador estão disponíveis. Se não
   estiverem, o Chrome não foi aberto com depuração remota — mande o usuário
   rodar `finep-agente\abrir-chrome.cmd` e pare.
2. Leia `finep-agente/estado/progresso.md`. Se houver trabalho anterior,
   retome de onde parou em vez de recomeçar.
3. Leia o documento de referência em `finep-agente/dados/`. Se for .docx,
   .xlsx ou .pdf, use a skill correspondente para extrair o conteúdo.
   Monte uma tabela mental: campo → valor → de onde veio.
4. Tire um snapshot da página e confirme com o usuário em que passo do
   formulário vocês estão.

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

## Regras do ZK (aprendidas neste sistema)

O formulário é ZK (`formRender.zul`). Isso não é detalhe cosmético:

- **Os ids são descartáveis.** `cXAQhi` e afins são uuids regerados a cada
  renderização e a cada `Adicionar`. Nunca guarde um seletor entre passos:
  localize o campo pelo rótulo, no snapshot atual.
- **Campo com id terminado em `-real` é combobox**, não texto livre. Abra a
  lista e clique na opção; digitar por cima costuma ser descartado. No
  formulário da equipe são: Sexo, Titulação, Empresa/CNPJ, Vínculo, Função no
  projeto, Nível.
- **O estado vive no servidor.** Toda escrita dispara um round-trip. Espere a
  página assentar antes da ação seguinte; não encadeie cliques às cegas.
- **Blocos repetidos** (equipe, atividades, orçamento) nascem de `Adicionar`,
  que renderiza um bloco novo e pode trocar os ids da seção inteira. Faça um
  membro por vez: Adicionar, preencher, conferir, Salvar, próximo.
- **Sessão expira.** Diálogo falando em sessão ou timeout significa parar,
  avisar o usuário e registrar o progresso — não tente relogar.

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

Ao chegar na tela final, **não submeta**. Entregue ao usuário:

- os passos preenchidos e o que o `Verificar pendências` ainda acusa;
- a lista de pendências com o motivo de cada uma;
- a instrução explícita de que a submissão é manual, feita por ele.
