# Squad de orçamento — Acta Robotics

Squad de agentes para Claude Code que dimensiona e orça soluções robóticas: requisitos, arquitetura, cronograma, BOM, tributos, custos, risco (Monte Carlo P50/P80), preço, estrutura contratual, fluxo de caixa, DRE e proposta. Os agentes escrevem premissas com fonte; um motor em Python faz todas as contas e gera a planilha mestre. O squad aprende registrando cotações reais e o realizado dos projetos.

## Como funciona

```
F0 Descoberta   Descoberta + Avaliador de Prontidão: nota de prontidão e
                até 7 perguntas-chave por rodada (máx. 2), com resposta proposta
F0 Requisitos   Requisitos (só depois da especificação liberada)
                ▶ G1 (Marcus): matriz de requisitos e premissas
F1 Solução      Engenharia Robótica → Operações e Pós-venda
F2 Execução     Gestão de Projetos + Suprimentos (3 pontos por item crítico)
                ▶ G2 (Marcus): escopo, BOM, cotações pendentes, capacidade
F3 Custo        Tributário + Cost Engineering + Riscos → motor (Monte Carlo)
F4 Economia     Comercial e Pricing → Contratos + Financeiro (ajustes preço ↔ marcos ↔ caixa)
F5 Proposta     Marketing e Proposta
F6 Controle     Red Team (4 personas) → Auditor de Consistência
                ▶ G3 (Marcus): pacote final → versão congelada → Drive
Fora do fluxo   Data & Calibration (/atualizar-base, /retro)
```

- **27 agentes** em `.claude/agents/`: Descoberta (Sonnet) e Avaliador de Prontidão (Opus), 11 especialistas (Sonnet), 11 supervisores (Opus), Red Team e Auditor (Opus), Data & Calibration (Sonnet).
- **Especificação antes de orçar**: a descoberta mede a prontidão em 10 dimensões (`conhecimento/descoberta/dimensoes.csv`) e só pergunta o que muda solução, custo ou preço. O resto vira premissa declarada, que entra na proposta. As perguntas saem prontas em `saidas/perguntas_marcus.md` (com resposta proposta) e `saidas/perguntas_cliente.md` (mensagem para o cliente).
- **Supervisores** revisam com rubrica, checagens automáticas e foco em otimização; máximo de 2 rodadas.
- **Gatekeeper** (`motor/validar.py`) bloqueia a fase quando falta informação crítica, fonte ou cotação.
- **Estado versionado**: cada nó tem dono e carimbo com as versões das entradas; mudanças marcam só o que ficou desatualizado.
- **Neutralidade tecnológica**: a engenharia escolhe a solução por matriz de alternativas de mercado com critérios e pesos (mínimo de 3 alternativas no modo completo e 2 no rápido). Produto da Acta ou de fornecedor parceiro só entra se vencer a matriz.
- **Modo rápido** (classe 5/4): 5 especialistas, sem supervisores, para triagem de lead. **Modo completo** (classe 3+): squad inteiro, para proposta.

## Instalação

1. Coloque esta pasta dentro do repositório `acta-agentes` (por exemplo `acta-agentes/squad-orcamento/`). Não altere o `SKILL.md` e o `README.md` da raiz do repositório.
2. Python 3.10+ e dependências, a partir da pasta `squad-orcamento`:
   ```
   pip install -r requirements.txt
   ```
3. Teste o motor com o exemplo fictício (funciona no PowerShell, no terminal do Linux ou do Mac):
   ```
   python exemplos/teste_motor_ficticio/testar.py
   ```
   A última linha deve ser `TESTE OK`.
4. Abra o Claude Code **dentro desta pasta** (no PowerShell: `cd C:\Dev\acta-agentes\squad-orcamento` e depois `claude`), para que `.claude/agents`, `.claude/skills` e `.claude/commands` sejam carregados.

## Configuração antes do primeiro orçamento (obrigatória)

| O quê | Onde | Quem |
|---|---|---|
| Pasta do Drive (Acta > Orçamentos), sincronizada no computador | `config/config.json` → `drive_orcamentos_dir` | Marcus |
| Margem alvo, margem mínima, comissão, marcos padrão, custo de capital | `config/config.json` → `politica_comercial` | Marcus + Renato |
| Condição padrão de pagamento a fornecedores (opcional) | `config/config.json` → `pagamento_padrao_bom` | Suprimentos |
| Custo/hora por perfil (com encargos) | `conhecimento/mao_de_obra/custo_hora.csv` | Renato (Budget 2026) |
| Pessoas, horas/mês e alocação atual por perfil | `conhecimento/mao_de_obra/capacidade_time.csv` | Marcus + CTO |
| Parâmetros tributários padrão (modo rápido) | `conhecimento/tributos/parametros_padrao.csv` | Contador |

