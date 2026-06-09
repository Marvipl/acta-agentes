# acta-agentes

Repositório-casa dos agentes de inteligência e prospecção da Acta Robotics.

Este repositório existe porque as rotinas (Claude Code Routines) são repo-cêntricas:
cada execução na nuvem clona um repositório. Aqui guardamos apenas conteúdo estável
(playbooks dos agentes e arquivos de referência), que muda raramente. Dados que mudam
todo dia (sugestões de contato, status, briefings) ficam no Google Drive, nunca aqui.

## Os dois agentes (v3)

A solução foi separada em DOIS agentes especializados, cada um em sua própria rotina
Remote:

1. AGENTE DE NOTÍCIAS ("Inteligência Acta") — só inteligência de mercado e editais.
   Prompt: `referencia/prompt_agente_noticias.md`. Entrega na pasta `Acta/Briefings`,
   rótulo de e-mail "BriefingActa/Enviar". Usa os 5 briefings mais recentes do Drive
   como memória de deduplicação. Janela de notícias: máximo 3 dias.

2. AGENTE DE PROSPECÇÃO ("Prospecção Acta") — só descoberta de candidatos e rascunhos
   de contato. Prompt: `referencia/prompt_agente_prospeccao.md`. Entrega na pasta
   `Acta/Prospeccao`, rótulo de e-mail "ProspeccaoActa/Enviar". Usa a planilha
   `Tracking Acta` para deduplicação.

## Estrutura

- `SKILL.md` — papel, regras inegociáveis e perfis (resumo compartilhado).
- `referencia/prompt_agente_noticias.md` — prompt completo do Agente de Notícias.
- `referencia/prompt_agente_prospeccao.md` — prompt completo do Agente de Prospecção.
- `referencia/fontes_noticias.md` — lista curada de fontes de notícia e reports.
- `referencia/icp_acta.md` — perfil de cliente/fornecedor/parceiro.
- `referencia/portfolio_acta.md` — divisões, produtos e disciplina de nomenclatura.
- `referencia/guardrails.md` — regras de segurança e de não-invenção.

Observação: `referencia/prompt_rotina.md` é o prompt antigo (v2, agente único) mantido
apenas como histórico. Para a operação v3, use os dois prompts separados acima.

## Envio de e-mail

Os agentes não enviam: cada um cria um rascunho no Gmail, formatado em HTML com
hyperlinks, e o marca com seu rótulo ("BriefingActa/Enviar" ou "ProspeccaoActa/Enviar").
Um Google Apps Script na conta do CEO (`EnviarBriefingActa.gs`, fora deste repositório)
roda por gatilho diário, processa os dois rótulos, envia e re-marca como
"BriefingActa/Enviado". As mensagens de LinkedIn são sempre manuais.

## Privado

Este repositório deve ser privado. Não contém segredos, mas não há motivo para ser
público.
