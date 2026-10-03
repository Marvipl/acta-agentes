"""Monta o pacote de publicação de uma versão, igual ao que a publicação local copia para o Drive:
saidas/ (documentos, planilha, JSON, CSV, gráficos), nos/, revisoes/, insumos/indice.*, controle.json, estado.json
e, quando existirem, evidencias/, contrato/ e revisoes_trimestrais/. Nunca inclui dados brutos, entradas,
originais dos insumos, bancos locais nem chaves.

Gera em <squad>/publicados/<projeto>/v<n>/:
  - a cópia de tudo, com as mesmas subpastas;
  - manifesto_publicacao.json: lista de arquivos (caminho, tamanho, sha256, tipo) e a pasta de destino no Drive;
  - <projeto>_v<n>_pacote_completo.zip: o mesmo conteúdo num arquivo só.
O envio ao Drive é feito pelo comando /publicar-drive, que usa o manifesto.

Uso (na raiz):  python ferramentas/publicar_nuvem.py squad-orcamento projetos/<id>/v1
"""
import hashlib, json, mimetypes, shutil, sys, zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PASTAS = ["saidas", "nos", "revisoes", "evidencias", "contrato", "revisoes_trimestrais"]
ARQUIVOS = ["controle.json", "estado.json", "insumos/indice.md", "insumos/indice.json"]
IGNORAR = shutil.ignore_patterns("*.duckdb*", "dados", "originais", "paginas", "__pycache__", "chave_local.key", "*.parquet")
MIME = {".md": "text/markdown", ".json": "application/json", ".csv": "text/csv",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".html": "text/html", ".png": "image/png", ".zip": "application/zip", ".txt": "text/plain"}


def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def publicar(squad_nome, rel_dv):
    squad = RAIZ / squad_nome; dv = (squad / rel_dv).resolve()
    if not (dv / "nos" / "meta.json").exists():
        sys.exit(f"Não encontrei {dv}/nos/meta.json")
    meta = json.loads((dv / "nos" / "meta.json").read_text(encoding="utf-8"))
    pid, ver = meta.get("projeto_id", dv.parent.name), f"v{meta.get('versao', 1)}"
    destino = (squad / "publicados" / pid / ver).resolve()
    if destino == dv:
        # republicação a partir de um pacote já publicado (por exemplo, commitado numa sessão anterior): só refaz manifesto e zip
        for velho in list(destino.glob("*_pacote_completo.zip")) + [destino / "manifesto_publicacao.json"]:
            velho.unlink(missing_ok=True)
    else:
        if destino.exists():
            shutil.rmtree(destino)
        destino.mkdir(parents=True)
        for p in PASTAS:
            if (dv / p).is_dir():
                shutil.copytree(dv / p, destino / p, ignore=IGNORAR)
        for a in ARQUIVOS:
            if (dv / a).is_file():
                (destino / a).parent.mkdir(parents=True, exist_ok=True); shutil.copy2(dv / a, destino / a)
    cfg = json.loads((RAIZ / "ferramentas" / "squads.json").read_text(encoding="utf-8")) if (RAIZ / "ferramentas" / "squads.json").exists() else {}
    pasta_drive = f"{(cfg.get(squad_nome) or {}).get('drive', 'Acta')} > {pid} > {ver}"
    arquivos = sorted(p for p in destino.rglob("*") if p.is_file())
    zip_nome = f"{pid}_{ver}_pacote_completo.zip"
    with zipfile.ZipFile(destino / zip_nome, "w", zipfile.ZIP_DEFLATED) as z:
        for p in arquivos:
            z.write(p, p.relative_to(destino).as_posix())
    itens = [{"caminho": p.relative_to(destino).as_posix(), "bytes": p.stat().st_size, "sha256": _sha(p),
              "tipo": MIME.get(p.suffix.lower()) or mimetypes.guess_type(p.name)[0] or "application/octet-stream"}
             for p in sorted(destino.rglob("*")) if p.is_file()]
    manifesto = {"projeto_id": pid, "versao": ver, "squad": squad_nome, "pasta_drive": pasta_drive,
                 "pasta_local": destino.relative_to(RAIZ).as_posix(), "total_arquivos": len(itens),
                 "subpastas": sorted({i["caminho"].rsplit("/", 1)[0] for i in itens if "/" in i["caminho"]}), "arquivos": itens}
    (destino / "manifesto_publicacao.json").write_text(json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")
    por_pasta = {}
    for i in itens:
        k = i["caminho"].split("/")[0] if "/" in i["caminho"] else "(raiz)"; por_pasta[k] = por_pasta.get(k, 0) + 1
    print(f"Pacote: {manifesto['pasta_local']} ({len(itens)} arquivos + manifesto)")
    print("Por pasta: " + ", ".join(f"{k}: {v}" for k, v in sorted(por_pasta.items())))
    print(f"Destino no Drive: {pasta_drive}")
    print("Próximo passo: envie ao Drive com /publicar-drive (ou, no computador, use python -m motor.publicar do squad).")
    return manifesto


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    publicar(sys.argv[1], sys.argv[2])
