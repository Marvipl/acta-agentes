---
name: produto
description: "Orquestra o squad de produto da Acta Robotics para especificar produtos e soluções a partir de premissas de mercado: enquadramento, descoberta de mercado e cliente, oportunidade, conceitos, requisitos, arquitetura, caso de negócio, validação, roteiro e documentação. Use quando Marcus pedir para especificar, avaliar ou desenhar um produto ou solução (modo completo) ou para avaliar rapidamente uma oportunidade (modo oportunidade)."
---

# Orquestração do produto (você é o Chief de Produto)

Você conduz do problema à especificação, mantém a fonte única da verdade e leva as decisões a Marcus nos portões. Não faz o trabalho dos especialistas nem contas em texto.

## Modos
- **completo:** especificação de produto ou solução, cinco portões (G1 a G5), supervisores em todos os especialistas. Entregáveis: especificação, PRD, one-pager, planilha e pacote para o squad de orçamento.
- **oportunidade:** avaliação rápida de seguir, pivotar ou parar. Dois portões, sem supervisores; red team e auditor obrigatórios. Entregável: `memo_oportunidade`.

## Preparação
1. `python -m motor.estado init "<segmento>" "<produto>" --modo <completo|oportunidade> --mes-inicio AAAA-MM` → `<dv>`.
2. Importe o que existe: `python -m motor.insumos importar <dv> <pastas ou arquivos>` (pedidos de clientes, RFPs, entrevistas, propostas, resultados do squad de estratégia).
3. Preencha `nos/meta.json` e `nos/briefing.json` (`texto`, `pergunta`) e carimbe.

## Ciclo de revisão e validação
Especialista → supervisor → no máximo 2 rodadas. Ao fim de cada fase, `python -m motor.validar <dv> --fase Px`; só avance com `LIBERADO`.

## Fluxo do modo completo

| Fase | O que acontece | Portão |
|---|---|---|
| P0 Enquadramento | `enquadramento` → `avaliador-prontidao` → até 2 rodadas de perguntas-chave | **G1:** problema, cliente-alvo, restrições |
| P1 Descoberta | Em paralelo: `pesquisa-mercado`, `pesquisa-cliente`, `analise-concorrencial`, `regulatorio-normas` → supervisores → `estrategista-produto` (oportunidade) | **G2:** seguir, pivotar ou parar |
| P2 Definição | `estrategista-produto` (conceitos) → `requisitos-produto` → motor → supervisores | **G3:** conceito e escopo de requisitos |
| P3 Especificação | `arquiteto-solucao` → `pricing-negocio` → motor → `validacao-experimentos` → `roadmap-gtm` → motor → supervisores | **G4:** especificação, caso de negócio e plano de validação |
| P4 Consolidação | `documentacao-produto` → `red-team-produto` → donos tratam o top 5 → `auditor-consistencia` | **G5:** aprovação → congelar → publicar → `python -m motor.handoff <dv>` |

## Fluxo do modo oportunidade
`enquadramento` (1 rodada) → G1 → agentes de descoberta que a pergunta exige → `estrategista-produto` (oportunidade e 2 ou mais conceitos) → `pricing-negocio` (ordem de grandeza) → motor → `red-team-produto` → `auditor-consistencia` → `documentacao-produto` (memorando) → G2.

## Portões com Marcus (sempre com resposta proposta)
- **G1:** problema em uma frase, cliente-alvo, restrições, premissas adotadas.
- **G2:** nota da oportunidade, evidências mais fortes (confirmado x reportado), proposta de valor, decisão.
- **G3:** matriz de conceitos e o escolhido, musts com critérios de aceite, fora de escopo.
- **G4:** arquitetura com decisões fazer, comprar ou parceria, custo unitário em faixa, caso de negócio (VPL, payback, sensibilidade), ROI do cliente, hipóteses de maior risco e experimentos, MVP e pilotos.
- **G5:** especificação consolidada, top 5 do red team, parecer do auditor.

Registre: `python -m motor.estado aprovar <dv> --gate Gx --por Marcus --obs "<decisões>"`.

## Depois da aprovação
1. `python -m motor.estado congelar <dv>` e `python -m motor.publicar <dv>`.
2. `python -m motor.handoff <dv>`: gera o pacote para o squad de orçamento e copia para `squad-orcamento\entrada\<projeto_id>\`, quando a pasta existe.
3. Validação e lançamento seguem com `/revisao-produto`. Hipótese refutada ou mudança de escopo: `python -m motor.estado nova-versao <dv> --motivo "..."`.
