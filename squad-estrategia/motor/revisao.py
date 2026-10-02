"""Revisão trimestral do plano: compara o realizado com a baseline congelada e registra o aprendizado.

Uso:
  python -m motor.revisao trimestre <dir_versao_congelada> --trimestre T1 --realizado <realizado.json>
  python -m motor.revisao historico

realizado.json:
  {"fonte": "...", "krs": {"KR1.1": 12}, "receita_por_linha_ytd": {"<linha>": 350000},
   "caixa": 900000, "wmbt": {"O1-W1": "confirmada|refutada|em_teste"}}
Status do KR (convenção ajustável em config.revisao): verde >= 0,7 do caminho entre baseline e meta do trimestre; amarelo >= 0,4; vermelho abaixo.
"""
import argparse, sys
from collections import defaultdict
from pathlib import Path
from .util import CONHEC, carregar_json, ler_csv, escrever_csv, config, brl, pct, hoje

HIST = CONHEC / "historico" / "previsto_vs_realizado.csv"
CAMPOS = ["ciclo", "trimestre", "area", "metrica", "previsto", "realizado", "razao", "data", "fonte"]


def trimestre(dv, tri, arq):
    dv = Path(dv)
    base = carregar_json(dv / "saidas" / "baseline.json")
    if not base:
        sys.exit("Versão sem baseline congelada (python -m motor.estado congelar).")
    real = carregar_json(arq)
    nos = {n: carregar_json(dv / "nos" / f"{n}.json", {}) for n in ["okrs", "opcoes", "riscos", "meta"]}
    q = int(tri.strip().upper().lstrip("T"))
    lim = config().get("revisao") or {"verde": 0.7, "amarelo": 0.4}
    ciclo = nos["meta"].get("ciclo")
    hist = ler_csv(HIST)
    linhas = [f"# Revisão {tri} — plano {ciclo}", "", f"Fonte do realizado: {real.get('fonte', '[●]')}", "", "## Resultados-chave", "",
              "| KR | Baseline | Meta do trimestre | Realizado | Progresso | Status |", "|---|---|---|---|---|---|"]
    cont = defaultdict(int)
    for k in nos["okrs"].get("krs", []) or []:
        if k["id"] not in (real.get("krs") or {}):
            linhas.append(f"| {k['id']} {k.get('kr', '')} | {k.get('baseline')} | {(k.get('metas_trimestrais') or {}).get(f'T{q}')} | sem dado | — | sem dado |")
            cont["sem dado"] += 1; continue
        b, meta_t, v = k.get("baseline"), (k.get("metas_trimestrais") or {}).get(f"T{q}"), real["krs"][k["id"]]
        prog = None if meta_t is None or meta_t == b else (v - b) / (meta_t - b)
        st = "sem meta" if prog is None else ("verde" if prog >= lim["verde"] else ("amarelo" if prog >= lim["amarelo"] else "vermelho"))
        cont[st] += 1
        linhas.append(f"| {k['id']} {k.get('kr', '')} | {b} | {meta_t} | {v} | {pct(prog) if prog is not None else '—'} | {st} |")
        if meta_t is not None:
            hist.append({"ciclo": ciclo, "trimestre": tri, "area": "kr", "metrica": k["id"], "previsto": meta_t, "realizado": v,
                         "razao": round(v / meta_t, 4) if meta_t else "", "data": hoje(), "fonte": real.get("fonte", "")})
    linhas += ["", f"Resumo: {dict(cont)}", "", "## Receita por linha (cenário base, acumulado no ano)", "",
               "| Linha | Previsto | Realizado | Realizado/previsto |", "|---|---|---|---|"]
    resumo = base["resumo"]
    ano = int(str(ciclo)[:4]) if ciclo else None
    anual = ((resumo.get("cenarios") or {}).get("base") or {}).get("anual") or {}
    fin = carregar_json(dv / "nos" / "financeiro.json", {})
    for l in (((fin.get("cenarios") or {}).get("base") or {}).get("linhas") or []):
        nome = l.get("linha")
        if nome not in (real.get("receita_por_linha_ytd") or {}):
            continue
        rec_ano = (l.get("receita") or {}).get(str(ano)) or 0
        prev = float(rec_ano) * q / 4
        v = float(real["receita_por_linha_ytd"][nome])
        linhas.append(f"| {nome} | {brl(prev)} | {brl(v)} | {pct(v / prev) if prev else '—'} |")
        if prev:
            hist.append({"ciclo": ciclo, "trimestre": tri, "area": "receita", "metrica": nome, "previsto": round(prev, 2), "realizado": v,
                         "razao": round(v / prev, 4), "data": hoje(), "fonte": real.get("fonte", "")})
    if real.get("caixa") is not None and anual:
        # caixa previsto ao fim do trimestre: interpolação linear dentro do primeiro ano (indicativo)
        linhas += ["", f"Caixa realizado ao fim do {tri}: {brl(real['caixa'])} (compare com Caixa_base na planilha da baseline)."]
    ref = [w for w, s in (real.get("wmbt") or {}).items() if s == "refutada"]
    linhas += ["", "## Hipóteses (o que precisa ser verdade)", "", f"Atualizadas: {len(real.get('wmbt') or {})}. Refutadas: {ref or 'nenhuma'}."]
    if ref:
        linhas.append("Hipótese refutada é gatilho de revisão da tese: leve ao conselho e avalie nova versão do plano.")
    destino = dv / "revisoes_trimestrais" / tri
    destino.mkdir(parents=True, exist_ok=True)
    (destino / "relatorio.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    escrever_csv(HIST, hist, CAMPOS)
    print(f"Relatório: {destino / 'relatorio.md'}")
    print("\n".join(linhas[:4]))


def historico():
    g = defaultdict(list)
    for l in ler_csv(HIST):
        try:
            g[(l["area"], l["metrica"])].append(float(l["razao"]))
        except Exception:
            pass
    if not g:
        print("Histórico vazio."); return
    print(f"{'área':10} {'métrica':30} {'n':>3} {'realizado/previsto médio':>26}")
    for (a, m), v in sorted(g.items()):
        print(f"{a:10} {m:30} {len(v):>3} {sum(v) / len(v):>26.2f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("trimestre"); a.add_argument("dv"); a.add_argument("--trimestre", required=True); a.add_argument("--realizado", required=True)
    sp.add_parser("historico")
    x = ap.parse_args()
    trimestre(x.dv, x.trimestre, x.realizado) if x.cmd == "trimestre" else historico()
