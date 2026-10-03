"""Livro de evidências: cada insight é um registro em evidencias/INS-xxx.json que passa por cinco estados.

descoberto → quantificado → validado → acionavel → aprovado   (só "aprovado" entra no memorando e no relatório)

Uso:
  python -m motor.insights checar <dv>                         confere todos e gera saidas/insights.json
  python -m motor.insights avancar <dv> <INS-xxx> <estado> --por <agente>
  python -m motor.insights aprovar <dv> --por Marcus [--ids INS-001 INS-002]   (exige G3 registrado)
Números na afirmação só por marcadores {{v.apelido}}, resolvidos a partir das análises.
"""
import argparse, json, re, sys
from pathlib import Path
from .util import carregar_json, salvar_json, agora
from .registro import valor

ESTADOS = ["descoberto", "quantificado", "validado", "acionavel", "aprovado"]
NIVEIS = {"descritivo", "associativo", "causal"}
NUM_DIGITADO = re.compile(r"(R\$\s*\d|\d+(?:[.,]\d+)?\s*(%|p\.p\.|mil\b|mi\b|bi\b|h\b|horas|dias|min\b|kg\b|km\b)|\d+[.,]\d+)")
PESO = {"alta": 1.0, "media": 0.6, "baixa": 0.3}


def _fmt(v):
    if v is None: return "[●]"
    x, u = v["valor"], (v.get("unidade") or "")
    if u == "%": s = f"{x * 100:.1f}%".replace(".", ",")
    elif u == "p.p.": s = f"{x * 100:.1f}".replace(".", ",") + " p.p."
    elif u in ("R$", "BRL"): s = "R$ " + f"{x:,.0f}".replace(",", ".")
    else: s = (f"{x:,.0f}" if abs(x) >= 100 else f"{x:,.2f}").replace(",", "X").replace(".", ",").replace("X", ".") + (f" {u}" if u else "")
    inc = v.get("incerteza")
    if inc and inc.get("inferior") is not None and u not in ("R$", "BRL"):
        f = (lambda y: f"{y * 100:.1f}".replace(".", ",")) if u in ("%", "p.p.") else (lambda y: f"{y:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        suf = "%" if u == "%" else (" p.p." if u == "p.p." else "")
        rot = {"intervalo_previsao": "previsão entre", "faixa_cenarios": "faixa de cenários de", "bootstrap": "IC bootstrap"}.get(inc["tipo"], "IC")
        sep = " e " if inc["tipo"] == "intervalo_previsao" else " a "
        s += f" ({rot} {f(inc['inferior'])}{suf}{sep}{f(inc['superior'])}{suf})"
    return s


def requisitos(dv, ins, estado_alvo):
    """Lista o que falta para o insight estar no estado pedido (cumulativo)."""
    dv = Path(dv); falta = []; alvo = ESTADOS.index(estado_alvo)
    dec = carregar_json(dv / "nos" / "decisao.json", {}) or {}
    plano = {a["id"]: a for a in (carregar_json(dv / "nos" / "plano.json", {}) or {}).get("analises", [])}
    pergs = {p["id"] for p in dec.get("perguntas", []) or []} | {c["id"] for c in dec.get("criterios", []) or []}
    if not ins.get("afirmacao"): falta.append("afirmação vazia")
    if not (ins.get("pergunta_ref") in pergs or ins.get("criterio_ref") in pergs): falta.append("não liga a uma pergunta ou critério da decisão")
    if alvo >= 1:
        refs = ins.get("valores") or {}
        if not refs: falta.append("sem valores ligados a análises")
        for ap, ref in refs.items():
            aid = ref.split(".")[0]
            if aid not in plano: falta.append(f"{ref}: análise fora do plano")
            elif valor(dv, ref) is None: falta.append(f"{ref}: resultado não encontrado")
            else:
                a = plano[aid]; v = valor(dv, ref)
                if a.get("incerteza") not in (None, "nenhuma") and not v.get("contagem") and not v.get("incerteza"): falta.append(f"{ref}: sem incerteza")
                if ins.get("nivel") == "causal" and (a.get("nivel") != "causal" or not a.get("desenho_causal")): falta.append(f"{ref}: afirmação causal sem desenho causal no plano")
        if ins.get("nivel") not in NIVEIS: falta.append("nível (descritivo, associativo, causal) ausente")
        resto = re.sub(r"\{\{.*?\}\}", "", ins.get("afirmacao", ""))
        if NUM_DIGITADO.search(resto): falta.append("número digitado na afirmação; use {{v.apelido}}")
        for ap in re.findall(r"\{\{v\.([\w-]+)\}\}", ins.get("afirmacao", "")):
            if ap not in refs: falta.append(f"marcador v.{ap} sem valor ligado")
    if alvo >= 2:
        rob = ins.get("robustez") or []
        if len(rob) < 2: falta.append("robustez: menos de 2 recortes")
        if any(r.get("resultado") == "falha" and not r.get("nota") for r in rob): falta.append("robustez: recorte que falha sem explicação")
        if (ins.get("red_team_analitico") or {}).get("veredito") not in ("sobrevive", "ressalva"): falta.append("sem aprovação do red team analítico")
        exploratorio = any(plano.get(r.split(".")[0], {}).get("tipo") == "exploratoria" for r in (ins.get("valores") or {}).values())
        if exploratorio:
            c = ins.get("confirmacao") or {}
            origem = {r.split(".")[0] for r in (ins.get("valores") or {}).values()}
            if c.get("resultado") != "confirma" or not c.get("analise") or c.get("analise") in origem: falta.append("exploratório sem confirmação em outra análise")
    if alvo >= 3:
        imp = carregar_json(dv / "saidas" / "impacto.json", {}) or {}
        if (ins.get("impacto") or {}).get("modelo") not in (imp.get("modelos") or {}): falta.append("modelo de impacto não calculado")
        for k in ["acao", "dono"]:
            if not ins.get(k): falta.append(f"{k} vazio")
        if not ins.get("premissas"): falta.append("premissas vazias")
        if ins.get("confianca") not in PESO: falta.append("confiança (alta, media, baixa) ausente")
    if alvo >= 4:
        if (ins.get("red_team_decisao") or {}).get("veredito") not in ("sobrevive", "ressalva"): falta.append("sem aprovação do red team da decisão")
        if (carregar_json(dv / "saidas" / "auditoria.json", {}) or {}).get("status") != "ok": falta.append("auditoria de reprodutibilidade não aprovada")
        gates = {a["gate"] for a in (carregar_json(dv / "controle.json", {}) or {}).get("aprovacoes", [])}
        if "G3" not in gates: falta.append("portão G3 não aprovado")
    return falta


def todos(dv):
    return [carregar_json(p) for p in sorted((Path(dv) / "evidencias").glob("INS-*.json"))]


def checar(dv):
    dv = Path(dv); imp = (carregar_json(dv / "saidas" / "impacto.json", {}) or {}).get("modelos", {}); lista, problemas = [], []
    for ins in todos(dv):
        falta = requisitos(dv, ins, ins.get("estado", "descoberto"))
        problemas += [f"{ins['id']} ({ins.get('estado')}): {f}" for f in falta]
        vals = {ap: valor(dv, ref) for ap, ref in (ins.get("valores") or {}).items()}
        txt = re.sub(r"\{\{v\.([\w-]+)\}\}", lambda m: _fmt(vals.get(m.group(1))), ins.get("afirmacao", ""))
        m = imp.get((ins.get("impacto") or {}).get("modelo"))
        lista.append({"id": ins["id"], "estado": ins.get("estado"), "texto": txt, "nivel": ins.get("nivel"), "confianca": ins.get("confianca"),
                      "impacto": m, "acao": ins.get("acao"), "dono": ins.get("dono"), "ok": not falta,
                      "prioridade": (abs(m["p50"]) * PESO.get(ins.get("confianca"), 0.3)) if m else 0.0})
    lista.sort(key=lambda x: (-ESTADOS.index(x["estado"] or "descoberto"), -x["prioridade"]))
    salvar_json(dv / "saidas" / "insights.json", {"em": agora(), "insights": lista})
    return lista, problemas


def avancar(dv, iid, estado, por):
    p = Path(dv) / "evidencias" / f"{iid}.json"; ins = carregar_json(p)
    if not ins: sys.exit(f"{iid} não encontrado")
    if estado == "aprovado": sys.exit("Aprovação só pelo comando aprovar, depois do G3.")
    falta = requisitos(dv, ins, estado)
    if falta: sys.exit(f"{iid} não pode ir para {estado}:\n- " + "\n- ".join(falta))
    ins["estado"] = estado; ins.setdefault("historico", []).append({"estado": estado, "em": agora(), "por": por})
    salvar_json(p, ins); print(f"{iid} → {estado}")


def aprovar(dv, por, ids=None):
    for ins in todos(dv):
        if ids and ins["id"] not in ids or ins.get("estado") != "acionavel": continue
        falta = requisitos(dv, ins, "aprovado")
        if falta: print(f"{ins['id']}: não aprovado — " + "; ".join(falta)); continue
        ins["estado"] = "aprovado"; ins.setdefault("historico", []).append({"estado": "aprovado", "em": agora(), "por": por})
        salvar_json(Path(dv) / "evidencias" / f"{ins['id']}.json", ins); print(f"{ins['id']} → aprovado")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("checar"); a.add_argument("dv")
    a = sp.add_parser("avancar"); a.add_argument("dv"); a.add_argument("id"); a.add_argument("estado", choices=ESTADOS); a.add_argument("--por", required=True)
    a = sp.add_parser("aprovar"); a.add_argument("dv"); a.add_argument("--por", required=True); a.add_argument("--ids", nargs="*")
    x = ap.parse_args()
    if x.cmd == "checar":
        l, p = checar(x.dv)
        for i in l: print(f"{i['id']} [{i['estado']}] {i['texto'][:110]}")
        for e in p: print("PENDÊNCIA:", e)
    elif x.cmd == "avancar": avancar(x.dv, x.id, x.estado, x.por)
    else: aprovar(x.dv, x.por, x.ids)
