"""Auditoria de reprodutibilidade: refaz tudo a partir dos dados brutos numa cópia limpa e compara os números.

Uso: python -m motor.reprodutibilidade <dv>   → saidas/auditoria.json (status ok | falhou | bloqueado)
Máximo de 2 tentativas reprovadas por versão; na terceira o status fica "bloqueado" até você decidir.
"""
import argparse, json, math, shutil, sys, tempfile
from pathlib import Path
from .util import carregar_json, salvar_json, agora

TOL = 1e-9


def _apagar(func, caminho, _):
    import os, stat
    os.chmod(caminho, stat.S_IWRITE); func(caminho)


def _iguais(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=TOL, abs_tol=1e-12) or (math.isnan(a) and math.isnan(b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_iguais(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_iguais(x, y) for x, y in zip(a, b))
    return a == b


def assinatura_registro(dv):
    import hashlib
    reg = carregar_json(Path(dv) / "saidas" / "registro.json", {}) or {}
    return hashlib.sha256(json.dumps({k: v.get("resultado_sha256") for k, v in sorted(reg.items())}, sort_keys=True).encode()).hexdigest()


def auditar(dv):
    from . import ingestao, pipeline, registro, impacto
    dv = Path(dv).resolve(); ant = carregar_json(dv / "saidas" / "auditoria.json", {}) or {}
    tentativa = (ant.get("tentativa", 0) + 1) if ant.get("status") != "ok" else 1
    tmp = Path(tempfile.mkdtemp(prefix="auditoria_")) / "v"
    try:
        shutil.copytree(dv, tmp, ignore=shutil.ignore_patterns("analise.duckdb*", "preparados", "saidas", "revisoes"))
        (tmp / "saidas").mkdir(exist_ok=True)
        shutil.copy2(dv / "saidas" / "catalogo.json", tmp / "saidas" / "catalogo.json")
        if (dv / "saidas" / "perfil.json").exists():
            shutil.copy2(dv / "saidas" / "perfil.json", tmp / "saidas" / "perfil.json")
        div = ingestao.reconstruir(tmp)
        pipeline.rodar(tmp)
        _, erros = registro.rodar(tmp)
        impacto.calcular(tmp)
        div += [f"erro ao refazer: {e}" for e in erros]
        orig, novo = carregar_json(dv / "saidas" / "pipeline.json", {}), carregar_json(tmp / "saidas" / "pipeline.json", {})
        for eo, en in zip(orig.get("etapas", []), novo.get("etapas", [])):
            if eo["tabelas"] != en["tabelas"]: div.append(f"preparação {eo['arquivo']}: tabelas diferentes ao refazer")
        for p in sorted((dv / "saidas" / "analises").glob("*/resultado.json")):
            q = tmp / "saidas" / "analises" / p.parent.name / "resultado.json"
            a, b = carregar_json(p).get("valores"), (carregar_json(q) or {}).get("valores")
            if not _iguais(a, b): div.append(f"{p.parent.name}: valores diferentes ao refazer")
        ia, ib = carregar_json(dv / "saidas" / "impacto.json", {}).get("modelos", {}), carregar_json(tmp / "saidas" / "impacto.json", {}).get("modelos", {})
        if not _iguais(ia, ib): div.append("impacto: valores diferentes ao refazer")
    except SystemExit as e:
        div = [f"falha ao refazer: {e}"]
    finally:
        shutil.rmtree(tmp.parent, onerror=_apagar)
    status = "ok" if not div else ("bloqueado" if tentativa > 2 else "falhou")
    out = {"status": status, "tentativa": tentativa, "divergencias": div, "em": agora(), "registro_auditado": assinatura_registro(dv)}
    salvar_json(dv / "saidas" / "auditoria.json", out)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("dv"); x = ap.parse_args(); o = auditar(x.dv)
    print(f"Auditoria: {o['status']} (tentativa {o['tentativa']})"); [print(" -", d) for d in o["divergencias"]]
    sys.exit(0 if o["status"] == "ok" else 1)
