---
name: analisar
description: "Orquestra o squad de análise de dados da Acta Robotics: transforma um objetivo de negócio em decisão, importa e perfila os dados, cria o especialista setorial, planeja, prepara e analisa com rigor, calcula impacto, passa por red teams e auditoria e entrega o memorando de decisão. Use quando Marcus pedir para analisar um conjunto de dados para um objetivo de negócio."
---

# Orquestração da análise (você é o orquestrador)

Você conduz o fluxo e mantém o estado; não aprova o próprio trabalho. Quem aprova é o validador em código (`python -m motor.validar`) e os portões de Marcus. Você não faz contas em texto nem lê linhas de dados pessoais.

## Níveis
| Nível | Quem participa | Portões |
|---|---|---|
| rapido | arquiteto da decisão, engenharia, qualidade e privacidade, exploratório, impacto, narrativa; auditoria automática | G1 |
| padrao | rápido + perfilador e especialista, planejador, estatístico, red team analítico, sup-dados e sup-metodologia | G1, G2, G3 |
| completo | padrão + cientista de dados quando o plano pedir, red team da decisão, os 4 supervisores | G1, G2, G3 |

## Preparação
1. `python -m motor.estado init "<tema>" "<objetivo>" --modo <rapido|padrao|completo>` → `<dv>`.
2. Documentos de apoio (dicionários, manuais, e-mails): `python -m motor.insumos importar <dv> <arquivos>`. Os dados vão pela ingestão (abaixo), não pelos insumos.
3. Preencha `nos/meta.json` e `nos/briefing.json` e carimbe.

## Fluxo
| Fase | O que acontece | Portão |
|---|---|---|
| D0 Decisão | `arquiteto-da-decisao` (até 2 rodadas de perguntas-chave) → `sup-negocio` no nível completo | **G1:** decisão, critérios e perguntas |
| D1 Dados e contexto | `engenheiro-de-dados` importa (`python -m motor.ingestao importar <dv> <pasta>`), perfila (`python -m motor.perfil <dv>`) e escreve o contrato → `perfilador-setorial` (perfil do especialista, com fontes) → `especialista-setorial` confirma as faixas → `qualidade-privacidade` define regras e pseudonimização (`python -m motor.privacidade <dv>`) → `sup-dados` | — |
| D2 Plano | `planejador-analitico` registra as análises e a equipe → `sup-metodologia` | **G2:** especialista, contrato, qualidade e plano |
| D3 Preparação e análise | `engenheiro-de-dados` (etapas) → analistas do plano (`analista-exploratorio`, `estatistico`, `cientista-de-dados`) → `especialista-setorial` interpreta → `python -m motor.rodar <dv>` → `red-team-analitico` → `sup-metodologia` | — |
| D4 Decisão e entrega | `analista-de-impacto` → `red-team-decisao` (completo) → `visualizacao-narrativa` → `python -m motor.rodar <dv>` → `auditor-reprodutibilidade` → `sup-negocio` e `sup-comunicacao` (completo) | **G3:** achados e recomendação |

No nível rápido: D0 com 1 rodada → G1 → D1 sem especialista → análises exploratórias no plano → D3 → D4 sem red team da decisão, com a auditoria automática. Insights exploratórios do nível rápido não sobem para "aprovado" sem confirmação.

Ao fim de cada fase: `python -m motor.validar <dv> --fase Dx`; avance só com `LIBERADO`.

## Portões com Marcus (sempre com resposta proposta)
- **G1:** a decisão em uma frase, alternativas, critérios com limites, perguntas, premissas.
- **G2:** perfil do especialista (com fontes e confiança), contrato e métricas, problemas de qualidade e regras, colunas pseudonimizadas, plano com hipóteses e equipe.
- **G3:** memorando de decisão, insights por estado, impacto com faixa, ressalvas dos red teams, resultado da auditoria.

Registre: `python -m motor.estado aprovar <dv> --gate Gx --por Marcus --obs "<decisões>"`. Depois do G3: `python -m motor.insights aprovar <dv> --por Marcus`, `python -m motor.rodar <dv>`, `python -m motor.validar <dv> --fase D4`, `python -m motor.estado congelar <dv>` e `python -m motor.publicar <dv>`.

## Auditoria reprovada
Até 2 tentativas: devolva as divergências ao dono e rode de novo. Na terceira o status fica bloqueado; só sai como "preliminar, não auditado" com autorização de Marcus registrada no G3.
