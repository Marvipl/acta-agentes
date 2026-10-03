"""Gatekeeper do planejamento estratégico. Sai com código 1 se houver bloqueio.

Uso: python -m motor.validar <dir_versao> --fase E0|E1|E2|E3|E4
"""
import argparse, glob, re, sys
from pathlib import Path
from .util import NOS, carregar_json, carregar_nos, config, hash_obj
from .estado import status as status_nos

FASES = ["E0", "E1", "E2", "E3", "E4"]
NOS_DA_FASE = {"E0": ["meta", "briefing", "enquadramento"],
               "E1": ["mercado", "concorrencia", "regulatorio", "interno", "capacidades", "diagnostico"],
               "E2": ["opcoes", "portfolio", "financeiro_opcoes"],
               "E3": ["okrs", "organizacao", "iniciativas", "planos_funcionais", "juridico_tributario", "financeiro", "riscos", "governanca"], "E4": []}
NOS_ESTUDO = {"meta", "briefing", "enquadramento", "mercado", "concorrencia", "regulatorio", "interno", "capacidades",
              "diagnostico", "opcoes", "financeiro_opcoes"}
ESPECIALISTAS = ["enquadramento", "inteligencia-mercado", "concorrencia", "regulatorio-fomento", "desempenho-interno",
                 "capacidades-organizacao", "arquiteto-estrategia", "portfolio-iniciativas", "financeiro-estrategico",
                 "okr-kpi", "planos-funcionais", "riscos-governanca", "narrativa-comunicacao"]
TIPOS_EV = {"confirmado", "reportado", "estimativa", "interno"}
MODELOS = {"fabricante", "integradora", "distribuidora", "plataforma", "operadora"}
RECEITAS = {"venda", "locacao_raas", "recorrencia", "distribuicao", "servicos"}
AREAS_PLANO = ["comercial_marketing", "produto_tecnologia", "operacoes", "parcerias"]
AREAS_INI = set(AREAS_PLANO) | {"pessoas", "captacao", "juridico", "outra"}


class R:
    def __init__(self, modo): self.modo, self.bloq, self.aviso = modo, [], []
    def b(self, m): self.bloq.append(m)
    def a(self, m): self.aviso.append(m)
    def bp(self, m): (self.bloq if self.modo == "plano" else self.aviso).append(m)


def _ev_ids(nos):
    ids, tipos = set(), {}
    for n in ["mercado", "concorrencia", "regulatorio", "interno", "capacidades"]:
        for e in (nos[n] or {}).get("evidencias", []) or []:
            ids.add(e.get("id")); tipos[e.get("id")] = e.get("tipo")
    return ids, tipos


