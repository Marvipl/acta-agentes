"""Pseudonimização com chave local: cria as tabelas base_* a partir das raw_*, trocando colunas pessoais por códigos.

A chave fica só em config/chave_local.key (fora do git). O mesmo valor gera sempre o mesmo código, então a
análise é reproduzível; a correspondência código → original fica em dados/privado/ (fora do git) para quem
tiver autorização voltar ao original.

Uso: python -m motor.privacidade <dv>
Colunas tratadas: as listadas em nos/qualidade.json → pseudonimizar; enquanto esse nó não existir, todas as
colunas com dado pessoal provável no perfil. Colunas em excluir_colunas saem das tabelas base_*.
"""
import argparse, secrets
from pathlib import Path
from .util import RAIZ, carregar_json, salvar_json, config, agora
from .dados import conectar, tabelas

CHAVE = RAIZ / "config" / "chave_local.key"


def chave():
    if not CHAVE.exists():
        CHAVE.parent.mkdir(parents=True, exist_ok=True)
        CHAVE.write_text(secrets.token_hex(32), encoding="utf-8")
    return CHAVE.read_text(encoding="utf-8").strip()


def colunas_alvo(dv):
    q = carregar_json(Path(dv) / "nos" / "qualidade.json", {}) or {}
    if q and not q.get("_template") and q.get("pseudonimizar") is not None:
        alvo = {(x["tabela"], x["coluna"]) for x in q.get("pseudonimizar", []) if x.get("tabela") and x.get("coluna")}
    else:
        p = carregar_json(Path(dv) / "saidas" / "perfil.json", {}) or {}
        alvo = {(t, c["coluna"]) for t, d in (p.get("tabelas") or {}).items() for c in d["colunas"] if c.get("pessoal")}
    excl = {(x["tabela"], x["coluna"]) for x in (q.get("excluir_colunas") or []) if x.get("tabela") and x.get("coluna")} if q and not q.get("_template") else set()
    return alvo, excl


def aplicar(dv):
    dv = Path(dv); cfg = config().get("privacidade", {})
    ativa = cfg.get("ativa", True) or not cfg.get("desligada_autorizada_por")
    alvo, excl = colunas_alvo(dv) if ativa else (set(), set())
    k = chave().replace("'", "")
    con = conectar(dv); feito = {}
    (dv / "dados" / "privado").mkdir(parents=True, exist_ok=True)
    for raw in tabelas(con, "raw_"):
        base = "base_" + raw[4:]
        cols = [r[0] for r in con.execute(f"select column_name from information_schema.columns where table_name='{raw}' order by ordinal_position").fetchall()]
        sel = []
        for c in cols:
            if (raw, c) in excl:
                continue
            if (raw, c) in alvo:
                tok = f"case when \"{c}\" is null then null else 'P_' || substr(sha256('{k}' || '|{raw}|{c}|' || cast(\"{c}\" as varchar)), 1, 16) end"
                sel.append(f'{tok} as "{c}"')
                arq = (dv / "dados" / "privado" / f"correspondencia_{raw}_{c}.parquet").as_posix()
                con.execute(f"copy (select distinct cast(\"{c}\" as varchar) as original, {tok} as codigo from \"{raw}\" where \"{c}\" is not null) to '{arq}' (format parquet)")
                feito.setdefault(raw, []).append(c)
            else:
                sel.append(f'"{c}"')
        con.execute(f'create or replace table "{base}" as select {", ".join(sel)} from "{raw}"')
    con.close()
    salvar_json(dv / "saidas" / "privacidade.json", {"em": agora(), "ativa": bool(ativa), "pseudonimizadas": feito,
                                                     "excluidas": sorted(f"{t}.{c}" for t, c in excl)})
    return feito


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("dv"); x = ap.parse_args()
    f = aplicar(x.dv)
    print("Pseudonimizadas: " + (", ".join(f"{t}.{c}" for t, cs in f.items() for c in cs) or "nenhuma") + ". Analise sempre as tabelas base_* ou prep_*.")
