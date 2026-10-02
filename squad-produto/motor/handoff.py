"""Gera o pacote de entrada para o squad de orçamento a partir da especificação aprovada.

Uso: python -m motor.handoff <dir_versao> [--destino <pasta>]
Por padrão grava em <dv>/saidas/handoff_orcamento/ e, se existir, copia para ../squad-orcamento/entrada/<projeto_id>/ (config: orcamento_entrada_dir).
"""
import argparse, shutil
from pathlib import Path
from .util import RAIZ, carregar_nos, escrever_csv, config


def gerar(dv, destino=None):
    dv = Path(dv); nos = carregar_nos(dv); meta = nos["meta"] or {}
    out = dv / "saidas" / "handoff_orcamento"; out.mkdir(parents=True, exist_ok=True)
    req = (nos["requisitos"] or {}).get("itens", []) or []
    escrever_csv(out / "requisitos.csv", req, ["id", "tipo", "prioridade", "descricao", "criterio_aceite", "metrica", "valor_alvo", "release"])
    comp = (nos["arquitetura"] or {}).get("componentes", []) or []
    linhas = [{"id": c.get("id"), "nome": c.get("nome"), "tipo": c.get("tipo"), "decisao": c.get("decisao"), "trl": c.get("trl"),
               "custo_provavel_estimado": (c.get("custo_unitario") or {}).get("provavel"), "fonte_custo": c.get("fonte_custo"),
               "alternativas": "; ".join(f"{a.get('opcao')} ({a.get('fornecedor')})" for a in c.get("alternativas", []) or [])} for c in comp]
    escrever_csv(out / "componentes.csv", linhas, list(linhas[0].keys()) if linhas else ["id"])
    cc = nos["conceitos"] or {}
    esc = next((c for c in cc.get("conceitos", []) or [] if c.get("id") == cc.get("escolhido")), {})
    neg = nos["negocio"] or {}
    txt = [f"# Briefing para orçamento — {meta.get('produto')}", "",
           f"Origem: especificação de produto {meta.get('projeto_id')} v{meta.get('versao')} (squad de produto).", "",
           "## Solução escolhida", f"{esc.get('nome', '[●]')}: {esc.get('descricao', '')}", "",
           "## Arquitetura", (nos["arquitetura"] or {}).get("visao", "[●]"), "",
           "## Escopo do MVP", "Requisitos must e o critério de aceite de cada um estão em `requisitos.csv`. Componentes e alternativas avaliadas estão em `componentes.csv`.", "",
           "## Premissas comerciais", f"Modelo de receita: {neg.get('modelo_receita', '[●]')}; unidades por cliente: {neg.get('unidades_por_cliente', '[●]')}.", "",
           "## O que pedir ao squad de orçamento",
           "Dimensionar e orçar a implantação do MVP para um cliente típico do segmento-alvo, com cotações reais para os componentes críticos. Os custos estimados aqui são premissas de produto, não cotações."]
    (out / "briefing.md").write_text("\n".join(txt) + "\n", encoding="utf-8")
    alvo = Path(destino) if destino else (RAIZ / (config().get("orcamento_entrada_dir") or "../squad-orcamento/entrada")).resolve()
    if alvo.exists():
        d = alvo / meta.get("projeto_id", "produto")
        shutil.copytree(out, d, dirs_exist_ok=True)
        print(f"Pacote copiado para {d}. No squad de orçamento: /orcar completo \"<cliente>\" \"{meta.get('produto')}\" entrada\\{d.name}")
    print(f"Pacote gerado em {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("dv"); ap.add_argument("--destino")
    a = ap.parse_args(); gerar(a.dv, a.destino)
