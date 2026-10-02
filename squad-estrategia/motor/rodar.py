"""Executa o motor: monta estado, calcula projeções, portfólio e capacidade, gera planilha e entregáveis.

Uso: python -m motor.rodar <dir_versao> [--forcar]
"""
import argparse, sys
from pathlib import Path
from .util import NOS, carregar_nos, carregar_json, salvar_json, escrever_csv, hash_obj, agora, brl
from .estado import montar
from .estrategia import calcular
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
        sys.exit(f"Erro no cálculo: {e}. Rode 'python -m motor.validar {dv} --fase E3' para ver o que falta preencher.")
    res["_hashes"] = {n: hash_obj(nos[n]) for n in NOS}
    res["_gerado_em"] = agora()
    s = dv / "saidas"; s.mkdir(exist_ok=True)
    salvar_json(s / "resumo.json", res)
    for k, linhas in det.items():
        if isinstance(linhas, list) and linhas:
            escrever_csv(s / f"{k}.csv", linhas, list(linhas[0].keys()))
    meta = nos["meta"] or {}
    nome = f"plano_{meta.get('projeto_id', 'ciclo')}_v{meta.get('versao', 1)}.xlsx"
    gerar(s / nome, res, det, nos)
    faltando = renderizar(dv, res)
    for c, d in res.get("cenarios", {}).items():
        i = d["indicadores"]
        print(f"Cenário {c}: menor caixa {brl(i['menor_caixa'])} em {i['mes_menor_caixa']} | captação necessária sem plano: {brl(i['necessidade_captacao'])} | EBITDA positivo: {i['ano_ebitda_positivo'] or 'fora do horizonte'}")
    for o, d in res.get("opcoes", {}).items():
        i = d["indicadores"]
        print(f"Opção {o}: menor caixa {brl(i['menor_caixa'])} | captação necessária: {brl(i['necessidade_captacao'])} | EBITDA positivo: {i['ano_ebitda_positivo'] or 'fora do horizonte'}")
    print(f"Planilha: {s / nome}")
    for a in res["alertas"]: print("alerta:", a)
    for k, v in faltando.items():
        if v: print(f"entregável {k}: variáveis sem valor {v}")
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("dv"); ap.add_argument("--forcar", action="store_true")
    a = ap.parse_args(); rodar(a.dv, a.forcar)
