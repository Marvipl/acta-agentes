"""Preenche os entregáveis (*.md.tpl) com os números do motor.

Os textos usam variáveis {{caminho.no.resumo}}, por exemplo {{fmt.preco_sugerido}} ou {{meta.cliente}}.
Assim nenhum número é digitado à mão e todos os documentos batem com a planilha.
"""
import re
from pathlib import Path
from .util import salvar_json

PADRAO = re.compile(r"\{\{\s*([\w\.]+)\s*\}\}")


def _resolver(d, caminho):
    cur = d
    for p in caminho.split("."):
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        elif isinstance(cur, list) and p.isdigit() and int(p) < len(cur):
            cur = cur[int(p)]
        else:
            return None
    return cur


def renderizar(dv, resumo):
    dv = Path(dv)
    faltando = {}
    for tpl in sorted((dv / "entregaveis").glob("*.md.tpl")):
        txt = tpl.read_text(encoding="utf-8")
        falta = []
        def troca(m):
            v = _resolver(resumo, m.group(1))
            if v is None:
                falta.append(m.group(1)); return "[●]"
            return str(v)
        out = PADRAO.sub(troca, txt)
        nome = tpl.name[:-4]  # remove .tpl
        (dv / "saidas" / nome).write_text(out, encoding="utf-8")
        faltando[nome] = sorted(set(falta))
    salvar_json(dv / "saidas" / "render_status.json", {"faltando": faltando})
    return faltando
