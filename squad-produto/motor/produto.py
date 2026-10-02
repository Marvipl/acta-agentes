"""Cálculos determinísticos do produto: notas ponderadas, cobertura de requisitos, custo unitário,
caso de negócio de 3 anos com sensibilidade, ROI do cliente, priorização de hipóteses e capacidade do roteiro."""
from collections import defaultdict
from .util import tri, prov, ler_csv, brl, pct, num, caminho_capacidade, mes_label


def ponderar(criterios, notas):
    tw = sum(float(c.get("peso") or 0) for c in criterios or [])
    if not tw or not notas:
        return None
    return sum(float(c.get("peso") or 0) * float((notas or {}).get(c["criterio"], 0) or 0) for c in criterios) / tw


def _v(x, k):
    """k: 0 min, 1 provável, 2 max."""
    if x is None:
        return 0.0
    return tri(x)[k] if isinstance(x, dict) else float(x)


def custo_unitario(arq, neg, k=1):
    if neg.get("custo_unitario_override") is not None:
        return _v(neg["custo_unitario_override"], k)
    return sum(_v(c.get("custo_unitario"), k) for c in (arq or {}).get("componentes", []) or [] if c.get("por_unidade", True))


def caso_negocio(neg, arq, sel=None):
    """sel: dict driver -> índice (0 min, 1 provável, 2 max) para análise de sensibilidade."""
    sel = sel or {}
    k = lambda d: sel.get(d, 1)
    mix = neg.get("mix") or {}
    pv, pl = float(mix.get("venda") or 0), float(mix.get("locacao") or 0)
    f_preco = (1 + 0.2 * (k("preco") - 1)) if "preco" in sel else 1.0
    preco_venda = float(neg.get("preco_venda") or 0) * f_preco
    preco_loc = float(neg.get("preco_locacao_mensal") or 0) * f_preco
    preco_srv = float(neg.get("preco_servico_mensal") or 0)
    preco_impl = float(neg.get("preco_implantacao") or 0)
    upc = float(neg.get("unidades_por_cliente") or 1) or 1
    cu = custo_unitario(arq, neg, k("custo_unitario"))
    c_impl = _v(neg.get("custo_implantacao_por_cliente"), 1)
    c_sup = _v(neg.get("custo_suporte_mensal_por_unidade"), 1)
    imp, com = float(neg.get("impostos_receita_pct") or 0), float(neg.get("comissao_pct") or 0)
    taxa = float(neg.get("taxa_desconto_aa") or 0)
    base_loc = base_total = 0.0
    anos, acum, vpl = [], 0.0, 0.0
    for i, a in enumerate(["ano1", "ano2", "ano3"], 1):
        novas = _v((neg.get("volume_unidades_novas") or {}).get(a), k("volume"))
        nre = _v((neg.get("investimento_desenvolvimento") or {}).get(a), k("investimento"))
        vendidas, locadas = novas * pv, novas * pl
        clientes_novos = novas / upc
        base_loc_ini = base_loc
        base_loc += locadas; base_total += novas
        base_loc_media = (base_loc_ini + base_loc) / 2
        base_total_media = base_total - novas / 2
        receita = vendidas * preco_venda + base_loc_media * preco_loc * 12 + base_total_media * preco_srv * 12 + clientes_novos * preco_impl
        custo_equip_venda = vendidas * cu
        capex_locacao = locadas * cu
        custo_impl = clientes_novos * c_impl
        custo_sup = base_total_media * c_sup * 12
        impostos, comissao = receita * imp, receita * com
        margem_contrib = receita - impostos - comissao - custo_equip_venda - custo_impl - custo_sup
        fluxo = margem_contrib - capex_locacao - nre
        acum += fluxo
        vpl += fluxo / (1 + taxa) ** i
        anos.append({"ano": a, "unidades_novas": novas, "base_instalada": base_total, "receita": receita, "impostos": impostos, "comissao": comissao,
                     "custo_equipamentos_vendidos": custo_equip_venda, "custo_implantacao": custo_impl, "custo_suporte": custo_sup,
                     "margem_contribuicao": margem_contrib, "capex_locacao": capex_locacao, "investimento_desenvolvimento": nre,
                     "fluxo": fluxo, "acumulado": acum})
    payback = next((x["ano"] for x in anos if x["acumulado"] >= 0), None)
    return {"anos": anos, "vpl": vpl, "acumulado_3anos": acum, "payback": payback, "custo_unitario": cu,
            "margem_unitaria_venda": (preco_venda * (1 - imp - com) - cu) if preco_venda else None}


