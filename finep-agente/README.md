# Agente de preenchimento do formulário da FINEP

Um agente que enxerga o formulário, preenche a partir de um documento de
referência, avança de passo e repete — sem você colar código em cada aba.
A submissão continua manual, feita por você.

## Por que roda na sua máquina

O formulário está numa sessão logada no **seu** navegador. Nenhum Claude na
nuvem alcança isso. Então o agente roda localmente, no seu Windows, e conversa
com o Chrome que você mesmo abriu. Suas credenciais não saem da sua máquina e
o documento com os dados da equipe também não.

## Instalação (uma vez só)

Abra o **PowerShell** e rode, um de cada vez:

```powershell
winget install OpenJS.NodeJS.LTS
winget install Git.Git
```

Feche e reabra o PowerShell (para o PATH atualizar), depois:

```powershell
npm install -g @anthropic-ai/claude-code
git clone https://github.com/Marvipl/acta-agentes.git
cd acta-agentes
claude
```

Na primeira execução do `claude`, faça login na sua conta. Quando ele
perguntar se aprova o servidor MCP `playwright` deste projeto, aprove — é
por ele que o agente enxerga o navegador.

Se `winget` não existir na sua máquina, instale o Node.js LTS e o Git pelos
sites oficiais e siga do `npm install` em diante.

## Uso (toda vez)

1. **Abra o navegador do agente**: dê dois cliques em
   `finep-agente\abrir-chrome.cmd`. Ele abre uma janela do Chrome num perfil
   separado, com depuração remota na porta 9222. Faça login no FINEP nessa
   janela e navegue até o formulário. Deixe a janela aberta.

   Perfil separado de propósito: a porta de depuração deixa qualquer programa
   local dirigir aquela janela, e não faz sentido expor seu navegador do dia a
   dia. Feche essa janela quando terminar.

2. **Coloque o documento** com os dados em `finep-agente\dados\`
   (.docx, .xlsx, .pdf ou .md — veja `dados\LEIA-ME.md`). Nada dessa pasta vai
   para o repositório.

3. **Rode o agente**: no PowerShell, dentro da pasta `acta-agentes`:

   ```powershell
   claude
   ```

   e peça: `/finep-formulario preencher a aba de equipe`.

4. **Acompanhe.** Ele mostra cada campo antes de escrever, pede confirmação
   antes do primeiro "Próximo Passo" e registra tudo em
   `finep-agente\estado\progresso.md`.

## O que ele não faz

- Não clica em Enviar, Submeter, Finalizar ou Assinar. Chegando na tela final,
  ele para e devolve o controle.
- Não inventa dado. Campo sem correspondência no documento fica vazio e vira
  pendência no relatório.
- Não tenta relogar. Sessão expirada é motivo de parar e avisar.

## Se der errado

- **O agente diz que não tem ferramentas de navegador**: o Chrome não está com
  a depuração ligada. Rode o `abrir-chrome.cmd` e reinicie o `claude`.
  Para conferir, abra `http://localhost:9222/json/version` no navegador — tem
  que devolver um JSON.
- **O MCP não sobe no Windows**: é quase sempre o `npx`. O `.mcp.json` da raiz
  já usa a forma `cmd /c npx`, que é a que funciona no Windows.
- **A flag `--cdp-endpoint` foi recusada**: rode
  `npx @playwright/mcp@latest --help` e me mande a lista de opções.

## Pasta irmã

`../finep-preenchimento/` são os scripts de console da primeira abordagem.
Ficam como diagnóstico — o `01-mapear.js` continua útil para dumpar uma tela
inteira de uma vez. Para o uso normal, prefira o agente.
