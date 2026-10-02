"""Importa dados de entrada (arquivos ou pastas) para a análise: cópia somente leitura em dados/brutos e tabelas raw_* no DuckDB.

Uso:
  python -m motor.ingestao importar <dv> <arquivo_ou_pasta> [...]
  python -m motor.ingestao reconstruir <dv>     (recria as tabelas a partir de dados/brutos e do catálogo)
Formatos: .csv .tsv .txt (separador e codificação detectados), .xlsx (todas as abas), .parquet, .json/.jsonl, .sqlite/.db.
"""
import argparse, shutil, sqlite3, stat, sys
from pathlib import Path
from .util import carregar_json, salvar_json, agora
from .dados import conectar, slug, sha256_arquivo

SUPORTADOS = {".csv", ".tsv", ".txt", ".xlsx", ".xlsm", ".parquet", ".json", ".jsonl", ".ndjson", ".sqlite", ".db"}


def _csv(con, nome, p):
    p = str(p).replace("\\", "/")
    try:
        sn = con.execute(f"select Delimiter from sniff_csv('{p}')").fetchone()
        dec = ", decimal_separator=','" if sn and sn[0] == ";" else ""
    except Exception:
        dec = ""
    for enc in ["", ", encoding='latin-1'"]:
        try:
            con.execute(f"create or replace table {nome} as select * from read_csv('{p}', auto_detect=true, sample_size=-1{dec}{enc})")
            return "duckdb" + (" latin-1" if enc else "") + (" decimal ," if dec else "")
        except Exception as e:
            erro = e
    import pandas as pd
    for enc in ["utf-8", "latin-1", "cp1252"]:
        try:
            df = pd.read_csv(p, sep=None, engine="python", encoding=enc)
            con.register("_tmp_df", df); con.execute(f"create or replace table {nome} as select * from _tmp_df"); con.unregister("_tmp_df")
            return f"pandas {enc}"
        except Exception as e:
            erro = e
    raise RuntimeError(f"não consegui ler {Path(p).name}: {erro}")


def _registrar(con, p, base):
    ext = p.suffix.lower(); feitas = []
    if ext in (".csv", ".tsv", ".txt"):
        nome = f"raw_{base}"; obs = _csv(con, nome, p); feitas.append((nome, obs, None))
    elif ext in (".xlsx", ".xlsm"):
        import pandas as pd
        for aba, df in pd.read_excel(p, sheet_name=None).items():
            nome = f"raw_{base}_{slug(aba)}"
            con.register("_tmp_df", df); con.execute(f"create or replace table {nome} as select * from _tmp_df"); con.unregister("_tmp_df")
            feitas.append((nome, "excel", aba))
    elif ext == ".parquet":
        nome = f"raw_{base}"; con.execute(f"create or replace table {nome} as select * from read_parquet('{str(p).replace(chr(92), '/')}')"); feitas.append((nome, "parquet", None))
    elif ext in (".json", ".jsonl", ".ndjson"):
        nome = f"raw_{base}"; con.execute(f"create or replace table {nome} as select * from read_json_auto('{str(p).replace(chr(92), '/')}')"); feitas.append((nome, "json", None))
    elif ext in (".sqlite", ".db"):
        import pandas as pd
        lite = sqlite3.connect(str(p))
        for (t,) in lite.execute("select name from sqlite_master where type='table'").fetchall():
            df = pd.read_sql_query(f'select * from "{t}"', lite); nome = f"raw_{base}_{slug(t)}"
            con.register("_tmp_df", df); con.execute(f"create or replace table {nome} as select * from _tmp_df"); con.unregister("_tmp_df")
            feitas.append((nome, "sqlite", t))
        lite.close()
    return feitas


def importar(dv, caminhos):
    dv = Path(dv); destino = dv / "dados" / "brutos"; destino.mkdir(parents=True, exist_ok=True)
    cat = carregar_json(dv / "saidas" / "catalogo.json", {"arquivos": [], "tabelas": []})
    con = conectar(dv)
    arquivos = []
    for c in caminhos:
        c = Path(c)
        if c.is_dir():
            arquivos += [x for x in sorted(c.rglob("*")) if x.is_file() and x.suffix.lower() in SUPORTADOS]
        elif c.is_file():
            arquivos.append(c)
        else:
            print(f"não encontrado: {c}")
    for a in arquivos:
        if a.suffix.lower() not in SUPORTADOS:
            print(f"ignorado (formato não suportado): {a.name}"); continue
        alvo = destino / a.name
        if alvo.exists():
            alvo.chmod(stat.S_IWRITE | stat.S_IREAD)
        shutil.copy2(a, alvo)
        alvo.chmod(stat.S_IREAD)
        h = sha256_arquivo(alvo); base = slug(a.stem)
        try:
            feitas = _registrar(con, alvo, base)
        except Exception as e:
            print(f"ERRO ao ler {a.name}: {e}"); continue
        cat["arquivos"] = [x for x in cat["arquivos"] if x["arquivo"] != a.name] + [{"arquivo": a.name, "sha256": h, "importado_em": agora()}]
        for nome, obs, parte in feitas:
            n = con.execute(f"select count(*) from {nome}").fetchone()[0]
            cols = [r[0] for r in con.execute(f"select column_name from information_schema.columns where table_name='{nome}' order by ordinal_position").fetchall()]
            cat["tabelas"] = [t for t in cat["tabelas"] if t["tabela"] != nome] + [{"tabela": nome, "arquivo": a.name, "parte": parte, "leitura": obs, "linhas": int(n), "colunas": len(cols)}]
            print(f"{nome}: {n} linhas, {len(cols)} colunas ({obs})")
    con.close()
    salvar_json(dv / "saidas" / "catalogo.json", cat)
    return cat


def reconstruir(dv):
    """Recria as tabelas raw_* a partir de dados/brutos, conferindo as assinaturas do catálogo."""
    dv = Path(dv); cat = carregar_json(dv / "saidas" / "catalogo.json")
    if not cat:
        sys.exit("Sem catálogo: importe os dados primeiro.")
    con = conectar(dv); divergencias = []
    for a in cat["arquivos"]:
        p = dv / "dados" / "brutos" / a["arquivo"]
        if not p.exists():
            divergencias.append(f"arquivo bruto ausente: {a['arquivo']}"); continue
        if sha256_arquivo(p) != a["sha256"]:
            divergencias.append(f"arquivo bruto alterado: {a['arquivo']}")
        _registrar(con, p, slug(p.stem))
    con.close()
    return divergencias


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("importar"); a.add_argument("dv"); a.add_argument("caminhos", nargs="+")
    a = sp.add_parser("reconstruir"); a.add_argument("dv")
    x = ap.parse_args()
    if x.cmd == "importar":
        importar(x.dv, x.caminhos)
    else:
        d = reconstruir(x.dv); print("\n".join(d) if d else "Tabelas reconstruídas; assinaturas conferem.")
