"""Aprendizado do squad de produto: resultados de experimentos e premissas x realizado depois do lançamento.

Uso:
  python -m motor.revisao experimento <dv> --hipotese H03 --resultado confirmada|refutada|inconclusiva --dado "<o que foi observado>" --fonte "<documento>"
  python -m motor.revisao lancamento <dv> --realizado <realizado.json>
  python -m motor.revisao historico

realizado.json (após o lançamento): {"fonte": "...", "preco_venda": 0, "preco_locacao_mensal": 0, "custo_unitario": 0,
  "unidades_novas_ano1": 0, "custo_implantacao_por_cliente": 0, "custo_suporte_mensal_por_unidade": 0}
"""
import argparse, sys
from collections import defaultdict
from pathlib import Path
from .util import CONHEC, carregar_json, salvar_json, ler_csv, escrever_csv, hoje, prov
from .produto import custo_unitario

HIP = CONHEC / "historico" / "hipoteses.csv"
PVR = CONHEC / "historico" / "previsto_vs_realizado.csv"


def experimento(dv, hid, resultado, dado, fonte):
    dv = Path(dv)
    val = carregar_json(dv / "nos" / "validacao.json", {})
    h = next((x for x in val.get("hipoteses", []) or [] if x.get("id") == hid), None)
    if not h:
        sys.exit(f"Hipótese {hid} não encontrada em nos/validacao.json")
    reg = carregar_json(dv / "resultados_validacao.json", [])
    reg.append({"hipotese": hid, "resultado": resultado, "dado": dado, "fonte": fonte, "em": hoje()})
    salvar_json(dv / "resultados_validacao.json", reg)
    meta = carregar_json(dv / "nos" / "meta.json", {})
    linhas = ler_csv(HIP)
    linhas.append({"projeto_id": meta.get("projeto_id"), "segmento": meta.get("segmento"), "hipotese": h.get("hipotese"), "categoria": h.get("categoria"),
                   "impacto": h.get("impacto"), "incerteza": h.get("incerteza"), "resultado": resultado, "data": hoje(), "fonte": fonte})
    escrever_csv(HIP, linhas, ["projeto_id", "segmento", "hipotese", "categoria", "impacto", "incerteza", "resultado", "data", "fonte"])
    print(f"Resultado registrado. O agente validacao-experimentos deve atualizar o status de {hid} no nó e carimbar; hipótese refutada pode desatualizar conceito, requisitos e caso de negócio.")


def lancamento(dv, arq):
    dv = Path(dv)
    base = carregar_json(dv / "saidas" / "baseline.json")
    if not base:
        sys.exit("Versão sem baseline congelada (python -m motor.estado congelar).")
    real = carregar_json(arq); neg = carregar_json(dv / "nos" / "negocio.json", {}); arq_ = carregar_json(dv / "nos" / "arquitetura.json", {})
    prev = {"preco_venda": neg.get("preco_venda"), "preco_locacao_mensal": neg.get("preco_locacao_mensal"), "custo_unitario": custo_unitario(arq_, neg),
            "unidades_novas_ano1": prov((neg.get("volume_unidades_novas") or {}).get("ano1") or {"provavel": 0}),
            "custo_implantacao_por_cliente": prov(neg.get("custo_implantacao_por_cliente") or {"provavel": 0}),
            "custo_suporte_mensal_por_unidade": prov(neg.get("custo_suporte_mensal_por_unidade") or {"provavel": 0})}
    meta = carregar_json(dv / "nos" / "meta.json", {})
    linhas = ler_csv(PVR)
    for k, p in prev.items():
        if k in real and p:
            linhas.append({"projeto_id": meta.get("projeto_id"), "segmento": meta.get("segmento"), "metrica": k, "previsto": p, "realizado": real[k],
                           "razao": round(float(real[k]) / float(p), 4), "data": hoje(), "fonte": real.get("fonte", "")})
            print(f"{k:34} previsto {p:>14,.2f} realizado {float(real[k]):>14,.2f} razão {float(real[k]) / float(p):.2f}")
    escrever_csv(PVR, linhas, ["projeto_id", "segmento", "metrica", "previsto", "realizado", "razao", "data", "fonte"])


def historico():
    g = defaultdict(list)
    for l in ler_csv(PVR):
        try: g[l["metrica"]].append(float(l["razao"]))
        except Exception: pass
    if g:
        print("Premissas x realizado (média de realizado/previsto):")
        for m, v in sorted(g.items()): print(f"  {m:34} n={len(v):<3} {sum(v) / len(v):.2f}")
    h = defaultdict(lambda: defaultdict(int))
    for l in ler_csv(HIP): h[l["categoria"]][l["resultado"]] += 1
    if h:
        print("Hipóteses testadas por categoria:")
        for c, d in h.items(): print(f"  {c:16} {dict(d)}")
    if not g and not h: print("Histórico vazio.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("experimento"); a.add_argument("dv"); a.add_argument("--hipotese", required=True)
    a.add_argument("--resultado", choices=["confirmada", "refutada", "inconclusiva"], required=True); a.add_argument("--dado", required=True); a.add_argument("--fonte", required=True)
    a = sp.add_parser("lancamento"); a.add_argument("dv"); a.add_argument("--realizado", required=True)
    sp.add_parser("historico")
    x = ap.parse_args()
    if x.cmd == "experimento": experimento(x.dv, x.hipotese, x.resultado, x.dado, x.fonte)
    elif x.cmd == "lancamento": lancamento(x.dv, x.realizado)
    else: historico()
