"""Aprendizado do squad: compara estimado x realizado e propõe fatores de correção.

Uso:
  python -m motor.calibrar registrar <dir_versao_congelada> --realizado <realizado.json>
  python -m motor.calibrar propor
  python -m motor.calibrar aprovar --categoria <cat> --por <nome> [--forcar]

Salvaguardas:
  - compara contra a baseline AJUSTADA pelas mudanças de escopo aprovadas (aumento de escopo não é erro de estimativa);
  - remove o efeito de fatores já aplicados (mede o erro bruto da estimativa);
  - um fator só fica 'aplicavel' com amostra mínima (config) e pesos maiores para casos recentes;
  - nenhum fator entra no cálculo sem aprovação humana (arquivo fatores_correcao.csv).
"""
import argparse, sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from .util import CONHEC, carregar_json, ler_csv, escrever_csv, config, agora, hoje

HIST = CONHEC / "historico"
CAMPOS_H = ["projeto_id", "versao", "tipo_projeto", "data", "categoria", "estimado_bruto", "ajuste_escopo",
            "estimado_ajustado", "realizado", "razao", "fonte"]


def _estimativas(dv):
    s = Path(dv) / "saidas"
    base = carregar_json(s / "baseline.json")
    if not base:
        sys.exit("Versão sem baseline congelada (python -m motor.estado congelar).")
    res = base["resumo"]; fat = res.get("fatores_aplicados", {})
    est = defaultdict(float)
    for l in ler_csv(s / "mao_de_obra.csv"):
        cat = f"horas_{l['categoria']}"
        est[cat] += float(l["horas"]) / fat.get(cat, 1.0)
    for l in ler_csv(s / "indiretos.csv"):
        cat = f"indiretos_{l['categoria']}"
        est[cat] += float(l["valor_brl"]) / fat.get(cat, 1.0)
    est["bom"] = res["custos"]["equipamentos"] / fat.get("bom", 1.0)
    est["prazo_dias"] = res["prazo"]["dias_provavel"]
    est["recorrente"] = res["custos"]["recorrente_mensal"] / fat.get("recorrente", 1.0)
    return res, est


def registrar(dv, arq_realizado):
    real = carregar_json(arq_realizado)
    res, est = _estimativas(dv)
    ajustes = defaultdict(float)
    for m in real.get("mudancas_escopo", []) or []:
        for cat, v in (m.get("categorias") or {}).items():
            ajustes[cat] += float(v)
    linhas = ler_csv(HIST / "estimado_vs_realizado.csv")
    novas = 0
    for cat, realizado in (real.get("categorias") or {}).items():
        if cat not in est:
            print(f"aviso: categoria '{cat}' não existe na estimativa; ignorada"); continue
        aj = est[cat] + ajustes[cat]
        if aj <= 0:
            continue
        linhas.append({"projeto_id": res["meta"]["projeto_id"], "versao": res["meta"]["versao"],
                       "tipo_projeto": real.get("tipo_projeto", ""), "data": real.get("data_encerramento", hoje()),
                       "categoria": cat, "estimado_bruto": round(est[cat], 2), "ajuste_escopo": round(ajustes[cat], 2),
                       "estimado_ajustado": round(aj, 2), "realizado": realizado, "razao": round(float(realizado) / aj, 4),
                       "fonte": real.get("fonte", "")})
        novas += 1
    escrever_csv(HIST / "estimado_vs_realizado.csv", linhas, CAMPOS_H)
    print(f"{novas} categoria(s) registradas em historico/estimado_vs_realizado.csv")


def propor():
    cfg = config()
    nmin = int(cfg.get("calibracao_amostra_minima", 3)); meia = float(cfg.get("calibracao_meia_vida_meses", 12))
    grupos = defaultdict(list)
    for l in ler_csv(HIST / "estimado_vs_realizado.csv"):
        grupos[l["categoria"]].append(l)
    for l in ler_csv(HIST / "benchmark_vs_cotacao.csv"):
        grupos["bom_benchmark"].append({"razao": l["razao"], "data": l["data"]})
    out = []
    for cat, ls in sorted(grupos.items()):
        pares = []
        for l in ls:
            try:
                idade = (date.today() - date.fromisoformat(l["data"][:10])).days / 30.4
            except Exception:
                idade = 0
            pares.append((float(l["razao"]), 0.5 ** (idade / meia)))
        sw = sum(w for _, w in pares)
        f = sum(r * w for r, w in pares) / sw
        disp = (sum(w * (r - f) ** 2 for r, w in pares) / sw) ** 0.5
        out.append({"categoria": cat, "fator_proposto": round(f, 3), "n": len(pares), "dispersao": round(disp, 3),
                    "status": "aplicavel" if len(pares) >= nmin else "amostra_insuficiente", "gerado_em": hoje()})
    escrever_csv(HIST / "fatores_correcao_proposta.csv", out, ["categoria", "fator_proposto", "n", "dispersao", "status", "gerado_em"])
    for o in out:
        print(f"{o['categoria']:28} fator {o['fator_proposto']:.3f}  n={o['n']}  dispersão={o['dispersao']:.3f}  {o['status']}")


def aprovar(categoria, por, forcar=False):
    prop = {l["categoria"]: l for l in ler_csv(HIST / "fatores_correcao_proposta.csv")}
    if categoria not in prop:
        sys.exit("Categoria sem proposta. Rode 'propor' antes.")
    p = prop[categoria]
    if p["status"] != "aplicavel" and not forcar:
        sys.exit(f"Amostra insuficiente (n={p['n']}). Use --forcar só com justificativa.")
    ap = [l for l in ler_csv(HIST / "fatores_correcao.csv") if l["categoria"] != categoria]
    ap.append({"categoria": categoria, "fator": p["fator_proposto"], "n": p["n"], "aprovado_por": por, "aprovado_em": agora(),
               "observacao": "forçado" if forcar and p["status"] != "aplicavel" else ""})
    escrever_csv(HIST / "fatores_correcao.csv", ap, ["categoria", "fator", "n", "aprovado_por", "aprovado_em", "observacao"])
    print(f"fator {categoria} = {p['fator_proposto']} aprovado por {por}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("registrar"); a.add_argument("dv"); a.add_argument("--realizado", required=True)
    sp.add_parser("propor")
    a = sp.add_parser("aprovar"); a.add_argument("--categoria", required=True); a.add_argument("--por", required=True); a.add_argument("--forcar", action="store_true")
    x = ap.parse_args()
    if x.cmd == "registrar": registrar(x.dv, x.realizado)
    elif x.cmd == "propor": propor()
    else: aprovar(x.categoria, x.por, x.forcar)
