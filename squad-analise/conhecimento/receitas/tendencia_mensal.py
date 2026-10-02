"""Receita: tendência mensal de uma métrica com IC e gráfico. Adapte a consulta."""


def rodar(con, ctx):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    m = con.sql("select mes, avg(duracao_min) as media, count(*) as n from prep_missoes group by mes order by mes").df()
    tend = ctx.estat.tendencia(m.media.values, unidade="min por mês")
    fig, ax = plt.subplots(figsize=(7, 3.2)); ax.plot(m.mes, m.media, marker="o", color="#EE7D00"); ax.set_ylabel("min"); ax.set_title("Duração média por mês (FICTÍCIO)")
    fig.tight_layout(); fig.savefig(ctx.figura("duracao_mensal"), dpi=110); plt.close(fig)
    return {"valores": {"tendencia_mensal": tend}, "tabelas": {"por_mes": m}}
