# Planejador analítico: dependência circular ANA-000 ↔ ANA-012 (AUD-D1), r4

- Projeto: `projetos/2026-10-03_social_kappabot-operacao/v1` · 2026-10-03 · agente `planejador-analitico`
- Entrada: `revisoes/auditor-reprodutibilidade.json` (AUD-D1, bloqueia; AUD-D2 em cascata) e a correção acordada com o orquestrador.
- Saída: `nos/plano.json`, recarimbado.
- Não li nenhum dado nem resultado: só os nomes de análises citados nos scripts, para conferir a ordem.

## Desvio declarado

É uma correção de reprodutibilidade, sem mudança de método nem de valores.

1. **O problema.** ANA-000 lia os limiares de ANA-012 para o poder de PT-D1, PT-D3 e PT-D4. Ao mesmo tempo, ANA-012 lia `n_*` e `mde_*` de ANA-000. Numa cópia limpa, nenhuma ordem resolvia o ciclo.
2. **A correção.** O cálculo de poder das três pistas sai de ANA-000 e vai para uma análise nova, a ANA-017 ("poder das pistas da descoberta"). A conferência agregada do incidente da Royal Canin nas semanas pares vai junto.
   - ANA-017 grava só `n_*`, `ep_*` e `mde_*`; nenhum efeito, estimativa pontual ou p.
   - Lê ANA-000 (alfa e convenções) e ANA-012 (limiares e pesos de `limiares_descoberta`).
   - Está posicionada na lista `analises` imediatamente antes de ANA-016. O motor executa na ordem da lista.
   - Campos: pergunta_ref P9, confirmatória, descritiva, retrato, incerteza nenhuma, estatístico, `analises/ANA-017.py`.
   - Métricas: M01, M02, M05, M10, M11 e M14, as do bloco PT-D que saiu de ANA-000.
3. **ANA-000.** Mantém F1a, F1b, as três pistas a priori da F2 (o alfa continua alfa ÷ 6) e a equivalência de ANA-006. Não lê nada de ANA-012. Saíram das chaves `mde_pt_d1`, `mde_pt_d3` e `mde_pt_d4`.
4. **ANA-016.** Lê o poder das pistas a priori em ANA-000, o das pistas PT-D e a marcação do incidente em ANA-017.
5. **`definicoes.dependencias_entre_scripts`.** Agora traz a ordem sem ciclo:

   ANA-000 → ANA-001 a ANA-011 → ANA-012 → ANA-013 a ANA-015 → ANA-017 → ANA-016

   Nenhuma análise lê outra que venha depois dela na lista.
6. **Conferência.** Busquei nos scripts as leituras de resultados registrados (`comum.valor_de`, `comum.poder`) e de `limiares_descoberta`. Com ANA-017 no lugar do bloco de ANA-000, todas as leituras apontam para análises anteriores na lista. ANA-004 executa ANA-005 dentro de si, sem ler resultado registrado.
7. **Valores.** Não devem mudar: as chaves `pt_d*` de ANA-017 têm de ser iguais às que ANA-000 gravou antes. O red team e o auditor conferem na tentativa 2.

## Pendências

- Estatístico: escrever `analises/ANA-017.py` com o bloco tirado de ANA-000 e registrar na ordem da lista.
- Orquestrador: pedir a tentativa 2 da auditoria.
- F2, pistas, Holm e regras de leitura não mudam.
