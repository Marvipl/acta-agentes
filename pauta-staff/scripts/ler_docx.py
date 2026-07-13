#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ler_docx.py — Extrai o texto de um DOCX (parágrafos e tabelas) sem dependências
externas. Usado pela rotina para ler a pauta/ata anterior baixada do Slack.

Uso:
    python3 scripts/ler_docx.py arquivo.docx
"""
import re
import signal
import sys
import zipfile

try:  # evita BrokenPipeError quando a saída é cortada (ex.: | head)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (AttributeError, ValueError):
    pass
from html import unescape


def texto_paragrafo(p_xml):
    return unescape(''.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', p_xml, re.S)))


def main(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read('word/document.xml').decode('utf-8')

    corpo = xml[xml.find('<w:body>'):xml.find('</w:body>')]
    # percorre elementos de nível superior na ordem do documento
    pos = 0
    for m in re.finditer(r'<w:tbl>.*?</w:tbl>|<w:p\b[^>]*/>|<w:p\b[^>]*>.*?</w:p>',
                         corpo, re.S):
        el = m.group(0)
        if el.startswith('<w:tbl>'):
            print('--- TABELA ---')
            for tr in re.findall(r'<w:tr\b.*?</w:tr>', el, re.S):
                celulas = [texto_paragrafo(tc).strip()
                           for tc in re.findall(r'<w:tc>.*?</w:tc>', tr, re.S)]
                print(' | '.join(celulas))
            print('--- FIM TABELA ---')
        else:
            t = texto_paragrafo(el).strip()
            if t:
                print(t)
        pos = m.end()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
