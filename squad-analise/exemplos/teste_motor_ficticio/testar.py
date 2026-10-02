"""Teste do motor do squad de análise com dados FICTÍCIOS (Windows, Linux ou Mac). Não altera a base real.

Uso, a partir da pasta squad-analise:  python exemplos/teste_motor_ficticio/testar.py
"""
import os, shutil, stat, sys, tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
EX = RAIZ / "exemplos" / "teste_motor_ficticio"
os.environ["SQUAD_CONHECIMENTO"] = str(EX / "conhecimento")
sys.path.insert(0, str(RAIZ))

from motor.util import NOS                      # noqa: E402
from motor import estado, ingestao, perfil, rodar, reprodutibilidade, insights, validar  # noqa: E402


def _apagar(func, caminho, _):
    os.chmod(caminho, stat.S_IWRITE); func(caminho)


tmp = Path(tempfile.mkdtemp(prefix="teste_analise_")); dv = tmp / "v1"
shutil.copytree(EX / "v1", dv)
for sub in ["saidas", "dados/brutos", "dados/preparados", "dados/privado"]:
    (dv / sub).mkdir(parents=True, exist_ok=True)
ok = True
try:
    print("=== Importação e perfil ===")
    ingestao.importar(dv, [EX / "dados_fonte"])
    p = perfil.perfilar(dv)
    pes = sorted(f"{t}.{c['coluna']}" for t, d in p["tabelas"].items() for c in d["colunas"] if c["pessoal"])
    print("Dado pessoal detectado:", pes)
    ok &= {"raw_missoes.operador_nome", "raw_missoes.operador_cpf"} <= set(pes)
    for no in NOS:
        estado.carimbar(dv, no, "teste")
    for g in ["G1", "G2"]:
        estado.aprovar(dv, g, "teste")
    print("\n=== Motor ===")
    ok &= not rodar.rodar(dv)
    print("\n=== Auditoria de reprodutibilidade ===")
    a = reprodutibilidade.auditar(dv); print("Auditoria:", a["status"], a["divergencias"]); ok &= a["status"] == "ok"
    print("\n=== Validação até D3 ===")
    v = validar.validar(dv, "D3")
    for m in v.bloq: print("BLOQUEIO:", m)
    ok &= not v.bloq
    print("\n=== G3, aprovação dos insights e validação até D4 ===")
    estado.aprovar(dv, "G3", "teste"); insights.aprovar(dv, "teste")
    rodar.rodar(dv)
    v = validar.validar(dv, "D4")
    for m in v.bloq: print("BLOQUEIO:", m)
    ok &= not v.bloq
    print("\n" + (dv / "saidas" / "memo_decisao.md").read_text(encoding="utf-8"))
    base = (dv / "dados" / "analise.duckdb")
    import duckdb
    con = duckdb.connect(str(base), read_only=True)
    amostra = con.execute("select operador_nome, operador_cpf from base_missoes limit 1").fetchone(); con.close()
    print("Amostra pseudonimizada:", amostra); ok &= all(str(x).startswith("P_") for x in amostra)
finally:
    shutil.copytree(dv / "saidas", EX / "ultima_execucao", dirs_exist_ok=True)
    shutil.rmtree(tmp, onerror=_apagar)
print("\nTESTE", "OK" if ok else "COM DIFERENÇAS (veja as mensagens acima)")
