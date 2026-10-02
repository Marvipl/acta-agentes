# Perfil dos dados

Gerado pelo motor. Colunas com dado pessoal provável têm valores mascarados.

## raw_missoes

3000 linhas · 0 linhas duplicadas

| Coluna | Tipo | Nulos | Distintos | Mín | Mediana | Máx | Observação |
|---|---|---|---|---|---|---|---|
| id_missao | VARCHAR | 0.0% | 3137 | M00000 | nan | M02999 | chave candidata |
| robo_id | VARCHAR | 0.0% | 6 | R01 | nan | R06 |  |
| data | DATE | 0.0% | 228 | 2026-01-01 | 2026-04-02 | 2026-06-30 |  |
| turno | VARCHAR | 0.0% | 3 | manha | nan | tarde |  |
| duracao_min | DOUBLE | 0.0% | 1140 | 2.59 | 13.413162064282481 | 36.49 |  |
| distancia_m | DOUBLE | 0.0% | 1260 | 40.3 | 179.09348201112243 | 335.8 |  |
| carga_kg | DOUBLE | 0.0% | 1013 | 5.0 | 49.895456667008176 | 95.0 |  |
| falha | BIGINT | 0.0% | 2 | 0 | 0 | 1 |  |
| operador_nome | VARCHAR | 0.0% | 25 | — | — | — | PESSOAL? nome da coluna |
| operador_cpf | VARCHAR | 0.0% | 3109 | — | — | — | chave candidata; PESSOAL? nome da coluna, valores com formato de cpf |

## raw_robos

6 linhas · 0 linhas duplicadas

| Coluna | Tipo | Nulos | Distintos | Mín | Mediana | Máx | Observação |
|---|---|---|---|---|---|---|---|
| robo_id | VARCHAR | 0.0% | 6 | R01 | nan | R06 | chave candidata |
| modelo | VARCHAR | 0.0% | 2 | K100 | nan | T300 |  |
| ano_fabricacao | BIGINT | 0.0% | 3 | 2023 | 2024 | 2025 |  |

## Ligações prováveis entre tabelas

| De | Para | Cobertura |
|---|---|---|
| raw_missoes.robo_id | raw_robos.robo_id | 100% |
