"""Executa o motor completo: monta estado, calcula, simula, gera planilha e entregáveis.

Uso: python -m motor.rodar <dir_versao>
"""
import argparse, sys
from pathlib import Path
from .util import NOS, carregar_nos, salvar_json, escrever_csv, hash_obj, brl, pct, agora
from .estado import montar
from .calculo import calcular
from .monte_carlo import simular
from .planilha import gerar
from .renderizar import renderizar
from .validar import itens_sem_cotacao


def rodar(dv, forcar=False):
    dv = Path(dv)
    from .util import carregar_json
    if (carregar_json(dv / "controle.json", {}) or {}).get("congelado") and not forcar:
        sys.exit("Versão congelada: crie nova versão (python -m motor.estado nova-versao) ou use --forcar para só reler.")
    montar(dv)
    nos = carregar_nos(dv)
    try:
        base, _ = calcular(nos, contingencia=0.0)
    except Exception as e:
        sys.exit(f"Erro no cálculo: {e}. Rode 'python -m motor.validar {dv} --fase F4' para ver o que falta preencher.")
    try:
        mc = simular(nos)
    except Exception as e:
        mc = None
        print(f"aviso: Monte Carlo não executado ({e})")
    cont = max(mc["custo_percentil_contingencia"] - base["custos"]["base"], 0.0) if mc else 0.0
    res, det = calcular(nos, contingencia=cont, mc=mc)
    det["mc_contrib"] = (mc or {}).get("maiores_contribuidores", [])
    res["_hashes"] = {n: hash_obj(nos[n]) for n in NOS}
    res["_gerado_em"] = agora()
    s = dv / "saidas"
    salvar_json(s / "resumo.json", res)
    if mc: salvar_json(s / "monte_carlo.json", mc)
    escrever_csv(s / "bom.csv", det["bom"], list(det["bom"][0].keys()) if det["bom"] else ["id"])
    escrever_csv(s / "mao_de_obra.csv", det["mao_de_obra"], list(det["mao_de_obra"][0].keys()) if det["mao_de_obra"] else ["id"])
    escrever_csv(s / "indiretos.csv", det["indiretos"], ["id", "descricao", "categoria", "valor_brl", "fonte"])
    escrever_csv(s / "fluxo_caixa.csv", det["fluxo"], list(det["fluxo"][0].keys()) if det["fluxo"] else ["mes"])
    escrever_csv(s / "cronograma.csv", det["cronograma"], ["id", "nome", "inicio_dia", "fim_dia", "folga_dias", "critica"])
    salvar_json(s / "dre_por_ano.json", det["dre_ano"])
    salvar_json(s / "histograma.json", det["histograma"])
    meta = nos["meta"] or {}
    nome_xlsx = f"orcamento_{meta.get('projeto_id', 'projeto')}_v{meta.get('versao', 1)}.xlsx"
    gerar(s / nome_xlsx, res, det, nos)
    faltando = renderizar(dv, res)
    pend = itens_sem_cotacao(nos)
    linhas = ["# Cotações pendentes", "", f"Projeto: {meta.get('cliente')} – {meta.get('projeto')} (v{meta.get('versao')})", ""]
    if not pend:
        linhas.append("Nenhum item crítico sem cotação válida.")
    for p in pend:
        linhas += [f"## {p['id']} – {p['descricao']}", f"- Fabricante/modelo: {p.get('fabricante') or '[●]'} / {p.get('modelo') or '[●]'}",
                   f"- Quantidade: {p.get('qtd')}", f"- Especificação: {p.get('especificacao') or '[●]'}",
                   f"- Peso na BOM: {p['pct_bom']:.1%} | fonte atual: {p['fonte_atual']} | idade: {p['idade_dias']} dias", ""]
    (s / "cotacoes_pendentes.md").write_text("\n".join(linhas), encoding="utf-8")
    c, pr, f = res["custos"], res["preco"], res["fluxo"]
    print(f"Custo base: {brl(c['base'])} | contingência: {brl(c['contingencia'])} | com contingência: {brl(c['com_contingencia'])}")
    if mc: print(f"Monte Carlo: P50 {brl(mc['custo_p50'])} | P80 {brl(mc['custo_p80'])} | prazo P80 {mc['prazo_p80_dias']:.0f} dias")
    print(f"Preço sugerido: {brl(pr['sugerido'])} | mínimo: {brl(pr['minimo'])} | receita usada ({pr['origem_receita']}): {brl(pr['receita_implantacao'])}")
    print(f"Margem resultante: {pct(pr['margem_resultante'])} | resultado do projeto: {brl(res['dre']['resultado_projeto'])} ({pct(res['dre']['margem_liquida'])})")
    print(f"Exposição máxima de caixa: {brl(f['exposicao_maxima'])} em {f['mes_pico']} | payback: {f['payback']}")
    print(f"Planilha: {s / nome_xlsx}")
    for a in res["alertas"]: print("alerta:", a)
    for k, v in faltando.items():
        if v: print(f"entregável {k}: variáveis sem valor {v}")
    if pend: print(f"{len(pend)} item(ns) com COTAÇÃO HUMANA NECESSÁRIA (ver saidas/cotacoes_pendentes.md)")
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("dv"); ap.add_argument("--forcar", action="store_true")
    a = ap.parse_args(); rodar(a.dv, a.forcar)
