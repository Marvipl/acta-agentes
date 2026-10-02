"""Executa as etapas de preparação em ordem (etapas/*.sql e etapas/*.py) sobre as tabelas base_*.

Cada etapa cria tabelas prep_*; o motor registra contagem de linhas e impressão digital de cada uma, salva em
dados/preparados/<tabela>.parquet e grava saidas/pipeline.json.
Etapa .py recebe `con` (DuckDB), `pd` e `np` e roda como script.

Uso: python -m motor.pipeline <dv>
"""
import argparse, hashlib, sys
from pathlib import Path
from .util import salvar_json, agora
from .dados import conectar, tabelas, impressao
from . import privacidade


def rodar(dv):
    dv = Path(dv)
    privacidade.aplicar(dv)
    (dv / "dados" / "preparados").mkdir(parents=True, exist_ok=True)
    con = conectar(dv)
    for t in tabelas(con, "prep_"):
        con.execute(f'drop table "{t}"')
    etapas = sorted([p for p in (dv / "etapas").glob("*") if p.suffix in (".sql", ".py")])
    registro = {"em": agora(), "etapas": [], "base": {t: impressao(con, t) for t in tabelas(con, "base_")}}
    for p in etapas:
        antes = set(tabelas(con)); cod = p.read_text(encoding="utf-8")
        try:
            if p.suffix == ".sql":
                con.execute(cod)
            else:
                import pandas as pd, numpy as np
                exec(compile(cod, str(p), "exec"), {"con": con, "pd": pd, "np": np, "__name__": "__etapa__"})
        except Exception as e:
            con.close(); sys.exit(f"Etapa {p.name} falhou: {e}")
        novas = sorted(set(tabelas(con)) - antes)
        fora = [t for t in novas if not t.startswith("prep_")]
        if fora:
            con.close(); sys.exit(f"Etapa {p.name} criou tabelas fora do padrão prep_*: {fora}")
        saidas = {}
        for t in novas:
            saidas[t] = impressao(con, t)
            arq = (dv / "dados" / "preparados" / f"{t}.parquet").as_posix()
            con.execute(f"copy \"{t}\" to '{arq}' (format parquet)")
        registro["etapas"].append({"arquivo": p.name, "sha256": hashlib.sha256(cod.encode()).hexdigest(), "tabelas": saidas})
        print(f"{p.name}: " + ", ".join(f"{t} ({v['linhas']} linhas)" for t, v in saidas.items()))
    con.close()
    salvar_json(dv / "saidas" / "pipeline.json", registro)
    return registro


def atualizado(dv):
    from .util import carregar_json
    dv = Path(dv); reg = carregar_json(dv / "saidas" / "pipeline.json")
    if not reg:
        return False
    atuais = {p.name: hashlib.sha256(p.read_text(encoding="utf-8").encode()).hexdigest() for p in (dv / "etapas").glob("*") if p.suffix in (".sql", ".py")}
    return atuais == {e["arquivo"]: e["sha256"] for e in reg["etapas"]}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("dv"); x = ap.parse_args(); rodar(x.dv)
