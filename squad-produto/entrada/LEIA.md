# Pasta de entrada dos briefings

Coloque aqui, pelo Windows Explorer, uma subpasta por orçamento com os documentos do cliente:

```
entrada\ocean\
    apresentacao.pdf
    planta_terreo.pdf
    email_briefing.eml
    requisitos.xlsx
```

Depois, no Claude Code:

```
/orcar rapido "Cliente" "Projeto" entrada\ocean
```

Também vale apontar direto para uma pasta do Google Drive para desktop, entre aspas:
`/orcar rapido "Cliente" "Projeto" "G:\Meu Drive\Acta\Clientes\Ocean"`

Os arquivos são **copiados** para o orçamento (`projetos\<id>\v1\insumos\`); esta pasta não é alterada e fica fora do git.

Formatos lidos: PDF (inclusive digitalizado, por imagem), Word (.docx), Excel (.xlsx), PowerPoint (.pptx), e-mail (.eml), imagens, texto, CSV e .zip.
Formatos antigos (.doc, .xls, .ppt) e e-mails do Outlook (.msg): salve como .docx/.xlsx/.pptx/.pdf/.eml antes.
