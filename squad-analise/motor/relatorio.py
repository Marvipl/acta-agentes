"""Gera os entregáveis: preenche os textos (*.md.tpl) com variáveis do motor, cartões de insight, painel HTML local e planilha.

Variáveis disponíveis nos textos: {{meta.*}}, {{decisao.*}}, {{fmt.*}} — por exemplo {{fmt.ins_INS_001}} (texto do insight
com os números), {{fmt.imp_IMP_001_p50}}, {{fmt.n_aprovados}}, {{fmt.auditoria}}.
"""
import base64, html
from pathlib import Path
from .util import carregar_json, agora
from .renderizar import renderizar


def _num(v, u=""):
    if v is None: return "[●]"
    if u in ("R$", "BRL", "R$/mes", "R$/mês", "R$/ano"):
        return "R$ " + f"{v:,.0f}".replace(",", ".") + (u[2:] if u.startswith("R$/") else "")
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + (f" {u}" if u else "")


def resumo(dv):
    dv = Path(dv); ins = (carregar_json(dv / "saidas" / "insights.json", {}) or {}).get("insights", [])
    imp = (carregar_json(dv / "saidas" / "impacto.json", {}) or {}).get("modelos", {})
    aud = carregar_json(dv / "saidas" / "auditoria.json", {}) or {}
    f = {"n_insights": str(len(ins)), "n_aprovados": str(sum(1 for i in ins if i["estado"] == "aprovado")),
         "auditoria": {"ok": "aprovada", "falhou": "reprovada", "bloqueado": "bloqueada"}.get(aud.get("status"), "não executada")}
    for i in ins:
        k = i["id"].replace("-", "_")
        f[f"ins_{k}"] = i["texto"]; f[f"ins_{k}_confianca"] = i.get("confianca") or "[●]"; f[f"ins_{k}_acao"] = i.get("acao") or "[●]"
    for mid, m in imp.items():
        k = mid.replace("-", "_"); u = m.get("unidade") or ""
        for q in ("provavel", "p10", "p50", "p90"):
            f[f"imp_{k}_{q}"] = _num(m[q], u)
    return {"meta": carregar_json(dv / "nos" / "meta.json", {}), "decisao": carregar_json(dv / "nos" / "decisao.json", {}), "fmt": f}


def cartoes(dv):
    dv = Path(dv); ins = (carregar_json(dv / "saidas" / "insights.json", {}) or {}).get("insights", [])
    rotulo = {"aprovado": "APROVADO", "acionavel": "acionável, aguardando G3", "validado": "validado, sem impacto calculado",
              "quantificado": "quantificado, não validado", "descoberto": "apenas descoberto"}
    l = ["# Cartões de insight", "", f"Gerado em {agora()}. Só os aprovados entram no memorando e no relatório.", ""]
    for i in ins:
        l += [f"## {i['id']} · {rotulo.get(i['estado'], i['estado'])}", "", i["texto"], "",
              f"- Nível: {i.get('nivel') or '[●]'} · confiança: {i.get('confianca') or '[●]'}"]
        if i.get("impacto"):
            m = i["impacto"]; l.append(f"- Impacto ({m.get('descricao')}): provável {_num(m['provavel'], m.get('unidade') or '')}; P10 {_num(m['p10'], m.get('unidade') or '')} a P90 {_num(m['p90'], m.get('unidade') or '')}")
        if i.get("acao"): l.append(f"- Ação: {i['acao']} (dono: {i.get('dono') or '[●]'})")
        l.append("")
    (dv / "saidas" / "cartoes_insight.md").write_text("\n".join(l), encoding="utf-8")


