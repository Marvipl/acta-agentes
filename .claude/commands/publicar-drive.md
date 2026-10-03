---
description: "Publica no Google Drive o pacote completo de uma versão: documentos finais e metadados (JSON, CSV, planilha, nós, revisões), igual à publicação local"
argument-hint: <squad> <pasta da versão, relativa ao squad>
---
1. Rode `python ferramentas/publicar_nuvem.py $ARGUMENTS`. Ele monta `<squad>/publicados/<projeto>/v<n>/` com as mesmas subpastas da publicação local, o `manifesto_publicacao.json` e um zip com tudo.
2. Leia o manifesto: `pasta_drive` é o destino (por exemplo `Acta > Orçamentos > <projeto> > v1`). Com o conector do Google Drive, encontre cada nível dessa pasta e crie só o que não existir; nunca crie pasta duplicada.
3. Envie **todos** os arquivos listados em `arquivos`, recriando as subpastas (`saidas/`, `nos/`, `revisoes/`, `insumos/` e as demais do manifesto), mais o próprio `manifesto_publicacao.json`. Use o tipo do manifesto e mantenha o formato original: não converta JSON, CSV, MD ou XLSX para Google Docs ou Planilhas.
4. Se a pasta da versão já tiver arquivos de uma publicação anterior, substitua os que têm o mesmo nome e caminho.
5. Confira: liste cada pasta no Drive e compare nomes e quantidades com o manifesto. Reenvie o que faltar. Se um arquivo não subir depois de duas tentativas, informe nome, tamanho e erro, e confirme que ele está dentro do zip enviado.
6. Faça commit e push de `<squad>/publicados/` na branch da sessão.
7. Responda com o link da pasta da versão no Drive, o total enviado por subpasta e qualquer pendência.
