"""Teste do motor com dados FICTÍCIOS (Windows, Linux ou Mac). Não altera a base real.

Uso, a partir da pasta squad-orcamento:
    python exemplos/teste_motor_ficticio/testar.py
"""
import os, shutil, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
EX = RAIZ / "exemplos" / "teste_motor_ficticio"
os.environ["SQUAD_CONHECIMENTO"] = str(EX / "conhecimento")  # só vale para este processo
sys.path.insert(0, str(RAIZ))

from motor.util import NOS, carregar_json          # noqa: E402
from motor import estado, rodar, prontidao, validar  # noqa: E402

dv = EX / "v1"
for sub in ["saidas", "revisoes"]:
    shutil.rmtree(dv / sub, ignore_errors=True)
    (dv / sub).mkdir()
for f in ["controle.json", "estado.json"]:
    (dv / f).unlink(missing_ok=True)

for no in NOS:
    estado.carimbar(dv, no, "teste")
estado.aprovar(dv, "G1", "teste")
estado.aprovar(dv, "G2", "teste")

print("\n=== Motor ===")
rodar.rodar(dv)

print("\n=== Prontidão da especificação ===")
esp = carregar_json(dv / "nos" / "especificacao.json")
r = prontidao.avaliar(esp, "completo")
print(f"Prontidão: {r['nota']:.0%} (mínimo {r['limiar']:.0%}) -> {'PRONTO' if r['liberado'] else 'AINDA NÃO'}")

print("\n=== Validação até F4 (bloqueio do item B02 é o esperado) ===")
v = validar.validar(dv, "F4")
for m in v.bloq:
    print("BLOQUEIO:", m)
print("RESULTADO:", "BLOQUEADO" if v.bloq else "LIBERADO")

ok = r["liberado"] and len(v.bloq) == 1 and "B02" in v.bloq[0]
print("\nTESTE", "OK" if ok else "COM DIFERENÇAS (veja as mensagens acima)")
print(f"Planilha gerada em: {dv / 'saidas'}")