def validar(dv, fase):
    dv = Path(dv); nos = carregar_nos(dv); meta = nos["meta"] or {}
    r = R(meta.get("modo", "plano")); ate = FASES.index(fase)
    ctrl = carregar_json(dv / "controle.json", {"aprovacoes": []})
    gates = {a["gate"] for a in ctrl.get("aprovacoes", [])}

    # E0
    for k in ["projeto_id", "ciclo", "titulo", "modo", "data_base"]:
        if not meta.get(k): r.b(f"meta.{k} vazio")
    if not re.fullmatch(r"\d{4}-\d{2}", str(meta.get("mes_inicio", ""))): r.b("meta.mes_inicio deve ser AAAA-MM")
    if r.modo == "estudo" and not (nos["briefing"] or {}).get("pergunta_estudo"): r.b("briefing.pergunta_estudo vazio (modo estudo)")
    enq = nos["enquadramento"] or {}
    if enq:
        from .prontidao import avaliar
        pr = avaliar(enq, "completo" if r.modo == "plano" else "rapido")
        for m in pr["bloqueios"]: r.b(f"enquadramento: {m}")
        if pr["abertas"]: r.b(f"enquadramento: {len(pr['abertas'])} pergunta(s) aberta(s)")
        if not enq.get("ambicao"): r.b("enquadramento.ambicao vazio")

    # E1
    if ate >= 1:
        if "G1" not in gates: r.b("falta aprovação G1 (enquadramento)")
        ids, tipos = _ev_ids(nos)
        for n in ["mercado", "concorrencia", "regulatorio", "interno", "capacidades"]:
            for e in (nos[n] or {}).get("evidencias", []) or []:
                if e.get("tipo") not in TIPOS_EV: r.b(f"{n}: evidência {e.get('id')} com tipo inválido")
                if not e.get("fonte") or not e.get("data"): r.b(f"{n}: evidência {e.get('id')} sem fonte ou data")
                if e.get("tipo") in ("confirmado", "reportado", "estimativa") and not e.get("url"):
                    r.a(f"{n}: evidência {e.get('id')} externa sem link")
        externas = [i for i, t in tipos.items() if t in ("confirmado", "reportado", "estimativa")]
        if externas and sum(1 for i in externas if tipos[i] == "confirmado") / len(externas) < 0.3:
            r.a("menos de 30% das evidências externas são confirmadas por fonte primária")
        def refs_ok(lista, onde):
            for x in lista or []:
                faltam = [e for e in x.get("evidencias", []) or [] if e not in ids]
                if not x.get("evidencias"): r.b(f"{onde}: item sem evidência ({str(x.get('titulo') or x.get('nome') or x.get('texto') or x.get('segmento') or x.get('linha'))[:40]})")
                elif faltam: r.b(f"{onde}: evidências inexistentes {faltam}")
        mk = nos["mercado"] or {}
        refs_ok(mk.get("tendencias"), "mercado.tendencias"); refs_ok(mk.get("dimensionamento"), "mercado.dimensionamento")
        for d in mk.get("dimensionamento", []) or []:
            if not d.get("memoria_calculo"): r.b(f"dimensionamento {d.get('segmento')}: sem memória de cálculo")
        co = nos["concorrencia"] or {}
        if len(co.get("concorrentes", []) or []) < 3: r.bp("concorrencia: menos de 3 concorrentes mapeados")
        refs_ok(co.get("concorrentes"), "concorrencia")
        refs_ok((nos["interno"] or {}).get("retrospectiva"), "interno.retrospectiva")
        comp = (nos["interno"] or {}).get("comparacao_metas", []) or []
        for ref in config().get("retrospectiva_referencias_obrigatorias", []):
            linhas = [c for c in comp if (c.get("referencia") or "").lower() == ref.lower()]
            ok = any(c.get("status") == "comparado" and c.get("meta") is not None and c.get("realizado") is not None for c in linhas) or \
                 any(c.get("status") == "indisponivel" and c.get("justificativa") for c in linhas)
            if not ok: r.bp(f"retrospectiva: sem comparação com '{ref}' (ou marque indisponível com justificativa)")
        refs_ok((nos["capacidades"] or {}).get("ativos"), "capacidades.ativos")
        dg = nos["diagnostico"] or {}
        sw = dg.get("swot") or {}
        for q in ["forcas", "fraquezas", "oportunidades", "ameacas"]:
            if not sw.get(q): r.b(f"diagnostico.swot.{q} vazio")
            refs_ok(sw.get(q), f"swot.{q}")
        qc = dg.get("questoes_criticas", []) or []
        if not (3 <= len(qc) <= 5) and r.modo == "plano": r.b("diagnostico: de 3 a 5 questões críticas")

    # E2
    if ate >= 2:
        if "G2" not in gates: r.b("falta aprovação G2 (diagnóstico)")
        op = nos["opcoes"] or {}
        ops = op.get("opcoes", []) or []
        if len(ops) < 2: r.b("opcoes: pelo menos 2 opções estratégicas reais")
        if not op.get("criterios_escolha") or any(c.get("peso") is None for c in op.get("criterios_escolha") or []):
            r.b("opcoes.criterios_escolha sem critérios ou pesos")
        for o in ops:
            mn = (o.get("modelo_negocio") or {})
            if mn.get("central") not in MODELOS: r.bp(f"opção {o.get('id')}: modelo de negócio central ausente ou inválido")
            icp = o.get("icp") or {}
            if not icp.get("setor") or not icp.get("quem_compra"): r.bp(f"opção {o.get('id')}: ICP sem setor ou sem quem compra")
            if not o.get("proposta_valor"): r.bp(f"opção {o.get('id')}: proposta de valor vazia")
            if not [v for v in o.get("vantagens_defensaveis", []) or [] if v.get("vantagem") and v.get("por_que_e_defensavel")]: r.bp(f"opção {o.get('id')}: sem vantagem defensável justificada")
            mr = [m for m in o.get("modelo_receita", []) or [] if m.get("tipo") in RECEITAS]
            if not mr: r.bp(f"opção {o.get('id')}: modelo de receita ausente")
            for k in ["tese", "como_vencer"]:
                if not o.get(k): r.b(f"opção {o.get('id')}: {k} vazio")
            if not (o.get("onde_jogar") or {}).get("segmentos"): r.b(f"opção {o.get('id')}: onde_jogar sem segmentos")
            w = o.get("wmbt", []) or []
            if len(w) < 3: r.b(f"opção {o.get('id')}: menos de 3 condições 'o que precisa ser verdade'")
            for x in w:
                if not x.get("teste") or not x.get("criterio_de_falha"): r.b(f"{x.get('id')}: sem teste ou critério de falha")
        rec = (op.get("recomendacao") or {})
        if rec.get("opcao") not in {o.get("id") for o in ops}: r.b("opcoes.recomendacao aponta para opção inexistente")
        if not rec.get("o_que_nao_fazer"): r.bp("opcoes.recomendacao.o_que_nao_fazer vazio")
        fo = (nos["financeiro_opcoes"] or {}).get("opcoes") or {}
        for o in ops:
            if o.get("id") not in fo: r.b(f"financeiro_opcoes sem modelo para a opção {o.get('id')}")
        for oid, m in fo.items():
            anos_m = [str(a) for a in m.get("anos") or []]
            pa = m.get("pessoal_anual") or {}
            if not anos_m: r.b(f"financeiro_opcoes {oid}: anos vazio")
            if not isinstance(pa, dict) or any(pa.get(a) is None for a in anos_m):
                r.b(f"financeiro_opcoes {oid}: pessoal_anual precisa de valor em todos os anos (no E2 ainda não há organização detalhada)")
            if m.get("caixa_inicial") is None: r.b(f"financeiro_opcoes {oid}: caixa_inicial vazio")
        if r.modo == "plano":
            pt = nos["portfolio"] or {}
            for crit in ["criterios_atratividade", "criterios_capacidade"]:
                if any(c.get("peso") is None for c in pt.get(crit, []) or []): r.b(f"portfolio.{crit} sem pesos")
            for l in pt.get("linhas", []) or []:
                if l.get("decisao") not in ("investir", "manter", "colher", "descontinuar", "separar"): r.b(f"portfolio: linha '{l.get('linha')}' sem decisão válida")

    # E3
    if ate >= 3 and r.modo == "plano":
        if "G3" not in gates: r.b("falta aprovação G3 (escolha estratégica)")
        ok = nos["okrs"] or {}
        objs = ok.get("objetivos", []) or []
        if not (3 <= len(objs) <= 5): r.a(f"okrs: {len(objs)} objetivos (recomendado 3 a 5)")
        for o in objs:
            krs = [k for k in ok.get("krs", []) or [] if k.get("objetivo_id") == o.get("id")]
            if not (2 <= len(krs) <= 5): r.b(f"objetivo {o.get('id')}: {len(krs)} KRs (2 a 5)")
        for k in ok.get("krs", []) or []:
            for c in ["metrica", "dono", "fonte_dado"]:
                if not k.get(c): r.b(f"{k.get('id')}: {c} vazio")
            if not isinstance(k.get("baseline"), (int, float)) or not isinstance(k.get("meta_anual"), (int, float)):
                r.b(f"{k.get('id')}: baseline e meta_anual precisam ser números")
        for o in objs:
            if not o.get("dono"): r.b(f"objetivo {o.get('id')}: sem dono")
        oids = {o.get("id") for o in objs}
        for i in (nos["iniciativas"] or {}).get("itens", []) or []:
            if i.get("objetivo_id") not in oids: r.b(f"iniciativa {i.get('id')}: objetivo inexistente")
            if not i.get("dono"): r.b(f"iniciativa {i.get('id')}: sem dono")
            if i.get("area") not in AREAS_INI: r.b(f"iniciativa {i.get('id')}: área ausente ou inválida")
            if not i.get("marco_de_decisao"): r.a(f"iniciativa {i.get('id')}: sem marco de decisão (continuar/parar)")
        res = carregar_json(dv / "saidas" / "resumo.json")
        if not res: r.b("motor não executado (python -m motor.rodar)")
        else:
            if res.get("_hashes") != {n: hash_obj(nos[n]) for n in NOS}: r.b("saídas do motor desatualizadas: rode o motor de novo")
            org = nos["organizacao"] or {}
            for c, m in ((nos["financeiro"] or {}).get("cenarios") or {}).items():
                if m.get("pessoal_anual") is None and org.get("custo_pessoal_mensal_atual") is None:
                    r.b(f"cenário {c}: sem custo de pessoal (preencha organizacao.custo_pessoal_mensal_atual ou pessoal_anual)")
                if m.get("caixa_inicial") is None: r.b(f"cenário {c}: caixa_inicial vazio")
            base = (res.get("cenarios") or {}).get("base")
            if not base: r.b("financeiro: cenário base não modelado")
            elif base["indicadores"]["meses_caixa_negativo"]:
                r.b(f"cenário base com caixa negativo a partir de {base['indicadores']['meses_caixa_negativo'][0]}: ajuste plano de captação, ritmo ou escopo")
        for x in (nos["riscos"] or {}).get("itens", []) or []:
            if not x.get("gatilho") or not x.get("dono") or not x.get("mitigacao"): r.b(f"risco {x.get('id')}: sem gatilho, dono ou mitigação")
        ritos = (nos["governanca"] or {}).get("ritos", []) or []
        if not ritos: r.b("governanca.ritos vazio")
        if not any(x.get("frequencia") == "semestral" for x in ritos): r.b("governança: falta a revisão semestral do plano")
        for x in ritos:
            if not x.get("dono"): r.a(f"rito '{x.get('nome')}': sem dono")
        pf = {a.get("area"): a for a in (nos["planos_funcionais"] or {}).get("areas", []) or []}
        temas_obr = config().get("temas_obrigatorios_planos", {})
        krs_ids = {k.get("id") for k in (nos["okrs"] or {}).get("krs", []) or []}
        ini = {i.get("id"): i for i in (nos["iniciativas"] or {}).get("itens", []) or []}
        for area in AREAS_PLANO:
            a = pf.get(area)
            if not a: r.b(f"plano funcional '{area}' ausente"); continue
            if not a.get("dono") or not a.get("objetivo_area"): r.b(f"plano '{area}': sem dono ou objetivo da área")
            if not [m for m in a.get("metas", []) or [] if isinstance(m.get("meta"), (int, float)) and m.get("fonte")]: r.b(f"plano '{area}': sem meta numérica com fonte")
            temas = {p.get("tema") for p in a.get("politicas", []) or [] if p.get("decisao")}
            falta = [t for t in temas_obr.get(area, []) if t not in temas]
            if falta: r.b(f"plano '{area}': faltam decisões sobre {falta}")
            for k in a.get("krs", []) or []:
                if k not in krs_ids: r.b(f"plano '{area}': KR {k} inexistente")
            for i in a.get("iniciativas", []) or []:
                if i not in ini: r.b(f"plano '{area}': iniciativa {i} inexistente")
            soltas = [i for i, x in ini.items() if x.get("area") == area and i not in (a.get("iniciativas") or [])]
            if soltas: r.a(f"plano '{area}': iniciativas da área fora do plano {soltas}")
        jt = nos["juridico_tributario"] or {}
        if not (jt.get("regime_tributario") or {}).get("decisao") or not (jt.get("regime_tributario") or {}).get("prazo"): r.b("jurídico e tributário: decisão e prazo do regime tributário")
        if not (jt.get("matriz_filial") or {}).get("decisao"): r.b("jurídico e tributário: decisão sobre matriz e filial")
        for x in jt.get("acoes", []) or []:
            if not x.get("dono") or not x.get("prazo"): r.b(f"jurídico: ação '{(x.get('acao') or '')[:40]}' sem dono ou prazo")
        cen = (nos["financeiro"] or {}).get("cenarios") or {}
        for c in ["conservador", "base", "otimista"]:
            if c not in cen: r.b(f"financeiro: cenário {c} ausente")
        if res and (res.get("cenarios") or {}).get("base"):
            nec = res["cenarios"]["base"]["indicadores"]["necessidade_captacao"]
            instr = ((nos["financeiro"] or {}).get("plano_captacao") or {}).get("instrumentos", []) or []
            if nec > 0 and not [x for x in instr if x.get("valor") and x.get("prazo") and x.get("status")]: r.b("captação: há necessidade de capital e nenhum instrumento com valor, prazo e status")
            base = cen.get("base") or {}; anos = [str(x) for x in base.get("anos") or []]
            if anos:
                desp = sum(float((d.get("valor") or {}).get(anos[0]) or 0) for d in base.get("despesas", []) or [])
                rec = sum(float(x.get("valor_anual") or 0) for a in pf.values() for x in a.get("despesas_recorrentes", []) or [])
                if rec > desp + 1: r.a("as despesas recorrentes dos planos funcionais são maiores que as despesas do cenário base no ano 1")

    # E4
    if ate >= 4:
        if r.modo == "plano" and "G4" not in gates: r.b("falta aprovação G4 (plano detalhado)")
        rs = carregar_json(dv / "saidas" / "render_status.json", {})
        if not rs: r.b("entregáveis não renderizados")
        for arq, faltas in (rs.get("faltando") or {}).items():
            if faltas: r.b(f"{arq}: variáveis sem valor {faltas}")
        for f in list((dv / "entregaveis").glob("*")) + list((dv / "saidas").glob("*.md")):
            txt = f.read_text(encoding="utf-8", errors="ignore")
            for t in config().get("termos_proibidos", []):
                if re.search(rf"\b{re.escape(t)}\b", txt, re.I): r.b(f"{f.name}: termo proibido '{t}'")
            if f.suffix == ".md" and f.parent.name == "saidas" and "[●]" in txt: r.bp(f"{f.name}: contém [●]")
            if f.name.endswith(".tpl") and re.search(r"R\$\s?\d", re.sub(r"\{\{.*?\}\}", "", txt)):
                r.a(f"{f.name}: valor em R$ digitado; use variáveis do motor")
        rev = {}
        for f in sorted(glob.glob(str(dv / "revisoes" / "*.json"))):
            d = carregar_json(f); rev.setdefault(d.get("agente_revisado") or Path(f).stem, []).append(d)
        if r.modo == "plano":
            for e in ESPECIALISTAS:
                u = sorted(rev.get(e, []), key=lambda x: x.get("rodada", 0))
                if not u: r.b(f"sem revisão para {e}")
                elif u[-1].get("veredito") not in ("aprovado", "aprovado_com_ressalvas"): r.b(f"{e}: último veredito '{u[-1].get('veredito')}'")
        if "red-team-estrategia" not in rev: r.b("sem relatório do red team")
        aud = rev.get("auditor-consistencia")
        if not aud: r.b("sem relatório do auditor")
        elif aud[-1].get("veredito") != "aprovado": r.b(f"auditor: veredito '{aud[-1].get('veredito')}'")

    st = status_nos(dv, imprimir=False)
    alvo = [n for f in FASES[:ate + 1] for n in NOS_DA_FASE[f]]
    if r.modo == "estudo":
        alvo = [n for n in alvo if n in NOS_ESTUDO]
    for n in alvo:
        s, det = st[n]
        if s == "vazio": r.b(f"nó {n}: não preenchido")
        elif s in ("desatualizado", "alterado_sem_carimbo", "nao_carimbado"): r.b(f"nó {n}: {s} {det if det else ''}".strip())
    return r


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("dv"); ap.add_argument("--fase", choices=FASES, required=True)
    x = ap.parse_args(); r = validar(x.dv, x.fase)
    print(f"== Validação até {x.fase} ({r.modo}) ==")
    for m in r.bloq: print("BLOQUEIO:", m)
    for m in r.aviso: print("aviso:", m)
    print("RESULTADO:", "BLOQUEADO" if r.bloq else "LIBERADO")
    sys.exit(1 if r.bloq else 0)


if __name__ == "__main__":
    main()
