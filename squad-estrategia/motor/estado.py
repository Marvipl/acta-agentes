"""Gestão do estado do orçamento: criar projeto, carimbar nós, status, versões e aprovações.

Uso:
  python -m motor.estado init <ciclo> <titulo> --modo plano|estudo [--mes-inicio AAAA-MM]
  python -m motor.estado status <dir_versao>
  python -m motor.estado carimbar <dir_versao> <no> --agente <nome>
  python -m motor.estado aprovar <dir_versao> --gate G1|G2|G3 --por <nome> [--obs texto]
  python -m motor.estado montar <dir_versao>
  python -m motor.estado nova-versao <dir_versao> --motivo <texto>
  python -m motor.estado congelar <dir_versao>
"""
import argparse, re, shutil, sys
from pathlib import Path
from .util import (RAIZ, NOS, DEPENDENCIAS, DONOS, carregar_json, salvar_json, hash_obj, agora, hoje)

TEMPLATES = RAIZ / "estado" / "templates"


def _slug(s):
    s = s.lower().strip()
    s = re.sub(r"[áàãâä]", "a", s); s = re.sub(r"[éèêë]", "e", s); s = re.sub(r"[íìîï]", "i", s)
    s = re.sub(r"[óòõôö]", "o", s); s = re.sub(r"[úùûü]", "u", s); s = s.replace("ç", "c")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def _controle(dv):
    return carregar_json(Path(dv) / "controle.json", {"nos": {}, "aprovacoes": [], "congelado": False, "historico": []})


def _salvar_controle(dv, c):
    salvar_json(Path(dv) / "controle.json", c)


def hash_no(dv, no):
    return hash_obj(carregar_json(Path(dv) / "nos" / f"{no}.json"))


def init(cliente, projeto, modo, mes_inicio=None):
    pid = f"{hoje()}_{_slug(cliente)}_{_slug(projeto)}"
    dv = RAIZ / "projetos" / pid / "v1"
    if dv.exists():
        sys.exit(f"Já existe: {dv}")
    for sub in ["nos", "revisoes", "saidas", "entregaveis"]:
        (dv / sub).mkdir(parents=True, exist_ok=True)
    for no in NOS:
        tpl = carregar_json(TEMPLATES / f"{no}.json", {"_template": True})
        salvar_json(dv / "nos" / f"{no}.json", tpl)
    meta = carregar_json(dv / "nos" / "meta.json")
    meta.update({"projeto_id": pid, "ciclo": cliente, "titulo": projeto, "versao": 1, "modo": modo, "data_base": hoje()})
    if mes_inicio:
        meta["mes_inicio"] = mes_inicio
    meta.pop("_template", None)
    salvar_json(dv / "nos" / "meta.json", meta)
    for tpl in (RAIZ / "templates").glob("*.md.tpl"):
        if (modo == "estudo") == (tpl.name == "memo_estudo.md.tpl"):
            shutil.copy(tpl, dv / "entregaveis" / tpl.name)
    c = _controle(dv)
    c["historico"].append({"em": agora(), "evento": "criado", "modo": modo})
    _salvar_controle(dv, c)
    print(dv)
    return dv


def status(dv, imprimir=True):
    c = _controle(dv)
    atual = {no: hash_no(dv, no) for no in NOS}
    res = {}
    for no in NOS:
        conteudo = carregar_json(Path(dv) / "nos" / f"{no}.json", {})
        stamp = c["nos"].get(no)
        if not conteudo or conteudo.get("_template"):
            res[no] = ("vazio", [])
        elif not stamp:
            res[no] = ("nao_carimbado", [])
        elif stamp["hash"] != atual[no]:
            res[no] = ("alterado_sem_carimbo", [])
        else:
            mudou = [d for d in DEPENDENCIAS[no] if stamp.get("entradas", {}).get(d) != atual[d]]
            res[no] = ("desatualizado", mudou) if mudou else ("ok", [])
    # propagação transitiva
    for _ in NOS:
        for no in NOS:
            if res[no][0] == "ok":
                ruins = [d for d in DEPENDENCIAS[no] if res[d][0] in ("desatualizado", "alterado_sem_carimbo")]
                if ruins:
                    res[no] = ("desatualizado", [f"{d} (transitivo)" for d in ruins])
    if imprimir:
        print(f"{'nó':18} {'status':22} {'dono':22} detalhe")
        for no in NOS:
            st, det = res[no]
            print(f"{no:18} {st:22} {DONOS[no]:22} {', '.join(det)}")
        print(f"aprovações: {[a['gate'] for a in c['aprovacoes']]} | congelado: {c['congelado']}")
    return res


