"""Gera revisoes/orquestrador_tabela_criterios.md a partir das chaves de classificação já registradas (nada é recalculado).
Uso: python revisoes/gerar_tabela_criterios.py  (a partir da pasta da versão)"""
import json
from pathlib import Path
dv = Path(__file__).resolve().parent.parent
def v(aid, k):
    d = json.load(open(dv / 'saidas' / 'analises' / aid / 'resultado.json'))['valores'].get(k)
    return None if d is None else d['valor']
def cls(x, rotulos=('falha', 'inconclusivo', 'passa')):
    if x is None: return '[●] chave ausente'
    return {-1: rotulos[0], 0: rotulos[1], 1: rotulos[2]}.get(int(round(x)), str(x))
def sim(x): return '[●]' if x is None else ('sim' if int(x) == 1 else 'não')
def n(x, u=''): return '[●]' if x is None else (f"{x:,.0f}".replace(',', '.') + (f' {u}' if u else ''))
L = ["# Tabela por critério: leitura registrada no plano × desvios declarados", "",
     "Gerada pelo orquestrador a partir das chaves de classificação já registradas (script `revisoes/gerar_tabela_criterios.py`). Nada foi recalculado. Pedido do sup-metodologia D3 r1.", "",
     "| Critério | Leitura registrada no plano | Resultado | Desvio ou variante | Resultado | Motivo do desvio | Quem decide |", "|---|---|---|---|---|---|---|"]
L.append(f"| CR2 franquia, ALT3 | janela 31/08–25/09 (plano) | {cls(v('ANA-002','classe_cr2_alt3'))} | janela normal 24/08–18/09 | {cls(v('ANA-002','classe_cr2_alt3_normal'))} | incidente real na RC em 21–25/09 (Marcus) | Marcus (G3) |")
L.append(f"| CR2 franquia, ALT2 | janela do plano | {cls(v('ANA-002','classe_cr2_alt2'))} | janela normal | {cls(v('ANA-002','classe_cr2_alt2_normal'))} | idem | Marcus (G3) |")
L.append(f"| CR3 linha de base ≤ PR06 | teto 300 s (conservador do G2) | {cls(v('ANA-004','classe_cr3_t300'))} | tetos 600/900/1.800 s; S2 (truncar pausas) 300/900/1.800 s | {cls(v('ANA-004','classe_cr3_t600'))} / {cls(v('ANA-004','classe_cr3_t900'))} / {cls(v('ANA-004','classe_cr3_t1800'))}; S2: {cls(v('ANA-004','classe_cr3_s2_t300'))} / {cls(v('ANA-004','classe_cr3_s2_t900'))} / {cls(v('ANA-004','classe_cr3_s2_t1800'))} | variantes pré-registradas (sensibilidade) | — (leitura registrada vale) |")
L.append(f"| CR4 frota no p90, ALT3 | frota dia a dia, período inteiro | {n(v('ANA-009','frota_necessaria_alt3'),'robôs')} | pós-colmeia (base); banda (otimista) | {n(v('ANA-009','frota_necessaria_alt3_pos_colmeia'),'robôs')}; {n(v('ANA-009','frota_necessaria_alt3_banda_pos_colmeia'),'robôs')} | colmeia mudou o mix (decisão do orquestrador) | Marcus (G3) |")
L.append(f"| CR5 outros depositantes | linhas compatíveis (plano) | {cls(v('ANA-010','classe_cr5_linhas'))} | após robustez por mês; todo o pedido-a-pedido | {cls(v('ANA-010','classe_cr5_linhas_apos_robustez'))}; {cls(v('ANA-010','classe_cr5_linhas_todo_pap'))} | robustez do plano; sensibilidade de definição de 'compatível' | Marcus (G3) |")
L.append(f"| CR7 colmeia (passa = exclusão se sustenta) | teto 900 s, passa só se S2 e 1.800 s passarem | {cls(v('ANA-007','classe_cr7_primaria'))} | S2; 1.800 s; janela normal | {cls(v('ANA-007','classe_cr7_s2'))}; {cls(v('ANA-007','classe_cr7_t1800'))}; {cls(v('ANA-007','classe_cr7_primaria_normal'))} | — | — (inconclusivo mantém a colmeia candidata) |")
L.append(f"| CR8 reforço no p90 | M23 autônoma (plano) | passa: {sim(v('ANA-009','cr8_passa_no_dia_p90'))} | M23 colaborativa; pós-colmeia | colaborativa: {sim(v('ANA-009','cr8_passa_no_dia_p90_colab'))}; pós-colmeia autônoma: {sim(v('ANA-009','cr8_passa_no_dia_p90_pos_colmeia'))}; pós-colmeia colaborativa: {sim(v('ANA-009','cr8_passa_no_dia_p90_colab_pos_colmeia'))} | Kappabot é colaborativo (red team) | Marcus (G3) |")
L.append(f"| H06 devolutiva manual do robô | DiD por operador-semana | confirmada: {sim(v('ANA-005','h06_confirmada'))} | — | — | — | — |")
L.append(f"| H13 jornada maior no pico | H13a e H13b | H13: {sim(v('ANA-003','h13_confirmada'))} (a: {sim(v('ANA-003','h13a_confirmada'))}; b: {sim(v('ANA-003','h13b_confirmada'))}) | — | — | — | — |")
L.append(f"| H-P3 checkout (slide 10) | equivalência ±10% | {cls(v('ANA-006','classe_h_p3_checkout_rc'), ('não reproduz','inconclusivo','reproduz'))} | — | — | — | — |")
L.append(f"| H01 fila de segunda-feira | diferença da primeira hora | {cls(v('ANA-008','classe_h01'))} | — | — | — | — |")
L.append(f"| H-P4c previsão | média de 4 semanas vence a história | confirmada: {sim(v('ANA-014','h_p4c_confirmada'))} | — | — | — | — |")
for p in ['d1', 'd3', 'd4']:
    L.append(f"| Pista PT-{p.upper()} (F2) | regra do plano sem critério de inversão fixado | ver ao lado | (a) IC oposto adotado; (b) só sinal; (c) leave-one-out | (a) {sim(v('ANA-016',f'pt_{p}_confirmada'))} · demais em `ANA-016/leituras_criterio_inversao.csv` | plano não fixava o critério; (a) fixado depois dos sinais | Marcus (G3) |")
for p in ['h04', 'h09', 'h10']:
    L.append(f"| Pista PT-{p.upper()} (F2) | regra do plano | confirmada: {sim(v('ANA-016',f'pt_{p}_confirmada'))} | — | — | — | — |")
imp = dv / 'saidas' / 'impacto.json'
if imp.exists():
    m = json.load(open(imp)).get('modelos', {})
    L += ["", "## Modelos de impacto (CR1, CR6 e demais)", "", "| Modelo | Descrição | Provável | P10 | P90 | Unidade |", "|---|---|---|---|---|---|"]
    for k, x in m.items():
        L.append(f"| {k} | {x.get('descricao')} | {x['provavel']:,.2f} | {x['p10']:,.2f} | {x['p90']:,.2f} | {x.get('unidade')} |")
(dv / 'revisoes' / 'orquestrador_tabela_criterios.md').write_text("\n".join(L) + "\n", encoding='utf-8')
print("\n".join(L))