def sensibilidade(neg, arq):
    base = caso_negocio(neg, arq)["vpl"]
    out = []
    for d, rot in [("volume", "Volume de unidades"), ("custo_unitario", "Custo unitário"), ("investimento", "Investimento de desenvolvimento"), ("preco", "Preço ±20%")]:
        baixo = caso_negocio(neg, arq, {d: 0})["vpl"]
        alto = caso_negocio(neg, arq, {d: 2})["vpl"]
        out.append({"driver": rot, "vpl_min": baixo, "vpl_max": alto, "amplitude": abs(alto - baixo)})
    out.sort(key=lambda x: -x["amplitude"])
    return base, out


def roi_cliente(neg, arq):
    r = neg.get("roi_cliente") or {}
    if r.get("custo_atual_anual") is None or r.get("custo_operacao_com_solucao_anual") is None:
        return None
    upc = float(neg.get("unidades_por_cliente") or 1)
    mix = neg.get("mix") or {}
    venda = float(mix.get("venda") or 0) >= float(mix.get("locacao") or 0)
    invest = (float(neg.get("preco_venda") or 0) * upc if venda else 0.0) + float(neg.get("preco_implantacao") or 0)
    mensal = (0.0 if venda else float(neg.get("preco_locacao_mensal") or 0) * upc) + float(neg.get("preco_servico_mensal") or 0) * upc
    economia = float(r["custo_atual_anual"]) - float(r["custo_operacao_com_solucao_anual"]) - mensal * 12
    payback = (invest / (economia / 12)) if economia > 0 and invest > 0 else (0.0 if economia > 0 else None)
    return {"modelo_avaliado": "venda" if venda else "locacao", "investimento_cliente": invest, "mensalidade_cliente": mensal,
            "economia_liquida_anual": economia, "payback_meses": payback}


def cobertura(nos):
    req = (nos["requisitos"] or {}).get("itens", []) or []
    musts = [r for r in req if r.get("prioridade") == "must"]
    alvo = (nos["oportunidade"] or {}).get("jtbd_alvo", []) or []
    cobertos = {o for r in musts for o in r.get("origem", []) or []}
    normas = [n for n in (nos["normas"] or {}).get("itens", []) or [] if n.get("aplicavel")]
    return {"total": len(req), "por_prioridade": {p: sum(1 for r in req if r.get("prioridade") == p) for p in ["must", "should", "could", "wont"]},
            "jtbd_sem_must": [j for j in alvo if j not in cobertos],
            "normas_sem_requisito": [n["id"] for n in normas if n["id"] not in {o for r in req for o in r.get("origem", []) or []}]}


def hipoteses(val):
    out = []
    for h in (val or {}).get("hipoteses", []) or []:
        risco = float(h.get("impacto") or 0) * float(h.get("incerteza") or 0)
        out.append({"id": h.get("id"), "hipotese": h.get("hipotese"), "categoria": h.get("categoria"), "risco": risco,
                    "status": h.get("status"), "tem_experimento": bool((h.get("experimento") or {}).get("criterio_sucesso"))})
    out.sort(key=lambda x: -x["risco"])
    return out


def capacidade_roadmap(rm, meta):
    rel = (rm or {}).get("releases", []) or []
    if not rel:
        return [], {}
    ini = min(r.get("inicio") or meta.get("mes_inicio") for r in rel)
    fim_n = max((int(r.get("duracao_meses") or 0) for r in rel), default=0) + 36
    meses = [mes_label(ini, i) for i in range(fim_n)]
    cap = {}
    for l in ler_csv(caminho_capacidade()):
        try:
            cap[l["perfil"]] = float(l["pessoas"]) * (1 - float(l.get("alocacao_atual_pct") or 0))
        except Exception:
            pass
    uso = defaultdict(lambda: defaultdict(float))
    for r in rel:
        ms = [m for m in meses if m >= (r.get("inicio") or ini)][:int(r.get("duracao_meses") or 0)]
        for p in r.get("perfis", []) or []:
            for m in ms:
                uso[p.get("perfil")][m] += float(p.get("fte") or 0)
    sobre = []
    for p, ms in uso.items():
        for m, v in sorted(ms.items()):
            d = cap.get(p)
            if d is None:
                sobre.append({"perfil": p, "mes": m, "fte_necessario": v, "fte_disponivel": None}); break
            if v > d + 1e-9:
                sobre.append({"perfil": p, "mes": m, "fte_necessario": round(v, 2), "fte_disponivel": round(d, 2)})
    return sobre, {p: dict(ms) for p, ms in uso.items()}


