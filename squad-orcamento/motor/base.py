"""Base de preços: registrar cotações reais e medir o erro dos benchmarks (aprendizado desde o primeiro orçamento).

Uso:
  python -m motor.base registrar-cotacao --item "..." --fabricante X --modelo Y --fornecedor Z --moeda USD --preco 1000 \
      --data AAAA-MM-DD --validade-dias 30 --ref precos/cotacoes/arquivo.pdf [--incoterm FOB] [--lead-time-dias 60] \
      [--qtd-minima 1] [--frete-incluso nao] [--estimativa-anterior 900 --projeto <projeto_id>] [--obs "..."]
  python -m motor.base buscar <termo>
  python -m motor.base validar
"""
import argparse, sys
from datetime import date
from .util import CONHEC, ler_csv, escrever_csv, hoje

BASE = CONHEC / "precos" / "base_precos.csv"
BENCH = CONHEC / "historico" / "benchmark_vs_cotacao.csv"
CAMPOS = ["id", "data", "item", "fabricante", "modelo", "especificacao", "fornecedor", "moeda", "preco_unit", "qtd_minima",
          "incoterm", "frete_incluso", "lead_time_dias", "validade_dias", "ref_documento", "registrado_em", "observacoes"]


def registrar(a):
    linhas = ler_csv(BASE)
    novo_id = f"P{len(linhas) + 1:04d}"
    linhas.append({"id": novo_id, "data": a.data, "item": a.item, "fabricante": a.fabricante, "modelo": a.modelo,
                   "especificacao": a.especificacao or "", "fornecedor": a.fornecedor, "moeda": a.moeda, "preco_unit": a.preco,
                   "qtd_minima": a.qtd_minima or "", "incoterm": a.incoterm or "", "frete_incluso": a.frete_incluso or "",
                   "lead_time_dias": a.lead_time_dias or "", "validade_dias": a.validade_dias, "ref_documento": a.ref,
                   "registrado_em": hoje(), "observacoes": a.obs or ""})
    escrever_csv(BASE, linhas, CAMPOS)
    print(f"cotação registrada: {novo_id}")
    if a.estimativa_anterior:
        b = ler_csv(BENCH)
        b.append({"data": a.data, "projeto_id": a.projeto or "", "id_preco": novo_id, "item": a.item, "moeda": a.moeda,
                  "estimativa_benchmark": a.estimativa_anterior, "cotacao": a.preco,
                  "razao": round(float(a.preco) / float(a.estimativa_anterior), 4)})
        escrever_csv(BENCH, b, ["data", "projeto_id", "id_preco", "item", "moeda", "estimativa_benchmark", "cotacao", "razao"])
        print(f"erro do benchmark registrado: cotação/estimativa = {float(a.preco)/float(a.estimativa_anterior):.3f}")


def buscar(termo):
    t = termo.lower()
    for l in ler_csv(BASE):
        if t in " ".join(str(v) for v in l.values()).lower():
            print(l)


def validar():
    erros = 0
    for l in ler_csv(BASE):
        try:
            float(l["preco_unit"]); date.fromisoformat(l["data"]); int(l["validade_dias"])
        except Exception:
            print(f"linha inválida: {l.get('id')}"); erros += 1
        if not l.get("ref_documento"):
            print(f"{l.get('id')}: sem documento de referência"); erros += 1
    print("OK" if not erros else f"{erros} problema(s)")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("registrar-cotacao")
    for k in ["item", "fabricante", "modelo", "fornecedor", "moeda", "preco", "data", "validade-dias", "ref"]:
        a.add_argument(f"--{k}", required=True)
    for k in ["especificacao", "qtd-minima", "incoterm", "frete-incluso", "lead-time-dias", "estimativa-anterior", "projeto", "obs"]:
        a.add_argument(f"--{k}")
    a = sp.add_parser("buscar"); a.add_argument("termo")
    sp.add_parser("validar")
    x = ap.parse_args()
    if x.cmd == "registrar-cotacao": registrar(x)
    elif x.cmd == "buscar": buscar(x.termo)
    else: validar()
