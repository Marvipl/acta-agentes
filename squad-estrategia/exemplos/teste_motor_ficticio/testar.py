"""Teste do motor do squad de estratégia com dados FICTÍCIOS (Windows, Linux ou Mac). Não altera a base real.

Uso, a partir da pasta squad-estrategia:  python exemplos/teste_motor_ficticio/testar.py
"""
import os, shutil, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
EX = RAIZ / "exemplos" / "teste_motor_ficticio"
os.environ["SQUAD_CONHECIMENTO"] = str(EX / "conhecimento")
sys.path.insert(0, str(RAIZ))

from motor.util import NOS, carregar_json        # noqa: E402
from motor import estado, rodar, prontidao, validar  # noqa: E402

dv = EX / "v1"
for sub in ["saidas", "revisoes"]:
    shutil.rmtree(dv / sub, ignore_errors=True); (dv / sub).mkdir()
for f in ["controle.json", "estado.json"]:
    (dv / f).unlink(missing_ok=True)
for no in NOS:
    estado.carimbar(dv, no, "teste")
for g in ["G1", "G2", "G3"]:
    estado.aprovar(dv, g, "teste")

print("\n=== Motor ===")
rodar.rodar(dv)
print("\n=== Prontidão do enquadramento ===")
r = prontidao.avaliar(carregar_json(dv / "nos" / "enquadramento.json"), "completo")
print(f"Prontidão: {r['nota']:.0%} -> {'PRONTO' if r['liberado'] else 'AINDA NÃO'}")
print("\n=== Validação até E3 ===")
v = validar.validar(dv, "E3")
for m in v.bloq: print("BLOQUEIO:", m)
for m in v.aviso: print("aviso:", m)
print("RESULTADO:", "BLOQUEADO" if v.bloq else "LIBERADO")
ok = r["liberado"] and not v.bloq
print("\nTESTE", "OK" if ok else "COM DIFERENÇAS (veja as mensagens acima)")
print(f"Planilha gerada em: {dv / 'saidas'}")
