"""Motor de cálculo do squad de orçamento da Acta Robotics.

Os agentes escrevem premissas estruturadas nos arquivos de nós (projetos/<id>/v<n>/nos/*.json).
Todo número derivado (custos, cronograma, Monte Carlo, preço, fluxo de caixa, DRE, planilha)
é calculado aqui, de forma determinística. Agentes nunca fazem essas contas em texto.
"""
