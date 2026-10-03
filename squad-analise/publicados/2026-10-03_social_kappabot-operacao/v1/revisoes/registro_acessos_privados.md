# Registro de acessos a dados pessoais e à correspondência (para ratificação de Marcus no G2)

Regra do squad: agentes trabalham sobre perfil, agregados e tabelas `base_*`/`prep_*` pseudonimizadas; `dados/privado/` guarda a correspondência código → login e só é lido com autorização. Marcus autorizou em 2026-10-03 o uso destes dados na nuvem (nos/briefing.json); a leitura da correspondência pela etapa da conta do robô (PQ09) ainda depende de autorização específica.

Nenhum login de operador foi impresso, citado em arquivo de texto ou enviado ao modelo. Todos os acessos abaixo devolveram só contagens ou um booleano.

| # | Quem | Quando (fase) | O que acessou | O que saiu | Observação |
|---|---|---|---|---|---|
| 1 | orquestrador | D1, perfil | `saidas/perfil.json` gerado pelo motor continha mín./máx. de `Usuário` (o regex do motor não detecta a coluna) | nada impresso; valores mascarados por script antes de qualquer leitura | perfil.md nunca exibiu logins |
| 2 | engenheiro-de-dados | D1, contrato | `raw_.Usuário` por contagem com padrões (robo, kappa, acta, bot, fleet) | contagens de contas e linhas (1 conta de sistema) | identificação da conta do robô (P8) |
| 3 | qualidade-privacidade | D1, regra conta_robo | `dados/privado/correspondencia_*_Usuário.parquet`, uma consulta agregada | contagem (1 código casa com o padrão) | antes da autorização específica; declarado pelo agente |
| 4 | sup-dados | D1, r1 e r2 | `raw_.Usuário` e a correspondência por contagem; busca de vazamento carregou logins num script local | só contagens | declarado pelo supervisor |

Daqui em diante, até a decisão de Marcus no G2: ninguém consulta `raw_.Usuário` nem `dados/privado/`, nem por contagem.

## Atualização (2026-10-03, G2)
- Marcus autorizou no G2 (controle.json) a etapa `00_conta_robo.py` a ler a correspondência de `Usuário` em `dados/privado/` só para obter o código da conta de sistema do robô (PQ09). Também ratificou os 4 acessos agregados acima.
- A auditoria de reprodutibilidade (tentativa 2, aprovada) confirmou que a etapa 00 grava só `prep_conta_robo(codigo)` e que nenhum arquivo de texto do squad contém login de operador.
- Fora do git e não publicado: o insumo original `insumos/originais/performance-report.html`, baixado da pasta de Marcus no Drive, contém 5 logins de operador. Proposta: manter fora da publicação (já está) e, se Marcus quiser, guardar uma cópia mascarada.
