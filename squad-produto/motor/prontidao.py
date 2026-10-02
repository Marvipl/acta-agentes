"""Prontidão da especificação: mede se há informação suficiente para orçar e controla as perguntas-chave.

Regras:
  - Nota = média ponderada do status de cada dimensão (pesos em conhecimento/descoberta/dimensoes.csv).
  - Modo rápido: nota >= limiar e nenhuma dimensão crítica 'ausente'.
  - Modo completo: nota >= limiar e toda dimensão crítica 'completo' ou 'premissa' aceita por Marcus.
  - Perguntas: só impacto alto ou médio (impacto baixo vira premissa), no máximo N abertas por rodada,
    no máximo R rodadas; cada pergunta com motivo, resposta proposta e destinatário.

Uso: python -m motor.prontidao <dir_versao>   (gera saidas/perguntas_marcus.md e saidas/perguntas_terceiros.md: clientes, parceiros, especialistas)
"""
import argparse, sys
from pathlib import Path
from .util import CONHEC, carregar_json, ler_csv, config

STATUS_OK = {"completo", "premissa", "parcial", "ausente", "nao_se_aplica"}


def dimensoes_ref():
    out = {}
    for l in ler_csv(CONHEC / "enquadramento" / "dimensoes.csv"):
        out[l["id"]] = {"nome": l["nome"], "critica": l["critica"].strip().lower() == "sim", "peso": float(l["peso"])}
    return out


def avaliar(esp, modo):
    cfg = config().get("descoberta") or {}
    val = cfg.get("valor_status") or {"completo": 1.0, "premissa": 0.7, "parcial": 0.5, "ausente": 0.0}
    lim = (cfg.get("prontidao_minima") or {}).get(modo, 0.8)
    max_p, max_r = int(cfg.get("max_perguntas_por_rodada", 7)), int(cfg.get("max_rodadas", 2))
    ref = dimensoes_ref()
    bloq, aviso = [], []
    dims = {d.get("id"): d for d in (esp or {}).get("dimensoes", []) or []}
    for did in ref:
        if did not in dims:
            bloq.append(f"dimensão {did} ({ref[did]['nome']}) não avaliada")
    soma = peso = 0.0
    criticas_ruins = []
    for did, d in dims.items():
        if did not in ref:
            aviso.append(f"dimensão {did} não existe em dimensoes.csv"); continue
        st = d.get("status")
        if st not in STATUS_OK:
            bloq.append(f"dimensão {did}: status inválido '{st}'"); continue
        if st == "premissa" and not d.get("premissa_adotada"):
            bloq.append(f"dimensão {did}: status premissa sem premissa_adotada")
        if st == "nao_se_aplica":
            if ref[did]["critica"]:
                aviso.append(f"dimensão crítica {did} marcada como não se aplica: justificar em evidencias")
            continue
        soma += ref[did]["peso"] * float(val.get(st, 0)); peso += ref[did]["peso"]
        if ref[did]["critica"]:
            if modo == "completo":
                ok = st == "completo" or (st == "premissa" and d.get("premissa_aceita_por"))
            else:
                ok = st != "ausente"
            if not ok:
                criticas_ruins.append(f"{did} ({ref[did]['nome']}): {st}")
    nota = soma / peso if peso else 0.0
    if nota < lim:
        bloq.append(f"prontidão {nota:.0%} abaixo do mínimo de {lim:.0%} para o modo {modo}")
    for c in criticas_ruins:
        bloq.append(f"dimensão crítica insuficiente para o modo {modo}: {c}")

    pergs = (esp or {}).get("perguntas", []) or []
    rodada = int((esp or {}).get("rodada_atual", 1) or 1)
    if rodada > max_r:
        bloq.append(f"rodada {rodada} acima do máximo de {max_r}: converta as lacunas restantes em premissas para Marcus aceitar")
    abertas = [p for p in pergs if p.get("status") == "aberta"]
    if len([p for p in abertas if int(p.get("rodada", 1)) == rodada]) > max_p:
        bloq.append(f"mais de {max_p} perguntas abertas na rodada {rodada}: mantenha só as perguntas-chave")
    for p in abertas:
        pid = p.get("id", "?")
        if p.get("impacto") not in ("alto", "medio"):
            bloq.append(f"pergunta {pid}: impacto '{p.get('impacto')}' não justifica pergunta; converta em premissa")
        for k in ["dimensao", "pergunta", "por_que_importa", "resposta_proposta", "destinatario"]:
            if not p.get(k):
                bloq.append(f"pergunta {pid}: campo {k} vazio")
        if p.get("destinatario") not in ("marcus", "terceiros"):
            bloq.append(f"pergunta {pid}: destinatário deve ser marcus ou terceiros")
    return {"nota": nota, "limiar": lim, "bloqueios": bloq, "avisos": aviso, "abertas": abertas,
            "liberado": not bloq and not abertas}


