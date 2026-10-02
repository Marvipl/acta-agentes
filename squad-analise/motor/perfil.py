"""Perfil automático das tabelas brutas (resumo do DuckDB), dados pessoais prováveis, chaves e ligações entre tabelas.

Uso: python -m motor.perfil <dv>   → saidas/perfil.json e saidas/perfil.md (este é o que os agentes leem)
Valores de colunas com cara de dado pessoal são mascarados no perfil.
"""
import argparse, json, re
from pathlib import Path
from .util import salvar_json, agora
from .dados import conectar, tabelas

NOME_PESSOAL = re.compile(r"(cpf|rg\b|cnh|e-?mail|telefone|celular|fone|whats|nome|name|endere|logradouro|cep|nascimento|placa)", re.I)
VALOR = {"cpf": re.compile(r"^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$"), "email": re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", re.I),
         "telefone": re.compile(r"^\(?\d{2}\)?\s?9?\d{4}-?\d{4}$"), "cnpj": re.compile(r"^\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}$")}


def _pessoal(con, t, c, tipo):
    motivos = []
    if NOME_PESSOAL.search(c):
        motivos.append("nome da coluna")
    if "VARCHAR" in tipo.upper():
        amostra = [str(r[0]).strip() for r in con.execute(f'select distinct "{c}" from "{t}" where "{c}" is not null limit 200').fetchall()]
        for k, rx in VALOR.items():
            if amostra and sum(1 for v in amostra if rx.match(v)) / len(amostra) >= 0.6:
                motivos.append(f"valores com formato de {k}")
    return motivos


def perfilar(dv):
    dv = Path(dv); con = conectar(dv); out = {"gerado_em": agora(), "tabelas": {}, "ligacoes": []}
    for t in tabelas(con, "raw_"):
        df = con.execute(f'summarize "{t}"').df()
        n = con.execute(f'select count(*) from "{t}"').fetchone()[0]
        cols = []
        for _, r in df.iterrows():
            c, tipo = r["column_name"], str(r["column_type"])
            pes = _pessoal(con, t, c, tipo)
            nulos = float(str(r["null_percentage"]).replace("%", "") or 0) / 100 if r["null_percentage"] is not None else 0.0
            uniq = int(r["approx_unique"]) if r["approx_unique"] is not None else None
            cols.append({"coluna": c, "tipo": tipo, "nulos_pct": round(nulos, 4), "distintos_aprox": uniq,
                         "min": None if pes else (None if r["min"] is None else str(r["min"])), "max": None if pes else (None if r["max"] is None else str(r["max"])),
                         "media": None if r["avg"] is None or pes else str(r["avg"]), "desvio": None if r["std"] is None or pes else str(r["std"]),
                         "q25": None if pes else (None if r["q25"] is None else str(r["q25"])), "q50": None if pes else (None if r["q50"] is None else str(r["q50"])),
                         "q75": None if pes else (None if r["q75"] is None else str(r["q75"])),
                         "chave_candidata": bool(n and uniq is not None and uniq >= 0.98 * n and nulos == 0), "pessoal": pes})
        dup = con.execute(f'select count(*) - count(distinct t) from "{t}" t').fetchone()[0]
        out["tabelas"][t] = {"linhas": int(n), "duplicadas": int(dup), "colunas": cols}
    nomes = list(out["tabelas"])
    for i, a in enumerate(nomes):
        for b in nomes[i + 1:]:
            ca = {c["coluna"].lower(): c["coluna"] for c in out["tabelas"][a]["colunas"]}
            cb = {c["coluna"].lower(): c["coluna"] for c in out["tabelas"][b]["colunas"]}
            for k in set(ca) & set(cb):
                try:
                    tot, achou = con.execute(f'select count(distinct x."{ca[k]}"), count(distinct y."{cb[k]}") from (select distinct "{ca[k]}" from "{a}") x left join (select distinct "{cb[k]}" from "{b}") y on x."{ca[k]}" = y."{cb[k]}"').fetchone()
                    out["ligacoes"].append({"de": f"{a}.{ca[k]}", "para": f"{b}.{cb[k]}", "cobertura": round(achou / tot, 4) if tot else None})
                except Exception:
                    pass
    con.close()
    salvar_json(dv / "saidas" / "perfil.json", out)
    (dv / "saidas" / "perfil.md").write_text(_md(out), encoding="utf-8")
    return out


def _md(p):
    l = ["# Perfil dos dados", "", "Gerado pelo motor. Colunas com dado pessoal provável têm valores mascarados.", ""]
    for t, d in p["tabelas"].items():
        l += [f"## {t}", "", f"{d['linhas']} linhas · {d['duplicadas']} linhas duplicadas", "", "| Coluna | Tipo | Nulos | Distintos | Mín | Mediana | Máx | Observação |", "|---|---|---|---|---|---|---|---|"]
        for c in d["colunas"]:
            obs = "; ".join(filter(None, ["chave candidata" if c["chave_candidata"] else "", ("PESSOAL? " + ", ".join(c["pessoal"])) if c["pessoal"] else ""]))
            l.append(f"| {c['coluna']} | {c['tipo']} | {c['nulos_pct']:.1%} | {c['distintos_aprox']} | {c['min'] if c['min'] is not None else '—'} | {c['q50'] if c['q50'] is not None else '—'} | {c['max'] if c['max'] is not None else '—'} | {obs} |")
        l.append("")
    if p["ligacoes"]:
        l += ["## Ligações prováveis entre tabelas", "", "| De | Para | Cobertura |", "|---|---|---|"] + [f"| {x['de']} | {x['para']} | {x['cobertura']:.0%} |" if x["cobertura"] is not None else f"| {x['de']} | {x['para']} | — |" for x in p["ligacoes"]]
    return "\n".join(l) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("dv"); x = ap.parse_args()
    p = perfilar(x.dv)
    pes = [(t, c["coluna"]) for t, d in p["tabelas"].items() for c in d["colunas"] if c["pessoal"]]
    print(f"{len(p['tabelas'])} tabela(s) perfiladas. Colunas com dado pessoal provável: {pes or 'nenhuma'}")
