---
description: "Publica no Google Drive o pacote completo de uma versão: documentos finais e metadados (JSON, CSV, planilha, nós, revisões), igual à publicação local"
argument-hint: <squad> <pasta da versão, relativa ao squad>
---
1. Rode `python ferramentas/publicar_nuvem.py $ARGUMENTS`. Ele monta `<squad>/publicados/<projeto>/v<n>/` com as mesmas subpastas da publicação local, o `manifesto_publicacao.json` e um zip com tudo.
2. Envie com `python ferramentas/drive.py publicar <squad>/publicados/<projeto>/v<n>/manifesto_publicacao.json`. Ele cria só as pastas que faltam em `pasta_drive`, envia todos os arquivos do manifesto e o próprio manifesto sem limite de tamanho e sem converter formatos, substitui os de mesmo nome e confere no Drive nomes e tamanhos. Se terminar com pendências, rode de novo uma vez e informe o que continuar faltando.
3. Só se o passo 2 sair com código 3 (sem `ACTA_DRIVE_CREDENCIAL`), use o conector do Google Drive: encontre cada nível de `pasta_drive` e crie só o que não existir (nunca pasta duplicada); envie **todos** os arquivos de `arquivos`, recriando as subpastas, mais o `manifesto_publicacao.json`, com o tipo do manifesto e `disableConversionToGoogleType`; substitua os de mesmo nome e caminho.
4. Pelo conector, arquivos acima de 10 MB costumam falhar. Não insista: liste nome e tamanho como pendência, diga que eles estão no zip e no commit de `publicados/`, e lembre Marcus de configurar `ACTA_DRIVE_CREDENCIAL` (NUVEM.md, Arquivos grandes).
5. Pelo conector, confira: liste cada pasta no Drive e compare nomes e quantidades com o manifesto. Reenvie o que faltar, no máximo duas tentativas por arquivo.
6. Faça commit e push de `<squad>/publicados/` na branch da sessão.
7. Responda com o link da pasta da versão no Drive, o total enviado por subpasta e qualquer pendência.