def renderizar_perguntas(dv, esp, res):
    dv = Path(dv); (dv / "saidas").mkdir(parents=True, exist_ok=True)
    ref = dimensoes_ref()
    meta = carregar_json(dv / "nos" / "meta.json", {})
    ordem = {"alto": 0, "medio": 1}
    abertas = sorted([p for p in res["abertas"] if p.get("impacto") in ("alto", "medio")],
                     key=lambda p: (ordem.get(p.get("impacto"), 2), p.get("id", "")))
    m = [f"# Perguntas para Marcus — {meta.get('produto')} · {meta.get('segmento')}", "",
         f"Prontidão atual: {res['nota']:.0%} (mínimo para {meta.get('modo')}: {res['limiar']:.0%}).",
         "Responda confirmando ou corrigindo a resposta proposta. Perguntas sem resposta viram premissa declarada na proposta.", ""]
    for i, p in enumerate([p for p in abertas if p.get("destinatario") == "marcus"], 1):
        m += [f"**{i}. {p.get('pergunta')}** ({ref.get(p.get('dimensao'), {}).get('nome', p.get('dimensao'))} · impacto {p.get('impacto')})",
              f"- Por que importa: {p.get('por_que_importa')}",
              f"- Resposta proposta: {p.get('resposta_proposta')}"]
        if p.get("opcoes"):
            m.append(f"- Opções: {' | '.join(p['opcoes'])}")
        m.append("")
    (dv / "saidas" / "perguntas_marcus.md").write_text("\n".join(m), encoding="utf-8")
    c = [f"Para especificarmos a solução, precisamos das seguintes informações:", ""]
    cli = [p for p in abertas if p.get("destinatario") == "terceiros"]
    for i, p in enumerate(cli, 1):
        linha = f"{i}. {p.get('pergunta')}"
        if p.get("opcoes"):
            linha += f" ({' / '.join(p['opcoes'])})"
        c.append(linha)
    c += ["", "Onde não houver resposta, adotaremos premissas que ficarão registradas na especificação."]
    (dv / "saidas" / "perguntas_terceiros.md").write_text("\n".join(c) if cli else "Nenhuma pergunta pendente a terceiros.\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("dv"); x = ap.parse_args()
    dv = Path(x.dv)
    esp = carregar_json(dv / "nos" / "enquadramento.json", {})
    modo = (carregar_json(dv / "nos" / "meta.json", {}) or {}).get("modo", "completo")
    if not esp or esp.get("_template"):
        sys.exit("enquadramento ainda não preenchido")
    res = avaliar(esp, modo)
    renderizar_perguntas(dv, esp, res)
    print(f"Prontidão: {res['nota']:.0%} (mínimo {res['limiar']:.0%}, modo {modo}) | perguntas abertas: {len(res['abertas'])}")
    for b in res["bloqueios"]: print("BLOQUEIO:", b)
    for a in res["avisos"]: print("aviso:", a)
    print("RESULTADO:", "PRONTO PARA A DESCOBERTA" if res["liberado"] else "AINDA NÃO")
    sys.exit(0 if res["liberado"] else 1)


if __name__ == "__main__":
    main()
