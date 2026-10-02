"""Gatekeeper da especificação de produto. Sai com código 1 se houver bloqueio.

Uso: python -m motor.validar <dir_versao> --fase P0|P1|P2|P3|P4
"""
import argparse, glob, re, sys
from pathlib import Path
from .util import NOS, carregar_json, carregar_nos, config, hash_obj
from .estado import status as status_nos

FASES = ["P0", "P1", "P2", "P3", "P4"]
NOS_DA_FASE = {"P0": ["meta", "briefing", "enquadramento"], "P1": ["mercado", "clientes", "concorrencia", "normas", "oportunidade"],
               "P2": ["conceitos", "requisitos"], "P3": ["arquitetura", "negocio", "validacao", "roadmap"], "P4": []}
NOS_OPORTUNIDADE = {"meta", "briefing", "enquadramento", "mercado", "clientes", "concorrencia", "normas", "oportunidade", "conceitos", "negocio"}
ESPECIALISTAS = ["enquadramento", "pesquisa-mercado", "pesquisa-cliente", "analise-concorrencial", "regulatorio-normas", "estrategista-produto",
                 "requisitos-produto", "arquiteto-solucao", "pricing-negocio", "validacao-experimentos", "roadmap-gtm", "documentacao-produto"]
TIPOS = {"confirmado", "reportado", "estimativa", "interno"}


class R:
    def __init__(self, modo): self.modo, self.bloq, self.aviso = modo, [], []
    def b(self, m): self.bloq.append(m)
    def a(self, m): self.aviso.append(m)
    def bc(self, m): (self.bloq if self.modo == "completo" else self.aviso).append(m)


