# Squad de análise de dados — Acta Robotics

Squad que transforma um objetivo de negócio e um conjunto de dados em memorando de decisão, com insights quantificados, rastreáveis e auditados. Orquestração na skill `analisar` (sessão principal = orquestrador). Agentes em `.claude/agents/`, cálculos em `motor/`, memória em `conhecimento/`.

## Regras invioláveis
1. **Decisão antes dos dados.** Toda análise parte de uma decisão com alternativas, critérios e limites (ou é declarada exploratória).
2. **Números só do motor.** Nenhum agente digita número em nó de texto, insight ou entregável. Todo número sai de uma análise registrada ou do motor; insights usam `{{v.apelido}}`, entregáveis usam variáveis `fmt.*`.
3. **Nunca invente** dados, definições, fontes, faixas de setor ou pessoas. Sem fonte: `[●]` e pergunta com resposta proposta.
4. **Dados brutos intocáveis.** `dados/brutos/` é cópia somente leitura; toda transformação é etapa versionada em `etapas/`.
5. **Privacidade pelo sistema.** Scripts processam os dados localmente; agentes trabalham sobre o perfil, agregados e tabelas `base_*`/`prep_*` pseudonimizadas. Tudo o que um agente lê vai para o modelo: por isso nenhum agente lê linhas pessoais sem autorização registrada. Agentes que leem dados não têm internet; comandos de download estão bloqueados em `.claude/settings.json`.
6. **Contrato antes da análise.** Toda tabela e toda métrica definidas por escrito no contrato.
7. **Plano antes do resultado.** Análises confirmatórias com hipótese prévia; o resto é exploratório e precisa de confirmação.
8. **Três níveis de afirmação** (descritivo, associativo, causal) e **incerteza adequada ao método**.
9. **Quem produz não aprova.** O validador em código e os portões de Marcus decidem; insights passam por cinco estados e só os aprovados vão ao memorando.
10. **Reprodutível.** O auditor refaz tudo a partir dos brutos; até 2 tentativas reprovadas, depois bloqueio.
11. **O especialista setorial é uma lente.** Interpretações decisivas são validadas por uma pessoa da área.
12. **Português do Brasil**, frases curtas, conclusão primeiro.

## Disciplina de nomes
9fleet (K.FLEET só interno); Roboteazy (K.CONCEPT nunca externo); nunca citar o fornecedor de reconhecimento facial; Venturus e SiDi não são parceiros; parceiro de hardware: HBR.

## Estrutura de uma análise
`projetos/<data>_<tema>/v<n>/`: `dados/` (brutos, preparados, privado e o DuckDB; fora do git), `nos/`, `etapas/`, `analises/`, `evidencias/`, `saidas/`, `revisoes/`, `entregaveis/`. Contrato de dados entre agentes: `estado/README.md`.

## Comandos do motor
```
python -m motor.ingestao importar <dv> <pasta>     python -m motor.perfil <dv>
python -m motor.privacidade <dv>                   python -m motor.pipeline <dv>
python -m motor.registro <dv> [ANA-xxx]            python -m motor.impacto <dv>
python -m motor.insights checar|avancar|aprovar    python -m motor.rodar <dv>
python -m motor.reprodutibilidade <dv>             python -m motor.validar <dv> --fase D0..D4
python -m motor.comparar <dv_anterior> <dv_novo>   python -m motor.linhagem <dv>
```