def calcular(nos):
    meta = nos["meta"] or {}
    res = {"meta": {k: meta.get(k) for k in ["projeto_id", "produto", "segmento", "versao", "modo", "data_base", "mes_inicio"]}}
    alertas = []
    op = nos["oportunidade"] or {}
    res["oportunidade"] = {"nota": ponderar(op.get("criterios"), op.get("notas")), "decisao": op.get("decisao")}
    cc = nos["conceitos"] or {}
    ranking = sorted([{"id": c.get("id"), "nome": c.get("nome"), "abordagem": c.get("abordagem"), "nota": ponderar(cc.get("criterios_selecao"), c.get("notas"))}
                      for c in cc.get("conceitos", []) or []], key=lambda x: -(x["nota"] or 0))
    res["conceitos"] = {"ranking": ranking, "escolhido": cc.get("escolhido")}
    if ranking and cc.get("escolhido") and ranking[0]["id"] != cc.get("escolhido"):
        alertas.append(f"conceito escolhido ({cc.get('escolhido')}) não é o de maior nota ({ranking[0]['id']}): a justificativa precisa explicar")
    res["requisitos"] = cobertura(nos)
    neg, arq = nos["negocio"] or {}, nos["arquitetura"] or {}
    if neg:
        cn = caso_negocio(neg, arq)
        vpl, tornado = sensibilidade(neg, arq)
        res["negocio"] = {**{k: v for k, v in cn.items() if k != "anos"}, "anos": cn["anos"], "sensibilidade": tornado,
                          "custo_unitario_min": custo_unitario(arq, neg, 0), "custo_unitario_max": custo_unitario(arq, neg, 2)}
        res["roi_cliente"] = roi_cliente(neg, arq)
        if cn["payback"] is None:
            alertas.append("caso de negócio: investimento não se paga em 3 anos no cenário provável")
    res["benchmark"] = benchmark(nos)
    alertas += res["benchmark"]["alertas"]
    res["hipoteses"] = hipoteses(nos["validacao"])
    sem_exp = [h["id"] for h in res["hipoteses"] if h["risco"] >= 15 and not h["tem_experimento"]]
    if sem_exp:
        alertas.append(f"hipóteses de alto risco sem experimento: {sem_exp}")
    sobre, uso = capacidade_roadmap(nos["roadmap"], meta)
    res["capacidade"] = {"sobrecargas": sobre}
    if sobre:
        alertas.append(f"{len(sobre)} sobrecarga(s) de capacidade no roteiro")
    res["alertas"] = alertas
    res["fmt"] = _fmt(res)
    return res, {"uso_fte": uso}


def _fmt(res):
    f = {"oportunidade_nota": num(res["oportunidade"]["nota"], 2) if res["oportunidade"]["nota"] is not None else "[●]",
         "n_requisitos": num(res["requisitos"]["total"]), "n_must": num(res["requisitos"]["por_prioridade"]["must"]),
         "n_hipoteses": num(len(res["hipoteses"]))}
    bm = res.get("benchmark") or {}
    f.update({"n_concorrentes": num(len(bm.get("produtos", []))), "n_especificacoes": num(len(bm.get("especificacoes", []))),
              "cobertura_benchmark": pct(bm.get("cobertura_dados")), "benchmark_confirmado": pct(bm.get("dados_confirmados")),
              "n_requisitos_benchmark": num(len(bm.get("atendimento", []))),
              "n_requisitos_abaixo_mediana": num(sum(1 for a in bm.get("atendimento", []) if a["posicao"] == "abaixo da mediana do mercado"))})
    n = res.get("negocio")
    if n:
        f.update({"vpl_3anos": brl(n["vpl"]), "acumulado_3anos": brl(n["acumulado_3anos"]), "payback": n["payback"] or "além de 3 anos",
                  "custo_unitario": brl(n["custo_unitario"]), "custo_unitario_min": brl(n["custo_unitario_min"]), "custo_unitario_max": brl(n["custo_unitario_max"]),
                  "margem_unitaria_venda": brl(n["margem_unitaria_venda"])})
        for a in n["anos"]:
            for k in ["receita", "margem_contribuicao", "fluxo", "acumulado"]:
                f[f"{k}_{a['ano']}"] = brl(a[k])
            f[f"unidades_{a['ano']}"] = num(a["unidades_novas"])
        f["maior_sensibilidade"] = n["sensibilidade"][0]["driver"] if n["sensibilidade"] else "[●]"
    r = res.get("roi_cliente")
    if r:
        f.update({"roi_investimento_cliente": brl(r["investimento_cliente"]), "roi_mensalidade_cliente": brl(r["mensalidade_cliente"]),
                  "roi_economia_anual": brl(r["economia_liquida_anual"]),
                  "roi_payback_meses": num(r["payback_meses"], 1) if r["payback_meses"] is not None else "não se paga"})
    return f


# ---------------- benchmark técnico ----------------
def _numero(v):
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).replace(",", "."))
    except Exception:
        return None


