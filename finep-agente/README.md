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

Rode **um comando por vez**, não cole o bloco inteiro: o PATH só passa a
conhecer o `node` e o `git` numa janela aberta *depois* da instalação deles.

Etapa 1 — abra o PowerShell e instale as duas dependências:

```powershell
winget install OpenJS.NodeJS.LTS
```

```powershell
winget install Git.Git
```

Etapa 2 — **feche essa janela e abra um PowerShell novo**. Vá para uma pasta
sua (nunca `C:\Windows\system32`) e confirme que os dois foram reconhecidos:

```powershell
cd $HOME\Documents
node -v; npm -v; git --version
```

Se algum não responder, recarregue o PATH sem reabrir:

```powershell
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
```

Se o `npm -v` falhar com *"a execução de scripts foi desabilitada neste
sistema"*, é a política de execução do PowerShell bloqueando o `npm.ps1` — não
tem a ver com o Node. Libere para o seu usuário (não precisa de administrador):

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

`RemoteSigned` libera script local e continua exigindo assinatura em script
baixado da internet. Sem isso o `claude` esbarra na mesma trava depois.

Etapa 3 — instale o Claude Code e baixe este repositório:

```powershell
npm install -g @anthropic-ai/claude-code
```

```powershell
git clone https://github.com/Marvipl/acta-agentes.git
```

```powershell
cd acta-agentes
claude
```

Na primeira execução do `claude`, faça login na sua conta.

Etapa 4 — registre o servidor MCP que dá visão do navegador ao agente. Rode
uma vez, dentro da pasta `acta-agentes`, com o `claude` **fechado**:

```powershell
claude mcp add playwright -- cmd /c npx -y @playwright/mcp@latest --cdp-endpoint http://localhost:9222
```

O registro fica na sua máquina, não no repositório. É de propósito: as rotinas
da Acta clonam este repositório e rodam em Linux, onde `cmd` não existe — um
`.mcp.json` versionado com esse comando quebraria o carregamento de MCP em
todas elas.

Se `winget` não existir na sua máquina, instale o Node.js LTS e o Git pelos
sites oficiais e siga da etapa 2 em diante.

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
- **O MCP não sobe**: confira se ele foi registrado, com `claude mcp list`. No
  Windows o `npx` precisa ser chamado via `cmd /c`, que é a forma usada na
  etapa 4 — sem isso o servidor falha com "Executable not found".
- **A flag `--cdp-endpoint` foi recusada**: rode
  `npx @playwright/mcp@latest --help` e me mande a lista de opções.

## Pasta irmã

`../finep-preenchimento/` são os scripts de console da primeira abordagem.
Ficam como diagnóstico — o `01-mapear.js` continua útil para dumpar uma tela
inteira de uma vez. Para o uso normal, prefira o agente.
