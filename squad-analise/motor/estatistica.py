"""Funções estatísticas padronizadas. Todas devolvem dicionários prontos para o resultado de uma análise:
{"valor": ..., "unidade": ..., "incerteza": {"tipo": ..., "inferior": ..., "superior": ..., "nivel": ...} | None, ...}

Tipos de incerteza: nenhuma · intervalo_confianca · intervalo_previsao · bootstrap · faixa_cenarios
"""
import numpy as np
from scipy import stats

AMOSTRA_MINIMA = 30


def _ic(tipo, inf, sup, nivel):
    return {"tipo": tipo, "inferior": float(inf), "superior": float(sup), "nivel": nivel}


def contagem(n, unidade="registros"):
    """Contagem de um censo (todos os registros do período): sem incerteza amostral."""
    return {"valor": int(n), "unidade": unidade, "incerteza": None, "contagem": True}


def media(x, unidade="", nivel=0.95):
    x = np.asarray(x, float); x = x[~np.isnan(x)]; n = len(x); m = float(x.mean())
    se = x.std(ddof=1) / np.sqrt(n) if n > 1 else float("nan"); t = stats.t.ppf(0.5 + nivel / 2, n - 1) if n > 1 else float("nan")
    return {"valor": m, "unidade": unidade, "incerteza": _ic("intervalo_confianca", m - t * se, m + t * se, nivel), "n": n, "amostra_pequena": n < AMOSTRA_MINIMA}


def diferenca_medias(a, b, unidade="", nivel=0.95):
    """Diferença média(a) − média(b), teste de Welch, IC e tamanho de efeito (d de Cohen)."""
    a = np.asarray(a, float); a = a[~np.isnan(a)]; b = np.asarray(b, float); b = b[~np.isnan(b)]
    na, nb = len(a), len(b); d = a.mean() - b.mean()
    va, vb = a.var(ddof=1) / na, b.var(ddof=1) / nb; se = np.sqrt(va + vb)
    gl = (va + vb) ** 2 / (va ** 2 / (na - 1) + vb ** 2 / (nb - 1))
    t = stats.t.ppf(0.5 + nivel / 2, gl); p = stats.ttest_ind(a, b, equal_var=False).pvalue
    sp = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    return {"valor": float(d), "unidade": unidade, "incerteza": _ic("intervalo_confianca", d - t * se, d + t * se, nivel),
            "p_valor": float(p), "efeito_d": float(d / sp) if sp else None, "n": [na, nb], "teste": "Welch",
            "amostra_pequena": min(na, nb) < AMOSTRA_MINIMA, "media_a": float(a.mean()), "media_b": float(b.mean())}


def diferenca_relativa(a, b, nivel=0.95, n_boot=4000, semente=42):
    """(média(a) − média(b)) / média(b), com intervalo por bootstrap."""
    a = np.asarray(a, float); a = a[~np.isnan(a)]; b = np.asarray(b, float); b = b[~np.isnan(b)]
    rng = np.random.default_rng(semente)
    bs = [(rng.choice(a, len(a)).mean() - (mb := rng.choice(b, len(b)).mean())) / mb for _ in range(n_boot)]
    lo, hi = np.percentile(bs, [50 * (1 - nivel), 100 - 50 * (1 - nivel)])
    return {"valor": float((a.mean() - b.mean()) / b.mean()), "unidade": "%", "incerteza": _ic("bootstrap", lo, hi, nivel), "n": [len(a), len(b)]}


def diferenca_proporcoes(sa, na, sb, nb, nivel=0.95):
    from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep
    d = sa / na - sb / nb
    lo, hi = confint_proportions_2indep(sa, na, sb, nb, method="newcomb", alpha=1 - nivel)
    p = proportions_ztest([sa, sb], [na, nb])[1]
    return {"valor": float(d), "unidade": "p.p.", "incerteza": _ic("intervalo_confianca", lo, hi, nivel), "p_valor": float(p), "n": [na, nb]}


def bootstrap(dados, funcao, unidade="", nivel=0.95, n_boot=4000, semente=42):
    x = np.asarray(dados); rng = np.random.default_rng(semente)
    bs = [funcao(x[rng.integers(0, len(x), len(x))]) for _ in range(n_boot)]
    lo, hi = np.percentile(bs, [50 * (1 - nivel), 100 - 50 * (1 - nivel)])
    return {"valor": float(funcao(x)), "unidade": unidade, "incerteza": _ic("bootstrap", lo, hi, nivel), "n": len(x)}


def correlacao(x, y, nivel=0.95):
    x = np.asarray(x, float); y = np.asarray(y, float); m = ~(np.isnan(x) | np.isnan(y)); x, y = x[m], y[m]; n = len(x)
    r, p = stats.pearsonr(x, y); z = np.arctanh(r); se = 1 / np.sqrt(n - 3); q = stats.norm.ppf(0.5 + nivel / 2)
    return {"valor": float(r), "unidade": "r", "incerteza": _ic("intervalo_confianca", np.tanh(z - q * se), np.tanh(z + q * se), nivel),
            "p_valor": float(p), "spearman": float(stats.spearmanr(x, y)[0]), "n": n}


def tendencia(y, x=None, unidade="por período", nivel=0.95):
    import statsmodels.api as sm
    y = np.asarray(y, float); x = np.arange(len(y)) if x is None else np.asarray(x, float)
    mod = sm.OLS(y, sm.add_constant(x)).fit(); lo, hi = mod.conf_int(1 - nivel)[1]
    return {"valor": float(mod.params[1]), "unidade": unidade, "incerteza": _ic("intervalo_confianca", lo, hi, nivel), "p_valor": float(mod.pvalues[1]), "n": len(y)}


def corrigir(p_valores, metodo="holm", alfa=0.05):
    from statsmodels.stats.multitest import multipletests
    rej, pc, _, _ = multipletests(p_valores, alpha=alfa, method={"holm": "holm", "bh": "fdr_bh"}.get(metodo, metodo))
    return [{"p_original": float(p), "p_corrigido": float(c), "significativo": bool(r)} for p, c, r in zip(p_valores, pc, rej)]


def robustez(df, coluna_recorte, funcao, minimo=AMOSTRA_MINIMA):
    """Aplica `funcao(sub_df) -> dict com 'valor'` em cada recorte e verifica se o sinal se mantém (inversão por segmento)."""
    geral = funcao(df)["valor"]; recs = []
    for k, sub in df.groupby(coluna_recorte):
        if len(sub) < minimo:
            recs.append({"recorte": str(k), "valor": None, "nota": f"amostra pequena ({len(sub)})"}); continue
        v = funcao(sub)["valor"]; recs.append({"recorte": str(k), "valor": float(v), "mesmo_sinal": bool(np.sign(v) == np.sign(geral))})
    validos = [r for r in recs if r["valor"] is not None]
    return {"geral": float(geral), "recortes": recs, "consistente": bool(validos) and all(r["mesmo_sinal"] for r in validos),
            "inversao": any(not r["mesmo_sinal"] for r in validos)}


def avaliar_previsao(y_real, y_prev, y_referencia):
    """Erro do modelo contra uma referência simples (por exemplo, a média ou o último valor) em dados fora do treino."""
    y_real, y_prev, y_ref = (np.asarray(v, float) for v in (y_real, y_prev, y_referencia))
    mae, mae_ref = float(np.mean(np.abs(y_real - y_prev))), float(np.mean(np.abs(y_real - y_ref)))
    return {"mae": mae, "mae_referencia": mae_ref, "ganho_vs_referencia": (1 - mae / mae_ref) if mae_ref else None, "melhor_que_referencia": mae < mae_ref}
