"""Gatekeeper: valida o estado até a fase indicada. Sai com código 1 se houver bloqueio.

Uso: python -m motor.validar <dir_versao> --fase F0|F1|F2|F3|F4|F5|F6
"""
import argparse, glob, json, re, sys
from pathlib import Path
from .util import (RAIZ, NOS, carregar_json, carregar_nos, config, tri, tri_valido, prov, dias_desde,
                   custo_hora_por_perfil, hash_obj)
from .calculo import itens_esforco, ordem_topologica
from .estado import status as status_nos

FASES = ["F0", "F1", "F2", "F3", "F4", "F5", "F6"]
NOS_DA_FASE = {"F0": ["meta", "briefing", "especificacao", "requisitos"], "F1": ["escopo", "solucao", "operacoes"],
               "F2": ["cronograma", "bom"], "F3": ["tributos", "custos_indiretos", "riscos"],
               "F4": ["preco", "contrato", "financeiro"], "F5": [], "F6": []}
ESPECIALISTAS = ["descoberta", "requisitos", "engenharia-robotica", "operacoes-posvenda", "gestao-projetos", "suprimentos", "tributario",
                 "cost-engineering", "financeiro", "contratos-riscos", "comercial-pricing", "marketing-proposta"]
FONTES_OK = {"cotacao", "base_interna", "benchmark", "premissa"}


class R:
    def __init__(self, modo):
        self.modo, self.bloq, self.aviso = modo, [], []
    def b(self, m): self.bloq.append(m)
    def a(self, m): self.aviso.append(m)
    def bc(self, m):  # bloqueia no completo, avisa no rápido
        (self.bloq if self.modo == "completo" else self.aviso).append(m)


def _vazio(no):
    return not no or no.get("_template")


def valor_bom_brl(it, meta):
    cam = {"BRL": 1.0}
    for m, c in (meta.get("cambio") or {}).items():
        t = c.get("taxa") if isinstance(c, dict) else c
        if t is not None:
            cam[m] = float(t)
    try:
        return prov(it["preco_unit"]) * float(it.get("qtd", 1)) * cam.get(it.get("moeda", "BRL"), 0)
    except Exception:
        return 0.0


def itens_sem_cotacao(nos):
    """Itens críticos sem cotação/base interna válida."""
    cfg = config(); meta = nos["meta"] or {}
    itens = (nos["bom"] or {}).get("itens", []) or []
    total = sum(valor_bom_brl(i, meta) for i in itens) or 1
    lim, val = float(cfg.get("item_critico_pct_bom", 0.05)), int(cfg.get("validade_cotacao_dias", 90))
    tec = {t["id"]: t for t in (nos["solucao"] or {}).get("lista_tecnica", []) or []}
    out = []
    for i in itens:
        critico = i.get("critico") or tec.get(i.get("ref_tecnica"), {}).get("critico") or valor_bom_brl(i, meta) / total >= lim
        f = i.get("fonte") or {}
        idade = dias_desde(f.get("data"))
        ok = f.get("tipo") in ("cotacao", "base_interna") and idade is not None and idade <= int(f.get("validade_dias") or val)
        if critico and not ok:
            out.append({"id": i["id"], "descricao": i.get("descricao"), "fabricante": i.get("fabricante"), "modelo": i.get("modelo"),
                        "qtd": i.get("qtd"), "especificacao": tec.get(i.get("ref_tecnica"), {}).get("especificacao"),
                        "fonte_atual": f.get("tipo"), "idade_dias": idade, "pct_bom": valor_bom_brl(i, meta) / total})
    return out


