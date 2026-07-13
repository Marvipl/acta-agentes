#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_pauta.py — Gera a pauta/ata de Staff C-Level da Acta Robotics a partir de
um template DOCX real da empresa e de um JSON de conteúdo.

Uso:
    python3 scripts/gerar_pauta.py \
        --template templates/Template_Ata_Staff.docx \
        --json conteudo.json \
        --out Pauta_Staff_2026-07-15.docx

Sem dependências externas (usa apenas stdlib: zipfile, re, json, html, shutil).

O template fornece: logo, estilos, numeração de bullets, cabeçalho/rodapé e
configuração de página. O corpo do documento é 100% reconstruído a partir do JSON.

Esquema do JSON (todas as chaves de seção são opcionais):
{
  "titulo": "PAUTA DE REUNIÃO",
  "subtitulo": "STAFF C-LEVEL",
  "footer_data": "15/07/2026",                       // substitui a data no rodapé
  "info": [["Reunião","Reunião de Staff C-Level"], ["Data","15 de julho de 2026"], ...],
  "participantes": [["Marcus Lima","CEO"], ["Renato Correa","CFO"], ...],
  "secoes": [
    {
      "titulo": "1. Pendências da Semana Anterior",
      "nota": "Follow-up das ações da reunião anterior.",
      "pendencias": [["Vinicius","1 Kappabot disponível","3ª semana de julho"], ...],
      "bullets": ["texto simples", [["Prefixo em negrito: ", true], ["resto do texto.", false]]],
      "blocos": [
        {"subtitulo": "Kappabot", "bullets": [ ... mesmo formato ... ]}
      ],
      "quebra_pagina": false
    }
  ],
  "plano_acao": {"titulo": "5. Plano de Ação",
                 "nota": "Próximos passos definidos na reunião.",
                 "linhas": [["1","Ação","Responsável","Prazo"]],
                 "linhas_vazias": 5},
  "encerramento": "Nada mais havendo a tratar, ...",
  "assinaturas": [["Marcus Lima","CEO"], ...]
}

Um bullet pode ser:
  - string simples: "Texto do bullet."
  - lista de runs: [["Deliberar: ", true], ["texto normal.", false]]  (true = negrito)