def benchmark(nos):
    co = nos["concorrencia"] or {}
    specs = co.get("especificacoes", []) or []
    prods = co.get("produtos", []) or []
    tipos_ev = {e.get("id"): e.get("tipo") for e in co.get("evidencias", []) or []}
    linhas, alertas = [], []
    celulas = preenchidas = confirmadas = 0
    for e in specs:
        vals, num = {}, []
        for p in prods:
            c = (p.get("specs") or {}).get(e.get("id")) or {}
            v = c.get("valor")
            celulas += 1
            if v not in (None, ""):
                preenchidas += 1
                if tipos_ev.get(c.get("fonte")) == "confirmado":
                    confirmadas += 1
                vals[p.get("id")] = v
                n = _numero(v)
                if n is not None:
                    num.append((n, p.get("id")))
        melhor = mediana = lider = None
        if num and e.get("melhor") in ("maior", "menor"):
            ordem = sorted(num, key=lambda x: x[0], reverse=(e["melhor"] == "maior"))
            melhor, lider = ordem[0]
            xs = sorted(x[0] for x in num)
            mediana = xs[len(xs) // 2] if len(xs) % 2 else (xs[len(xs) // 2 - 1] + xs[len(xs) // 2]) / 2
        if len(vals) < 2:
            alertas.append(f"especificação {e.get('id')} ({e.get('nome')}): menos de 2 produtos com dado")
        linhas.append({"id": e.get("id"), "nome": e.get("nome"), "unidade": e.get("unidade"), "melhor": e.get("melhor"),
                       "valores": vals, "melhor_valor": melhor, "mediana": mediana, "lider": lider, "n_dados": len(vals)})
    por_id = {l["id"]: l for l in linhas}
    nomes = {p.get("id"): p.get("nome") or p.get("id") for p in prods}
    atend = []
    for r in (nos["requisitos"] or {}).get("itens", []) or []:
        ref = r.get("especificacao_ref")
        if not ref or ref not in por_id:
            continue
        l = por_id[ref]
        alvo = _numero(r.get("valor_alvo_num") if r.get("valor_alvo_num") is not None else r.get("valor_alvo"))
        atendem, posicao = [], "sem alvo numérico"
        if alvo is not None and l["melhor"] in ("maior", "menor"):
            ok = (lambda v: v >= alvo) if l["melhor"] == "maior" else (lambda v: v <= alvo)
            atendem = [nomes[pid] for pid, v in l["valores"].items() if _numero(v) is not None and ok(_numero(v))]
            if l["melhor_valor"] is not None:
                melhor_que = (alvo > l["melhor_valor"]) if l["melhor"] == "maior" else (alvo < l["melhor_valor"])
                pior_que_med = (alvo < l["mediana"]) if l["melhor"] == "maior" else (alvo > l["mediana"])
                posicao = ("acima do melhor do mercado" if melhor_que else
                           "igual ao melhor do mercado" if alvo == l["melhor_valor"] else
                           "abaixo da mediana do mercado" if pior_que_med else "entre a mediana e o melhor")
                if r.get("prioridade") == "must" and pior_que_med:
                    alertas.append(f"{r.get('id')}: alvo ({alvo:g} {l['unidade'] or ''}) abaixo da mediana do mercado ({l['mediana']:g}); justifique ou eleve")
                if melhor_que and not r.get("justificativa_alvo"):
                    alertas.append(f"{r.get('id')}: alvo acima do melhor do mercado sem justificativa (diferencial ou risco técnico)")
        atend.append({"requisito": r.get("id"), "descricao": r.get("descricao"), "prioridade": r.get("prioridade"), "especificacao": ref,
                      "nome_especificacao": l["nome"], "unidade": l["unidade"], "alvo": alvo, "melhor_mercado": l["melhor_valor"],
                      "lider": nomes.get(l["lider"]), "mediana": l["mediana"], "atendem": atendem, "posicao": posicao})
    precos = [{"produto": p.get("nome"), "fabricante": p.get("fabricante"), "valor": (p.get("preco") or {}).get("valor"),
               "moeda": (p.get("preco") or {}).get("moeda"), "tipo": (p.get("preco") or {}).get("tipo"),
               "unidade": (p.get("preco") or {}).get("unidade"), "suporte_brasil": p.get("suporte_brasil")} for p in prods]
    return {"produtos": [{"id": p.get("id"), "nome": p.get("nome"), "fabricante": p.get("fabricante"), "tipo": p.get("tipo"),
                          "ficha_tecnica_url": p.get("ficha_tecnica_url")} for p in prods],
            "especificacoes": linhas, "atendimento": atend, "precos": precos,
            "cobertura_dados": (preenchidas / celulas) if celulas else None,
            "dados_confirmados": (confirmadas / preenchidas) if preenchidas else None, "alertas": alertas}
