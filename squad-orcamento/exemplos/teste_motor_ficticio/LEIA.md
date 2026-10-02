# Exemplo fictício para testar o motor

**Todos os valores desta pasta são fictícios.** Servem apenas para verificar que o motor, o Monte Carlo, a planilha, a prontidão e o gatekeeper funcionam na sua máquina. Não usar como referência de preço, horas ou impostos. O teste usa a base de conhecimento desta pasta, não a base real.

Teste (Windows, Linux ou Mac), a partir da pasta `squad-orcamento`:
```
python exemplos/teste_motor_ficticio/testar.py
```

Resultado esperado: o motor gera `v1/saidas/` (planilha, resumo, entregáveis), a prontidão fica em 83% e o validador bloqueia apenas o item B02 (benchmark num item crítico no modo completo). A última linha mostra `TESTE OK`.