def validar(dv, fase):
    dv = Path(dv)
    nos = carregar_nos(dv)
    meta = nos["meta"] or {}
    r = R(meta.get("modo", "completo"))
    cfg = config()
    ate = FASES.index(fase)
    ctrl = carregar_json(dv / "controle.json", {"aprovacoes": []})
    gates = {a["gate"] for a in ctrl.get("aprovacoes", [])}

    # ---------- F0
    for k in ["projeto_id", "cliente", "projeto", "modo", "classe_estimativa", "data_base"]:
        if not meta.get(k): r.b(f"meta.{k} vazio")
    if not re.fullmatch(r"\d{4}-\d{2}", str(meta.get("mes_inicio", ""))): r.b("meta.mes_inicio deve ser AAAA-MM")
    if _vazio(nos["briefing"]) or not (nos["briefing"] or {}).get("texto"): r.b("briefing.texto vazio")
    if not _vazio(nos["especificacao"]):
        from .prontidao import avaliar as avaliar_prontidao
        pr = avaliar_prontidao(nos["especificacao"], r.modo)
        for m in pr["bloqueios"]: r.b(f"especificação: {m}")
        for m in pr["avisos"]: r.a(f"especificação: {m}")
        if pr["abertas"]: r.b(f"especificação: {len(pr['abertas'])} pergunta(s) ainda aberta(s)")
    req = nos["requisitos"] or {}
    itens_req = req.get("itens", []) or []
    if _vazio(req) or not itens_req: r.b("requisitos sem itens")
    for it in itens_req:
        for k in ["id", "descricao", "origem", "status", "prioridade"]:
            if not it.get(k): r.b(f"requisito {it.get('id', '?')}: campo {k} vazio")
        if it.get("origem") == "inferido" and it.get("status") == "confirmado" and "G1" not in gates:
            r.a(f"requisito {it.get('id')}: inferido marcado como confirmado antes da aprovação G1")
    pend = [i["id"] for i in itens_req if i.get("prioridade") == "obrigatorio" and i.get("status") == "pendente"]
    if pend: r.a(f"requisitos obrigatórios pendentes: {pend} (precisam estar nas perguntas abertas)")

    # ---------- F1
    if ate >= 1:
        if "G1" not in gates: r.b("falta aprovação G1 (matriz de requisitos)")
        esc = nos["escopo"] or {}
        wbs = {w["id"] for w in esc.get("wbs", []) or []}
        if not wbs: r.b("escopo.wbs vazio")
        for p in esc.get("premissas", []) or []:
            if not p.get("fonte") or not p.get("confianca"): r.b(f"premissa {p.get('id')}: sem fonte ou confiança")
        sol = nos["solucao"] or {}
        if not sol.get("solucoes"): r.b("solucao.solucoes vazio")
        min_alt = 3 if r.modo == "completo" else 2
        if not sol.get("criterios_selecao") or any(c.get("peso") is None for c in sol.get("criterios_selecao") or []):
            r.bc("solucao.criterios_selecao sem critérios ou sem pesos")
        for s in sol.get("solucoes", []) or []:
            alts = s.get("alternativas", []) or []
            if len(alts) < min_alt:
                r.bc(f"solução {s.get('id')}: {len(alts)} alternativa(s) de mercado avaliada(s); mínimo {min_alt} (neutralidade tecnológica)")
            if alts and (not s.get("escolhida") or not s.get("justificativa")):
                r.b(f"solução {s.get('id')}: sem alternativa escolhida ou sem justificativa pela matriz")
            for a in alts:
                if not a.get("fonte") or a.get("origem") not in ("mercado", "acta", "parceiro"):
                    r.b(f"solução {s.get('id')}: alternativa {a.get('id')} sem fonte ou com origem inválida")
            for d in s.get("dimensionamento", []) or []:
                if not d.get("memoria_calculo") or not d.get("fonte"):
                    r.b(f"dimensionamento '{d.get('parametro')}' da solução {s.get('id')}: sem memória de cálculo ou fonte")
        if not sol.get("lista_tecnica"): r.b("solucao.lista_tecnica vazia")
        for t in sol.get("lista_tecnica", []) or []:
            if t.get("wbs_id") not in wbs: r.b(f"lista técnica {t.get('id')}: wbs_id inexistente")
        rastreados = {x.get("requisito_id") for x in sol.get("rastreabilidade", []) or []}
        faltam = [i["id"] for i in itens_req if i.get("prioridade") == "obrigatorio" and i["id"] not in rastreados]
        if faltam: r.b(f"requisitos obrigatórios sem rastreabilidade na solução: {faltam}")
        if not sol.get("requisitos_infra_cliente"): r.a("solucao.requisitos_infra_cliente vazio")
        if _vazio(nos["operacoes"]): r.bc("operacoes vazio")
        ch = custo_hora_por_perfil()
        for it in itens_esforco(nos):
            if it.get("wbs_id") not in wbs and not it.get("atividade_id"): r.b(f"esforço {it.get('id')}: wbs_id inexistente")
            if not tri_valido(it.get("horas")): r.b(f"esforço {it.get('id')}: horas sem 3 pontos válidos (min ≤ provável ≤ max)")
            if not it.get("fonte"): r.b(f"esforço {it.get('id')}: sem fonte")
            if ate >= 2 and ch.get(it.get("perfil")) is None:
                r.b(f"perfil '{it.get('perfil')}' sem custo/hora em conhecimento/mao_de_obra/custo_hora.csv")
        for c in (nos["operacoes"] or {}).get("custos_recorrentes", []) or []:
            if not tri_valido(c.get("custo_mensal")) or not c.get("fonte"): r.b(f"custo recorrente {c.get('id')}: valor ou fonte inválidos")

    # ---------- F2
    if ate >= 2:
        cr = nos["cronograma"] or {}
        ats = cr.get("atividades", []) or []
        if not ats: r.b("cronograma sem atividades")
        ids = [a["id"] for a in ats]
        if len(ids) != len(set(ids)): r.b("cronograma: ids repetidos")
        for a in ats:
            if not tri_valido(a.get("duracao_dias")): r.b(f"atividade {a['id']}: duração sem 3 pontos válidos")
            for p in a.get("predecessoras", []) or []:
                if p not in ids: r.b(f"atividade {a['id']}: predecessora {p} inexistente")
        try:
            ordem_topologica(ats)
        except Exception as e:
            r.b(f"cronograma: {e}")
        mapeados = {w for a in ats for w in (a.get("wbs_ids") or [])}
        usados = {it.get("wbs_id") for it in itens_esforco(nos) if not it.get("atividade_id")}
        usados |= {b.get("wbs_id") for b in (nos["bom"] or {}).get("itens", []) or [] if not b.get("atividade_id")}
        sem = sorted(x for x in usados - mapeados if x)
        if sem: r.b(f"wbs sem atividade no cronograma: {sem}")
        bom = nos["bom"] or {}
        refs = {b.get("ref_tecnica") for b in bom.get("itens", []) or []}
        faltam = [t["id"] for t in (nos["solucao"] or {}).get("lista_tecnica", []) or [] if t["id"] not in refs]
        if faltam: r.b(f"itens da lista técnica sem preço na BOM: {faltam}")
        moedas = {m for m, c in (meta.get("cambio") or {}).items() if (c.get("taxa") if isinstance(c, dict) else c) is not None} | {"BRL"}
        pag_cfg = cfg.get("pagamento_padrao_bom") or {}
        for b in bom.get("itens", []) or []:
            if not tri_valido(b.get("preco_unit")): r.b(f"BOM {b['id']}: preço sem 3 pontos válidos")
            if not b.get("qtd") or float(b.get("qtd")) <= 0: r.b(f"BOM {b['id']}: quantidade inválida")
            if b.get("moeda", "BRL") not in moedas: r.b(f"BOM {b['id']}: moeda {b.get('moeda')} sem câmbio em meta.cambio")
            if b.get("origem") not in ("importado", "nacional"): r.b(f"BOM {b['id']}: origem deve ser importado|nacional")
            f = b.get("fonte") or {}
            if f.get("tipo") not in FONTES_OK or not f.get("ref") or not f.get("data"): r.b(f"BOM {b['id']}: fonte incompleta (tipo, ref, data)")
            if not tri_valido(b.get("lead_time_dias")): r.b(f"BOM {b['id']}: lead time sem 3 pontos válidos")
            if not b.get("pagamento") and not pag_cfg.get(b.get("origem")):
                r.bc(f"BOM {b['id']}: sem condição de pagamento (e sem padrão em config)")
        for c in (meta.get("cambio") or {}).values():
            if isinstance(c, dict) and (not c.get("data") or not c.get("fonte")): r.b("meta.cambio sem data ou fonte")
        pend = itens_sem_cotacao(nos)
        for p in pend:
            msg = f"COTAÇÃO HUMANA NECESSÁRIA: BOM {p['id']} ({p['descricao']}) — {p['pct_bom']:.1%} da BOM, fonte atual: {p['fonte_atual']}"
            r.bc(msg)

    # ---------- F3
    if ate >= 3:
        if "G2" not in gates: r.bc("falta aprovação G2 (escopo, BOM e cotações)")
        tr = nos["tributos"] or {}
        if _vazio(tr): r.b("tributos vazio")
        if not tr.get("regime"): r.b("tributos.regime vazio")
        if any(b.get("origem") == "importado" for b in (nos["bom"] or {}).get("itens", []) or []):
            imp = tr.get("custo_importacao_pct")
            if imp is None or (isinstance(imp, dict) and imp.get("padrao") is None): r.b("tributos.custo_importacao_pct.padrao vazio")
        if not tr.get("memoria_calculo") or not tr.get("fontes"): r.bc("tributos sem memória de cálculo ou fontes")
        ci = nos["custos_indiretos"] or {}
        if _vazio(ci): r.b("custos_indiretos vazio")
        if ci.get("overhead_pct") is None: r.bc("custos_indiretos.overhead_pct vazio")
        for it in ci.get("itens", []) or []:
            if not tri_valido(it.get("valor")) or not it.get("fonte"): r.b(f"indireto {it.get('id')}: valor ou fonte inválidos")
        ri = nos["riscos"] or {}
        if not ri.get("itens"): r.bc("riscos sem itens")
        for x in ri.get("itens", []) or []:
            p = x.get("probabilidade")
            if p is None or not (0 <= float(p) <= 1): r.b(f"risco {x.get('id')}: probabilidade fora de 0–1")
            if not x.get("dono") or not x.get("mitigacao"): r.b(f"risco {x.get('id')}: sem dono ou mitigação")
        dr = ri.get("drivers") or {}
        if not dr.get("cambio") or not dr.get("produtividade"): r.bc("riscos.drivers (câmbio e produtividade) não definidos")

    # ---------- F4
    if ate >= 4:
        pr = nos["preco"] or {}
        comp = pr.get("composicao_receita") or {}
        if not comp or abs(sum(comp.values()) - 1) > 1e-6: r.b("preco.composicao_receita deve somar 1")
        aliq = (nos["tributos"] or {}).get("impostos_receita_pct") or {}
        for t in comp:
            if aliq.get(t) is None: r.b(f"tributos.impostos_receita_pct sem tipo '{t}'")
        if pr.get("comissao_pct") is None: r.b("preco.comissao_pct vazio (use 0 se não houver)")
        if not pr.get("receita_fixada") and (pr.get("margem_alvo") is None or pr.get("margem_minima") is None):
            r.b("defina preco.margem_alvo e preco.margem_minima (ou preco.receita_fixada)")
        if not pr.get("roi_cliente"): r.bc("preco.roi_cliente vazio")
        ct = nos["contrato"] or {}
        mc_ = ct.get("marcos", []) or []
        if not mc_ or abs(sum(float(m["pct"]) for m in mc_) - 1) > 1e-6: r.b("contrato.marcos devem somar 1")
        ats = {a["id"] for a in (nos["cronograma"] or {}).get("atividades", []) or []}
        for m in mc_:
            if "mes" not in m and m.get("atividade_id") not in ats: r.b(f"marco {m.get('id')}: atividade inexistente")
        if (nos["financeiro"] or {}).get("custo_capital_aa") is None: r.b("financeiro.custo_capital_aa vazio")
        res = carregar_json(dv / "saidas" / "resumo.json")
        if not res: r.b("motor não executado (python -m motor.rodar)")
        elif res.get("_hashes") != {n: hash_obj(nos[n]) for n in NOS}: r.b("saídas do motor desatualizadas: rode o motor de novo")

    # ---------- F5
    if ate >= 5:
        rs = carregar_json(dv / "saidas" / "render_status.json", {})
        if not rs: r.b("entregáveis não renderizados")
        for arq, faltas in (rs.get("faltando") or {}).items():
            if faltas: r.b(f"{arq}: variáveis sem valor {faltas}")
        proib = cfg.get("termos_proibidos", [])
        for f in list((dv / "entregaveis").glob("*")) + list((dv / "saidas").glob("*.md")):
            txt = f.read_text(encoding="utf-8", errors="ignore")
            for t in proib:
                if re.search(rf"\b{re.escape(t)}\b", txt, re.I): r.b(f"{f.name}: termo proibido '{t}'")
            if f.suffix == ".md" and "[●]" in txt: r.bc(f"{f.name}: contém placeholder [●]")
            if f.name.endswith(".tpl") and re.search(r"R\$\s?\d", re.sub(r"\{\{.*?\}\}", "", txt)):
                r.a(f"{f.name}: valor em R$ digitado no texto; use variáveis do motor")

    # ---------- F6
    if ate >= 6:
        rev = {}
        for f in sorted(glob.glob(str(dv / "revisoes" / "*.json"))):
            d = carregar_json(f); rev.setdefault(d.get("agente_revisado") or Path(f).stem, []).append(d)
        if r.modo == "completo":
            for e in ESPECIALISTAS:
                ult = sorted(rev.get(e, []), key=lambda x: x.get("rodada", 0))
                if not ult: r.b(f"sem revisão do supervisor para {e}")
                elif ult[-1].get("veredito") not in ("aprovado", "aprovado_com_ressalvas"):
                    r.b(f"{e}: último veredito '{ult[-1].get('veredito')}'")
            if "red-team" not in rev: r.b("sem relatório do red team")
        aud = rev.get("auditor-consistencia")
        if not aud: r.bc("sem relatório do auditor de consistência")
        elif aud[-1].get("veredito") != "aprovado": r.b(f"auditor: veredito '{aud[-1].get('veredito')}'")

    # ---------- staleness e nós não preenchidos
    st = status_nos(dv, imprimir=False)
    alvo = [n for f in FASES[:ate + 1] for n in NOS_DA_FASE[f]]
    for n in alvo:
        s, det = st[n]
        if s == "vazio":
            r.b(f"nó {n}: não preenchido")
        elif s in ("desatualizado", "alterado_sem_carimbo", "nao_carimbado"):
            r.b(f"nó {n}: {s} {det if det else ''}".strip())
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dv"); ap.add_argument("--fase", choices=FASES, required=True)
    x = ap.parse_args()
    r = validar(x.dv, x.fase)
    print(f"== Validação até {x.fase} ({r.modo}) ==")
    for m in r.bloq: print("BLOQUEIO:", m)
    for m in r.aviso: print("aviso:", m)
    print("RESULTADO:", "BLOQUEADO" if r.bloq else "LIBERADO")
    sys.exit(1 if r.bloq else 0)


if __name__ == "__main__":
    main()
