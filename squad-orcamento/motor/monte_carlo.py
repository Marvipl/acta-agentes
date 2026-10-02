"""Simulação de Monte Carlo de custo de implantação e prazo.

- Cada item tem estimativa de 3 pontos (min, provável, max) -> distribuição triangular.
- Fatores comuns (câmbio e produtividade, em riscos.drivers) afetam vários itens ao mesmo tempo,
  para não subestimar o risco por cancelamento de erros independentes.
- Riscos do registro com no_monte_carlo=true entram como eventos (Bernoulli x impacto).
"""
import numpy as np
from .util import tri, config, custo_hora_por_perfil, fatores_aprovados
from .calculo import itens_esforco, atividade_do_wbs, ordem_topologica


def _amostra(rng, v, n):
    a, m, b = tri(v)
    if b - a < 1e-12:
        return np.full(n, m)
    return rng.triangular(a, m, b, n)


def simular(nos):
    cfg = config()
    n = int(cfg.get("monte_carlo_iteracoes", 10000))
    rng = np.random.default_rng(cfg.get("semente_aleatoria", 42))
    meta, trib, ind, ris = nos["meta"] or {}, nos["tributos"] or {}, nos["custos_indiretos"] or {}, nos["riscos"] or {}
    fat = fatores_aprovados()
    drivers = ris.get("drivers") or {}
    fx = _amostra(rng, drivers.get("cambio", 1.0), n)
    prodv = _amostra(rng, drivers.get("produtividade", 1.0), n)
    cambio = {"BRL": 1.0}
    for moeda, c in (meta.get("cambio") or {}).items():
        taxa = c.get("taxa") if isinstance(c, dict) else c
        if taxa is None:
            continue
        cambio[moeda] = float(taxa)
    imp = trib.get("custo_importacao_pct") or {}
    imp_padrao = imp.get("padrao") if isinstance(imp, dict) else imp
    nac = trib.get("custo_aquisicao_nacional_pct", 0.0) or 0.0

    contrib = {}
    bom = np.zeros(n)
    for it in (nos["bom"] or {}).get("itens", []) or []:
        moeda = it.get("moeda", "BRL")
        if moeda not in cambio:
            continue
        aliq = (imp.get(it["id"]) if isinstance(imp, dict) and it["id"] in imp else imp_padrao) if it.get("origem") == "importado" else nac
        v = _amostra(rng, it["preco_unit"], n) * float(it.get("qtd", 1)) * cambio[moeda] * (1 + float(aliq or 0)) * fat.get("bom", 1.0) \
            * (fat.get("bom_benchmark", 1.0) if (it.get("fonte") or {}).get("tipo") == "benchmark" else 1.0)
        if moeda != "BRL":
            v = v * fx
        bom += v; contrib[f"BOM {it['id']} {it.get('descricao', '')}"] = v

    ch = custo_hora_por_perfil()
    mo = np.zeros(n)
    for it in itens_esforco(nos):
        v = _amostra(rng, it["horas"], n) * prodv * float(ch.get(it.get("perfil")) or 0) * fat.get(f"horas_{it.get('categoria', 'geral')}", 1.0)
        mo += v; contrib[f"Horas {it['id']} {it.get('perfil', '')}"] = v

    indi = np.zeros(n)
    for it in ind.get("itens", []) or []:
        v = _amostra(rng, it["valor"], n) * fat.get(f"indiretos_{it.get('categoria', 'outros')}", 1.0)
        indi += v; contrib[f"Indireto {it['id']} {it.get('descricao', '')}"] = v
    overhead = (bom + mo) * float(ind.get("overhead_pct") or 0)

    eventos_custo = np.zeros(n); eventos_prazo = np.zeros(n)
    for r in ris.get("itens", []) or []:
        if not r.get("no_monte_carlo"):
            continue
        ocorre = rng.random(n) < float(r.get("probabilidade", 0))
        if r.get("impacto_custo") is not None:
            v = ocorre * _amostra(rng, r["impacto_custo"], n)
            eventos_custo += v; contrib[f"Risco {r['id']} {r.get('descricao', '')}"] = v
        if r.get("impacto_prazo_dias") is not None:
            eventos_prazo += ocorre * _amostra(rng, r["impacto_prazo_dias"], n)

    total = bom + mo + indi + overhead + eventos_custo

    atividades = (nos["cronograma"] or {}).get("atividades", []) or []
    prazo = np.zeros(n)
    if atividades:
        por_id = {a["id"]: a for a in atividades}
        ef = {}
        for i in ordem_topologica(atividades):
            es = np.zeros(n)
            for p in por_id[i].get("predecessoras", []):
                es = np.maximum(es, ef[p])
            ef[i] = es + _amostra(rng, por_id[i]["duracao_dias"], n) * fat.get("prazo_dias", 1.0)
        prazo = np.max(np.vstack(list(ef.values())), axis=0)
    prazo = prazo + eventos_prazo

    sens = []
    if np.std(total) > 0:
        for k, v in contrib.items():
            if np.std(v) > 0:
                sens.append((k, float(np.corrcoef(v, total)[0, 1]), float(np.std(v))))
    sens.sort(key=lambda x: -abs(x[1] * x[2]))
    pc = lambda a, q: float(np.percentile(a, q))
    # meta.percentil_contingencia (decisão de Marcus no projeto) prevalece sobre o padrão do config
    pct_cont = int(meta.get("percentil_contingencia") or cfg.get("percentil_contingencia", 80))
    return {
        "iteracoes": n,
        "custo_p10": pc(total, 10), "custo_p50": pc(total, 50), "custo_p80": pc(total, 80), "custo_p90": pc(total, 90),
        "custo_media": float(np.mean(total)),
        "prazo_p50_dias": pc(prazo, 50), "prazo_p80_dias": pc(prazo, 80), "prazo_p90_dias": pc(prazo, 90),
        "maiores_contribuidores": [{"item": k, "correlacao": round(c, 3), "desvio_brl": round(s, 2)} for k, c, s in sens[:10]],
        "drivers": {"cambio": drivers.get("cambio"), "produtividade": drivers.get("produtividade")},
        "percentil_contingencia": pct_cont,
        "custo_percentil_contingencia": pc(total, pct_cont),
    }
