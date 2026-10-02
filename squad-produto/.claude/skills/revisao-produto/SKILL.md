---
name: revisao-produto
description: "Registra resultados de experimentos de validação e, depois do lançamento, compara premissas do produto com o realizado. Use quando um experimento terminar, quando um piloto der resultado ou ao fechar o primeiro ano de vendas."
---

# Revisão de produto

1. Identifique a versão do produto (`projetos/<id>/v<n>`).
2. Experimento concluído: acione `calibracao-produto` para registrar o resultado com fonte. Se a hipótese foi refutada, rode `python -m motor.estado status <dv>` e leve a Marcus o que precisa ser revisto.
3. Depois do lançamento (versão congelada): acione `calibracao-produto` para o `realizado.json` e `python -m motor.revisao lancamento`.
4. Apresente a Marcus os desvios (preço, custo unitário, volume, implantação, suporte) e o que muda nos próximos produtos.
5. Feche com lições, banco de perguntas e propostas de melhoria das instruções (via PR).