def validar(dv, fase):
    dv = Path(dv); nos = carregar_nos(dv); meta = nos["meta"] or {}
    r = R(meta.get("modo", "completo")); ate = FASES.index(fase); comp = r.modo == "completo"
    gates = {a["gate"] for a in carregar_json(dv / "controle.json", {"aprovacoes": []}).get("aprovacoes", [])}

    for k in ["projeto_id", "produto", "segmento", "modo", "data_base"]:
        if not meta.get(k): r.b(f"meta.{k} vazio")
    if not re.fullmatch(r"\d{4}-\d{2}", str(meta.get("mes_inicio", ""))): r.b("meta.mes_inicio deve ser AAAA-MM")
    enq = nos["enquadramento"] or {}
    if enq:
        from .prontidao import avaliar
        pr = avaliar(enq, "completo" if comp else "rapido")
        for m in pr["bloqueios"]: r.b(f"enquadramento: {m}")
        if pr["abertas"]: r.b(f"enquadramento: {len(pr['abertas'])} pergunta(s) aberta(s)")
        if not enq.get("objetivo"): r.b("enquadramento.objetivo vazio")

    ids = set()
    if ate >= 1:
        if "G1" not in gates: r.b("falta aprovação G1 (enquadramento)")
        for n in ["mercado", "clientes", "concorrencia", "normas"]:
            for e in (nos[n] or {}).get("evidencias", []) or []:
                ids.add(e.get("id"))
                if e.get("tipo") not in TIPOS or not e.get("fonte") or not e.get("data"): r.b(f"{n}: evidência {e.get('id')} sem tipo válido, fonte ou data")
        def refs(lista, onde):
            for x in lista or []:
                ev = x.get("evidencias", []) or []
                if not ev: r.b(f"{onde}: item sem evidência ({str(x.get('id') or x.get('nome') or x.get('dor') or x.get('job') or x.get('alternativa'))[:40]})")
                elif [e for e in ev if e not in ids]: r.b(f"{onde}: evidências inexistentes {[e for e in ev if e not in ids]}")
        cl = nos["clientes"] or {}
        if not cl.get("jtbd"): r.b("clientes.jtbd vazio")
        refs(cl.get("jtbd"), "clientes.jtbd"); refs(cl.get("dores"), "clientes.dores"); refs(cl.get("alternativas_atuais"), "clientes.alternativas_atuais")
        if not cl.get("personas"): r.b("clientes.personas vazio")
        if not any(p.get("tipo") in ("decisor", "pagador") for p in cl.get("personas", []) or []): r.a("nenhuma persona decisora ou pagadora")
        mk = nos["mercado"] or {}
        refs(mk.get("segmentos"), "mercado.segmentos")
        for s in mk.get("segmentos", []) or []:
            if not s.get("memoria_calculo"): r.b(f"segmento {s.get('id')}: sem memória de cálculo")
        co = nos["concorrencia"] or {}
        if len(co.get("produtos", []) or []) < 3: r.bc("concorrencia: menos de 3 produtos ou alternativas comparados")
        refs(co.get("produtos"), "concorrencia.produtos")
        esp = co.get("especificacoes", []) or []
        if len(esp) < 5: r.bc(f"benchmark: {len(esp)} especificações comparáveis (mínimo 5)")
        eids = {e.get("id") for e in esp}
        for e in esp:
            if not e.get("nome") or e.get("melhor") not in ("maior", "menor", "qualitativo"): r.b(f"especificação {e.get('id')}: sem nome ou com 'melhor' inválido")
            if e.get("melhor") in ("maior", "menor") and not e.get("unidade"): r.b(f"especificação {e.get('id')}: numérica sem unidade")
        celulas = preench = 0
        for pr in co.get("produtos", []) or []:
            if pr.get("tipo") == "produto" and not pr.get("ficha_tecnica_url"): r.a(f"produto {pr.get('nome')}: sem link da ficha técnica")
            for k, c in (pr.get("specs") or {}).items():
                if k not in eids: r.b(f"produto {pr.get('nome')}: especificação {k} inexistente")
                if c.get("valor") not in (None, ""):
                    preench += 1
                    if c.get("fonte") not in ids: r.b(f"produto {pr.get('nome')}, {k}: valor sem evidência válida em 'fonte'")
            celulas += len(esp)
        if celulas and preench / celulas < 0.5: r.a(f"benchmark com só {preench / celulas:.0%} das especificações preenchidas")
        refs((nos["normas"] or {}).get("itens"), "normas.itens")
        op = nos["oportunidade"] or {}
        if not op.get("problema"): r.b("oportunidade.problema vazio")
        pv = op.get("proposta_de_valor") or {}
        for k in ["para_quem", "que_problema", "nossa_solucao", "diferente_de"]:
            if not pv.get(k): r.b(f"oportunidade.proposta_de_valor.{k} vazio")
        if any(c.get("peso") is None for c in op.get("criterios", []) or []): r.b("oportunidade.criterios sem pesos")
        faltam = [c["criterio"] for c in op.get("criterios", []) or [] if c["criterio"] not in (op.get("notas") or {})]
        if faltam: r.b(f"oportunidade: critérios sem nota {faltam}")
        jt = {j.get("id") for j in cl.get("jtbd", []) or []}
        if [j for j in op.get("jtbd_alvo", []) or [] if j not in jt]: r.b("oportunidade.jtbd_alvo aponta para JTBD inexistente")
        if op.get("decisao") not in ("seguir", "pivotar", "parar"): r.b("oportunidade.decisao inválida")

    if ate >= 2:
        if comp and "G2" not in gates: r.b("falta aprovação G2 (oportunidade)")
        cc = nos["conceitos"] or {}
        cs = cc.get("conceitos", []) or []
        if len(cs) < (3 if comp else 2): r.b(f"conceitos: mínimo de {3 if comp else 2} conceitos, incluindo integrar, revender ou parceria quando fizer sentido")
        if any(c.get("peso") is None for c in cc.get("criterios_selecao", []) or []): r.b("conceitos.criterios_selecao sem pesos")
        for c in cs:
            if c.get("abordagem") not in ("construir", "integrar", "revender", "parceria"): r.b(f"conceito {c.get('id')}: abordagem inválida")
            if [k["criterio"] for k in cc.get("criterios_selecao", []) or [] if k["criterio"] not in (c.get("notas") or {})]: r.b(f"conceito {c.get('id')}: critérios sem nota")
        if cc.get("escolhido") not in {c.get("id") for c in cs} or not cc.get("justificativa"): r.b("conceitos: escolhido inexistente ou sem justificativa")
        if comp:
            origens = {x.get("id") for k in ["jtbd", "dores", "ganhos"] for x in (nos["clientes"] or {}).get(k, []) or []} | {n.get("id") for n in (nos["normas"] or {}).get("itens", []) or []} | ids
            for q in (nos["requisitos"] or {}).get("itens", []) or []:
                if q.get("prioridade") not in ("must", "should", "could", "wont"): r.b(f"{q.get('id')}: prioridade inválida")
                if not q.get("origem") or [o for o in q["origem"] if o not in origens]: r.b(f"{q.get('id')}: origem vazia ou inexistente")
                if q.get("prioridade") == "must" and not q.get("criterio_aceite"): r.b(f"{q.get('id')}: must sem critério de aceite")
            eids = {e.get("id") for e in (nos["concorrencia"] or {}).get("especificacoes", []) or []}
            ligados = 0
            for q in (nos["requisitos"] or {}).get("itens", []) or []:
                ref = q.get("especificacao_ref")
                if ref:
                    ligados += 1
                    if ref not in eids: r.b(f"{q.get('id')}: especificacao_ref {ref} inexistente no benchmark")
            if eids and not ligados: r.b("nenhum requisito ligado ao benchmark (especificacao_ref): os alvos precisam ser comparados com o mercado")
            res = carregar_json(dv / "saidas" / "resumo.json") or {}
            cob = res.get("requisitos") or {}
            if cob.get("jtbd_sem_must"): r.b(f"JTBD-alvo sem requisito must: {cob['jtbd_sem_must']}")
            if cob.get("normas_sem_requisito"): r.b(f"normas aplicáveis sem requisito: {cob['normas_sem_requisito']}")

    if ate >= 3:
        if comp and "G3" not in gates: r.b("falta aprovação G3 (conceito e escopo)")
        ng = nos["negocio"] or {}
        if not ng: r.b("negocio vazio")
        mix = ng.get("mix") or {}
        if abs(float(mix.get("venda") or 0) + float(mix.get("locacao") or 0) - 1) > 1e-6: r.b("negocio.mix: venda + locacao deve somar 1")
        for k in ["impostos_receita_pct", "comissao_pct", "taxa_desconto_aa", "unidades_por_cliente"]:
            if ng.get(k) is None: r.b(f"negocio.{k} vazio")
        for a in ["ano1", "ano2", "ano3"]:
            if ((ng.get("volume_unidades_novas") or {}).get(a) or {}).get("provavel") is None: r.b(f"negocio.volume_unidades_novas.{a} sem 3 pontos")
        if not ng.get("wtp") or not any(w.get("evidencias") for w in ng.get("wtp") or []): r.bc("negocio.wtp sem evidência de disposição a pagar")
        if comp:
            for c in (nos["arquitetura"] or {}).get("componentes", []) or []:
                if c.get("decisao") not in ("fazer", "comprar", "parceria"): r.b(f"componente {c.get('id')}: decisão inválida")
                if len(c.get("alternativas", []) or []) < 2: r.b(f"componente {c.get('id')}: menos de 2 alternativas avaliadas (neutralidade)")
                if c.get("por_unidade", True) and (not c.get("custo_unitario") or c["custo_unitario"].get("provavel") is None or not c.get("fonte_custo")): r.b(f"componente {c.get('id')}: custo sem 3 pontos ou sem fonte")
            for h in (nos["validacao"] or {}).get("hipoteses", []) or []:
                risco = float(h.get("impacto") or 0) * float(h.get("incerteza") or 0)
                ex = h.get("experimento") or {}
                if risco >= 15 and (not ex.get("criterio_sucesso") or not ex.get("criterio_falha")): r.b(f"hipótese {h.get('id')} de alto risco sem experimento com critérios")
            if len((nos["validacao"] or {}).get("hipoteses", []) or []) < 5: r.a("menos de 5 hipóteses registradas")
            rm = nos["roadmap"] or {}
            musts = {q["id"] for q in (nos["requisitos"] or {}).get("itens", []) or [] if q.get("prioridade") == "must"}
            no_mvp = {q for rel in rm.get("releases", []) or [] if rel.get("id") == "MVP" for q in rel.get("requisitos", []) or []}
            if musts - no_mvp: r.b(f"requisitos must fora do MVP: {sorted(musts - no_mvp)}")
            for rel in rm.get("releases", []) or []:
                if not rel.get("marco_de_decisao"): r.b(f"release {rel.get('id')}: sem marco de decisão")
            if not (rm.get("gtm") or {}).get("pilotos"): r.b("roadmap.gtm.pilotos vazio")
        res = carregar_json(dv / "saidas" / "resumo.json")
        if not res: r.b("motor não executado (python -m motor.rodar)")
        elif res.get("_hashes") != {n: hash_obj(nos[n]) for n in NOS}: r.b("saídas do motor desatualizadas: rode o motor de novo")

    if ate >= 4:
        final = "G4" if comp else None
        if final and final not in gates: r.b("falta aprovação G4 (especificação)")
        rs = carregar_json(dv / "saidas" / "render_status.json", {})
        if not rs: r.b("entregáveis não renderizados")
        for arq, f in (rs.get("faltando") or {}).items():
            if f: r.b(f"{arq}: variáveis sem valor {f}")
        for f in list((dv / "entregaveis").glob("*")) + list((dv / "saidas").glob("*.md")):
            txt = f.read_text(encoding="utf-8", errors="ignore")
            for t in config().get("termos_proibidos", []):
                if re.search(rf"\b{re.escape(t)}\b", txt, re.I): r.b(f"{f.name}: termo proibido '{t}'")
            if f.suffix == ".md" and f.parent.name == "saidas" and "[●]" in txt: r.bc(f"{f.name}: contém [●]")
        rev = {}
        for f in sorted(glob.glob(str(dv / "revisoes" / "*.json"))):
            d = carregar_json(f); rev.setdefault(d.get("agente_revisado") or Path(f).stem, []).append(d)
        if comp:
            for e in ESPECIALISTAS:
                u = sorted(rev.get(e, []), key=lambda x: x.get("rodada", 0))
                if not u: r.b(f"sem revisão para {e}")
                elif u[-1].get("veredito") not in ("aprovado", "aprovado_com_ressalvas"): r.b(f"{e}: último veredito '{u[-1].get('veredito')}'")
        if "red-team-produto" not in rev: r.b("sem relatório do red team")
        aud = rev.get("auditor-consistencia")
        if not aud: r.b("sem relatório do auditor")
        elif aud[-1].get("veredito") != "aprovado": r.b(f"auditor: veredito '{aud[-1].get('veredito')}'")

    st = status_nos(dv, imprimir=False)
    alvo = [n for f in FASES[:ate + 1] for n in NOS_DA_FASE[f]]
    if not comp:
        alvo = [n for n in alvo if n in NOS_OPORTUNIDADE]
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
