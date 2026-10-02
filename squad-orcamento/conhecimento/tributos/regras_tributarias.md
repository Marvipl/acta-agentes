# Regras tributárias do squad

Este arquivo guarda **regras e contexto**. Alíquotas só entram em `aliquotas.csv`, sempre com fonte oficial e data.

## Contexto da Acta (a confirmar com o contador a cada orçamento)
- A Acta é optante do Simples Nacional, com saída do regime em planejamento.
- Matriz em Manaus/AM (CNPJ 36.091.111/0001-06) e filial em Campinas/SP (CNPJ 36.091.111/0002-89). O estabelecimento emissor muda ICMS/DIFAL e ISS.
- Contratos de valor alto podem ultrapassar o teto do Simples: o Tributário deve sinalizar o regime em que o contrato será faturado.
- Não assumir incentivos da Zona Franca de Manaus sem confirmação expressa: a Acta não tem estrutura para usufruir deles hoje.
- A partir de 2027, a transição da reforma tributária (EC 132/2023 e LC 214/2025) altera PIS/Cofins (CBS) e, depois, ICMS/ISS (IBS). Contratos longos precisam de cláusula de reequilíbrio tributário.

## Método obrigatório
1. Para cada item importado: identificar NCM, consultar TEC/TIPI vigentes e verificar Ex-tarifário. Registrar fonte e data.
2. Calcular `custo_importacao_pct` sobre o valor FOB convertido: II, IPI, PIS/Cofins-importação, ICMS, frete internacional, seguro, despachante, armazenagem e taxas portuárias. Mostrar a memória de cálculo.
3. Calcular `impostos_receita_pct` por tipo de receita (produto, serviço, locação) no regime em que o contrato será faturado. No Lucro Presumido, incluir IRPJ/CSLL sobre a base presumida.
4. Sinalizar DIFAL em vendas interestaduais e o município do ISS.
5. Quando faltar informação, usar `[●]` e registrar a pergunta para o contador. Nunca estimar alíquota de memória.
