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
2. Habilite o conector do Google Drive na sessão para buscar as entradas e, se quiser, devolver os entregáveis ao Drive.
3. Rode o comando do squad, por exemplo:
   - `/orcar completo "Cliente" "Projeto" <pasta do Drive com os documentos>`
   - `/estrategia plano "2027" "Plano estratégico 2027" <pasta do Drive>`
   - `/produto oportunidade "Segmento" "Produto" <pasta do Drive>`
   - `/analisar padrao "<objetivo>" <pasta do Drive com os dados>`
   O squad baixa os arquivos pelo conector para `<squad>/entrada/<trabalho>/` e segue como no uso local. Os portões você aprova pelo chat, no navegador ou no celular.
4. No fim, a publicação é automática: os comandos principais (`/orcar`, `/estrategia`, `/revisao-trimestral`, `/produto`, `/revisao-produto`, `/analisar`, `/atualizar-analise`) publicam sozinhos assim que a versão é congelada ou o último portão é aprovado, sem você pedir. Para publicar de novo ou manualmente, use `/publicar-drive <squad> <pasta da versão>` (por exemplo `/publicar-drive squad-orcamento projetos/<id>/v1`). Ele envia ao Drive o pacote completo, igual à publicação local: documentos finais, planilha, JSON, CSV, nós, revisões, o índice dos insumos, um manifesto com todos os arquivos e um zip com tudo. A pasta de destino de cada squad está em `ferramentas/squads.json`. Depois ele faz commit de `<squad>/publicados/` na branch da sessão. A máquina da nuvem é descartável: o que não for publicado assim se perde quando a sessão expira.
   Para republicar um pacote que já está commitado numa branch: `/publicar-drive squad-orcamento publicados/<id>/v1`.

## Dados sensíveis
Tudo o que entra numa sessão de nuvem passa pela máquina da nuvem e pelo modelo. Para dados com informação pessoal ou de cliente (squad de análise), a opção padrão é rodar no seu computador e acompanhar de qualquer lugar com Remote Control (`/remote-control` na sessão local): os arquivos não saem do seu PC, mas ele precisa ficar ligado.

## Custos e limites
- As sessões de nuvem usam o mesmo limite de uso da sua conta; squads em paralelo consomem proporcionalmente mais, e os supervisores usam Opus.
- Os 100 agentes ficam registrados em toda sessão, e as descrições deles ocupam contexto. O `montar_nuvem.py` encurta cada descrição para a primeira frase.
- A máquina tem cerca de 4 vCPUs, 16 GB de RAM e 30 GB de disco; análises de dados maiores que isso vão melhor no seu computador.
