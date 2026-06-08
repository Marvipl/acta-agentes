# acta-agentes

Repositório-casa dos agentes de inteligência e prospecção da Acta Robotics.

Este repositório existe porque as rotinas (Claude Code Routines) são repo-cêntricas:
cada execução na nuvem clona um repositório. Aqui guardamos apenas conteúdo estável
(o playbook do agente e os arquivos de referência), que muda raramente. Dados que
mudam todo dia (sugestões de contato, status) ficam na planilha "Tracking Acta" no
Google Drive, nunca aqui.

## Estrutura

- `SKILL.md` — playbook do agente (papel, regras inegociáveis, perfis-alvo). Versão
  enxuta. O prompt operacional completo da rotina fica no campo de instruções da
  própria rotina (ver `referencia/prompt_rotina.md` para a cópia de referência).
- `referencia/icp_acta.md` — perfil de cliente, fornecedor e parceiro ideal.
- `referencia/portfolio_acta.md` — divisões, produtos e disciplina de nomenclatura.
- `referencia/guardrails.md` — regras de segurança e de não-invenção.
- `referencia/prompt_rotina.md` — cópia do prompt completo que vai no campo de
  instruções da rotina (mantida aqui para versionamento e referência).

## Operação

A rotina "Briefing Acta" roda na nuvem da Anthropic todo dia útil às 07:00 (fuso de
Brasília). Ela pesquisa, cruza com a planilha de rastreamento para não repetir
contatos, e entrega um briefing diário. Nada é enviado automaticamente: o CEO revisa
e envia tudo manualmente (e-mail pelo Titan, mensagens pelo LinkedIn) e mantém a
planilha de rastreamento.

## Privado

Este repositório deve ser privado. Não contém segredos, mas também não há motivo para
ser público.