def carimbar(dv, no, agente):
    if no not in NOS:
        sys.exit(f"Nó desconhecido: {no}")
    c = _controle(dv)
    if c.get("congelado"):
        sys.exit("Versão congelada. Crie nova versão para alterar.")
    c["nos"][no] = {"hash": hash_no(dv, no), "agente": agente, "em": agora(),
                    "entradas": {d: hash_no(dv, d) for d in DEPENDENCIAS[no]}}
    c["historico"].append({"em": agora(), "evento": "carimbo", "no": no, "agente": agente})
    _salvar_controle(dv, c)
    print(f"carimbado: {no} por {agente}")


def aprovar(dv, gate, por, obs=""):
    c = _controle(dv)
    c["aprovacoes"].append({"gate": gate, "por": por, "em": agora(), "obs": obs,
                            "hashes": {no: hash_no(dv, no) for no in NOS}})
    _salvar_controle(dv, c)
    print(f"aprovação {gate} registrada por {por}")


def montar(dv):
    estado = {no: carregar_json(Path(dv) / "nos" / f"{no}.json") for no in NOS}
    salvar_json(Path(dv) / "estado.json", estado)
    return estado


def nova_versao(dv, motivo):
    dv = Path(dv)
    n = int(dv.name[1:]) + 1
    nova = dv.parent / f"v{n}"
    shutil.copytree(dv / "nos", nova / "nos")
    shutil.copytree(dv / "entregaveis", nova / "entregaveis")
    if (dv / "insumos").exists():
        shutil.copytree(dv / "insumos", nova / "insumos")
    for sub in ["revisoes", "saidas"]:
        (nova / sub).mkdir(parents=True, exist_ok=True)
    meta = carregar_json(nova / "nos" / "meta.json")
    meta["versao"] = n
    salvar_json(nova / "nos" / "meta.json", meta)
    c = _controle(dv)
    c2 = {"nos": {}, "aprovacoes": [], "congelado": False,
          "historico": [{"em": agora(), "evento": "nova_versao", "de": dv.name, "motivo": motivo}]}
    _salvar_controle(nova, c2)
    print(nova)


def congelar(dv):
    c = _controle(dv)
    modo = (carregar_json(Path(dv) / "nos" / "meta.json", {}) or {}).get("modo", "plano")
    final = "G5" if modo == "plano" else "G3"
    if not any(a["gate"] == final for a in c["aprovacoes"]):
        sys.exit(f"Sem aprovação {final}. Não é possível congelar.")
    resumo = carregar_json(Path(dv) / "saidas" / "resumo.json")
    if not resumo:
        sys.exit("Rode o motor antes de congelar.")
    salvar_json(Path(dv) / "saidas" / "baseline.json", {"congelado_em": agora(), "resumo": resumo,
                                                         "hashes": {no: hash_no(dv, no) for no in NOS}})
    c["congelado"] = True
    c["historico"].append({"em": agora(), "evento": "congelado"})
    _salvar_controle(dv, c)
    print("versão congelada; baseline salva em saidas/baseline.json")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("init"); a.add_argument("cliente", metavar="ciclo"); a.add_argument("projeto", metavar="titulo")
    a.add_argument("--modo", choices=["plano", "estudo"], required=True); a.add_argument("--mes-inicio")
    a = sp.add_parser("status"); a.add_argument("dv")
    a = sp.add_parser("carimbar"); a.add_argument("dv"); a.add_argument("no"); a.add_argument("--agente", required=True)
    a = sp.add_parser("aprovar"); a.add_argument("dv"); a.add_argument("--gate", required=True)
    a.add_argument("--por", required=True); a.add_argument("--obs", default="")
    a = sp.add_parser("montar"); a.add_argument("dv")
    a = sp.add_parser("nova-versao"); a.add_argument("dv"); a.add_argument("--motivo", required=True)
    a = sp.add_parser("congelar"); a.add_argument("dv")
    x = ap.parse_args()
    if x.cmd == "init": init(x.cliente, x.projeto, x.modo, x.mes_inicio)
    elif x.cmd == "status": status(x.dv)
    elif x.cmd == "carimbar": carimbar(x.dv, x.no, x.agente)
    elif x.cmd == "aprovar": aprovar(x.dv, x.gate, x.por, x.obs)
    elif x.cmd == "montar": montar(x.dv); print("estado.json montado")
    elif x.cmd == "nova-versao": nova_versao(x.dv, x.motivo)
    elif x.cmd == "congelar": congelar(x.dv)


if __name__ == "__main__":
    main()
