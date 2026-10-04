# Rodar os squads no Claude Code na nuvem

Este kit deixa o repositório `acta-agentes` pronto para rodar os quatro squads numa sessão de nuvem (claude.ai/code, app do celular ou `claude --cloud`), sem mudar o código dos squads. No computador, tudo continua funcionando como hoje.

## Por que é preciso
Na nuvem a sessão começa na raiz do repositório e só o `.claude/` da raiz registra agentes, comandos e configurações. Os squads estão em subpastas, cada um com o seu `.claude/`, e têm agentes com o mesmo nome (por exemplo, `enquadramento` existe em três squads). O `montar_nuvem.py` gera na raiz uma versão de cada agente com prefixo do squad (`orc-`, `est-`, `prod-`, `dados-`) e os comandos apontando para a pasta certa.

## Uma vez, no seu computador
1. Coloque as pastas `squad-orcamento`, `squad-estrategia`, `squad-produto` e `squad-analise` na raiz do `acta-agentes`, e a pasta `ferramentas` deste kit também.
2. Na raiz, rode `python ferramentas\montar_nuvem.py`. Ele cria `.claude\agents\`, `.claude\commands\`, mescla o `.claude\settings.json` e adiciona blocos marcados ao `CLAUDE.md` e ao `.gitignore`. Arquivos que já existiam e não foram gerados por ele não são tocados (se houver conflito de nome, ele avisa e para).
3. Confira com `git status` que nenhum dado entrou (`projetos\`, `entrada\`, `dados\` e chaves ficam fora) e faça commit e push.
4. Rode o `montar_nuvem.py` de novo sempre que mudar um squad (ele refaz só o que gerou).

## Uma vez, em claude.ai/code
1. **Ambiente de nuvem:** no seletor de ambiente (ícone de nuvem acima da caixa de mensagem), crie "Squads Acta" com acesso de rede **Trusted** e este script de preparação:
   ```bash
   #!/bin/bash
   PKGS="duckdb pandas numpy scipy statsmodels scikit-learn pyarrow openpyxl matplotlib pypdfium2 pillow python-docx python-pptx"
   pip install -q $PKGS || pip install -q --break-system-packages $PKGS || true
   ```
   O resultado fica em cache, então as próximas sessões já começam com tudo instalado. Se as pesquisas na web dos squads de estratégia e produto falharem, troque o acesso para **Full**.
2. **Squad de análise (só se for usá-lo na nuvem):** crie um segundo ambiente, pessoal, com a variável `SQUAD_CHAVE_PSEUDONIMIZACAO` igual ao conteúdo do seu `squad-analise\config\chave_local.key`. Quem usa o ambiente consegue ler a variável; não compartilhe esse ambiente.

## A cada uso
1. Abra uma sessão em claude.ai/code com o repositório `acta-agentes` e o ambiente "Squads Acta".
2. Com `ACTA_DRIVE_CREDENCIAL` configurada (seção Arquivos grandes), os squads baixam e publicam no Drive sem limite de tamanho. Sem ela, habilite o conector do Google Drive na sessão, que só baixa arquivos de até 10 MB.
3. Rode o comando do squad, por exemplo:
   - `/orcar completo "Cliente" "Projeto" <pasta do Drive com os documentos>`
   - `/estrategia plano "2027" "Plano estratégico 2027" <pasta do Drive>`
   - `/produto oportunidade "Segmento" "Produto" <pasta do Drive>`
   - `/analisar padrao "<objetivo>" <pasta do Drive com os dados>`
   O squad baixa os arquivos (com `ferramentas/drive.py` ou, sem credencial, pelo conector) para `<squad>/entrada/<trabalho>/` e segue como no uso local. Os portões você aprova pelo chat, no navegador ou no celular.
4. No fim, a publicação é automática: os comandos principais (`/orcar`, `/estrategia`, `/revisao-trimestral`, `/produto`, `/revisao-produto`, `/analisar`, `/atualizar-analise`) publicam sozinhos assim que a versão é congelada ou o último portão é aprovado, sem você pedir. Para publicar de novo ou manualmente, use `/publicar-drive <squad> <pasta da versão>` (por exemplo `/publicar-drive squad-orcamento projetos/<id>/v1`). Ele envia ao Drive o pacote completo, igual à publicação local: documentos finais, planilha, JSON, CSV, nós, revisões, o índice dos insumos, um manifesto com todos os arquivos e um zip com tudo. A pasta de destino de cada squad está em `ferramentas/squads.json`. Depois ele faz commit de `<squad>/publicados/` na branch da sessão. A máquina da nuvem é descartável: o que não for publicado assim se perde quando a sessão expira.
   Para republicar um pacote que já está commitado numa branch: `/publicar-drive squad-orcamento publicados/<id>/v1`.

## Arquivos grandes (acima de 10 MB)
O conector do Google Drive só baixa arquivos de até 10 MB, e no envio o conteúdo vai dentro da chamada, o que também falha com arquivos grandes. Por isso os squads usam primeiro `ferramentas/drive.py`, que fala direto com a API do Drive, sem limite de tamanho, e só caem no conector quando não há credencial. Para ligar, uma vez:

1. Em console.cloud.google.com, com a sua conta do Google, crie um projeto (por exemplo "Acta Agentes") e ative a **Google Drive API** (APIs e serviços > Biblioteca).
2. Em **Tela de consentimento OAuth** (Google Auth Platform), escolha público externo, preencha nome e e-mail e adicione a sua conta como usuário de teste. Depois clique em **Publicar app** (status "Em produção"). Sem publicar, o Google expira a autorização em 7 dias. Como o app é só seu, não precisa de verificação; na autorização vai aparecer o aviso "app não verificado", e basta seguir em Avançado.
3. Em **Credenciais** > Criar credenciais > ID do cliente OAuth > tipo **App para computador**. Baixe o JSON (`client_secret_....json`).
4. No seu computador, na raiz do `acta-agentes`: `python ferramentas\drive.py autorizar caminho\do\client_secret.json`. O navegador abre; autorize com a conta dona das pastas Acta. O script imprime uma linha JSON.
5. No ambiente de nuvem do projeto (configurações do ambiente, variáveis de ambiente), crie `ACTA_DRIVE_CREDENCIAL` com essa linha inteira como valor. Não cole a linha no chat. Novas sessões já pegam a variável.
6. Teste numa sessão nova: `python ferramentas/drive.py testar` deve mostrar o seu nome e e-mail. Se der erro de rede, o acesso de rede do ambiente está bloqueando o Google: troque para **Full** ou, em **Custom**, libere `www.googleapis.com` e `oauth2.googleapis.com`.

Cuidados: a credencial dá acesso de leitura e escrita a todo o seu Drive, e quem usa o ambiente consegue lê-la; não compartilhe esse ambiente. Para revogar, remova o app em myaccount.google.com/permissions. Planilhas e documentos nativos do Google acima de 10 MB continuam limitados pela própria API de exportação; nesse caso baixe como .xlsx/.docx no Drive e use o arquivo baixado.

Comandos úteis: `python ferramentas/drive.py listar "Acta > Fornecedores"`, `python ferramentas/drive.py baixar "<link ou Acta > pasta>" squad-orcamento/entrada/<trabalho>/`, `python ferramentas/drive.py enviar <arquivo> "Acta > Orçamentos > <projeto>"`.

## Dados sensíveis
Tudo o que entra numa sessão de nuvem passa pela máquina da nuvem e pelo modelo. Para dados com informação pessoal ou de cliente (squad de análise), a opção padrão é rodar no seu computador e acompanhar de qualquer lugar com Remote Control (`/remote-control` na sessão local): os arquivos não saem do seu PC, mas ele precisa ficar ligado.

## Custos e limites
- As sessões de nuvem usam o mesmo limite de uso da sua conta; squads em paralelo consomem proporcionalmente mais, e os supervisores usam Opus.
- Os 100 agentes ficam registrados em toda sessão, e as descrições deles ocupam contexto. O `montar_nuvem.py` encurta cada descrição para a primeira frase.
- A máquina tem cerca de 4 vCPUs, 16 GB de RAM e 30 GB de disco; análises de dados maiores que isso vão melhor no seu computador.
