"""Gera a planilha mestre (xlsx) com fórmulas nas linhas de custo, fluxo e DRE.

Convenção: azul = premissa vinda dos nós; preto = fórmula; verde = vínculo entre abas.
A planilha espelha o motor. Para alterar números, edite os nós e rode o motor de novo.
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter as L

AZUL, VERDE = Font(name="Arial", size=10, color="0000FF"), Font(name="Arial", size=10, color="008000")
NORMAL, NEGRITO = Font(name="Arial", size=10), Font(name="Arial", size=10, bold=True)
CAB = Font(name="Arial", size=10, bold=True, color="FFFFFF")
FUNDO = PatternFill("solid", fgColor="111626")
DESTAQUE = PatternFill("solid", fgColor="F4F4F4")
BRL = '"R$" #,##0.00;("R$" #,##0.00);-'
PCT = '0.0%;(0.0%);-'


def _cab(ws, cols, larg=None):
    for i, c in enumerate(cols, 1):
        x = ws.cell(row=1, column=i, value=c)
        x.font, x.fill, x.alignment = CAB, FUNDO, Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[L(i)].width = (larg or {}).get(i, 16)
    ws.freeze_panes = "A2"


def _v(ws, r, c, v, fmt=None, font=AZUL):
    x = ws.cell(row=r, column=c, value=v)
    x.font = font
    if fmt: x.number_format = fmt
    return x


def gerar(caminho, resumo, det, nos):
    wb = Workbook()
    # ---------------- BOM
    ws = wb.active; ws.title = "BOM"
    _cab(ws, ["ID", "Descrição", "Qtd", "Moeda", "Preço unit. (moeda)", "Câmbio", "Alíq. aquisição", "Fator calibração", "Total (R$)", "Fonte", "Atividade", "Mês pedido", "Mês entrega"], {2: 38})
    r = 2
    for b in det["bom"]:
        _v(ws, r, 1, b["id"]); _v(ws, r, 2, b["descricao"]); _v(ws, r, 3, b["qtd"]); _v(ws, r, 4, b["moeda"])
        _v(ws, r, 5, b["preco_unit"], "#,##0.00"); _v(ws, r, 6, b["cambio"], "0.0000"); _v(ws, r, 7, b["aliq_aquisicao"], PCT)
        _v(ws, r, 8, b.get("fator", 1.0), "0.00")
        _v(ws, r, 9, f"=C{r}*E{r}*F{r}*(1+G{r})*H{r}", BRL, NORMAL)
        _v(ws, r, 10, b["fonte"]); _v(ws, r, 11, b["atividade"]); _v(ws, r, 12, b["mes_pedido"]); _v(ws, r, 13, b["mes_entrega"])
        r += 1
    bom_tot = r
    _v(ws, r, 2, "TOTAL", font=NEGRITO); _v(ws, r, 9, f"=SUM(I2:I{max(r-1,2)})", BRL, NEGRITO)

    # ---------------- Mão de obra
    wm = wb.create_sheet("Mao_de_obra")
    _cab(wm, ["ID", "Origem", "Perfil", "Categoria", "Horas (calibradas)", "Custo/hora (R$)", "Total (R$)", "Atividade"], {3: 26})
    r = 2
    for m in det["mao_de_obra"]:
        _v(wm, r, 1, m["id"]); _v(wm, r, 2, m["origem"]); _v(wm, r, 3, m["perfil"]); _v(wm, r, 4, m["categoria"])
        _v(wm, r, 5, m["horas"], "#,##0.0"); _v(wm, r, 6, m["custo_hora"], BRL)
        _v(wm, r, 7, f"=E{r}*F{r}", BRL, NORMAL); _v(wm, r, 8, m["atividade"]); r += 1
    mo_tot = r
    _v(wm, r, 3, "TOTAL", font=NEGRITO); _v(wm, r, 5, f"=SUM(E2:E{max(r-1,2)})", "#,##0.0", NEGRITO)
    _v(wm, r, 7, f"=SUM(G2:G{max(r-1,2)})", BRL, NEGRITO)

    # ---------------- Indiretos e custo
    wi = wb.create_sheet("Custos")
    _cab(wi, ["ID", "Descrição", "Categoria", "Valor (R$)", "Fonte"], {2: 40})
    r = 2
    for i in det["indiretos"]:
        _v(wi, r, 1, i["id"]); _v(wi, r, 2, i["descricao"]); _v(wi, r, 3, i["categoria"]); _v(wi, r, 4, i["valor_brl"], BRL); _v(wi, r, 5, i["fonte"]); r += 1
    ind_tot = r
    _v(wi, r, 2, "Total indiretos", font=NEGRITO); _v(wi, r, 4, f"=SUM(D2:D{max(r-1,2)})", BRL, NEGRITO)
    r += 2
    ov = (nos.get("custos_indiretos") or {}).get("overhead_pct") or 0
    linhas = [("Equipamentos (BOM)", f"=BOM!I{bom_tot}", VERDE), ("Mão de obra", f"=Mao_de_obra!G{mo_tot}", VERDE),
              ("Indiretos", f"=D{ind_tot}", NORMAL)]
    ini = r
    for nome, f, fnt in linhas:
        _v(wi, r, 2, nome, font=NORMAL); _v(wi, r, 4, f, BRL, fnt); r += 1
    _v(wi, r, 2, "Overhead (% sobre BOM + mão de obra)", font=NORMAL); _v(wi, r, 3, ov, PCT); _v(wi, r, 4, f"=C{r}*(D{ini}+D{ini+1})", BRL, NORMAL); r += 1
    _v(wi, r, 2, "Custo base", font=NEGRITO); _v(wi, r, 4, f"=SUM(D{ini}:D{r-1})", BRL, NEGRITO); base_r = r; r += 1
    _v(wi, r, 2, "Contingência (Monte Carlo)", font=NORMAL); _v(wi, r, 4, resumo["custos"]["contingencia"], BRL); r += 1
    _v(wi, r, 2, "Custo com contingência", font=NEGRITO); _v(wi, r, 4, f"=D{base_r}+D{r-1}", BRL, NEGRITO)

    # ---------------- Cronograma e histograma
    wc = wb.create_sheet("Cronograma")
    _cab(wc, ["ID", "Atividade", "Início (dia)", "Fim (dia)", "Folga (dias)", "Crítica"], {2: 40})
    for r, a in enumerate(det["cronograma"], 2):
        for c, k in enumerate(["id", "nome", "inicio_dia", "fim_dia", "folga_dias", "critica"], 1):
            _v(wc, r, c, a[k], "#,##0.0" if c in (3, 4, 5) else None, NORMAL)
    wh = wb.create_sheet("Histograma")
    meses = sorted({m for p in det["histograma"].values() for m in p})
    _cab(wh, ["Perfil (horas/mês)"] + meses, {1: 28})
    for r, (perfil, ms) in enumerate(det["histograma"].items(), 2):
        _v(wh, r, 1, perfil, font=NORMAL)
        for c, m in enumerate(meses, 2):
            _v(wh, r, c, ms.get(m, 0), "#,##0.0", NORMAL)

    # ---------------- Fluxo de caixa
    wf = wb.create_sheet("Fluxo_de_caixa")
    cols = ["receita_implantacao", "receita_recorrente", "receita_operacao", "impostos", "comissao", "equipamentos",
            "mao_de_obra", "indiretos", "overhead", "contingencia", "custos_recorrentes", "custo_variavel_operacao",
            "custo_financeiro"]
    _cab(wf, ["Mês", "Competência"] + [c.replace("_", " ").capitalize() for c in cols] + ["Saldo do mês", "Acumulado"])
    fl = det["fluxo"]
    for r, l in enumerate(fl, 2):
        _v(wf, r, 1, l["mes"], font=NORMAL); _v(wf, r, 2, l["competencia"], font=NORMAL)
        for c, k in enumerate(cols, 3):
            _v(wf, r, c, l[k], BRL)
        sc = 3 + len(cols)
        _v(wf, r, sc, f"=SUM(C{r}:{L(sc-1)}{r})", BRL, NORMAL)
        _v(wf, r, sc + 1, f"={L(sc)}{r}" if r == 2 else f"={L(sc+1)}{r-1}+{L(sc)}{r}", BRL, NORMAL)
    last = len(fl) + 1
    col = {k: L(i) for i, k in enumerate(cols, 3)}

    # ---------------- DRE
    wd = wb.create_sheet("DRE")
    _cab(wd, ["Linha", "Valor (R$)", "% receita bruta"], {1: 40})
    S = lambda k: f"SUM(Fluxo_de_caixa!{col[k]}2:{col[k]}{last})"
    dre = [("Receita bruta", f"={S('receita_implantacao')}+{S('receita_recorrente')}+{S('receita_operacao')}", True),
           ("(-) Impostos sobre receita", f"={S('impostos')}", False),
           ("Receita líquida", "=B2+B3", True),
           ("(-) Equipamentos", f"={S('equipamentos')}", False),
           ("(-) Mão de obra direta", f"={S('mao_de_obra')}", False),
           ("(-) Custos recorrentes (O&M)", f"={S('custos_recorrentes')}", False),
           ("(-) Custos variáveis da operação comercial", f"={S('custo_variavel_operacao')}", False),
           ("Lucro bruto", "=B4+B5+B6+B7+B8", True),
           ("(-) Comissão", f"={S('comissao')}", False),
           ("(-) Indiretos", f"={S('indiretos')}", False),
           ("(-) Overhead", f"={S('overhead')}", False),
           ("(-) Contingência", f"={S('contingencia')}", False),
           ("Resultado operacional", "=B9+B10+B11+B12+B13", True),
           ("(-) Custo financeiro", f"={S('custo_financeiro')}", False),
           ("Resultado do projeto", "=B14+B15", True)]
    for r, (nome, f, neg) in enumerate(dre, 2):
        fn = NEGRITO if neg else NORMAL
        _v(wd, r, 1, nome, font=fn); _v(wd, r, 2, f, BRL, VERDE if "Fluxo" in f else fn)
        _v(wd, r, 3, f"=IF($B$2=0,0,B{r}/$B$2)", PCT, fn)
        if neg:
            for c in (1, 2, 3): wd.cell(row=r, column=c).fill = DESTAQUE

    # ---------------- Marcos, Monte Carlo, Riscos, Premissas
    wk = wb.create_sheet("Marcos")
    _cab(wk, ["ID", "Evento", "%", "Mês (índice)", "Valor (R$)"], {2: 40})
    for r, m in enumerate(resumo.get("marcos", []), 2):
        _v(wk, r, 1, m["id"]); _v(wk, r, 2, m["evento"]); _v(wk, r, 3, m["pct"], PCT); _v(wk, r, 4, m["mes"]); _v(wk, r, 5, m["valor_brl"], BRL)

    wmc = wb.create_sheet("Monte_Carlo")
    _cab(wmc, ["Indicador", "Valor"], {1: 50, 2: 22})
    mc = resumo.get("monte_carlo") or {}
    r = 2
    for k in ["iteracoes", "custo_p10", "custo_p50", "custo_p80", "custo_p90", "prazo_p50_dias", "prazo_p80_dias"]:
        _v(wmc, r, 1, k, font=NORMAL); _v(wmc, r, 2, mc.get(k), BRL if k.startswith("custo") else "#,##0", NORMAL); r += 1
    r += 1; _v(wmc, r, 1, "Maiores contribuidores de incerteza", font=NEGRITO); r += 1
    for c in (det.get("mc_contrib") or []):
        _v(wmc, r, 1, c["item"], font=NORMAL); _v(wmc, r, 2, c["correlacao"], "0.00", NORMAL); r += 1

    wr = wb.create_sheet("Riscos")
    _cab(wr, ["ID", "Descrição", "Categoria", "Probabilidade", "Impacto custo (provável)", "Impacto prazo (dias)", "Mitigação", "Dono", "No Monte Carlo"], {2: 40, 7: 40})
    for r, x in enumerate((nos.get("riscos") or {}).get("itens", []) or [], 2):
        ic = x.get("impacto_custo"); ip = x.get("impacto_prazo_dias")
        vals = [x.get("id"), x.get("descricao"), x.get("categoria"), x.get("probabilidade"),
                ic.get("provavel") if isinstance(ic, dict) else ic, ip.get("provavel") if isinstance(ip, dict) else ip,
                x.get("mitigacao"), x.get("dono"), x.get("no_monte_carlo")]
        for c, v in enumerate(vals, 1):
            _v(wr, r, c, v, PCT if c == 4 else (BRL if c == 5 else None))

    wp = wb.create_sheet("Premissas")
    _cab(wp, ["ID", "Premissa", "Fonte", "Confiança"], {2: 70, 3: 30})
    for r, p in enumerate((nos.get("escopo") or {}).get("premissas", []) or [], 2):
        for c, k in enumerate(["id", "texto", "fonte", "confianca"], 1):
            _v(wp, r, c, p.get(k), font=NORMAL)

    # ---------------- Resumo (primeira aba)
    wsr = wb.create_sheet("Resumo", 0)
    _cab(wsr, ["Indicador", "Valor"], {1: 46, 2: 26})
    m = resumo["meta"]; p = resumo["preco"]; f = resumo["fluxo"]
    itens = [("Projeto", f"{m.get('cliente')} – {m.get('projeto')}", None), ("Versão / modo", f"v{m.get('versao')} / {m.get('modo')}", None),
             ("Classe da estimativa (AACE)", m.get("classe_estimativa"), None), ("Data-base", m.get("data_base"), None),
             ("Custo base", "=Custos!D" + str(base_r), BRL), ("Contingência", resumo["custos"]["contingencia"], BRL),
             ("Custo P50 (Monte Carlo)", mc.get("custo_p50"), BRL), ("Custo P80 (Monte Carlo)", mc.get("custo_p80"), BRL),
             ("Preço sugerido", p.get("sugerido"), BRL), ("Preço mínimo (walk-away)", p.get("minimo"), BRL),
             ("Receita de implantação usada", p.get("receita_implantacao"), BRL), ("Origem da receita", p.get("origem_receita"), None),
             ("Margem resultante", p.get("margem_resultante"), PCT), ("Resultado do projeto (DRE)", "=DRE!B16", BRL),
             ("Margem líquida (DRE)", "=DRE!C16", PCT), ("Exposição máxima de caixa", f.get("exposicao_maxima"), BRL),
             ("Mês do pico de exposição", f.get("mes_pico"), None), ("Payback", f.get("payback") or "não ocorre no horizonte", None),
             ("VPL ao custo de capital", f.get("vpl"), BRL), ("TIR anual", f.get("tir_aa"), PCT),
             ("Prazo provável (meses)", resumo["prazo"]["meses_provavel"], "0.0"),
             ("Prazo P80 (dias)", mc.get("prazo_p80_dias"), "#,##0")]
    for r, (k, v, fmt) in enumerate(itens, 2):
        _v(wsr, r, 1, k, font=NORMAL)
        _v(wsr, r, 2, v, fmt, VERDE if isinstance(v, str) and v.startswith("=") else NORMAL)
    r = len(itens) + 3
    _v(wsr, r, 1, "Alertas do motor", font=NEGRITO)
    for i, a in enumerate(resumo.get("alertas", []) or ["nenhum"], r + 1):
        _v(wsr, i, 1, a, font=NORMAL)
    r = i + 2
    _v(wsr, r, 1, "Legenda: azul = premissa dos nós; preto = fórmula; verde = vínculo entre abas. Edite os nós, não a planilha.", font=NORMAL)
    wb.save(caminho)
