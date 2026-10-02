"""Calcula os modelos de impacto (nos/impacto.json) com simulação: premissas em 3 pontos e resultados das análises.

Fórmula = expressão aritmética com os nomes das premissas e dos apelidos em usa_resultados
(+ - * / **, parênteses, min, max, abs, round). Saída: saidas/impacto.json com provável, P10, P50 e P90.

Uso: python -m motor.impacto <dv>
"""
import argparse, ast, operator as op, sys
from pathlib import Path
import numpy as np
from .util import carregar_json, salvar_json, agora
from .registro import valor

OPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.Pow: op.pow, ast.USub: op.neg, ast.UAdd: op.pos}
FUN = {"min": np.minimum, "max": np.maximum, "abs": np.abs, "round": np.round}


def avaliar(expr, nomes):
    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return n.value
        if isinstance(n, ast.Name):
            if n.id not in nomes: raise ValueError(f"nome desconhecido na fórmula: {n.id}")
            return nomes[n.id]
        if isinstance(n, ast.BinOp) and type(n.op) in OPS: return OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in OPS: return OPS[type(n.op)](ev(n.operand))
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in FUN and not n.keywords:
            args = [ev(a) for a in n.args]
            return FUN[n.func.id](*args) if n.func.id != "round" else np.round(*args)
        raise ValueError("fórmula com elemento não permitido")
    return ev(ast.parse(expr, mode="eval"))


def _tri(rng, p, it):
    lo, mo, hi = (float(p.get(k)) for k in ("min", "provavel", "max"))
    return np.full(it, mo) if lo == hi else rng.triangular(lo, mo, hi, it)


def calcular(dv):
    dv = Path(dv); no = carregar_json(dv / "nos" / "impacto.json", {}) or {}
    it = int(no.get("iteracoes") or 5000); rng = np.random.default_rng(42); out = {"em": agora(), "modelos": {}}; erros = []
    for m in no.get("modelos", []) or []:
        try:
            amostras, prov = {}, {}
            for nome, p in (m.get("premissas") or {}).items():
                if not p.get("fonte"): raise ValueError(f"premissa {nome} sem fonte")
                amostras[nome] = _tri(rng, p, it); prov[nome] = float(p["provavel"])
            for apelido, ref in (m.get("usa_resultados") or {}).items():
                v = valor(dv, ref)
                if v is None: raise ValueError(f"resultado {ref} não encontrado (rode as análises)")
                inc = v.get("incerteza")
                amostras[apelido] = (rng.triangular(min(inc["inferior"], v["valor"]), v["valor"], max(inc["superior"], v["valor"]), it)
                                     if inc and inc.get("inferior") is not None and inc["inferior"] != inc["superior"] else np.full(it, float(v["valor"])))
                prov[apelido] = float(v["valor"])
            sim = np.asarray(avaliar(m["formula"], amostras), float) * np.ones(it)
            out["modelos"][m["id"]] = {"descricao": m.get("descricao"), "unidade": m.get("unidade"), "insight_ref": m.get("insight_ref"),
                                       "provavel": float(avaliar(m["formula"], prov)), "p10": float(np.percentile(sim, 10)),
                                       "p50": float(np.percentile(sim, 50)), "p90": float(np.percentile(sim, 90))}
        except Exception as e:
            erros.append(f"{m.get('id')}: {e}")
    salvar_json(dv / "saidas" / "impacto.json", out)
    for e in erros: print("ERRO impacto:", e)
    return out, erros


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("dv"); x = ap.parse_args()
    o, e = calcular(x.dv)
    for k, v in o["modelos"].items(): print(f"{k}: provável {v['provavel']:,.2f} {v['unidade'] or ''} (P10 {v['p10']:,.2f} · P90 {v['p90']:,.2f})")
    sys.exit(1 if e else 0)
