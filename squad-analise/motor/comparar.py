"""Compara os resultados de duas versões da mesma análise (por exemplo, período novo com /atualizar-analise).

Uso: python -m motor.comparar <dv_anterior> <dv_novo>   → saidas/comparacao.md na versão nova
"""
import argparse
from pathlib import Path
from .util import carregar_json


def comparar(ant, novo):
    ant, novo = Path(ant), Path(novo); l = [f"# O que mudou entre {ant.name} e {novo.name}", "", "| Análise | Valor | Antes | Agora | Variação | Incerteza se sobrepõe? |", "|---|---|---|---|---|---|"]
    for p in sorted((novo / "saidas" / "analises").glob("*/resultado.json")):
        a = carregar_json(ant / "saidas" / "analises" / p.parent.name / "resultado.json", {}) or {}
        for k, v in (carregar_json(p).get("valores") or {}).items():
            o = (a.get("valores") or {}).get(k)
            if not o:
                l.append(f"| {p.parent.name} | {k} | — | {v['valor']:.4g} | nova | — |"); continue
            var = (v["valor"] - o["valor"]) / abs(o["valor"]) if o["valor"] else None
            ia, ib = o.get("incerteza") or {}, v.get("incerteza") or {}
            sob = "—" if not (ia and ib) else ("sim" if ia["inferior"] <= ib["superior"] and ib["inferior"] <= ia["superior"] else "não: mudança real")
            l.append(f"| {p.parent.name} | {k} | {o['valor']:.4g} | {v['valor']:.4g} | {('%+.1f%%' % (var * 100)) if var is not None else '—'} | {sob} |")
    (novo / "saidas" / "comparacao.md").write_text("\n".join(l) + "\n", encoding="utf-8")
    return l


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("anterior"); ap.add_argument("novo"); x = ap.parse_args()
    print("\n".join(comparar(x.anterior, x.novo)))
