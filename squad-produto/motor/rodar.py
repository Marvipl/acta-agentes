"""Executa o motor: monta o estado, calcula, gera planilha e entregáveis.

Uso: python -m motor.rodar <dir_versao> [--forcar]
"""
import argparse, sys
from pathlib import Path
from .util import NOS, carregar_nos, carregar_json, salvar_json, escrever_csv, hash_obj, agora, brl
from .estado import montar
from .produto import calcular
from .planilha import gerar
from .renderizar import renderizar


def rodar(dv, forcar=False):
    dv = Path(dv)
    if (carregar_json(dv / "controle.json", {}) or {}).get("congelado") and not forcar:
        sys.exit("Versão congelada: crie nova versão (python -m motor.estado nova-versao) ou use --forcar para só reler.")
    montar(dv)
    nos = carregar_nos(dv)
    try:
        res, det = calcular(nos)
    except Exception as e:
        sys.exit(f"Erro no cálculo: {e}. Rode 'python -m motor.validar {dv} --fase P3' para ver o que falta preencher.")
    res["_hashes"] = {n: hash_obj(nos[n]) for n in NOS}; res["_gerado_em"] = agora()
    s = dv / "saidas"; s.mkdir(exist_ok=True)
    salvar_json(s / "resumo.json", res)
    if res.get("negocio"):
        escrever_csv(s / "caso_de_negocio.csv", res["negocio"]["anos"], list(res["negocio"]["anos"][0].keys()))
    meta = nos["meta"] or {}
    nome = f"produto_{meta.get('projeto_id', 'produto')}_v{meta.get('versao', 1)}.xlsx"
    gerar(s / nome, res, nos)
    faltando = renderizar(dv, res)
    op = res["oportunidade"]
    print(f"Oportunidade: nota {op['nota']:.2f} | decisão {op['decisao']}" if op["nota"] is not None else "Oportunidade: sem nota")
    if res["conceitos"]["ranking"]:
        print("Conceitos: " + " | ".join(f"{c['id']} {c['nota']:.2f}" for c in res["conceitos"]["ranking"] if c["nota"] is not None) + f" | escolhido {res['conceitos']['escolhido']}")
    n = res.get("negocio")
    if n:
        print(f"Caso de negócio: custo unitário {brl(n['custo_unitario'])} | VPL 3 anos {brl(n['vpl'])} | payback {n['payback'] or 'além de 3 anos'} | maior sensibilidade: {n['sensibilidade'][0]['driver']}")
    if res.get("roi_cliente"):
        rc = res["roi_cliente"]
        print(f"ROI do cliente ({rc['modelo_avaliado']}): economia líquida anual {brl(rc['economia_liquida_anual'])} | payback {round(rc['payback_meses'], 1) if rc['payback_meses'] is not None else 'não se paga'} meses")
    print(f"Planilha: {s / nome}")
    for a in res["alertas"]: print("alerta:", a)
    for k, v in faltando.items():
        if v: print(f"entregável {k}: variáveis sem valor {v}")
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("dv"); ap.add_argument("--forcar", action="store_true")
    a = ap.parse_args(); rodar(a.dv, a.forcar)
