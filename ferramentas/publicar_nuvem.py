"""Publica as saídas de uma versão num lugar que sobrevive à sessão de nuvem: <squad>/publicados/<projeto>/v<n>/.

Copia saídas, nós, revisões e evidências; nunca copia dados, entradas, insumos originais nem bancos locais.
Depois faça commit e push dessa pasta na branch da sessão (e, se quiser, envie os entregáveis ao Drive pelo conector).

Uso (na raiz):  python ferramentas/publicar_nuvem.py squad-orcamento projetos/<id>/v1
"""
import json, shutil, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
INCLUIR = ["saidas", "nos", "revisoes", "evidencias", "contrato", "entregaveis", "revisoes_trimestrais", "controle.json", "estado.json"]
IGNORAR = shutil.ignore_patterns("*.duckdb*", "dados", "originais", "paginas", "__pycache__", "chave_local.key")

if len(sys.argv) != 3:
    sys.exit(__doc__)
squad = RAIZ / sys.argv[1]; dv = (squad / sys.argv[2]).resolve()
if not (dv / "nos" / "meta.json").exists():
    sys.exit(f"Não encontrei {dv}/nos/meta.json")
meta = json.loads((dv / "nos" / "meta.json").read_text(encoding="utf-8"))
destino = squad / "publicados" / meta.get("projeto_id", dv.parent.name) / f"v{meta.get('versao', 1)}"
destino.mkdir(parents=True, exist_ok=True)
for item in INCLUIR:
    o = dv / item
    if o.is_dir():
        shutil.copytree(o, destino / item, dirs_exist_ok=True, ignore=IGNORAR)
    elif o.is_file():
        shutil.copy2(o, destino / item)
rel = destino.relative_to(RAIZ).as_posix()
print(f"Publicado em {rel}\nPróximo passo: git add \"{rel}\" && git commit -m \"publica {meta.get('projeto_id')} v{meta.get('versao', 1)}\" && git push")