def painel(dv):
    dv = Path(dv); r = resumo(dv); ins = (carregar_json(dv / "saidas" / "insights.json", {}) or {}).get("insights", [])
    meta = r["meta"] or {}; dec = r["decisao"] or {}
    figs = []
    for p in sorted((dv / "saidas" / "analises").glob("*/*.png")):
        figs.append((p.parent.name, p.stem, base64.b64encode(p.read_bytes()).decode()))
    cor = {"aprovado": "#2BA5B2", "acionavel": "#EE7D00", "validado": "#3A3A3A"}
    cards = "".join(f"<div class='card' style='border-left:6px solid {cor.get(i['estado'], '#bbb')}'><div class='tag'>{html.escape(i['id'])} · {html.escape(i['estado'])} · {html.escape(i.get('nivel') or '')}</div><p>{html.escape(i['texto'])}</p>"
                    + (f"<p class='imp'>Impacto provável: {html.escape(_num(i['impacto']['provavel'], i['impacto'].get('unidade') or ''))}</p>" if i.get("impacto") else "")
                    + (f"<p class='acao'>Ação: {html.escape(i['acao'])}</p>" if i.get("acao") else "") + "</div>" for i in ins)
    graf = "".join(f"<figure><img src='data:image/png;base64,{b}' alt='{html.escape(a)} {html.escape(n)}'><figcaption>{html.escape(a)} · {html.escape(n)}</figcaption></figure>" for a, n, b in figs)
    doc = f"""<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>Análise · {html.escape(meta.get('tema') or '')}</title><style>
body{{font-family:Arial,Helvetica,sans-serif;margin:0;background:#F4F4F4;color:#111626}}header{{background:#111626;color:#fff;padding:20px 28px}}
header h1{{margin:0;font-size:22px}}header p{{margin:6px 0 0;color:#cfd3dc}}main{{max-width:1100px;margin:0 auto;padding:20px}}
.card{{background:#fff;border-radius:8px;padding:14px 18px;margin:12px 0}}.tag{{font-size:12px;color:#3A3A3A;text-transform:uppercase;letter-spacing:.04em}}
.imp{{color:#EE7D00;font-weight:bold}}.acao{{color:#3A3A3A}}figure{{background:#fff;border-radius:8px;padding:12px;margin:12px 0}}img{{max-width:100%}}
figcaption{{font-size:12px;color:#3A3A3A}}.aud{{display:inline-block;padding:4px 10px;border-radius:12px;background:#2BA5B2;color:#fff;font-size:12px}}</style></head>
<body><header><h1>{html.escape(meta.get('tema') or 'Análise')}</h1><p>{html.escape(dec.get('decisao') or meta.get('objetivo') or '')}</p>
<p><span class='aud'>Auditoria: {html.escape(r['fmt']['auditoria'])}</span> · {html.escape(r['fmt']['n_aprovados'])} de {html.escape(r['fmt']['n_insights'])} insights aprovados · gerado em {html.escape(agora())}</p></header>
<main><h2>Insights</h2>{cards or '<p>Nenhum insight registrado.</p>'}<h2>Gráficos das análises</h2>{graf or '<p>Nenhum gráfico.</p>'}</main></body></html>"""
    (dv / "saidas" / "painel.html").write_text(doc, encoding="utf-8")


def planilha(dv):
    import pandas as pd
    dv = Path(dv); arq = dv / "saidas" / f"resultados_{(carregar_json(dv / 'nos' / 'meta.json', {}) or {}).get('projeto_id', 'analise')}.xlsx"
    ins = (carregar_json(dv / "saidas" / "insights.json", {}) or {}).get("insights", [])
    with pd.ExcelWriter(arq, engine="openpyxl") as w:
        pd.DataFrame([{"id": i["id"], "estado": i["estado"], "insight": i["texto"], "nivel": i.get("nivel"), "confianca": i.get("confianca"),
                       "impacto_provavel": (i.get("impacto") or {}).get("provavel"), "unidade": (i.get("impacto") or {}).get("unidade"), "acao": i.get("acao"), "dono": i.get("dono")} for i in ins]
                     or [{"id": None}]).to_excel(w, sheet_name="Insights", index=False)
        linhas = []
        for p in sorted((dv / "saidas" / "analises").glob("*/resultado.json")):
            for k, v in (carregar_json(p).get("valores") or {}).items():
                inc = v.get("incerteza") or {}
                linhas.append({"analise": p.parent.name, "chave": k, "valor": v.get("valor"), "unidade": v.get("unidade"), "incerteza": inc.get("tipo"),
                               "inferior": inc.get("inferior"), "superior": inc.get("superior"), "p_valor": v.get("p_valor"), "n": str(v.get("n", ""))})
        pd.DataFrame(linhas or [{"analise": None}]).to_excel(w, sheet_name="Valores", index=False)
        imp = (carregar_json(dv / "saidas" / "impacto.json", {}) or {}).get("modelos", {})
        pd.DataFrame([{"modelo": k, **v} for k, v in imp.items()] or [{"modelo": None}]).to_excel(w, sheet_name="Impacto", index=False)
        for p in sorted((dv / "saidas" / "analises").glob("*/*.csv"))[:20]:
            pd.read_csv(p).head(50000).to_excel(w, sheet_name=f"{p.parent.name}_{p.stem}"[:31], index=False)
    return arq


def gerar(dv):
    cartoes(dv); painel(dv); arq = planilha(dv)
    falta = renderizar(dv, resumo(dv))
    return arq, falta
