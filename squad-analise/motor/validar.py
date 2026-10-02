"""Gatekeeper da análise. Sai com código 1 se houver bloqueio.

Uso: python -m motor.validar <dv> --fase D0|D1|D2|D3|D4
"""
import argparse, glob, re, sys
from pathlib import Path
from .util import NOS, carregar_json, carregar_nos, config
from .estado import status as status_nos

FASES = ["D0", "D1", "D2", "D3", "D4"]
NOS_DA_FASE = {"D0": ["meta", "briefing", "decisao"], "D1": ["contrato", "especialista", "qualidade"], "D2": ["plano"], "D3": [], "D4": ["impacto"]}
OBRIGATORIO = {"comparacao": "estatistico", "previsao": "cientista-de-dados", "causa": "estatistico", "investimento": "analista-de-impacto"}
SUPERVISORES = {"rapido": [], "padrao": ["sup-dados", "sup-metodologia"], "completo": ["sup-dados", "sup-metodologia", "sup-negocio", "sup-comunicacao"]}
TIPOS_INC = {"nenhuma", "intervalo_confianca", "intervalo_previsao", "bootstrap", "faixa_cenarios"}


class R:
    def __init__(s, modo): s.modo, s.bloq, s.aviso = modo, [], []
    def b(s, m): s.bloq.append(m)
    def a(s, m): s.aviso.append(m)


