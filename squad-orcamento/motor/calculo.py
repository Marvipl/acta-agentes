"""Cálculo determinístico (cenário provável): cronograma (CPM), custos, preço, fluxo de caixa e DRE."""
import math
from collections import defaultdict
from pathlib import Path
from .util import (RAIZ, CONHEC, tri, prov, config, carregar_json, ler_csv, custo_hora_por_perfil,
                   fatores_aprovados, mes_label, brl, pct, num)


# ---------- cronograma ----------
def ordem_topologica(atividades):
    ids = [a["id"] for a in atividades]
    pred = {a["id"]: list(a.get("predecessoras", [])) for a in atividades}
    feito, ordem = set(), []
    while len(ordem) < len(ids):
        progresso = False
        for i in ids:
            if i not in feito and all(p in feito for p in pred[i]):
                feito.add(i); ordem.append(i); progresso = True
        if not progresso:
            raise ValueError("cronograma com ciclo ou predecessora inexistente")
    return ordem


def cpm(atividades, duracoes):
    """duracoes: dict id->dias. Retorna es, ef, ls, lf, folga, total."""
    por_id = {a["id"]: a for a in atividades}
    ordem = ordem_topologica(atividades)
    es, ef = {}, {}
    for i in ordem:
        es[i] = max([ef[p] for p in por_id[i].get("predecessoras", [])], default=0.0)
        ef[i] = es[i] + duracoes[i]
    total = max(ef.values(), default=0.0)
    suc = defaultdict(list)
    for a in atividades:
        for p in a.get("predecessoras", []):
            suc[p].append(a["id"])
    lf, ls = {}, {}
    for i in reversed(ordem):
        lf[i] = min([ls[s] for s in suc[i]], default=total)
        ls[i] = lf[i] - duracoes[i]
    folga = {i: round(ls[i] - es[i], 6) for i in ordem}
    return es, ef, ls, lf, folga, total


def itens_esforco(nos):
    itens = []
    for fonte_no, chave in [("solucao", "esforco"), ("operacoes", "esforco"), ("cronograma", "esforco_gestao")]:
        for it in (nos.get(fonte_no) or {}).get(chave, []) or []:
            d = dict(it); d["_origem"] = fonte_no
            itens.append(d)
    return itens


def atividade_do_wbs(atividades, wbs_id, atividade_id=None):
    if atividade_id:
        return atividade_id
    for a in atividades:
        if wbs_id in (a.get("wbs_ids") or []):
            return a["id"]
    return None


