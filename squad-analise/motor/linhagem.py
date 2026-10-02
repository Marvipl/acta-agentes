"""Linhagem: assinatura de cada elo (arquivo bruto → preparação → análise → insight) e o ambiente da execução.

Uso: python -m motor.linhagem <dv>   → saidas/linhagem.json
"""
import argparse, hashlib, json, platform, sys
from importlib import metadata
from pathlib import Path
from .util import carregar_json, salvar_json, agora

PACOTES = ["duckdb", "pandas", "numpy", "scipy", "statsmodels", "scikit-learn", "pyarrow", "matplotlib", "openpyxl"]


def gerar(dv):
    dv = Path(dv)
    cat = carregar_json(dv / "saidas" / "catalogo.json", {}) or {}
    pip = carregar_json(dv / "saidas" / "pipeline.json", {}) or {}
    reg = carregar_json(dv / "saidas" / "registro.json", {}) or {}
    ins = {p.stem: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((dv / "evidencias").glob("INS-*.json"))}
    versoes = {}
    for p in PACOTES:
        try: versoes[p] = metadata.version(p)
        except Exception: versoes[p] = None
    out = {"gerado_em": agora(), "projeto": (carregar_json(dv / "nos" / "meta.json", {}) or {}).get("projeto_id"),
           "brutos": {a["arquivo"]: a["sha256"] for a in cat.get("arquivos", [])},
           "preparacao": [{"etapa": e["arquivo"], "sha256": e["sha256"], "tabelas": e["tabelas"]} for e in pip.get("etapas", [])],
           "analises": {k: {"script_sha256": v["script_sha256"], "resultado_sha256": v["resultado_sha256"]} for k, v in reg.items()},
           "insights": ins, "ambiente": {"python": sys.version.split()[0], "sistema": platform.platform(), "pacotes": versoes}}
    salvar_json(dv / "saidas" / "linhagem.json", out)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("dv"); x = ap.parse_args(); o = gerar(x.dv)
    print(f"Linhagem: {len(o['brutos'])} arquivo(s), {len(o['preparacao'])} etapa(s), {len(o['analises'])} análise(s), {len(o['insights'])} insight(s).")