def validar(dv, fase):
    dv = Path(dv); nos = carregar_nos(dv); meta = nos["meta"] or {}; r = R(meta.get("modo", "padrao")); ate = FASES.index(fase)
    rapido = r.modo == "rapido"
    gates = {a["gate"] for a in (carregar_json(dv / "controle.json", {"aprovacoes": []}) or {}).get("aprovacoes", [])}
    for k in ["projeto_id", "tema", "objetivo", "modo"]:
        if not meta.get(k): r.b(f"meta.{k} vazio")
    dec = nos["decisao"] or {}
    if dec:
        from .prontidao import avaliar
        pr = avaliar(dec, "rapido" if rapido else "completo")
        for m in pr["bloqueios"]: r.b(f"decisão: {m}")
        if pr["abertas"]: r.b(f"decisão: {len(pr['abertas'])} pergunta(s)-chave aberta(s)")
        if dec.get("tipo") == "decisao":
            if not dec.get("decisao"): r.b("decisao.decisao vazio")
            if len([x for x in dec.get("alternativas", []) if x]) < 2: r.b("decisão: pelo menos 2 alternativas")
            for c in dec.get("criterios", []):
                if not c.get("metrica") or not c.get("limite"): r.b(f"critério {c.get('id')}: sem métrica ou limite")
        elif dec.get("tipo") != "exploratoria":
            r.b("decisao.tipo deve ser 'decisao' ou 'exploratoria'")
        if not dec.get("perguntas"): r.b("decisão: nenhuma pergunta de negócio")
        ids_c = {c["id"] for c in dec.get("criterios", [])}
        for p in dec.get("perguntas", []):
            if dec.get("tipo") == "decisao" and p.get("criterio_ref") not in ids_c: r.b(f"pergunta {p.get('id')}: não liga a um critério")

    if ate >= 1:
        if "G1" not in gates: r.b("falta aprovação G1 (decisão e perguntas)")
        cat = carregar_json(dv / "saidas" / "catalogo.json"); per = carregar_json(dv / "saidas" / "perfil.json")
        if not cat: r.b("nenhum dado importado (python -m motor.ingestao importar)")
        if not per: r.b("perfil não gerado (python -m motor.perfil)")
        ct = nos["contrato"] or {}
        tabs = {t.get("nome"): t for t in ct.get("tabelas", [])}
        for t in (cat or {}).get("tabelas", []):
            c = tabs.get(t["tabela"]) or tabs.get("base_" + t["tabela"][4:])
            if not c: r.b(f"contrato: tabela {t['tabela']} sem contrato"); continue
            for k in ["origem", "granularidade", "data_extracao"]:
                if not c.get(k): r.b(f"contrato {t['tabela']}: {k} vazio")
            sem = [x["nome"] for x in c.get("colunas", []) if not x.get("significado")]
            if c.get("colunas") and len(sem) / len(c["colunas"]) > 0.2: r.a(f"contrato {t['tabela']}: {len(sem)} colunas sem significado")
        for m in ct.get("metricas", []):
            if not m.get("definicao") or not m.get("formula"): r.b(f"métrica {m.get('id')}: sem definição ou fórmula")
        q = nos["qualidade"] or {}
        if per:
            pessoais = {(t, c["coluna"]) for t, d in per["tabelas"].items() for c in d["colunas"] if c.get("pessoal")}
            tratadas = {(x["tabela"], x["coluna"]) for x in q.get("pseudonimizar", []) + q.get("excluir_colunas", [])} | {(x.get("tabela"), x.get("coluna")) for x in q.get("nao_pessoal", [])}
            for t, c in sorted(pessoais - tratadas): r.b(f"privacidade: {t}.{c} parece dado pessoal e não foi pseudonimizada, excluída nem justificada em nao_pessoal")
        if not q.get("conclusao"): r.b("qualidade.conclusao vazio")
        if not rapido:
            e = nos["especialista"] or {}
            for k in ["setor", "papel"]:
                if not e.get(k): r.b(f"especialista.{k} vazio")
            for c in e.get("conhecimentos", []) + e.get("indicadores", []) + e.get("faixas_plausiveis", []):
                if not c.get("fonte") or c.get("confianca") not in ("alta", "media", "baixa"): r.b("especialista: conhecimento sem fonte ou confiança"); break
            if not e.get("faixas_plausiveis"): r.b("especialista: nenhuma faixa plausível para orientar a limpeza")

    if ate >= 2 and not rapido:
        if "G2" not in gates and ate >= 3: r.b("falta aprovação G2 (especialista e plano)")
        pl = nos["plano"] or {}; pergs = {p["id"] for p in dec.get("perguntas", [])}
        mets = {m["id"] for m in (nos["contrato"] or {}).get("metricas", [])}
        conf = 0
        for a in pl.get("analises", []):
            i = a.get("id")
            if a.get("pergunta_ref") not in pergs: r.b(f"{i}: pergunta inexistente")
            if a.get("tipo") not in ("confirmatoria", "exploratoria"): r.b(f"{i}: tipo deve ser confirmatoria ou exploratoria")
            if a.get("nivel") not in ("descritivo", "associativo", "causal"): r.b(f"{i}: nível inválido")
            if a.get("incerteza") not in TIPOS_INC: r.b(f"{i}: tipo de incerteza inválido")
            if a.get("nivel") == "causal" and not a.get("desenho_causal"): r.b(f"{i}: causal sem desenho causal")
            if a.get("tipo") == "confirmatoria" and not a.get("hipotese"): r.b(f"{i}: confirmatória sem hipótese registrada")
            for m in a.get("metricas", []):
                if m not in mets: r.b(f"{i}: métrica {m} não definida no contrato")
            req = OBRIGATORIO.get(a.get("tipo_pergunta"))
            if req and req not in pl.get("equipe", []): r.b(f"{i}: pergunta do tipo {a.get('tipo_pergunta')} exige {req} na equipe")
            conf += a.get("tipo") == "confirmatoria"
        if conf > 1 and pl.get("correcao_multiplos_testes") in (None, "", "nenhuma"): r.a("vários testes confirmatórios sem correção para múltiplos testes")

    if ate >= 3:
        from .pipeline import atualizado
        if not atualizado(dv): r.b("preparação desatualizada ou não executada (python -m motor.rodar)")
        reg = carregar_json(dv / "saidas" / "registro.json", {}) or {}
        import hashlib
        for a in (nos["plano"] or {}).get("analises", []):
            e = reg.get(a["id"]); p = dv / a.get("script", "")
            if not p.exists(): r.b(f"{a['id']}: script {a.get('script')} não existe")
            elif not e: r.b(f"{a['id']}: não executada")
            elif p.exists() and hashlib.sha256(p.read_bytes()).hexdigest() != e["script_sha256"]: r.b(f"{a['id']}: script mudou depois da execução")
        from .insights import todos, requisitos
        lista = todos(dv)
        if not lista: r.b("nenhum insight registrado em evidencias/")
        for i in lista:
            for f in requisitos(dv, i, i.get("estado", "descoberto")): r.b(f"{i['id']} ({i.get('estado')}): {f}")
        if not rapido and not (dv / "revisoes" / "red-team-analitico.json").exists(): r.b("sem relatório do red team analítico")

    if ate >= 4:
        aud = carregar_json(dv / "saidas" / "auditoria.json", {}) or {}
        if aud.get("status") != "ok": r.b(f"auditoria de reprodutibilidade: {aud.get('status', 'não executada')}")
        else:
            from .reprodutibilidade import assinatura_registro
            if aud.get("registro_auditado") != assinatura_registro(dv): r.b("resultados mudaram depois da auditoria: rode python -m motor.reprodutibilidade de novo")
        rs = carregar_json(dv / "saidas" / "render_status.json", {}) or {}
        for arq, f in (rs.get("faltando") or {}).items():
            if f: r.b(f"{arq}: variáveis sem valor {f}")
        for f in list((dv / "entregaveis").glob("*.tpl")):
            txt = re.sub(r"\{\{.*?\}\}", "", f.read_text(encoding="utf-8")); txt = re.sub(r"<!--.*?-->", "", txt, flags=re.S)
            if re.search(r"(R\$\s*\d|\d+[.,]\d+|\d+\s*%)", txt): r.b(f"{f.name}: número digitado; use variáveis do motor")
            for t in config().get("termos_proibidos", []):
                if re.search(rf"\b{re.escape(t)}\b", txt, re.I): r.b(f"{f.name}: termo proibido '{t}'")
        if not rapido:
            rev = {Path(p).stem.split("_r")[0] for p in glob.glob(str(dv / "revisoes" / "*.json"))}
            for s in SUPERVISORES[r.modo]:
                if s not in rev: r.b(f"sem revisão de {s}")
            if r.modo == "completo" and "red-team-decisao" not in rev: r.b("sem relatório do red team da decisão")
    st = status_nos(dv, imprimir=False)
    alvo = [n for f in FASES[:ate + 1] for n in NOS_DA_FASE[f]]
    if rapido: alvo = [n for n in alvo if n not in ("especialista", "plano")]
    for n in alvo:
        s, det = st[n]
        if s == "vazio": r.b(f"nó {n}: não preenchido")
        elif s in ("desatualizado", "alterado_sem_carimbo", "nao_carimbado"): r.b(f"nó {n}: {s} {det or ''}".strip())
    return r


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("dv"); ap.add_argument("--fase", choices=FASES, required=True)
    x = ap.parse_args(); r = validar(x.dv, x.fase)
    print(f"== Validação até {x.fase} ({r.modo}) ==")
    for m in r.bloq: print("BLOQUEIO:", m)
    for m in r.aviso: print("aviso:", m)
    print("RESULTADO:", "BLOQUEADO" if r.bloq else "LIBERADO"); sys.exit(1 if r.bloq else 0)


if __name__ == "__main__":
    main()
