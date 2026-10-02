"""Roda as análises registradas no plano e guarda os resultados (registro de análises).

Cada script analises/ANA-xxx.py define:
    def rodar(con, ctx):
        ...
        return {"valores": {"chave": {"valor": 1.2, "unidade": "h", "incerteza": {...} ou None}},
                "tabelas": {"nome": DataFrame}, "notas": "..."}
`con` = DuckDB da análise (use as tabelas base_* e prep_*); `ctx.estat` = motor.estatistica; `ctx.figura("nome")` = caminho
para salvar um PNG; `ctx.analise` = o registro do plano.

Uso: python -m motor.registro <dv> [ANA-xxx ...]
"""
import argparse, hashlib, importlib.util, json, sys, time
from pathlib import Path
from types import SimpleNamespace
from .util import carregar_json, salvar_json, agora, config
from .dados import conectar
from . import estatistica

TIPOS_INCERTEZA = {"nenhuma", "intervalo_confianca", "intervalo_previsao", "bootstrap", "faixa_cenarios"}


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def rodar(dv, ids=None):
    dv = Path(dv); plano = carregar_json(dv / "nos" / "plano.json", {}) or {}
    analises = [a for a in plano.get("analises", []) if not ids or a["id"] in ids]
    if not analises:
        sys.exit("Nenhuma análise no plano (nos/plano.json).")
    con = conectar(dv); reg = carregar_json(dv / "saidas" / "registro.json", {}) or {}; erros = []
    for a in analises:
        scr = dv / a["script"]
        if not scr.exists():
            erros.append(f"{a['id']}: script {a['script']} não existe"); continue
        destino = dv / "saidas" / "analises" / a["id"]; destino.mkdir(parents=True, exist_ok=True)
        spec = importlib.util.spec_from_file_location(a["id"].replace("-", "_"), scr); mod = importlib.util.module_from_spec(spec)
        t0 = time.time()
        try:
            spec.loader.exec_module(mod)
            ctx = SimpleNamespace(estat=estatistica, analise=a, figura=lambda nome, d=destino: str(d / f"{nome}.png"))
            out = mod.rodar(con, ctx) or {}
        except Exception as e:
            erros.append(f"{a['id']}: falhou ({e})"); continue
        vals = out.get("valores") or {}
        for k, v in vals.items():
            if not isinstance(v, dict) or not _num(v.get("valor")):
                erros.append(f"{a['id']}.{k}: 'valor' precisa ser número"); continue
            inc = v.get("incerteza")
            if a.get("incerteza") not in (None, "nenhuma") and not v.get("contagem") and not inc:
                erros.append(f"{a['id']}.{k}: o plano pede {a['incerteza']} e o valor veio sem incerteza")
            if inc and inc.get("tipo") not in TIPOS_INCERTEZA:
                erros.append(f"{a['id']}.{k}: tipo de incerteza inválido")
        tabs = {}; minimo = config().get("minimo_registros_por_grupo", 5)
        for nome, df in (out.get("tabelas") or {}).items():
            arq = destino / f"{nome}.csv"; df.to_csv(arq, index=False); tabs[nome] = arq.name
            for col in [c for c in df.columns if str(c).lower() in ("n", "contagem", "registros", "qtd")]:
                if (df[col] < minimo).any(): print(f"aviso {a['id']}.{nome}: grupos com menos de {minimo} registros; não leve ao relatório sem agregar")
        res = {"id": a["id"], "valores": vals, "tabelas": tabs, "figuras": sorted(p.name for p in destino.glob("*.png")), "notas": out.get("notas", ""),
               "em": agora(), "segundos": round(time.time() - t0, 2)}
        salvar_json(destino / "resultado.json", res)
        reg[a["id"]] = {"pergunta_ref": a.get("pergunta_ref"), "tipo": a.get("tipo"), "nivel": a.get("nivel"), "metodo": a.get("metodo"),
                        "script": a["script"], "script_sha256": hashlib.sha256(scr.read_bytes()).hexdigest(),
                        "resultado_sha256": hashlib.sha256(json.dumps(vals, sort_keys=True, default=str).encode()).hexdigest(), "chaves": sorted(vals)}
        print(f"{a['id']}: {len(vals)} valor(es), {len(tabs)} tabela(s), {len(res['figuras'])} figura(s)")
    con.close()
    salvar_json(dv / "saidas" / "registro.json", reg)
    for e in erros: print("ERRO:", e)
    return reg, erros


def valor(dv, ref):
    """'ANA-001.chave' → dicionário do valor registrado (ou None)."""
    aid, _, k = ref.partition(".")
    return ((carregar_json(Path(dv) / "saidas" / "analises" / aid / "resultado.json", {}) or {}).get("valores") or {}).get(k)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("dv"); ap.add_argument("ids", nargs="*"); x = ap.parse_args()
    _, e = rodar(x.dv, x.ids or None); sys.exit(1 if e else 0)
