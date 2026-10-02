# Squad de orçamento — Acta Robotics

Este repositório é um squad de agentes que dimensiona e orça soluções robóticas da Acta Robotics. A orquestração está na skill `orcar` (sessão principal = Chief Estimator). Os agentes estão em `.claude/agents/`. Os cálculos estão em `motor/` (Python). A memória que aprende está em `conhecimento/`.

## Regras invioláveis
1. **Nunca invente dados.** Nenhum preço, alíquota, prazo, especificação, fornecedor ou pessoa sem fonte. Sem fonte: `[●]` no texto ou `null` no campo numérico, mais uma pergunta com resposta proposta para Marcus.
2. **Toda premissa tem origem.** Tipos de fonte: `cotacao` (documento do fornecedor), `base_interna` (arquivo em `conhecimento/`), `benchmark` (pesquisa rastreável, nunca tratada como cotação), `premissa` (hipótese explícita, com confiança).
3. **Incerteza em 3 pontos.** Valores incertos usam `{"min", "provavel", "max"}` com min ≤ provável ≤ max. O Monte Carlo do motor transforma isso em P50 e P80.
4. **O motor faz as contas.** Custo total, contingência, preço, fluxo de caixa, DRE, VPL, TIR e planilha saem de `python -m motor.rodar <dv>`. Nenhum agente calcula esses números em texto. Entregáveis citam números só por variáveis entre chaves duplas (ex.: `{{fmt.preco_sugerido}}`).
5. **Cada nó tem um dono.** Agentes escrevem só nos seus arquivos em `nos/` e carimbam ao terminar (`python -m motor.estado carimbar <dv> <no> --agente <nome>`). O carimbo registra as versões das entradas; quando uma entrada muda, o nó aparece como desatualizado.
6. **Especificação antes de orçar, com perguntas-chave apenas.** Todo orçamento começa pela descoberta: no máximo 7 perguntas por rodada e 2 rodadas, só de impacto alto ou médio, sempre com resposta proposta. Lacuna de impacto baixo vira premissa declarada, nunca pergunta.
7. **Portões humanos.** G1 (requisitos), G2 (escopo, BOM e cotações) e G3 (pacote final) são aprovados por Marcus e registrados com `python -m motor.estado aprovar`.
8. **Neutralidade tecnológica.** A solução nasce dos requisitos, não do catálogo. Toda escolha de tecnologia passa por matriz de alternativas de mercado com critérios e pesos; produto da Acta ou de fornecedor parceiro só entra se vencer a matriz.
9. **Contratos passam pelo jurídico.** Toda estrutura contratual ou minuta derivada é revisada por Janary antes de ir ao cliente.
10. **Português do Brasil** em todos os nós e entregáveis.

## Disciplina de nomes (material externo)
- Plataforma de gestão de frota: **9fleet** (K.FLEET só uso interno).
- Conceito de empreendimento robotizado: **Roboteazy** (K.CONCEPT nunca externamente).
- Nunca citar o fornecedor de software de reconhecimento facial; usar "software de reconhecimento facial".
- Venturus e SiDi não são parceiros. Parceiro tecnológico de hardware: HBR.
- Grafia correta dos produtos da Acta quando forem citados (não é lista de preferência): Kappabot, Robertron, Alpha5, STREAM, k.flexstore, K.SCAN, K.TWIN, 9fleet, Roboteazy, RobotForge, AEX Center.

## Fatos da empresa
- Acta Robotics Fabricação de Robôs Autônomos Ltda. Matriz em Manaus/AM (CNPJ 36.091.111/0001-06); filial em Campinas/SP (CNPJ 36.091.111/0002-89).
- Optante do Simples Nacional, com saída em planejamento: contratos grandes precisam do alerta de regime (ver `conhecimento/tributos/regras_tributarias.md`).
- Diferenciais verificáveis: fabricação nacional, suporte próximo, customização ao cenário do cliente, IA embarcada.

## Estrutura de um orçamento
`projetos/<AAAA-MM-DD>_<cliente>_<projeto>/v<n>/`
- `nos/` — premissas estruturadas, um arquivo por nó (fonte da verdade)
- `controle.json` — carimbos, aprovações, congelamento
- `revisoes/` — vereditos dos supervisores, red team e auditor
- `entregaveis/` — modelos `.md.tpl` escritos pelos agentes (texto + variáveis)
- `saidas/` — tudo gerado pelo motor: `resumo.json`, planilha mestre `.xlsx`, CSVs, Monte Carlo, entregáveis renderizados, cotações pendentes

Detalhes dos nós, donos e dependências: `estado/README.md`.

## Comandos úteis
```bash
python -m motor.estado status <dv>          # o que está pronto, pendente ou desatualizado
python -m motor.validar <dv> --fase F2      # gatekeeper da fase
python -m motor.rodar <dv>                  # calcula tudo e gera planilha e entregáveis
python -m motor.publicar <dv>               # copia para o Drive
```
