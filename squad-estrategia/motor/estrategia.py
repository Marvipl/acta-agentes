"""Cálculos determinísticos do planejamento: projeção financeira plurianual (mensal), portfólio, iniciativas e capacidade.

Os agentes escrevem premissas nos nós; tudo o que é conta sai daqui.
"""
from collections import defaultdict
from .util import ler_csv, prov, mes_label, brl, pct, num, caminho_capacidade


def _meses(meta, anos):
    ini = meta.get("mes_inicio") or f"{anos[0]}-01"
    return [mes_label(ini, i) for i in range(12 * len(anos))]


def _anual(d, ano):
    if d is None:
        return 0.0
    if isinstance(d, dict):
        v = d.get(str(ano), d.get(ano))
        return float(v or 0)
    return float(d)


def _pessoal_mensal(org, meses):
    base = float((org or {}).get("custo_pessoal_mensal_atual") or 0)
    out = {m: base for m in meses}
    for c in (org or {}).get("contratacoes", []) or []:
        q, cu, ini = float(c.get("quantidade") or 0), float(c.get("custo_mensal_unitario") or 0), c.get("mes_inicio") or meses[0]
        for m in meses:
            if m >= ini:
                out[m] += q * cu
    return out


def projetar(modelo, meta, org=None, fatores=None):
    """Projeção mensal; devolve linhas mensais, DRE anual e indicadores."""
    anos = [int(a) for a in modelo.get("anos") or []]
    if not anos:
        return None
    meses = _meses(meta, anos)
    imp = float(modelo.get("impostos_receita_pct") or 0)
    pessoal_org = _pessoal_mensal(org, meses) if (org and modelo.get("pessoal_anual") is None) else None
    eventos_fom, eventos_cap = defaultdict(float), defaultdict(float)
    for f in modelo.get("fomento", []) or []:
        if f.get("valor") and f.get("mes"):
            eventos_fom[f["mes"]] += float(f["valor"])
    for c in modelo.get("captacao", []) or []:
        if c.get("valor") and c.get("mes"):
            eventos_cap[c["mes"]] += float(c["valor"])
    caixa = float(modelo.get("caixa_inicial") or 0)
    caixa_sem_cap = caixa
    mensal = []
    for i, m in enumerate(meses):
        ano = anos[i // 12]
        receita = cpv = 0.0
        for l in modelo.get("linhas", []) or []:
            fator = (fatores or {}).get(l.get("linha"), 1.0)
            r = _anual(l.get("receita"), ano) / 12 * fator
            mg = l.get("margem_bruta_pct")
            mg = _anual(mg, ano) if isinstance(mg, dict) else float(mg or 0)
            receita += r; cpv += r * (1 - mg)
        impostos = receita * imp
        pessoal = pessoal_org[m] if pessoal_org is not None else _anual(modelo.get("pessoal_anual"), ano) / 12
        despesas = sum(_anual(d.get("valor"), ano) for d in modelo.get("despesas", []) or []) / 12
        ebitda = receita - impostos - cpv - pessoal - despesas
        capex = _anual(modelo.get("capex"), ano) / 12
        fom, cap = eventos_fom.get(m, 0.0), eventos_cap.get(m, 0.0)
        fluxo = ebitda + fom - capex
        caixa += fluxo + cap
        caixa_sem_cap += fluxo
        mensal.append({"mes": m, "ano": ano, "receita": receita, "impostos": impostos, "cpv": cpv, "pessoal": pessoal,
                       "despesas": despesas, "ebitda": ebitda, "fomento": fom, "capex": capex, "captacao": cap,
                       "fluxo_operacional": fluxo, "caixa": caixa, "caixa_sem_captacao": caixa_sem_cap})
    anual = {}
    for a in anos:
        ls = [x for x in mensal if x["ano"] == a]
        s = lambda k: sum(x[k] for x in ls)
        rb = s("receita")
        anual[a] = {"receita": rb, "impostos": s("impostos"), "receita_liquida": rb - s("impostos"), "cpv": s("cpv"),
                    "lucro_bruto": rb - s("impostos") - s("cpv"), "pessoal": s("pessoal"), "despesas": s("despesas"),
                    "ebitda": s("ebitda"), "margem_ebitda": (s("ebitda") / rb) if rb else None, "fomento": s("fomento"),
                    "capex": s("capex"), "captacao": s("captacao"), "caixa_final": ls[-1]["caixa"]}
    menor = min(mensal, key=lambda x: x["caixa"])
    menor_sem = min(mensal, key=lambda x: x["caixa_sem_captacao"])
    negativos = [x["mes"] for x in mensal if x["caixa"] < 0]
    be = next((a for a in anos if anual[a]["ebitda"] >= 0), None)
    queima = [-x["fluxo_operacional"] for x in mensal[:12] if x["fluxo_operacional"] < 0]
    zera = next((i for i, x in enumerate(mensal) if x["caixa_sem_captacao"] < 0), None)
    ind = {"menor_caixa": menor["caixa"], "mes_menor_caixa": menor["mes"], "meses_caixa_negativo": negativos,
           "runway_meses_sem_captacao": zera, 
           "necessidade_captacao": max(0.0, -menor_sem["caixa_sem_captacao"]), "mes_caixa_zera_sem_captacao":
           next((x["mes"] for x in mensal if x["caixa_sem_captacao"] < 0), None), "ano_ebitda_positivo": be,
           "queima_media_ano1": (sum(queima) / 12) if queima else 0.0, "caixa_final": mensal[-1]["caixa"]}
    return {"mensal": mensal, "anual": anual, "indicadores": ind}


def portfolio(port):
    ca = port.get("criterios_atratividade", []) or []
    cc = port.get("criterios_capacidade", []) or []
    def nota(d, crit):
        tw = sum(float(c.get("peso") or 0) for c in crit)
        if not tw:
            return None
        return sum(float(c.get("peso") or 0) * float((d or {}).get(c["criterio"], 0) or 0) for c in crit) / tw
    out, alertas = [], []
    for l in port.get("linhas", []) or []:
        a, c = nota(l.get("atratividade"), ca), nota(l.get("capacidade_vencer"), cc)
        quad = None if a is None or c is None else ("alta" if a >= 3 else "baixa") + " atratividade / " + ("alta" if c >= 3 else "baixa") + " capacidade"
        dec = l.get("decisao")
        if a is not None and c is not None:
            if dec == "investir" and a < 3 and c < 3:
                alertas.append(f"linha '{l.get('linha')}': decisão investir com atratividade e capacidade baixas")
            if dec in ("descontinuar", "colher") and a >= 3 and c >= 3:
                alertas.append(f"linha '{l.get('linha')}': decisão {dec} com atratividade e capacidade altas")
        out.append({"linha": l.get("linha"), "atratividade": a, "capacidade": c, "quadrante": quad, "decisao": dec})
    return out, alertas


def iniciativas(ini, org, meta, anos):
    meses = _meses(meta, anos)
    cap_base = {}
    for l in ler_csv(caminho_capacidade()):
        try:
            cap_base[l["perfil"]] = float(l["pessoas"]) * (1 - float(l.get("alocacao_atual_pct") or 0))
        except Exception:
            pass
    cap = {p: {m: v for m in meses} for p, v in cap_base.items()}
    for c in (org or {}).get("contratacoes", []) or []:
        p = c.get("perfil")
        cap.setdefault(p, {m: 0.0 for m in meses})
        for m in meses:
            if m >= (c.get("mes_inicio") or meses[0]):
                cap[p][m] += float(c.get("quantidade") or 0)
    uso = defaultdict(lambda: defaultdict(float))
    lista = []
    for it in (ini or {}).get("itens", []) or []:
        esf = prov(it.get("esforco_pessoas_mes") or {"provavel": 0}) if it.get("esforco_pessoas_mes") else 0
        val, conf = float(it.get("valor") or 0), float(it.get("confianca") or 0)
        prioridade = (val * conf / esf) if esf else None
        ini_m, dur = it.get("inicio") or meses[0], int(it.get("duracao_meses") or 0)
        ms = [m for m in meses if m >= ini_m][:dur]
        for p in it.get("perfis", []) or []:
            for m in ms:
                uso[p.get("perfil")][m] += float(p.get("fte") or 0)
        custo = prov(it["custo_externo"]) if it.get("custo_externo") and it["custo_externo"].get("provavel") is not None else 0.0
        lista.append({"id": it.get("id"), "nome": it.get("nome"), "objetivo_id": it.get("objetivo_id"), "tipo": it.get("tipo"),
                      "area": it.get("area"), "dono": it.get("dono"), "duracao_meses": dur,
                      "valor": val, "confianca": conf, "esforco_pessoas_mes": esf, "prioridade": prioridade,
                      "inicio": ini_m, "fim": ms[-1] if ms else None, "custo_externo": custo})
    lista.sort(key=lambda x: -(x["prioridade"] or 0))
    sobrecargas = []
    for p, ms in uso.items():
        for m, v in sorted(ms.items()):
            disp = cap.get(p, {}).get(m)
            if disp is None:
                sobrecargas.append({"perfil": p, "mes": m, "fte_necessario": round(v, 2), "fte_disponivel": None}); break
            if v > disp + 1e-9:
                sobrecargas.append({"perfil": p, "mes": m, "fte_necessario": round(v, 2), "fte_disponivel": round(disp, 2)})
    return lista, sobrecargas, {p: dict(ms) for p, ms in uso.items()}


def calcular(nos):
    meta = nos["meta"] or {}
    alertas = []
    res = {"meta": {k: meta.get(k) for k in ["projeto_id", "ciclo", "titulo", "versao", "modo", "data_base", "mes_inicio", "horizonte_execucao", "horizonte_direcao"]}}
    det = {}
    fo = (nos["financeiro_opcoes"] or {}).get("opcoes") or {}
    res["opcoes"] = {}
    for oid, mod in fo.items():
        pr = projetar(mod, meta)
        if pr:
            res["opcoes"][oid] = {"anual": pr["anual"], "indicadores": pr["indicadores"]}
            det[f"opcao_{oid}"] = pr["mensal"]
    fin = nos["financeiro"] or {}
    res["cenarios"] = {}
    for c, mod in (fin.get("cenarios") or {}).items():
        pr = projetar(mod, meta, nos["organizacao"])
        if pr:
            res["cenarios"][c] = {"anual": pr["anual"], "indicadores": pr["indicadores"]}
            det[f"cenario_{c}"] = pr["mensal"]
            if pr["indicadores"]["meses_caixa_negativo"]:
                alertas.append(f"cenário {c}: caixa negativo a partir de {pr['indicadores']['meses_caixa_negativo'][0]}")
    port, al = portfolio(nos["portfolio"] or {})
    res["portfolio"] = port; alertas += al
    anos = ((fin.get("cenarios") or {}).get("base") or {}).get("anos") or [int(str(meta.get("ciclo", "2027"))[:4])]
    lista, sobre, uso = iniciativas(nos["iniciativas"], nos["organizacao"], meta, anos)
    res["iniciativas"] = lista; res["capacidade"] = {"sobrecargas": sobre}
    det["uso_fte"] = uso
    if sobre:
        alertas.append(f"{len(sobre)} sobrecarga(s) de capacidade nas iniciativas")
    res["roadmap"] = roadmap(lista, meta)
    res["areas"] = areas(nos, lista, anos)
    okr = nos["okrs"] or {}
    res["contagens"] = {"objetivos": len(okr.get("objetivos", []) or []), "krs": len(okr.get("krs", []) or []),
                        "iniciativas": len(lista), "riscos": len((nos["riscos"] or {}).get("itens", []) or [])}
    res["alertas"] = alertas
    res["fmt"] = _fmt(res)
    return res, det


NOMES_AREA = {"comercial_marketing": "Comercial e marketing", "produto_tecnologia": "Produto e tecnologia", "operacoes": "Operações",
              "parcerias": "Parcerias e distribuição", "pessoas": "Pessoas e organização", "captacao": "Captação", "juridico": "Jurídico e tributário", "outra": "Outra"}


def _trim(mes):
    a, m = mes.split("-"); return f"{a}-T{(int(m) - 1) // 3 + 1}"


def roadmap(lista, meta):
    out = []
    for x in lista:
        if not x.get("inicio") or not x.get("duracao_meses"):
            continue
        meses = [mes_label(x["inicio"], i) for i in range(int(x["duracao_meses"]))]
        out.append({"id": x["id"], "nome": x["nome"], "area": x.get("area"), "dono": x.get("dono"), "prioridade": x.get("prioridade"),
                    "trimestres": sorted({_trim(m) for m in meses})})
    return out


def areas(nos, lista, anos):
    pf = {a.get("area"): a for a in (nos.get("planos_funcionais") or {}).get("areas", []) or []}
    ano1 = str(anos[0]) if anos else None
    agg = {}
    for x in lista:
        k = x.get("area") or "outra"
        d = agg.setdefault(k, {"area": k, "iniciativas": 0, "custo_externo": 0.0, "esforco_pessoas_mes": 0.0, "despesas_recorrentes_ano": 0.0})
        d["iniciativas"] += 1; d["custo_externo"] += x.get("custo_externo") or 0.0; d["esforco_pessoas_mes"] += x.get("esforco_pessoas_mes") or 0.0
    for k, a in pf.items():
        d = agg.setdefault(k, {"area": k, "iniciativas": 0, "custo_externo": 0.0, "esforco_pessoas_mes": 0.0, "despesas_recorrentes_ano": 0.0})
        d["despesas_recorrentes_ano"] = sum(float(x.get("valor_anual") or 0) for x in a.get("despesas_recorrentes", []) or [])
        d["dono"] = a.get("dono")
    for d in agg.values():
        d["orcamento_total"] = d["custo_externo"] + d["despesas_recorrentes_ano"]
    return sorted(agg.values(), key=lambda d: -d["orcamento_total"])


def _tabelas(res, f):
    tri = sorted({t for r in res.get("roadmap", []) for t in r["trimestres"]})
    if tri:
        l = ["| Iniciativa | Área | Dono | " + " | ".join(tri) + " |", "|---|---|---|" + "---|" * len(tri)]
        for r in res["roadmap"]:
            l.append(f"| {r['id']} · {r['nome']} | {NOMES_AREA.get(r['area'], r['area'] or '—')} | {r['dono'] or '[●]'} | " + " | ".join("■" if t in r["trimestres"] else "" for t in tri) + " |")
        f["roadmap_tabela"] = "\n".join(l)
    else:
        f["roadmap_tabela"] = "Sem iniciativas com início e duração definidos."
    l = ["| Área | Dono | Iniciativas | Esforço (pessoas-mês) | Custo externo das iniciativas | Despesas recorrentes no ano 1 | Total |", "|---|---|---|---|---|---|---|"]
    for d in res.get("areas", []):
        l.append(f"| {NOMES_AREA.get(d['area'], d['area'])} | {d.get('dono') or '[●]'} | {d['iniciativas']} | {num(d['esforco_pessoas_mes'], 1)} | {brl(d['custo_externo'])} | {brl(d['despesas_recorrentes_ano'])} | {brl(d['orcamento_total'])} |")
    f["orcamento_areas_tabela"] = "\n".join(l)
    cen = res.get("cenarios", {})
    if cen:
        ordem = [c for c in ("conservador", "base", "otimista") if c in cen] + [c for c in cen if c not in ("conservador", "base", "otimista")]
        l = ["| Indicador | " + " | ".join(c.capitalize() for c in ordem) + " |", "|---|" + "---|" * len(ordem)]
        a1 = lambda c, k: list(cen[c]["anual"].values())[0][k]
        for nome, fn in [("Receita do ano 1", lambda c: brl(a1(c, "receita"))), ("EBITDA do ano 1", lambda c: brl(a1(c, "ebitda"))),
                         ("Caixa no fim do ano 1", lambda c: brl(a1(c, "caixa_final"))), ("Menor caixa no horizonte", lambda c: brl(cen[c]["indicadores"]["menor_caixa"])),
                         ("Necessidade de captação", lambda c: brl(cen[c]["indicadores"]["necessidade_captacao"])),
                         ("Runway sem captação", lambda c: (f"{cen[c]['indicadores']['runway_meses_sem_captacao']} meses" if cen[c]["indicadores"]["runway_meses_sem_captacao"] is not None else "além do horizonte")),
                         ("Primeiro ano com EBITDA positivo", lambda c: str(cen[c]["indicadores"]["ano_ebitda_positivo"] or "fora do horizonte"))]:
            l.append(f"| {nome} | " + " | ".join(fn(c) for c in ordem) + " |")
        f["cenarios_tabela"] = "\n".join(l)
    return f


def _fmt(res):
    f = {}
    for grupo in ("cenarios", "opcoes"):
        for nome, d in res.get(grupo, {}).items():
            for idx, (ano, v) in enumerate(d["anual"].items(), 1):
                f[f"ano_{idx}"] = str(ano)
                for k, x in v.items():
                    txt = pct(x) if k.startswith("margem") else brl(x)
                    f[f"{nome}_{k}_{ano}"] = txt
                    f[f"{nome}_{k}_a{idx}"] = txt
            ind = d["indicadores"]
            f[f"{nome}_menor_caixa"] = brl(ind["menor_caixa"]); f[f"{nome}_mes_menor_caixa"] = ind["mes_menor_caixa"]
            f[f"{nome}_necessidade_captacao"] = brl(ind["necessidade_captacao"])
            f[f"{nome}_caixa_zera_sem_captacao"] = ind["mes_caixa_zera_sem_captacao"] or "não zera no horizonte"
            f[f"{nome}_ano_ebitda_positivo"] = str(ind["ano_ebitda_positivo"] or "fora do horizonte")
            f[f"{nome}_queima_media_ano1"] = brl(ind["queima_media_ano1"])
            f[f"{nome}_caixa_final"] = brl(ind["caixa_final"])
            f[f"{nome}_runway_meses"] = (f"{ind['runway_meses_sem_captacao']} meses" if ind.get("runway_meses_sem_captacao") is not None else "além do horizonte")
    for k, v in res.get("contagens", {}).items():
        f[f"n_{k}"] = num(v)
    return _tabelas(res, f)
