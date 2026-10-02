"""Hook de início de sessão: na nuvem, instala as dependências de todos os squads (se faltarem) e grava a chave de
pseudonimização do squad de análise a partir da variável de ambiente. No computador local não faz nada.
"""
import importlib.util, os, subprocess, sys
from pathlib import Path

if os.environ.get("CLAUDE_CODE_REMOTE") != "true":
    sys.exit(0)
raiz = Path(__file__).resolve().parents[1]
modulos = {"duckdb": "duckdb", "pandas": "pandas", "numpy": "numpy", "scipy": "scipy", "statsmodels": "statsmodels",
           "sklearn": "scikit-learn", "pyarrow": "pyarrow", "openpyxl": "openpyxl", "matplotlib": "matplotlib",
           "pypdfium2": "pypdfium2", "PIL": "pillow", "docx": "python-docx", "pptx": "python-pptx"}
faltam = [pacote for mod, pacote in modulos.items() if importlib.util.find_spec(mod) is None]
reqs = sorted({l.strip() for r in raiz.glob("squad-*/requirements.txt") for l in r.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")})
if faltam:
    cmd = [sys.executable, "-m", "pip", "install", "-q", *reqs]
    if subprocess.run(cmd).returncode != 0:
        subprocess.run(cmd + ["--break-system-packages"])
chave = os.environ.get("SQUAD_CHAVE_PSEUDONIMIZACAO", "").strip()
destino = raiz / "squad-analise" / "config" / "chave_local.key"
if chave and destino.parent.exists() and not destino.exists():
    destino.write_text(chave, encoding="utf-8")
print("Squads prontos na nuvem" + (f" (dependências instaladas: {', '.join(faltam)})" if faltam else "") + ".")
