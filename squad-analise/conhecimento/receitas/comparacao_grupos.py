"""Receita: comparação entre dois grupos (exemplo: noite contra dia) com IC, efeito e robustez por dois recortes. Adapte a consulta e os nomes."""


def rodar(con, ctx):
    df = con.sql("select periodo, modelo, mes, duracao_min from prep_missoes").df()
    noite, dia = df[df.periodo == "noite"].duracao_min, df[df.periodo == "dia"].duracao_min
    dif = ctx.estat.diferenca_medias(noite, dia, unidade="min")
    rel = ctx.estat.diferenca_relativa(noite, dia)
    f = lambda d: ctx.estat.diferenca_medias(d[d.periodo == "noite"].duracao_min, d[d.periodo == "dia"].duracao_min)
    por_modelo = ctx.estat.robustez(df, "modelo", f)
    por_mes = ctx.estat.robustez(df, "mes", f)
    meses = df.mes.nunique()
    import pandas as pd
    tab = pd.DataFrame([{"recorte": "modelo " + r["recorte"], "dif_min": r["valor"]} for r in por_modelo["recortes"]] + [{"recorte": "mes " + r["recorte"], "dif_min": r["valor"]} for r in por_mes["recortes"]])
    return {"valores": {"dif_duracao_min": dif, "dif_relativa": rel,
                        "missoes_noite_por_mes": ctx.estat.contagem(round(len(noite) / meses), "missões/mês"),
                        "robusto_por_modelo": {"valor": float(por_modelo["consistente"]), "unidade": "", "incerteza": None, "contagem": True},
                        "robusto_por_mes": {"valor": float(por_mes["consistente"]), "unidade": "", "incerteza": None, "contagem": True}},
            "tabelas": {"robustez": tab}, "notas": "FICTÍCIO"}
