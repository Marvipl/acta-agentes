"""Cria uma cópia de trabalho de uma versão para testar cenários sem tocar no orçamento real (funciona em Windows, Linux e Mac).

Uso: python -m motor.cenario <dir_versao> <nome_do_cenario>
     -> cria projetos/_cenarios/<nome_do_cenario>/ ; edite os nós da cópia e rode: python -m motor.rodar projetos/_cenarios/<nome>
"""
import argparse, shutil
from pathlib import Path
from .util import RAIZ, carregar_json, salvar_json


def criar(dv, nome):
    dv = Path(dv)
    destino = RAIZ / "projetos" / "_cenarios" / nome
    if destino.exists():
        shutil.rmtree(destino)
    shutil.copytree(dv, destino, ignore=shutil.ignore_patterns("saidas", "revisoes"))
    (destino / "saidas").mkdir(exist_ok=True); (destino / "revisoes").mkdir(exist_ok=True)
    c = carregar_json(destino / "controle.json", {})
    c["congelado"] = False
    salvar_json(destino / "controle.json", c)
    print(destino)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("dv"); ap.add_argument("nome")
    a = ap.parse_args(); criar(a.dv, a.nome)
