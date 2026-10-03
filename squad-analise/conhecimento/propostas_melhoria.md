# Propostas de melhoria das instruções dos agentes

Nenhum agente altera arquivos em `.claude/agents/` sozinho. Críticas recorrentes dos supervisores viram propostas aqui e só entram por PR aprovado por Marcus.

Formato:
## PM-000 — <agente> — AAAA-MM-DD
- **Evidência:** críticas repetidas (arquivos em revisoes/ de quais projetos).
- **Mudança proposta:** texto exato a incluir ou alterar.
- **Impacto esperado:** o que melhora e como medir.
- **Status:** proposta | aprovada | rejeitada

## 2026-10-03 · análise Social / Kappabot (projetos/2026-10-03_social_kappabot-operacao/v1)
Corrigidas nesta sessão (commits na branch da sessão):
- `motor.insights._fmt` e `motor.relatorio._num`: "p.p." virava "p,p,"; faixa de cenários aparecia como "IC"; frações em % e reais com unidade composta saíam ilegíveis. Agora usam `util.formatar_numero`.
- `motor.rodar` não gravava `saidas/resumo.json`, e `motor.estado congelar` não conseguia congelar versão nenhuma.
Pendentes (propostas):
- `motor.perfil`: o regex de coluna pessoal não pega "Usuário", "operador" nem "login", e marca "Qtde Endereços" como pessoal por conter "endere". Sugestão: incluir usuario|operador|login|matricula e excluir colunas numéricas de contagem.
- `motor.privacidade`: não há marcador de "conta de sistema" (ex.: conta do robô no WMS); hoje exige uma etapa que lê `dados/privado/` com autorização específica.
- `motor.cenario`: citado nas definições dos red teams, mas não existe; os red teams usaram cópias da versão no scratchpad.
- `motor.registro`: o hash registrado cobre só o script da análise, não módulos comuns importados (ex.: `analises/comum.py`); a linhagem também não os inclui.
- `motor.reprodutibilidade`: as análises que leem resultado de outra só reproduzem se a ordem do plano respeitar as dependências; vale um checador de dependências antes da auditoria (nesta análise houve um ciclo ANA-000 ↔ ANA-012 resolvido com ANA-017).
- Na nuvem, o download do Drive pelo conector chega como base64 no resultado da ferramenta; arquivos grandes são salvos pelo próprio Claude Code em `tool-results/` e podem ser decodificados de lá. Vale um utilitário em `ferramentas/`.
