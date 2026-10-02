"""Roda o motor de ponta a ponta: perfil (se faltar), pseudonimização, preparação, análises, impacto, insights,
linhagem e entregáveis. Não roda a auditoria (use python -m motor.reprodutibilidade).

Uso: python -m motor.rodar <dv> [--forcar]
"""
import argparse, sys
from pathlib import Path
from .util import carregar_json
from .estado import montar
from . import perfil, pipeline, registro, impacto, insights, linhagem, relatorio


def rodar(dv, forcar=False):
    dv = Path(dv)
    if (carregar_json(dv / "controle.json", {}) or {}).get("congelado") and not forcar:
        sys.exit("Versão congelada: crie nova versão (python -m motor.estado nova-versao).")
    if not (dv / "saidas" / "catalogo.json").exists():
        sys.exit("Sem dados importados: python -m motor.ingestao importar <dv> <pasta>")
    montar(dv)
    if not (dv / "saidas" / "perfil.json").exists():
        perfil.perfilar(dv)
    pipeline.rodar(dv)
    erros = []
    if (carregar_json(dv / "nos" / "plano.json", {}) or {}).get("analises"):
        _, erros = registro.rodar(dv)
    _, e2 = impacto.calcular(dv); erros += e2
    lista, pend = insights.checar(dv)
    linhagem.gerar(dv)
    arq, falta = relatorio.gerar(dv)
    print(f"\nInsights: {len(lista)} ({sum(1 for i in lista if i['estado'] == 'aprovado')} aprovados) · pendências: {len(pend)}")
    for p in pend: print("pendência:", p)
    for k, v in falta.items():
        if v: print(f"entregável {k}: variáveis sem valor {v}")
    print(f"Planilha: {arq}\nPainel: {dv / 'saidas' / 'painel.html'}")
    return erros


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("dv"); ap.add_argument("--forcar", action="store_true")
    x = ap.parse_args(); e = rodar(x.dv, x.forcar); sys.exit(1 if e else 0)
