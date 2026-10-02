# Squad de planejamento estratégico — Acta Robotics

Squad de agentes para Claude Code que conduz o planejamento estratégico do macro para o detalhe: enquadramento, diagnóstico com evidências classificadas, opções e escolha, OKRs, iniciativas, organização, cenários financeiros e de caixa, riscos, governança e narrativa. Os agentes escrevem análises com fonte; um motor em Python faz as contas e gera a planilha mestre. O plano aprende com as revisões trimestrais.

## Como funciona

```
E0 Enquadramento   enquadramento + avaliador de prontidão (até 7 perguntas por rodada, máx. 2)
                   ▶ G1 (Marcus): ambição, restrições, decisões já tomadas
E1 Diagnóstico     mercado, concorrência, regulatório e fomento, desempenho interno, capacidades
                   → SWOT com evidências, TOWS e 3 a 5 questões críticas
                   ▶ G2 (Marcus): diagnóstico
E2 Escolhas        arquiteto de estratégia (2 a 4 opções, hipóteses testáveis) + modelo financeiro por opção + portfólio
                   ▶ G3 (Marcus): opção, apostas e o que não fazer
E3 Desdobramento   OKRs → organização → iniciativas (capacidade) → cenários financeiros → riscos e governança
                   ▶ G4 (Marcus): plano detalhado
E4 Consolidação    narrativa → red team (5 personas) → auditor
                   ▶ G5 (Marcus): aprovação → baseline congelada → Drive
Execução           /revisao-trimestral: KRs, receita, caixa, hipóteses e gatilhos
```

- **27 agentes:** 12 especialistas (Sonnet; o arquiteto de estratégia em Opus), 11 supervisores, avaliador de prontidão, red team e auditor (Opus), calibração (Sonnet).
- **Dois modos:** `plano` (ciclo anual, cinco portões, supervisores) e `estudo` (uma decisão estratégica, três portões, red team e auditor, entrega um memorando).
- **Evidências classificadas:** confirmado, reportado, estimativa ou interno. Reportado nunca vira fato.
- **Motor:** projeção mensal plurianual por cenário e por opção (DRE, caixa, necessidade de captação, ano de EBITDA positivo), notas ponderadas de portfólio, prioridade de iniciativas e capacidade do time em FTE.

## Instalação
1. Coloque a pasta em `C:\Dev\acta-agentes\squad-estrategia\`, ao lado do `squad-orcamento`.
2. `pip install -r requirements.txt`
3. Teste: `python exemplos\teste_motor_ficticio\testar.py` (última linha `TESTE OK`).
4. Abra o Claude Code dentro da pasta: `cd C:\Dev\acta-agentes\squad-estrategia` e `claude`.

## Configuração
| O quê | Onde |
|---|---|
| Pasta do Drive para publicar (ex.: Acta > Planejamento Estratégico) | `config\config.json` → `drive_planejamento_dir` |
| Capacidade do time (por padrão, a mesma do squad de orçamento) | `config\config.json` → `capacidade_time_csv` |
| Contexto da empresa e trabalho em andamento | `conhecimento\contexto\acta.md` (revise antes do primeiro ciclo) |

## Uso
```
/estrategia plano "2027" "Plano estratégico 2027" entrada\plano-2027
/estrategia estudo "2027" "Entrada em humanoides" entrada\humanoides "Devemos criar uma linha de humanoides para pesquisa e eventos?"
/status-estrategia projetos\<id>\v1
/anexar projetos\<id>\v1 <arquivo ou pasta>
/revisao-trimestral projetos\<id>\v1 T1
```
Coloque em `entrada\<ciclo>\` o que já existe: trabalho anterior do plano, budget, DRE, pipeline e exportações da pasta Acta > Briefings. Documentos do Google Docs sincronizados pelo Drive para desktop são atalhos `.gdoc` sem conteúdo: exporte como .docx ou .pdf.

## Entregáveis (em `saidas\`)
- `plano_<id>_v<n>.xlsx`: Resumo, DRE por cenário, DRE por opção, Caixa mensal, Portfólio, Iniciativas e capacidade, OKRs, Riscos, Hipóteses.
- `plano_estrategico.md` (10 seções), `one_page.md`, `roteiro_deck.md` (brief para Claude Design ou pptx), `narrativa_investidor.md`; no modo estudo, `memo_estudo.md`.

## Como o plano aprende
- A revisão trimestral compara o realizado com a baseline congelada e registra previsto x realizado em `conhecimento\historico\`. Vieses que se repetem (por exemplo, receita de uma linha sempre abaixo do previsto) aparecem em `python -m motor.revisao historico` e entram no próximo ciclo.
- Hipóteses refutadas e gatilhos disparados viram recomendação objetiva: ajustar iniciativa, ajustar meta ou abrir nova versão do plano.
- Lições, banco de perguntas e contexto da empresa são atualizados pela calibração; mudanças nas instruções dos agentes só por PR.

## Integração com outros squads e skills
- Orçamento detalhado de uma iniciativa: squad de orçamento (`/orcar`).
- Deck de captação: skill `investor-pitch-builder`. Editais: skill `grant-project-builder`.
