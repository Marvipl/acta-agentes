"""Copia os entregáveis de uma versão para a pasta do Google Drive (subpasta por orçamento).

Destino: <drive_orcamentos_dir>/<projeto_id>/v<n>/
Configure config/config.json -> drive_orcamentos_dir (pasta sincronizada pelo Google Drive para desktop).
Uso: python -m motor.publicar <dir_versao>
"""
import argparse, shutil, sys
from pathlib import Path
from .util import config, carregar_json


def publicar(dv):
    dv = Path(dv)
    raiz = config().get("drive_orcamentos_dir")
    if not raiz or raiz.startswith("[") or not Path(raiz).expanduser().exists():
        sys.exit("Configure config/config.json -> drive_orcamentos_dir com a pasta 'Acta > Orçamentos' sincronizada no computador.")
    meta = carregar_json(dv / "nos" / "meta.json")
    destino = Path(raiz).expanduser() / meta["projeto_id"] / dv.name
    destino.mkdir(parents=True, exist_ok=True)
    for sub in ["saidas", "nos", "revisoes"]:
        if (dv / sub).exists():
            shutil.copytree(dv / sub, destino / sub, dirs_exist_ok=True)
    if (dv / "insumos" / "indice.md").exists():
        (destino / "insumos").mkdir(exist_ok=True)
        shutil.copy(dv / "insumos" / "indice.md", destino / "insumos" / "indice.md")
    for f in ["controle.json", "estado.json"]:
        if (dv / f).exists():
            shutil.copy(dv / f, destino / f)
    print(f"publicado em {destino}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("dv"); publicar(ap.parse_args().dv)
