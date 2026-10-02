"""Conexão com o banco local da análise (DuckDB) e utilitários de dados."""
import hashlib, re, unicodedata
from pathlib import Path


def conectar(dv):
    import duckdb
    p = Path(dv) / "dados" / "analise.duckdb"
    p.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(p))


def slug(t):
    t = unicodedata.normalize("NFKD", str(t)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_") or "tabela"


def sha256_arquivo(p, bloco=1 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(bloco)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def tabelas(con, prefixo=None):
    ts = [r[0] for r in con.execute("select table_name from information_schema.tables where table_schema='main' order by 1").fetchall()]
    return [t for t in ts if not prefixo or t.startswith(prefixo)]


def impressao(con, tabela):
    """Contagem e impressão digital do conteúdo da tabela (independe da ordem das linhas)."""
    n, fp = con.execute(f'select count(*), coalesce(bit_xor(hash(t)), 0) from "{tabela}" t').fetchone()
    return {"linhas": int(n), "impressao": str(fp)}
