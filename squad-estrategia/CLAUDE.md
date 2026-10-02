# Squad de planejamento estratégico — Acta Robotics

Squad de agentes que conduz o planejamento estratégico da Acta Robotics do macro para o detalhe, com portões de decisão do CEO. A orquestração está na skill `estrategia` (sessão principal = Chief Strategist). Agentes em `.claude/agents/`, cálculos em `motor/`, memória em `conhecimento/`.

## Regras invioláveis
1. **Nunca invente dados.** Nenhum número de mercado, rodada, concorrente, preço, pessoa ou fato interno sem fonte. Sem fonte: `[●]` no texto, `null` no número e uma pergunta com resposta proposta.
2. **Evidência classificada.** Toda afirmação externa é evidência com fonte, data, link e tipo: `confirmado`, `reportado`, `estimativa` ou `interno` (`conhecimento/fontes/regras_fontes.md`). Reportado nunca vira fato no texto.
3. **Do macro para o detalhe.** Enquadramento, diagnóstico, escolhas, desdobramento e consolidação, com portões de Marcus entre as fases. Nada de iniciativas antes da escolha.
4. **Escolha de verdade.** Pelo menos duas opções reais, critérios com pesos definidos antes das notas, hipóteses testáveis com critério de falha, e uma lista explícita do que a Acta não fará. Não defenda o status quo nem o portfólio atual por padrão.
5. **O motor faz as contas.** Projeções, caixa, DRE, notas ponderadas, prioridades e capacidade saem de `python -m motor.rodar <dv>`. Entregáveis citam números só por variáveis (`{{fmt.base_receita_a1}}`).
6. **Cada nó tem um dono** e é carimbado ao terminar (`python -m motor.estado carimbar <dv> <no> --agente <nome>`). Mudança numa entrada marca os dependentes como desatualizados.
7. **Perguntas-chave apenas.** Enquadramento com no máximo 7 perguntas por rodada e 2 rodadas, sempre com resposta proposta; lacuna de impacto baixo vira premissa declarada.
8. **Comece pelo que existe.** Trabalho anterior importado em `insumos/` é ponto de partida; pesquise só as lacunas.
9. **Confidencialidade.** O plano é interno. Nada sai para conselho, investidores ou parceiros a não ser por Marcus.
10. **Português do Brasil**, frases curtas, conclusão primeiro.

## Disciplina de nomes
- Plataforma de frotas: **9fleet** (K.FLEET só interno). Operações robotizadas: **Roboteazy** (K.CONCEPT nunca externo).
- Nunca citar o fornecedor de software de reconhecimento facial.
- Venturus e SiDi não são parceiros. Parceiro tecnológico de hardware: HBR.

## Estrutura de um ciclo
`projetos/<AAAA-MM-DD>_<ciclo>_<titulo>/v<n>/`: `nos/` (premissas e análises), `insumos/` (documentos importados), `revisoes/`, `entregaveis/` (textos com variáveis), `saidas/` (planilha mestre, resumo, entregáveis renderizados), `revisoes_trimestrais/`.
Contrato de dados: `estado/README.md`.

## Comandos úteis
```
python -m motor.estado status <dv>
python -m motor.prontidao <dv>
python -m motor.validar <dv> --fase E2
python -m motor.rodar <dv>
python -m motor.revisao trimestre <dv> --trimestre T1 --realizado <arquivo>
```