Sem custo/hora, a fase F2 bloqueia. Sem política comercial, a F4 bloqueia.

## Documentos do briefing

Para anexar documentos do cliente, crie uma subpasta em `entrada\` (por exemplo `entrada\ocean\`), copie os arquivos pelo Explorer e passe a pasta no comando. Também funciona com uma pasta do Google Drive para desktop, entre aspas.

```
/orcar rapido "Cliente" "Projeto" entrada\ocean
/anexar projetos\<id>\v1 "G:\Meu Drive\Acta\Clientes\Ocean\planta_nova.pdf"
```

O importador (`python -m motor.insumos`) copia os originais para `insumos\originais\`, extrai o texto de PDF, Word, Excel, PowerPoint e e-mail (.eml) para `insumos\texto\`, gera imagens das páginas de PDFs digitalizados em `insumos\paginas\` e monta `insumos\indice.md`. Os agentes citam a fonte como arquivo e página. Para um arquivo avulso no meio da conversa, também dá para citar o caminho com `@` no Claude Code, mas o importador é o caminho recomendado: mantém o índice, a citação por página e atualiza o status do orçamento.

## Uso no Claude Code

```
/orcar completo "Nome do Cliente" "Nome do Projeto" <cole o briefing ou indique os arquivos>
/orcar rapido "Nome do Cliente" "Nome do Projeto" <briefing>
/status-orcamento projetos/<id>/v1
/anexar projetos/<id>/v1 <arquivo ou pasta>
/atualizar-base <arquivo da cotação> [projeto_id] [estimativa anterior]
/retro projetos/<id>/v1
```

Cada orçamento fica em `projetos/<AAAA-MM-DD>_<cliente>_<projeto>/v<n>/` e, ao final, é publicado em `Acta > Orçamentos/<projeto_id>/v<n>/` no Drive (uma subpasta por orçamento e por versão). A pasta `projetos/` fica fora do git.

## Entregáveis (em `saidas/`)
- `orcamento_<id>_v<n>.xlsx` — planilha mestre: Resumo, BOM, Mão de obra, Custos, Cronograma, Histograma, Fluxo de caixa, DRE, Marcos, Monte Carlo, Riscos, Premissas (fórmulas nas linhas de custo, fluxo e DRE).
- `relatorio_executivo.md`, `proposta_comercial.md`, `one_pager.md`, `estrutura_contratual.md` — renderizados com os números do motor.
- `cotacoes_pendentes.md` — itens críticos que precisam de cotação real (pedido pronto para enviar).
- `resumo.json`, `monte_carlo.json`, CSVs de BOM, mão de obra, indiretos, fluxo e cronograma.

## Como o squad aprende
0. **Perguntas:** o banco de perguntas registra quais perguntas mudaram de fato a estimativa. Perguntas que nunca mudam nada viram premissa padrão, e a descoberta fica mais enxuta a cada orçamento.
1. **Partida a frio (desde o primeiro orçamento):** cada cotação real registrada com a estimativa anterior mede o erro dos benchmarks. Com 3 ou mais registros, o squad propõe o fator `bom_benchmark`.
2. **Projetos executados:** `/retro` compara a baseline congelada com o realizado, já descontando as mudanças de escopo aprovadas, e propõe fatores por categoria (horas por tipo, BOM, indiretos, prazo).
3. **Salvaguardas:** amostra mínima de 3, peso maior para casos recentes, e nenhum fator entra no cálculo sem aprovação de Marcus (`python -m motor.calibrar aprovar`).
4. **Instruções dos agentes:** críticas recorrentes dos supervisores viram propostas em `conhecimento/propostas_melhoria.md`; mudanças em `.claude/agents/` só por PR aprovado.

## Custos de uso
O modo completo aciona até 27 papéis e é longo: use-o para propostas. Para triagem de leads, use o modo rápido. Os agentes leem só os nós de que precisam, e os supervisores só entram depois que o validador da fase passa.

## Testar cenários sem mexer no orçamento
```
python -m motor.cenario projetos/<id>/v1 cambio-alto
(edite os nós em projetos/_cenarios/cambio-alto/nos/)
python -m motor.rodar projetos/_cenarios/cambio-alto
```

## Manutenção
- Regras gerais: `CLAUDE.md`. Contrato de dados: `estado/README.md` e `estado/schema.json`.
- Para ajustar um agente, edite o arquivo em `.claude/agents/` via PR, com a evidência registrada em `conhecimento/propostas_melhoria.md`.
