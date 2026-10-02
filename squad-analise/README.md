# Squad de análise de dados — Acta Robotics

Squad de agentes para Claude Code que recebe um objetivo de negócio e qualquer conjunto de dados e entrega um memorando de decisão com insights quantificados, rastreáveis e auditados. Os agentes planejam, escrevem os scripts e interpretam; o motor em Python (DuckDB) calcula, registra e audita.

## Como funciona
```
D0 Decisão          arquiteto da decisão: decisão, alternativas, critérios com limites, perguntas   ▶ G1
D1 Dados e contexto importação, perfil automático, contrato de dados, perfil do especialista setorial,
                    qualidade e privacidade (pseudonimização com chave local)
D2 Plano            hipóteses confirmatórias, métodos, nível, incerteza e equipe por tipo de pergunta ▶ G2
D3 Preparação e     etapas versionadas, análises registradas, interpretação do especialista,
   análise          red team analítico (só o que sobrevive segue)
D4 Decisão e        impacto (caso de negócio simulado), red team da decisão, memorando, auditoria   ▶ G3
   entrega          de reprodutibilidade a partir dos dados brutos
Acompanhamento      resultado das recomendações calibra o squad (/acompanhar)
```
- **19 agentes** em camadas: 14 de execução, 4 supervisores por área (dados, metodologia, negócio, comunicação) e a calibração.
- **Três níveis:** rápido, padrão e completo. A equipe de cada análise depende do tipo de pergunta (comparação, previsão, causa, investimento).
- **Livro de evidências:** cada insight é um registro com afirmação, valores ligados às análises, nível, incerteza, robustez, vereditos dos red teams, impacto e ação, e passa por cinco estados. Só os aprovados vão ao memorando.
- **Privacidade:** dados no seu computador, agentes sobre dados pseudonimizados e agregados, sem internet para quem lê dados.

## Instalação
1. Pasta em `C:\Dev\acta-agentes\squad-analise\`.
2. `pip install -r requirements.txt`
3. `python exemplos\teste_motor_ficticio\testar.py` (última linha `TESTE OK`).
4. `cd C:\Dev\acta-agentes\squad-analise` e `claude`.

## Uso
```
/analisar padrao "Decidir se vale ampliar a operação noturna" C:\dados\frota
/status-analise projetos\<id>\v1
/atualizar-analise projetos\<id>\v1 C:\dados\frota_julho
/acompanhar projetos\<id>\v1
```
Formatos aceitos: CSV (separador e codificação detectados, inclusive `;` com vírgula decimal), Excel (todas as abas), Parquet, JSON e SQLite. Formatos antigos (.xls) precisam ser salvos como .xlsx.

## Entregáveis (em `saidas\`)
- `memo_decisao.md` e `relatorio_executivo.md` (números só por variáveis do motor)
- `cartoes_insight.md`, `painel.html` (local, com gráficos), `resultados_<id>.xlsx`
- `perfil.md`, `catalogo.json`, contrato e dicionário de dados no nó `contrato`
- `linhagem.json` (assinaturas de cada elo e versões dos pacotes) e `auditoria.json`

## Configuração
| O quê | Onde |
|---|---|
| Pasta do Drive (Acta > Análises) | `config\config.json` → `drive_analises_dir` |
| Privacidade | `config\config.json` → `privacidade` (desligar exige nome de quem autorizou) |
| Chave da pseudonimização | `config\chave_local.key`, criada no primeiro uso; fora do git. Guarde uma cópia segura: sem ela os códigos de uma análise nova não batem com os anteriores |

## Limites conhecidos
- Dados observacionais sustentam associação; causa só com desenho adequado.
- O especialista setorial é um perfil construído por IA: interpretações decisivas devem ser validadas por uma pessoa da área.
- O DuckDB processa alguns GB num computador comum; acima disso, amostragem declarada ou banco externo.
- O painel é um HTML local; publicar no link como o painel de orçamento fica para uma segunda entrega.
