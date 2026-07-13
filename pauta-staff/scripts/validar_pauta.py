#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validar_pauta.py — Abre um DOCX e verifica se é uma pauta/ata de Staff C-Level
da Acta Robotics, extraindo a data da reunião do próprio conteúdo.

Critérios:
  - título/subtítulo (primeiros parágrafos) contém "STAFF" ou "C-LEVEL"
    (ignora acentos, maiúsculas, espaços e hífens — aceita "C LEVEL", "CLEVEL");
  - existe uma linha "Data" na tabela de informações com data interpretável
    ("08 de julho de 2026", "08/07/2026" ou "22 / 07 / 2026").

Saída: JSON em stdout, ex.:
  {"valido": true, "titulo_ok": true, "data_iso": "2026-07-08",
   "data_texto": "08 de julho de 2026", "motivo": null}

Exit code 0 se válido, 2 se inválido, 1 se erro de leitura.

Uso:
    python3 scripts/validar_pauta.py arquivo.docx [--tipo staff|conselho]

--tipo staff (padrao): titulo deve conter STAFF ou C-LEVEL.
--tipo conselho: titulo deve conter CONSELHO.
"""
import json
import re
import sys
import unicodedata
import zipfile

MESES = {
    'janeiro': 1, 'fevereiro': 2, 'marco': 3, 'abril': 4, 'maio': 5,
    'junho': 6, 'julho': 7, 'agosto': 8, 'setembro': 9, 'outubro': 10,
    'novembro': 11, 'dezembro': 12,
}


def normaliza(t):
    t = unicodedata.normalize('NFKD', t)
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'[\s\-_]+', '', t).upper()


def texto_paragrafo(p_xml):
    from html import unescape
    return unescape(''.join(
        re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', p_xml, re.S)))


def extrai_data(texto):
    """Devolve (iso, texto_original) ou (None, None)."""
    t = unicodedata.normalize('NFKD', texto)
    t = ''.join(c for c in t if not unicodedata.combining(c)).lower()
    m = re.search(r'(\d{1,2})\s*de\s*([a-z]+)\s*de\s*(\d{4})', t)
    if m and m.group(2) in MESES:
        d, mes, a = int(m.group(1)), MESES[m.group(2)], int(m.group(3))
        return f'{a:04d}-{mes:02d}-{d:02d}', texto.strip()
    m = re.search(r'(\d{1,2})\s*/\s*(\d{1,2})\s*/\s*(\d{4})', t)
    if m:
        d, mes, a = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if 1 <= mes <= 12 and 1 <= d <= 31:
            return f'{a:04d}-{mes:02d}-{d:02d}', texto.strip()
    return None, None


def main(path, tipo="staff"):
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read('word/document.xml').decode('utf-8')
    except Exception as e:
        print(json.dumps({'valido': False, 'motivo': f'erro de leitura: {e}'}))
        return 1

    corpo = xml[xml.find('<w:body>'):xml.find('</w:body>')]
    elementos = re.findall(
        r'<w:tbl>.*?</w:tbl>|<w:p\b[^>]*/>|<w:p\b[^>]*>.*?</w:p>', corpo, re.S)

    # 1) título: procura STAFF/C-LEVEL nos primeiros parágrafos (antes da 1ª tabela)
    titulo_ok = False
    for el in elementos[:8]:
        if el.startswith('<w:tbl>'):
            break
        t = normaliza(texto_paragrafo(el))
        if tipo == 'conselho':
            if 'CONSELHO' in t:
                titulo_ok = True
                break
        elif 'STAFF' in t or 'CLEVEL' in t:
            titulo_ok = True
            break

    # 2) data: procura linha "Data | ..." nas tabelas iniciais
    data_iso, data_texto = None, None
    for el in elementos:
        if not el.startswith('<w:tbl>'):
            continue
        for tr in re.findall(r'<w:tr\b.*?</w:tr>', el, re.S):
            celulas = [texto_paragrafo(tc).strip()
                       for tc in re.findall(r'<w:tc>.*?</w:tc>', tr, re.S)]
            if len(celulas) >= 2 and normaliza(celulas[0]) == 'DATA':
                data_iso, data_texto = extrai_data(celulas[1])
                break
        if data_iso:
            break

    valido = titulo_ok and data_iso is not None
    motivo = None
    if not titulo_ok:
        motivo = ('titulo nao contem CONSELHO' if tipo == 'conselho'
                  else 'titulo nao contem STAFF/C-LEVEL')
    elif not data_iso:
        motivo = 'linha Data nao encontrada ou data nao interpretavel'

    print(json.dumps({'valido': valido, 'titulo_ok': titulo_ok,
                      'data_iso': data_iso, 'data_texto': data_texto,
                      'motivo': motivo}, ensure_ascii=False))
    return 0 if valido else 2


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    tipo = 'staff'
    if '--tipo' in sys.argv:
        tipo = sys.argv[sys.argv.index('--tipo') + 1]
        args = [a for a in args if a != tipo]
    if len(args) != 1 or tipo not in ('staff', 'conselho'):
        print(__doc__)
        sys.exit(1)
    sys.exit(main(args[0], tipo))