"""
import argparse
import html
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

# ---------------------------------------------------------------- primitivas

CELL_B = ('<w:tcBorders><w:top w:val="single" w:sz="1" w:space="0" w:color="DDDDDD"/>'
          '<w:left w:val="single" w:sz="1" w:space="0" w:color="DDDDDD"/>'
          '<w:bottom w:val="single" w:sz="1" w:space="0" w:color="DDDDDD"/>'
          '<w:right w:val="single" w:sz="1" w:space="0" w:color="DDDDDD"/></w:tcBorders>')
CELL_M = ('<w:tcMar><w:top w:w="70" w:type="dxa"/><w:left w:w="130" w:type="dxa"/>'
          '<w:bottom w:w="70" w:type="dxa"/><w:right w:w="130" w:type="dxa"/></w:tcMar>')
TBL_PR = ('<w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
          '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
          '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
          '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
          '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
          '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/></w:tblBorders>'
          '<w:tblCellMar><w:left w:w="10" w:type="dxa"/><w:right w:w="10" w:type="dxa"/></w:tblCellMar>'
          '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" '
          'w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>')

LARANJA = 'EF7E06'
CINZA_ESCURO = '3A3A3A'
PRETO = '1A1A1A'


def esc(t):
    return html.escape(str(t), quote=False)


def run(t, bold=False, color=None, sz=19, italic=False, spacing=None):
    rpr = ''
    if bold:
        rpr += '<w:b/><w:bCs/>'
    if italic:
        rpr += '<w:i/><w:iCs/>'
    if color:
        rpr += f'<w:color w:val="{color}"/>'
    if spacing:
        rpr += f'<w:spacing w:val="{spacing}"/>'
    if sz:
        rpr += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
    rpr = f'<w:rPr>{rpr}</w:rPr>' if rpr else ''
    return f'<w:r>{rpr}<w:t xml:space="preserve">{esc(t)}</w:t></w:r>'


def par(runs, ppr=''):
    if isinstance(runs, str):
        runs = [runs]
    body = ''.join(runs)
    return f'<w:p><w:pPr>{ppr}</w:pPr>{body}</w:p>' if ppr else f'<w:p>{body}</w:p>'


def titulo(t):
    return par(run(t, bold=True, color=PRETO, sz=36),
               '<w:spacing w:before="160" w:after="30"/><w:jc w:val="center"/>')


def subtitulo(t):
    return par(run(t, bold=True, color=LARANJA, sz=22, spacing=60),
               '<w:spacing w:after="220"/><w:jc w:val="center"/>')


def h1(t, pagebreak=False):
    pb = '<w:pageBreakBefore/>' if pagebreak else ''
    return par(run(t, bold=True, color=PRETO, sz=26),
               f'{pb}<w:pBdr><w:bottom w:val="single" w:sz="14" w:space="4" '
               f'w:color="{LARANJA}"/></w:pBdr><w:spacing w:before="300" w:after="120"/>')


def h2(t):
    return (f'<w:p><w:pPr><w:spacing w:before="180" w:after="70"/></w:pPr>'
            f'<w:r><w:rPr><w:b/><w:bCs/><w:color w:val="{LARANJA}"/>'
            f'<w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr><w:t>\u258d</w:t></w:r>'
            f'<w:r><w:rPr><w:b/><w:bCs/><w:color w:val="{CINZA_ESCURO}"/>'
            f'<w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>'
            f'<w:t xml:space="preserve"> {esc(t)}</w:t></w:r></w:p>')


def nota(t):
    return par(run(t, italic=True, color='6B6B6B', sz=19), '<w:spacing w:after="60"/>')


def bullet(conteudo, num_id):
    """conteudo: str ou lista de [texto, bold]."""
    if isinstance(conteudo, str):
        partes = [(conteudo, False)]
    else:
        partes = [(p[0], bool(p[1]) if len(p) > 1 else False) for p in conteudo]
    runs = ''.join(
        f'<w:r>{"<w:rPr><w:b/><w:bCs/></w:rPr>" if b else ""}'
        f'<w:t xml:space="preserve">{esc(t)}</w:t></w:r>'
        for t, b in partes)
    return (f'<w:p><w:pPr><w:pStyle w:val="PargrafodaLista"/>'
            f'<w:numPr><w:ilvl w:val="0"/><w:numId w:val="{num_id}"/></w:numPr>'
            f'<w:spacing w:after="30"/></w:pPr>{runs}</w:p>')


def tabela_info(linhas):
    trs = ''
    for k, v in linhas:
        trs += ('<w:tr>'
                f'<w:tc><w:tcPr><w:tcW w:w="2100" w:type="dxa"/>{CELL_B}'
                '<w:shd w:val="clear" w:color="auto" w:fill="F3F3F3"/>'
                f'{CELL_M}</w:tcPr>{par(run(k, bold=True, color=CINZA_ESCURO))}</w:tc>'
                f'<w:tc><w:tcPr><w:tcW w:w="7260" w:type="dxa"/>{CELL_B}{CELL_M}</w:tcPr>'
                f'{par(run(v))}</w:tc></w:tr>')
    return ('<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/>' + TBL_PR + '</w:tblPr>'
            '<w:tblGrid><w:gridCol w:w="2100"/><w:gridCol w:w="7260"/></w:tblGrid>'
            f'{trs}</w:tbl>')


def tabela_dados(larguras, cabecalho, linhas, cols_centro=()):
    total = sum(larguras)

    def tc(w, conteudo, hdr=False, centro=False):
        shd = '<w:shd w:val="clear" w:color="auto" w:fill="1A1A1A"/>' if hdr else ''
        va = '<w:vAlign w:val="center"/>' if not hdr else ''
        jc = '<w:jc w:val="center"/>' if centro else ''
        r = run(conteudo, bold=hdr, color='FFFFFF' if hdr else None)
        p = f'<w:p><w:pPr>{jc}</w:pPr>{r}</w:p>' if jc else f'<w:p>{r}</w:p>'
        return f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{CELL_B}{shd}{CELL_M}{va}</w:tcPr>{p}</w:tc>'

    trs = ('<w:tr><w:trPr><w:trHeight w:val="220"/><w:tblHeader/></w:trPr>' +
           ''.join(tc(w, h, hdr=True) for w, h in zip(larguras, cabecalho)) + '</w:tr>')
    for linha in linhas:
        trs += ('<w:tr><w:trPr><w:trHeight w:val="441"/></w:trPr>' +
                ''.join(tc(w, c, centro=(i in cols_centro))
                        for i, (w, c) in enumerate(zip(larguras, linha))) + '</w:tr>')
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in larguras)
    return (f'<w:tbl><w:tblPr><w:tblW w:w="{total}" w:type="dxa"/>{TBL_PR}</w:tblPr>'
            f'<w:tblGrid>{grid}</w:tblGrid>{trs}</w:tbl>')


def assinatura(nome, cargo):
    return (f'<w:p><w:pPr><w:spacing w:after="60"/></w:pPr>'
            f'<w:r><w:rPr><w:b/><w:bCs/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>'
            f'<w:t>{esc(nome)}</w:t></w:r>'
            f'<w:r><w:rPr><w:color w:val="6B6B6B"/><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr>'
            f'<w:t xml:space="preserve">   \u2014   {esc(cargo)}</w:t></w:r></w:p>')


# ------------------------------------------------------------- utilitários XML

def acha_num_id_bullet(document_xml, numbering_xml):
    """Encontra um numId do template que renderize como bullet."""
    usados = re.findall(r'<w:numId w:val="(\d+)"/>', document_xml)
    if usados:
        # usa o numId mais frequente no documento original (é o bullet padrão da ata)
        return max(set(usados), key=usados.count)
    m = re.search(r'<w:numId w:val="(\d+)"', numbering_xml or '')
    return m.group(1) if m else '1'


def substitui_data_rodape(footer_xml, nova_data):
    """Troca a data dd/mm/aaaa do rodapé, mesmo se estiver fragmentada em runs."""
    # 1) junta o texto de todos os runs do parágrafo para localizar a data
    def merge_paragraph(par_xml):
        if '<w:drawing' in par_xml:
            return par_xml
        runs = re.findall(r'<w:r\b[^>]*>(?:(?!</w:r>).)*</w:r>', par_xml, re.S)
        if len(runs) < 2:
            return par_xml
        merged, buf_rpr, buf_txt = [], None, None
        for r in runs:
            m_rpr = re.search(r'<w:rPr>.*?</w:rPr>', r, re.S)
            rpr = m_rpr.group(0) if m_rpr else ''
            # só é mesclável se o conteúdo do run (fora o rPr) for exatamente um <w:t>
            interno = re.sub(r'^<w:r\b[^>]*>', '', r[:-len('</w:r>')])
            interno = re.sub(r'^<w:rPr>.*?</w:rPr>', '', interno, flags=re.S)
            m_t = re.fullmatch(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', interno.strip(), re.S)
            if m_t is None:
                if buf_txt is not None:
                    merged.append((buf_rpr, buf_txt))
                    buf_rpr = buf_txt = None
                merged.append((None, r))  # run não textual, mantém como está
                continue
            txt = m_t.group(1)
            if buf_txt is not None and rpr == buf_rpr:
                buf_txt += txt
            else:
                if buf_txt is not None:
                    merged.append((buf_rpr, buf_txt))
                buf_rpr, buf_txt = rpr, txt
        if buf_txt is not None:
            merged.append((buf_rpr, buf_txt))
        novo = ''
        for rpr, txt in merged:
            if rpr is None:
                novo += txt
            else:
                novo += f'<w:r>{rpr}<w:t xml:space="preserve">{txt}</w:t></w:r>'
        # reconstrói o parágrafo: mantém pPr, troca os runs
        m_ppr = re.search(r'<w:pPr>.*?</w:pPr>', par_xml, re.S)
        ppr = m_ppr.group(0) if m_ppr else ''
        abre = re.match(r'<w:p\b[^>]*>', par_xml).group(0)
        return f'{abre}{ppr}{novo}</w:p>'

    footer_xml = re.sub(r'<w:p\b[^>]*>(?:(?!</w:p>).)*</w:p>',
                        lambda m: merge_paragraph(m.group(0)), footer_xml, flags=re.S)
    footer_xml, n = re.subn(r'\d{1,2}/\d{2}/\d{4}', nova_data, footer_xml)
    if n == 0:
        print('AVISO: data nao encontrada no rodape; rodape mantido sem alteracao.',
              file=sys.stderr)
    return footer_xml


# --------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--template', required=True)
    ap.add_argument('--json', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    spec = json.loads(Path(args.json).read_text(encoding='utf-8'))

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        with zipfile.ZipFile(args.template) as z:
            z.extractall(tmp)

        doc_path = tmp / 'word' / 'document.xml'
        src = doc_path.read_text(encoding='utf-8')
        i0 = src.find('<w:body>') + len('<w:body>')
        i1 = src.find('</w:body>')
        corpo_original = src[i0:i1]
        prefixo, sufixo = src[:i0], src[i1:]

        m_logo = re.search(r'<w:p\b(?:(?!</w:p>).)*<w:drawing(?:(?!</w:p>).)*</w:p>',
                           corpo_original, re.S)
        logo = m_logo.group(0) if m_logo else ''
        m_sect = re.search(r'<w:sectPr\b.*?</w:sectPr>', corpo_original, re.S)
        sect = m_sect.group(0) if m_sect else ''

        num_path = tmp / 'word' / 'numbering.xml'
        numbering = num_path.read_text(encoding='utf-8') if num_path.exists() else ''
        NUM_ID = acha_num_id_bullet(corpo_original, numbering)

        D = [logo,
             titulo(spec.get('titulo', 'PAUTA DE REUNIÃO')),
             subtitulo(spec.get('subtitulo', 'STAFF C-LEVEL')),
             tabela_info(spec.get('info', []))]

        if spec.get('participantes'):
            D.append(h1('Participantes'))
            linhas = [[n, c, '(     )'] for n, c in spec['participantes']]
            D.append(tabela_dados([4200, 3400, 1760],
                                  ['Participante', 'Cargo', 'Presença'],
                                  linhas, cols_centro=(2,)))

        for sec in spec.get('secoes', []):
            D.append(h1(sec['titulo'], pagebreak=bool(sec.get('quebra_pagina'))))
            if sec.get('nota'):
                D.append(nota(sec['nota']))
            if sec.get('pendencias'):
                D.append(tabela_dados([1954, 5551, 1955],
                                      ['Responsável', 'Pendência', 'Prazo'],
                                      sec['pendencias']))
            for b in sec.get('bullets', []):
                D.append(bullet(b, NUM_ID))
            for bloco in sec.get('blocos', []):
                D.append(h2(bloco['subtitulo']))
                for b in bloco.get('bullets', []):
                    D.append(bullet(b, NUM_ID))

        pa = spec.get('plano_acao')
        if pa:
            D.append(h1(pa.get('titulo', 'Plano de Ação'),
                        pagebreak=bool(pa.get('quebra_pagina', True))))
            if pa.get('nota'):
                D.append(nota(pa['nota']))
            linhas = list(pa.get('linhas', []))
            for i in range(pa.get('linhas_vazias', 0)):
                linhas.append([str(len(linhas) + 1), '', ' ', ' '])
            D.append(tabela_dados([567, 5244, 1954, 1723],
                                  ['#', 'Ação', 'Responsável', 'Prazo'],
                                  linhas, cols_centro=(0,)))

        if spec.get('encerramento'):
            D.append(par(run('Encerramento e Aprovação', bold=True, color=PRETO, sz=24),
                         f'<w:pBdr><w:bottom w:val="single" w:sz="14" w:space="4" '
                         f'w:color="{LARANJA}"/></w:pBdr>'
                         '<w:spacing w:before="300" w:after="40"/>'))
            D.append(par(run(spec['encerramento']),
                         '<w:spacing w:before="120" w:after="200"/>'))
        for nome, cargo in spec.get('assinaturas', []):
            D.append(assinatura(nome, cargo))

        doc_path.write_text(prefixo + ''.join(D) + sect + sufixo, encoding='utf-8')

        if spec.get('footer_data'):
            for fpath in sorted((tmp / 'word').glob('footer*.xml')):
                fx = fpath.read_text(encoding='utf-8')
                fpath.write_text(substitui_data_rodape(fx, spec['footer_data']),
                                 encoding='utf-8')

        out = Path(args.out)
        if out.exists():
            out.unlink()
        with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
            for f in sorted(tmp.rglob('*')):
                if f.is_file():
                    z.write(f, f.relative_to(tmp).as_posix())
    print(f'OK: {args.out}')


if __name__ == '__main__':
    main()
