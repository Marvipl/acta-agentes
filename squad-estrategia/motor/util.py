import csv, hashlib, json, os, sys
from datetime import date, datetime
from pathlib import Path

for _fluxo in (sys.stdout, sys.stderr):
    try:
        _fluxo.reconfigure(errors="replace")
    except Exception:
        pass

RAIZ = Path(__file__).resolve().parent.parent
# Permite apontar para outra base (ex.: exemplo fictício de teste) sem tocar na base real
CONHEC = Path(os.environ.get("SQUAD_CONHECIMENTO", RAIZ / "conhecimento"))

# Ordem dos nós e dependências (entradas que cada nó usa)
NOS = ["meta", "briefing", "enquadramento", "mercado", "concorrencia", "regulatorio", "interno", "capacidades",
       "diagnostico", "opcoes", "portfolio", "financeiro_opcoes", "okrs", "organizacao", "iniciativas",
       "financeiro", "riscos", "governanca"]

DEPENDENCIAS = {
    "meta": [],
    "briefing": ["meta"],
    "enquadramento": ["briefing"],
    "mercado": ["enquadramento"],
    "concorrencia": ["enquadramento"],
    "regulatorio": ["enquadramento"],
    "interno": ["enquadramento"],
    "capacidades": ["enquadramento"],
    "diagnostico": ["mercado", "concorrencia", "regulatorio", "interno", "capacidades"],
    "opcoes": ["diagnostico"],
    "portfolio": ["diagnostico", "opcoes"],
    "financeiro_opcoes": ["opcoes", "portfolio", "interno"],
    "okrs": ["diagnostico", "opcoes"],
    "organizacao": ["opcoes", "capacidades", "okrs"],
    "iniciativas": ["opcoes", "portfolio", "okrs", "organizacao"],
    "financeiro": ["opcoes", "portfolio", "interno", "organizacao", "iniciativas"],
    "riscos": ["opcoes", "iniciativas", "financeiro"],
    "governanca": ["okrs", "riscos", "opcoes"],
}

DONOS = {
    "meta": "chief-strategist", "briefing": "chief-strategist", "diagnostico": "chief-strategist",
    "enquadramento": "enquadramento", "mercado": "inteligencia-mercado", "concorrencia": "concorrencia",
    "regulatorio": "regulatorio-fomento", "interno": "desempenho-interno", "capacidades": "capacidades-organizacao",
    "organizacao": "capacidades-organizacao", "opcoes": "arquiteto-estrategia", "portfolio": "portfolio-iniciativas",
    "iniciativas": "portfolio-iniciativas", "financeiro_opcoes": "financeiro-estrategico", "financeiro": "financeiro-estrategico",
    "okrs": "okr-kpi", "riscos": "riscos-governanca", "governanca": "riscos-governanca",
}


def carregar_json(caminho, padrao=None):
    p = Path(caminho)
    if not p.exists():
        return padrao
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def salvar_json(caminho, obj):
    p = Path(caminho)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def config():
    return carregar_json(RAIZ / "config" / "config.json", {})


def ler_csv(caminho):
    p = Path(caminho)
    if not p.exists():
        return []
    with open(p, encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if any((v or "").strip() for v in r.values())]


def escrever_csv(caminho, linhas, campos):
    p = Path(caminho)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for l in linhas:
            w.writerow({k: l.get(k, "") for k in campos})


def tri(v):
    """Converte {min, provavel, max} ou número em tupla (min, provavel, max)."""
    if isinstance(v, dict):
        a, m, b = v.get("min"), v.get("provavel"), v.get("max")
        if m is None:
            raise ValueError(f"valor sem 'provavel': {v}")
        a = m if a is None else a
        b = m if b is None else b
        return float(a), float(m), float(b)
    if v is None:
        raise ValueError("valor ausente")
    return float(v), float(v), float(v)


def prov(v):
    return tri(v)[1]


def tri_valido(v):
    try:
        a, m, b = tri(v)
    except Exception:
        return False
    return a <= m <= b and a >= 0


def hash_obj(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]


def brl(v):
    if v is None:
        return "[●]"
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-R$ " if v < 0 else "R$ ") + s


def pct(v, casas=1):
    if v is None:
        return "[●]"
    return f"{v*100:.{casas}f}%".replace(".", ",")


def num(v, casas=0):
    if v is None:
        return "[●]"
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def hoje():
    return date.today().isoformat()


def agora():
    return datetime.now().isoformat(timespec="seconds")


def dias_desde(data_iso):
    try:
        return (date.today() - date.fromisoformat(str(data_iso)[:10])).days
    except Exception:
        return None


def mes_label(mes_inicio, i):
    a, m = map(int, mes_inicio.split("-"))
    t = a * 12 + (m - 1) + i
    return f"{t // 12:04d}-{t % 12 + 1:02d}"


def carregar_nos(dir_versao):
    """Carrega os nós; nós ainda no modelo (_template) voltam como {} para não poluir cálculo e validação."""
    d = Path(dir_versao) / "nos"
    out = {}
    for n in NOS:
        v = carregar_json(d / f"{n}.json")
        out[n] = {} if (not v or v.get("_template")) else v
    return out


def custo_hora_por_perfil():
    out = {}
    for l in ler_csv(CONHEC / "mao_de_obra" / "custo_hora.csv"):
        try:
            out[l["perfil"].strip()] = float(str(l["custo_hora_brl"]).replace(",", "."))
        except Exception:
            out[l["perfil"].strip()] = None
    return out


def caminho_capacidade():
    """Capacidade do time: por padrão, a mesma planilha do squad de orçamento (uma única fonte)."""
    rel = config().get("capacidade_time_csv")
    if rel and not os.environ.get("SQUAD_CONHECIMENTO"):
        p = (RAIZ / rel).resolve()
        if p.exists():
            return p
    return CONHEC / "mao_de_obra" / "capacidade_time.csv"


def fatores_aprovados():
    out = {}
    for l in ler_csv(CONHEC / "historico" / "fatores_correcao.csv"):
        try:
            out[l["categoria"].strip()] = float(l["fator"].replace(",", "."))
        except Exception:
            pass
    return out