def meses_da_atividade(es, ef, dpm):
    ini = int(es // dpm)
    fim = int(max(ef - 1e-9, es) // dpm)
    return list(range(ini, fim + 1))


# ---------- cálculo principal ----------
def calcular(nos, contingencia=None, mc=None):
    cfg = config()
    dpm = float(cfg.get("dias_por_mes", 30.4))
    alertas = []
    meta, crono = nos["meta"] or {}, nos["cronograma"] or {}
    trib, ind, ris = nos["tributos"] or {}, nos["custos_indiretos"] or {}, nos["riscos"] or {}
    preco, contr, fin, ops = nos["preco"] or {}, nos["contrato"] or {}, nos["financeiro"] or {}, nos["operacoes"] or {}
    fatores = fatores_aprovados()
    fatores_usados = {}

    def fator(cat):
        f = fatores.get(cat)
        if f is not None:
            fatores_usados[cat] = f
            return f
        return 1.0

    # cronograma
    atividades = crono.get("atividades", []) or []
    f_prazo = fator("prazo_dias") if atividades else 1.0
    dur = {a["id"]: prov(a["duracao_dias"]) * f_prazo for a in atividades}
    es, ef, ls, lf, folga, total_dias = cpm(atividades, dur) if atividades else ({}, {}, {}, {}, {}, 0.0)
    caminho_critico = [a["id"] for a in atividades if abs(folga.get(a["id"], 1)) < 1e-6]
    meses_ativ = {i: meses_da_atividade(es[i], ef[i], dpm) for i in es}
    fim_projeto_m = int(max(total_dias - 1e-9, 0) // dpm)

    # câmbio
    cambio = {"BRL": 1.0}
    for moeda, c in (meta.get("cambio") or {}).items():
        taxa = c.get("taxa") if isinstance(c, dict) else c
        if taxa is None:
            continue
        cambio[moeda] = float(taxa)

    imp_pct = trib.get("custo_importacao_pct") or {}
    imp_padrao = imp_pct.get("padrao") if isinstance(imp_pct, dict) else imp_pct
    nac_pct = trib.get("custo_aquisicao_nacional_pct", 0.0) or 0.0

    # BOM
    bom_linhas, bom_total = [], 0.0
    pag_padrao = cfg.get("pagamento_padrao_bom") or {}
    saidas_mes = defaultdict(lambda: defaultdict(float))
    for it in (nos["bom"] or {}).get("itens", []) or []:
        moeda = it.get("moeda", "BRL")
        if moeda not in cambio:
            alertas.append(f"BOM {it['id']}: moeda {moeda} sem câmbio em meta.cambio"); continue
        aliq = (imp_pct.get(it["id"]) if isinstance(imp_pct, dict) and it["id"] in imp_pct else imp_padrao) \
            if it.get("origem") == "importado" else nac_pct
        if aliq is None:
            alertas.append(f"BOM {it['id']}: sem custo de importação definido em tributos"); aliq = 0.0
        unit_brl = prov(it["preco_unit"]) * cambio[moeda] * (1 + aliq)
        f_bench = fator("bom_benchmark") if (it.get("fonte") or {}).get("tipo") == "benchmark" else 1.0
        total = unit_brl * float(it.get("qtd", 1)) * fator("bom") * f_bench
        bom_total += total
        ativ = atividade_do_wbs(atividades, it.get("wbs_id"), it.get("atividade_id"))
        pedido_m = meses_ativ[ativ][0] if ativ in meses_ativ else 0
        entrega_m = pedido_m + math.ceil(prov(it.get("lead_time_dias", 0)) / dpm)
        eventos = it.get("pagamento") or pag_padrao.get(it.get("origem", "nacional"))
        if not eventos:
            alertas.append(f"BOM {it['id']}: sem condição de pagamento; assumido 100% no pedido")
            eventos = [{"evento": "pedido", "pct": 1.0}]
        for e in eventos:
            m = pedido_m if e["evento"] == "pedido" else entrega_m
            saidas_mes[m]["equipamentos"] += total * float(e["pct"])
        bom_linhas.append({"id": it["id"], "descricao": it.get("descricao"), "qtd": it.get("qtd"), "moeda": moeda,
                           "preco_unit": prov(it["preco_unit"]), "cambio": cambio[moeda], "aliq_aquisicao": aliq,
                           "fator": fatores.get("bom", 1.0) * f_bench,
                           "total_brl": total, "fonte": (it.get("fonte") or {}).get("tipo"), "atividade": ativ,
                           "mes_pedido": pedido_m, "mes_entrega": entrega_m})

    # mão de obra
    custo_h = custo_hora_por_perfil()
    mo_linhas, mo_total = [], 0.0
    hist = defaultdict(lambda: defaultdict(float))
    for it in itens_esforco(nos):
        ativ = atividade_do_wbs(atividades, it.get("wbs_id"), it.get("atividade_id"))
        ch = custo_h.get(it.get("perfil"))
        if ch is None:
            alertas.append(f"Esforço {it['id']}: perfil '{it.get('perfil')}' sem custo/hora"); ch = 0.0
        cat = it.get("categoria", "geral")
        horas = prov(it["horas"]) * fator(f"horas_{cat}")
        total = horas * ch
        mo_total += total
        meses = meses_ativ.get(ativ, [0])
        for m in meses:
            saidas_mes[m]["mao_de_obra"] += total / len(meses)
            hist[it.get("perfil")][m] += horas / len(meses)
        mo_linhas.append({"id": it["id"], "origem": it["_origem"], "perfil": it.get("perfil"), "categoria": cat,
                          "horas": horas, "custo_hora": ch, "total_brl": total, "atividade": ativ})

    # indiretos
    ind_linhas, ind_total = [], 0.0
    for it in ind.get("itens", []) or []:
        v = prov(it["valor"]) * fator(f"indiretos_{it.get('categoria', 'outros')}")
        ind_total += v
        d = it.get("distribuicao", "linear")
        if isinstance(d, dict) and "mes" in d:
            saidas_mes[int(d["mes"])]["indiretos"] += v
        elif d == "inicio":
            saidas_mes[0]["indiretos"] += v
        elif d == "fim":
            saidas_mes[fim_projeto_m]["indiretos"] += v
        else:
            for m in range(fim_projeto_m + 1):
                saidas_mes[m]["indiretos"] += v / (fim_projeto_m + 1)
        ind_linhas.append({"id": it["id"], "descricao": it.get("descricao"), "categoria": it.get("categoria"),
                           "valor_brl": v, "fonte": (it.get("fonte") or {}).get("tipo") if isinstance(it.get("fonte"), dict) else it.get("fonte")})
    overhead_pct = ind.get("overhead_pct")
    if overhead_pct is None:
        alertas.append("custos_indiretos.overhead_pct não definido (rateio de estrutura); usado 0")
        overhead_pct = 0.0
    overhead = (bom_total + mo_total) * float(overhead_pct)
    for m in range(fim_projeto_m + 1):
        saidas_mes[m]["overhead"] += overhead / (fim_projeto_m + 1)

    custo_base = bom_total + mo_total + ind_total + overhead
    cont = max(float(contingencia or 0.0), 0.0)
    for m in range(fim_projeto_m + 1):
        saidas_mes[m]["contingencia"] += cont / (fim_projeto_m + 1)
    custo_com_cont = custo_base + cont

    # preço
    aliq_rec = trib.get("impostos_receita_pct") or {}
    comp = preco.get("composicao_receita") or {}
    if comp and abs(sum(comp.values()) - 1) > 1e-6:
        alertas.append("preco.composicao_receita não soma 100%")
    imp_medio = sum(float(comp[t]) * float(aliq_rec.get(t, 0) or 0) for t in comp) if comp else None
    if comp and any(aliq_rec.get(t) is None for t in comp):
        alertas.append("tributos.impostos_receita_pct sem alíquota para algum tipo de receita")
    comissao = preco.get("comissao_pct")
    margem_alvo, margem_min = preco.get("margem_alvo"), preco.get("margem_minima")
    preco_sug = preco_min = None
    if imp_medio is not None and comissao is not None and margem_alvo is not None:
        den = 1 - imp_medio - comissao - margem_alvo
        preco_sug = custo_com_cont / den if den > 0 else None
        if den <= 0: alertas.append("impostos + comissão + margem ≥ 100%: preço indefinido")
    if imp_medio is not None and comissao is not None and margem_min is not None:
        den = 1 - imp_medio - comissao - margem_min
        preco_min = custo_com_cont / den if den > 0 else None
    receita_impl = preco.get("receita_fixada") or preco.get("preco_proposto") or preco_sug
    origem_receita = "receita_fixada" if preco.get("receita_fixada") else ("preco_proposto" if preco.get("preco_proposto") else "preco_sugerido")

    # receitas no tempo
    entradas_mes = defaultdict(lambda: defaultdict(float))
    impostos_mes, comissao_mes = defaultdict(float), defaultdict(float)
    marcos_out = []
    if receita_impl:
        ret = float(contr.get("retencao_pct") or 0)
        ultimo = 0
        for mc_ in contr.get("marcos", []) or []:
            if "mes" in mc_:
                m = int(mc_["mes"])
            else:
                a = mc_.get("atividade_id")
                base_m = meses_ativ[a][-1] if a in meses_ativ else fim_projeto_m
                m = base_m + math.ceil(float(mc_.get("prazo_pagamento_dias", 0)) / dpm)
            v = receita_impl * float(mc_["pct"])
            entradas_mes[m]["implantacao"] += v * (1 - ret)
            ultimo = max(ultimo, m)
            marcos_out.append({"id": mc_["id"], "evento": mc_.get("evento"), "pct": mc_["pct"], "mes": m,
                               "competencia": mes_label(meta.get("mes_inicio") or "2000-01", m), "valor_brl": v})
        if ret > 0:
            m_lib = ultimo + math.ceil(float(contr.get("liberacao_retencao_dias", 0)) / dpm)
            entradas_mes[m_lib]["implantacao"] += receita_impl * ret
        soma = sum(float(x["pct"]) for x in contr.get("marcos", []) or [])
        if contr.get("marcos") and abs(soma - 1) > 1e-6:
            alertas.append(f"marcos do contrato somam {soma:.2%}, não 100%")
    rec = preco.get("recorrente") or {}
    rec_mensal, rec_meses = rec.get("mensalidade"), int(rec.get("meses") or 0)
    rec_ini = fim_projeto_m + 1 + int(rec.get("inicio_rel_entrega", 0) or 0)
    if rec_mensal:
        for i in range(rec_meses):
            entradas_mes[rec_ini + i]["recorrente"] += float(rec_mensal)
    custo_rec_mensal = 0.0
    # custo da mensalidade: só linhas cobertas por ela (escopo "cliente", padrão), pela vida de cada
    # linha dentro da janela da mensalidade, dividida pelo prazo; linhas "operacao_comercial" ficam fora
    custo_rec_cliente_total = 0.0
    for it in ops.get("custos_recorrentes", []) or []:
        ini = fim_projeto_m + 1 + int(it.get("inicio_rel_entrega", 0) or 0)
        v = prov(it["custo_mensal"]) * fator("recorrente")
        custo_rec_mensal += v
        n_meses = int(it.get("meses") or 0)
        for i in range(n_meses):
            saidas_mes[ini + i]["custos_recorrentes"] += v
        if (it.get("escopo") or "cliente") == "cliente" and rec_meses:
            sobrepoe = max(0, min(ini + n_meses, rec_ini + rec_meses) - max(ini, rec_ini))
            custo_rec_cliente_total += v * sobrepoe
    custo_rec_cliente = custo_rec_cliente_total / rec_meses if rec_meses else None

    # operação comercial própria (ex.: quiosque e loja operados pela Acta): receita de vendas,
    # impostos pelo tipo indicado e custos variáveis em % da receita; custos fixos ficam em operacoes
    op_out = []
    for st in preco.get("operacao_comercial", []) or []:
        tipo = st.get("tipo")
        if aliq_rec.get(tipo) is None:
            alertas.append(f"operacao_comercial {st.get('id')}: tributos.impostos_receita_pct sem tipo '{tipo}'")
        aliq_op = float(aliq_rec.get(tipo, 0) or 0)
        ini = fim_projeto_m + 1 + int(st.get("inicio_rel_entrega", 0) or 0)
        rec_op = prov(st["receita_mensal"]) * fator("operacao_receita")
        cv_pct = prov(st.get("custo_variavel_pct") or 0)
        for i in range(int(st.get("meses") or 0)):
            entradas_mes[ini + i]["operacao"] += rec_op
            impostos_mes[ini + i] += rec_op * aliq_op
            saidas_mes[ini + i]["custo_variavel_operacao"] += rec_op * cv_pct
        op_out.append({"id": st.get("id"), "descricao": st.get("descricao"), "receita_mensal": rec_op,
                       "aliquota": aliq_op, "custo_variavel_pct": cv_pct, "inicio_mes": ini, "meses": int(st.get("meses") or 0),
                       "margem_contribuicao_mensal": rec_op * (1 - aliq_op - cv_pct)})

    aliq_rec_tipo = float(aliq_rec.get(rec.get("tipo", "servico"), 0) or 0)
    com_rec = bool(preco.get("comissao_sobre_recorrente"))
    for m, d in entradas_mes.items():
        impostos_mes[m] += d["implantacao"] * (imp_medio or 0) + d["recorrente"] * aliq_rec_tipo
        comissao_mes[m] += d["implantacao"] * (comissao or 0) + (d["recorrente"] * (comissao or 0) if com_rec else 0)

    # fluxo mensal
    horizonte = max([0] + list(saidas_mes.keys()) + list(entradas_mes.keys())) + 1
    taxa_aa = fin.get("custo_capital_aa")
    if taxa_aa is None:
        alertas.append("financeiro.custo_capital_aa não definido; custo financeiro = 0")
    taxa_m = (1 + float(taxa_aa or 0)) ** (1 / 12) - 1
    mes_ini = meta.get("mes_inicio") or "2000-01"
    fluxo, acum = [], 0.0
    cats_s = ["equipamentos", "mao_de_obra", "indiretos", "overhead", "contingencia", "custos_recorrentes",
              "custo_variavel_operacao"]
    for m in range(horizonte):
        e = entradas_mes[m]; s = saidas_mes[m]
        linha = {"mes": m, "competencia": mes_label(mes_ini, m),
                 "receita_implantacao": e["implantacao"], "receita_recorrente": e["recorrente"],
                 "receita_operacao": e["operacao"],
                 "impostos": -impostos_mes[m], "comissao": -comissao_mes[m]}
        for c in cats_s:
            linha[c] = -s[c]
        pre = sum(v for k, v in linha.items() if k not in ("mes", "competencia"))
        custo_fin = -abs(acum) * taxa_m if acum < 0 else 0.0
        linha["custo_financeiro"] = custo_fin
        linha["saldo_mes"] = pre + custo_fin
        acum += linha["saldo_mes"]
        linha["acumulado"] = acum
        fluxo.append(linha)

    exposicao = min([0.0] + [l["acumulado"] for l in fluxo])
    mes_pico = min(fluxo, key=lambda l: l["acumulado"])["mes"] if fluxo else None
    payback = None
    if exposicao < 0:
        for l in fluxo:
            if l["mes"] > mes_pico and l["acumulado"] >= 0:
                payback = l["mes"]; break
    saldos = [l["saldo_mes"] for l in fluxo]
    vpl = sum(v / (1 + taxa_m) ** i for i, v in enumerate(saldos)) if taxa_aa is not None else None
    tir_m = _tir(saldos)
    tir_aa = (1 + tir_m) ** 12 - 1 if tir_m is not None else None

    # DRE
    def soma(k): return sum(l[k] for l in fluxo)
    rb = soma("receita_implantacao") + soma("receita_recorrente") + soma("receita_operacao")
    dre = {"receita_bruta": rb, "impostos": soma("impostos")}
    dre["receita_liquida"] = rb + dre["impostos"]
    dre["cpv_equipamentos"] = soma("equipamentos"); dre["cpv_mao_de_obra"] = soma("mao_de_obra")
    dre["cpv_recorrente"] = soma("custos_recorrentes")
    dre["cpv_operacao"] = soma("custo_variavel_operacao")
    dre["lucro_bruto"] = (dre["receita_liquida"] + dre["cpv_equipamentos"] + dre["cpv_mao_de_obra"] + dre["cpv_recorrente"]
                          + dre["cpv_operacao"])
    dre["comissao"] = soma("comissao"); dre["indiretos"] = soma("indiretos"); dre["overhead"] = soma("overhead")
    dre["contingencia"] = soma("contingencia")
    dre["resultado_operacional"] = dre["lucro_bruto"] + dre["comissao"] + dre["indiretos"] + dre["overhead"] + dre["contingencia"]
    dre["custo_financeiro"] = soma("custo_financeiro")
    dre["resultado_projeto"] = dre["resultado_operacional"] + dre["custo_financeiro"]
    dre["margem_bruta"] = dre["lucro_bruto"] / rb if rb else None
    dre["margem_liquida"] = dre["resultado_projeto"] / rb if rb else None
    dre_ano = defaultdict(lambda: defaultdict(float))
    for l in fluxo:
        ano = l["competencia"][:4]
        for k in ["receita_implantacao", "receita_recorrente", "receita_operacao", "impostos", "comissao"] + cats_s + ["custo_financeiro", "saldo_mes"]:
            dre_ano[ano][k] += l[k]

    # recorrente
    margem_rec = None
    if rec_mensal:
        liq = float(rec_mensal) * (1 - aliq_rec_tipo - ((comissao or 0) if com_rec else 0))
        margem_rec = (liq - (custo_rec_cliente or 0.0)) / float(rec_mensal)

    # capacidade
    cap = {}
    for l in ler_csv(CONHEC / "mao_de_obra" / "capacidade_time.csv"):
        try:
            cap[l["perfil"]] = float(l["pessoas"]) * float(l["horas_mes_por_pessoa"]) * (1 - float(l["alocacao_atual_pct"]))
        except Exception:
            pass
    sobrecargas = []
    for perfil, meses in hist.items():
        disp = cap.get(perfil)
        if disp is None:
            sobrecargas.append({"perfil": perfil, "mes": None, "motivo": "perfil sem capacidade cadastrada"}); continue
        for m, h in meses.items():
            if h > disp + 1e-6:
                sobrecargas.append({"perfil": perfil, "mes": mes_label(mes_ini, m), "horas": round(h, 1), "disponivel": round(disp, 1)})

    margem_res = None
    if receita_impl:
        liq = receita_impl * (1 - (imp_medio or 0) - (comissao or 0))
        margem_res = (liq - custo_com_cont) / receita_impl

    r = {
        "meta": {k: meta.get(k) for k in ["projeto_id", "cliente", "projeto", "versao", "modo", "classe_estimativa", "data_base", "mes_inicio"]},
        "prazo": {"dias_provavel": total_dias, "meses_provavel": round(total_dias / dpm, 1), "caminho_critico": caminho_critico,
                  "fim_mes": mes_label(mes_ini, fim_projeto_m)},
        "custos": {"equipamentos": bom_total, "mao_de_obra": mo_total, "indiretos": ind_total, "overhead": overhead,
                   "base": custo_base, "contingencia": cont, "com_contingencia": custo_com_cont,
                   "recorrente_mensal": custo_rec_mensal, "recorrente_mensal_cliente": custo_rec_cliente},
        "preco": {"impostos_medios": imp_medio, "comissao": comissao, "margem_alvo": margem_alvo, "margem_minima": margem_min,
                  "sugerido": preco_sug, "minimo": preco_min, "receita_implantacao": receita_impl, "origem_receita": origem_receita,
                  "margem_resultante": margem_res, "recorrente_mensal": rec_mensal, "recorrente_meses": rec_meses,
                  "margem_recorrente": margem_rec},
        "fluxo": {"exposicao_maxima": exposicao, "mes_pico": mes_label(mes_ini, mes_pico) if mes_pico is not None else None,
                  "payback": mes_label(mes_ini, payback) if payback is not None else None, "vpl": vpl, "tir_aa": tir_aa,
                  "horizonte_meses": horizonte},
        "dre": dre,
        "operacao_comercial": op_out,
        "opcionais": (preco.get("opcionais") or {}).get("itens", []) if isinstance(preco.get("opcionais"), dict) else [],
        "marcos": marcos_out,
        "capacidade": {"sobrecargas": sobrecargas},
        "fatores_aplicados": fatores_usados,
        "alertas": alertas,
    }
    if mc:
        r["monte_carlo"] = {k: mc.get(k) for k in ["custo_p10", "custo_p50", "custo_p80", "custo_p90", "prazo_p50_dias", "prazo_p80_dias", "iteracoes"]}
    r["fmt"] = _formatar(r)
    detalhes = {"bom": bom_linhas, "mao_de_obra": mo_linhas, "indiretos": ind_linhas, "fluxo": fluxo,
                "dre_ano": {a: dict(v) for a, v in dre_ano.items()},
                "cronograma": [{"id": a["id"], "nome": a.get("nome"), "inicio_dia": es.get(a["id"]), "fim_dia": ef.get(a["id"]),
                                "folga_dias": folga.get(a["id"]), "critica": a["id"] in caminho_critico} for a in atividades],
                "histograma": {p: {mes_label(mes_ini, m): h for m, h in sorted(ms.items())} for p, ms in hist.items()}}
    return r, detalhes


def _tir(fluxos):
    if not fluxos or not (any(v < 0 for v in fluxos) and any(v > 0 for v in fluxos)):
        return None
    def npv(t): return sum(v / (1 + t) ** i for i, v in enumerate(fluxos))
    lo, hi = -0.99, 1.0
    if npv(lo) * npv(hi) > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if npv(lo) * npv(mid) <= 0: hi = mid
        else: lo = mid
    return (lo + hi) / 2


def _formatar(r):
    c, p, f, d = r["custos"], r["preco"], r["fluxo"], r["dre"]
    out = {k: brl(v) for k, v in c.items()}
    out.update({f"preco_{k}": (brl(v) if k in ("sugerido", "minimo", "receita_implantacao", "recorrente_mensal") else pct(v)) for k, v in p.items()
                if k not in ("origem_receita", "recorrente_meses")})
    sem_exposicao = (f["exposicao_maxima"] or 0) >= 0
    nao_se_aplica = "não se aplica (fluxo sem exposição)"
    out.update({"exposicao_maxima": brl(f["exposicao_maxima"]), "vpl": brl(f["vpl"]),
                "tir_aa": pct(f["tir_aa"]) if f["tir_aa"] is not None or not sem_exposicao else nao_se_aplica,
                "mes_pico": f["mes_pico"] or "[●]",
                "payback": f["payback"] or (nao_se_aplica if sem_exposicao else "não ocorre no horizonte")})
    for m in r.get("marcos", []) or []:
        out[f"marco_{m['id']}_pct"] = pct(m.get("pct"), 0)
        out[f"marco_{m['id']}_mes"] = m.get("competencia") or "[●]"
    for o in r.get("opcionais", []) or []:
        oid = str(o.get("id", "")).lower().replace("-", "_").removeprefix("opc_")
        for k, v in (o.get("preco_implantacao_brl") or {}).items():
            out[f"opc_{oid}_{k}"] = brl(v)
        for k, v in (o.get("mensalidade_adicional_brl") or {}).items():
            out[f"opc_{oid}_mensalidade_{k}"] = brl(v)
    out.update({f"dre_{k}": (pct(v) if k.startswith("margem") else brl(v)) for k, v in d.items()})
    out["prazo_meses"] = num(r["prazo"]["meses_provavel"], 1)
    if r.get("monte_carlo"):
        m = r["monte_carlo"]
        out.update({k: brl(m[k]) for k in ["custo_p10", "custo_p50", "custo_p80", "custo_p90"] if m.get(k) is not None})
        out["prazo_p50_meses"] = num((m.get("prazo_p50_dias") or 0) / 30.4, 1)
        out["prazo_p80_meses"] = num((m.get("prazo_p80_dias") or 0) / 30.4, 1)
    return out
