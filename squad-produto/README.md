# Squad de produto — Acta Robotics

Squad de agentes para Claude Code que especifica produtos e soluções a partir de premissas de mercado: do problema do cliente (JTBD, dores, evidências) à oportunidade, conceitos, requisitos com critérios de aceite, arquitetura com decisões fazer, comprar ou parceria, caso de negócio de 3 anos, ROI do cliente, plano de validação, roteiro e lançamento.

## Como funciona

```
P0 Enquadramento   enquadramento + avaliador de prontidão (até 7 perguntas por rodada, máx. 2)
                   ▶ G1: problema, cliente-alvo, restrições
P1 Descoberta      mercado, cliente (JTBD, dores, personas), concorrência, normas → oportunidade
                   ▶ G2: seguir, pivotar ou parar
P2 Definição       conceitos (construir, integrar, revender, parceria) → requisitos MoSCoW rastreáveis
                   ▶ G3: conceito e escopo
P3 Especificação   arquitetura (2+ alternativas por componente) → caso de negócio e ROI do cliente
                   → hipóteses e experimentos → MVP, releases e lançamento
                   ▶ G4: especificação
P4 Consolidação    especificação, PRD, one-pager → red team (5 personas) → auditor
                   ▶ G5: aprovação → baseline → Drive → pacote para o squad de orçamento
Validação          /revisao-produto: resultados de experimentos e premissas x realizado
```

- **27 agentes:** 12 especialistas (estrategista de produto em Opus), 11 supervisores, avaliador, red team e auditor (Opus), calibração.
- **Dois modos:** `completo` (especificação) e `oportunidade` (avaliação rápida com memorando).
- **Benchmark técnico:** o agente de benchmark pesquisa na internet as soluções existentes, monta a matriz de especificações normalizadas com link da ficha técnica, preços com tipo e fonte e suporte no Brasil. Os requisitos são comparados com o melhor do mercado e com a mediana (aba Benchmark da planilha).
- **Motor:** notas ponderadas, benchmark (melhor do mercado, mediana, quem atende cada requisito), cobertura de requisitos, custo unitário em faixa, caso de negócio de 3 anos com mix de venda e locação, VPL, payback e sensibilidade, ROI do cliente, prioridade de hipóteses e capacidade do roteiro.

## Instalação
1. Pasta em `C:\Dev\acta-agentes\squad-produto\`, ao lado dos outros squads.
2. `pip install -r requirements.txt`
3. `python exemplos\teste_motor_ficticio\testar.py` (última linha `TESTE OK`).
4. `cd C:\Dev\acta-agentes\squad-produto` e `claude`.

## Uso
```
/produto completo "Hospitais" "Robô de entrega hospitalar" entrada\hospital
/produto oportunidade "Condomínios" "Robô de entrega em condomínios" entrada\condominios
/status-produto projetos\<id>\v1
/anexar projetos\<id>\v1 <arquivo ou pasta>
/revisao-produto projetos\<id>\v1 experimento
```
Coloque em `entrada\<produto>\` o que existir: pedidos e e-mails de clientes, RFPs, entrevistas, propostas e resultados do squad de estratégia.

## Entregáveis (em `saidas\`)
- `produto_<id>_v<n>.xlsx`: Resumo, Benchmark, Conceitos, Requisitos, Arquitetura, Caso de negócio com sensibilidade, Hipóteses, Roadmap e capacidade.
- `especificacao_produto.md`, `prd.md`, `one_pager.md`; no modo oportunidade, `memo_oportunidade.md`.
- `handoff_orcamento\` (briefing, requisitos e componentes) para o `/orcar`.

## Configuração
| O quê | Onde |
|---|---|
| Pasta do Drive (ex.: Acta > Produtos) | `config\config.json` → `drive_produto_dir` |
| Capacidade do time (mesma do squad de orçamento) | `capacidade_time_csv` |
| Entrada do squad de orçamento | `orcamento_entrada_dir` |
| Contexto da empresa | `conhecimento\contexto\acta.md` (o mesmo do squad de estratégia; revise) |

## Como aprende
- Resultados de experimentos ficam em `conhecimento\historico\hipoteses.csv`: com o tempo, mostra que tipo de hipótese costuma cair.
- Depois do lançamento, premissas x realizado (preço, custo unitário, volume, implantação, suporte) entram em `previsto_vs_realizado.csv` e informam os próximos casos de negócio.
- Banco de perguntas, lições e propostas de melhoria das instruções, como nos outros squads.
