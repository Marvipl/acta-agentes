# Resposta do perfilador setorial à revisão do sup-negocio (D1, r1)

- Projeto: `projetos/2026-10-03_social_kappabot-operacao/v1` · 2026-10-03 · agente `perfilador-setorial`
- Entrada: `revisoes/sup-negocio_D1_r1.json` (veredito: revisar).
- Saídas corrigidas: `nos/especialista.json` e `perfil_especialista.md` (recarimbados).
- Escopo: respondo aos pontos do perfilador. Os pontos que são só do especialista (A4, H02, H09, F4 e a citação do art. 58) ficam com o especialista-setorial; marquei onde o perfil foi afetado.
- Nenhum número da análise entrou no perfil. Os números novos são de fontes setoriais ou legais, cada um com fonte, URL e confiança.

## Ponto alta: falta quantificar a dificuldade de contratação (CR8)

**Aceito.** Entraram nove conhecimentos e quatro indicadores, ligados a CR8, P13, P18 e P19.

| Tema | O que entrou | Fonte | Confiança |
|---|---|---|---|
| Hora extra e trabalho noturno | Até 2 h extras por dia, com adicional mínimo de 50%. Das 22 h às 5 h, adicional mínimo de 20% e hora de 52 min 30 s. | Constituição, art. 7º, XVI; CLT, arts. 59 e 73 | alta |
| Trabalho temporário | Feito via empresa de trabalho temporário, para demanda complementar (inclusive sazonal) ou substituição. Até 180 dias, prorrogáveis por mais 90. Nova contratação na mesma tomadora só 90 dias depois. Texto conferido na Câmara. | Lei 6.019/1974, na redação da Lei 13.429/2017 | alta |
| Volume de temporários | 2025: mais de 2,5 milhões de contratos, 522 mil de outubro a dezembro, cerca de 500 mil efetivados; logística do e-commerce como motor. | ASSERTTEM, via InfoMoney (26/01/2026) | média |
| Taxa da agência de temporários | Nenhuma fonte verificável: [●]. Os resumos de busca citam planilhas de licitação de terceirização, que não são trabalho temporário. | — | baixa |
| Custo de desligamento | Aviso prévio de 30 dias mais 3 por ano, até 90; multa de 40% do FGTS; férias e 13º proporcionais. | Lei 12.506/2011; Lei 8.036/1990, art. 18, §1º; CLT, art. 487 | alta |
| Custo de reposição | EUA: cerca de 16% do salário anual em cargos de menos de US$ 30 mil (11 estudos, de 1992 a 2007; só 2 incluem a perda de produtividade). Brasil: [●]. | Boushey e Glynn, CAP (2012) | baixa |
| Rotatividade na definição usual | Mínimo entre admissões e desligamentos ÷ estoque médio (RAIS). Em 2014, celetistas do subsetor Transporte e Comunicação: global de 53,0% e descontada de 34,7%. É proxy amplo e antigo; separadores e Social: [●]. | DIEESE (2016), Anexo, Tabela 5 | média |
| Encargos sobre o salário | O peso total depende do conceito: 27,8% da folha (DIEESE) contra 102,06% do salário-base (Pastore). A análise continua com PR10. | DIEESE (2006), citando Pastore (1996) | média |
| Tempo para repor a vaga | Sem fonte brasileira: [●]. | — | baixa |

- **Novos indicadores:** custo da hora extra, custo de repor um separador, uso de temporários no pico e tempo para preencher a vaga.
- **Novas perguntas à Social:** horas extras pagas e adicional da convenção, temporários por pico e custo da agência, custo e prazo de reposição.
- **Resposta proposta nas lacunas:** até a Social responder, CR8 usa os componentes legais (alta) e a referência externa de reposição (baixa) só como argumento qualitativo, sem quantificar a economia.

## Ponto média: sete afirmações além da fonte

**Aceito.** Corrigi texto, fonte e confiança item a item.

- **(a) Bartholdi, Fig. 15.5.** Tirei "horas totais" e "muito abaixo do tempo em tarefa". Fica: "pick-lines per person-hour", com eixo de cerca de 15 a 25 e sem denominador declarado. A regra "comparar só com o mesmo denominador" ficou marcada como interpretação. Confiança: baixa.
- **(b) BLS.**
  - A fórmula do indicador agora traz as duas definições.
  - A taxa de tempo perdido (horas ausentes ÷ horas habituais) é de 1,8% e é a que entra em horas e FTE.
  - A taxa de ausência (proporção de trabalhadores ausentes) é de 3,4%.
  - O `.md` mostra as duas.
- **(c) MD Logistics.** Agora cita "2.6x pick rate improvement" e, na fala do diretor, "more than 25% on a daily basis, and 50% on the busiest days", com a ressalva de que a base não é definida.
- **(d) DHL.** Tirei "carrinho" e "EUA". Os 30% a 180% são de "mais de 40 sites no mundo" (Automated Warehouse, 23/02/2026, data conferida). O método e o país da base não são informados.
- **(e) SC Digest.** A frase "100% não é realista" virou interpretação do perfilador.
- **(f) Times Brasil.**
  - Os 16,1% do e-commerce são do ICVA (Cielo).
  - Os 13% da ABOL são crescimento sobre o ano anterior, não multiplicador de pico.
  - Ficou uma armadilha nova: não usar os 13% em CR8 ou P19.
- **(g) Bartholdi 3.3.**
  - Citação literal: "more than two pick-lines but too few to sufficiently amortize the cost of walking".
  - A leitura sobre o pedido-a-pedido virou um conhecimento separado, de confiança baixa, que fala em 3 ou mais endereços. O de 2 endereços fica na fronteira.

## Ponto média: âncora de 15 min da CLT usada para endossar 900 s

**Aceito.** A pausa de 15 min (art. 71, §1º) só vale para trabalho de 4 h a 6 h e não se aplica a PR12.

- Retirei o "endosso do setor" a 900 s da faixa de M10, da lacuna do teto e do conhecimento da CLT.
- **O que fica:** mínimo de 0 e máximo de 1.800 s, sem mudar números. O máximo é o limite superior do contrato e coincide com a refeição mínima por convenção (art. 611-A, III): acima dele, o intervalo comporta uma refeição legal.
- **Teto base e conservador:** o perfil não sustenta valor. Eles se apoiam nos dados (intervalo humano entre pedidos do deck, slide 6, com mediana e quartis abaixo de 300 s, e a distribuição de M10) e em PQ03. A faixa caiu para confiança baixa.
- **Proposta ao planejador, como na revisão:** percentil de M10 declarado antes do resultado; reportar 300, 600, 900 e 1.800 s; Marcus decide.
- **Pendência:** o texto dos arts. 71 e 611-A segue sem reconferência no Planalto (503 também nesta rodada). Ficou registrado no conhecimento.

## Ponto média: confiança superestimada

**Aceito.**

1. **3PL multi-cliente.** O fato da fonte segue com confiança alta. A leitura de frota compartilhada (ALT6) virou um conhecimento separado, de confiança baixa, porque a fonte não trata disso.
2. **Curva de aprendizagem.**
   - O conhecimento foi renomeado para "treino não é proficiência" e caiu para confiança baixa.
   - O tempo até a proficiência, manual ou com AMR, ficou [●].
   - O indicador e a armadilha nova dizem que o argumento do temporário só pode sair como "treino mais curto", com confiança baixa.
3. **Piso físico de 3,6 s.** O número fica, como limiar de marcação já usado pela qualidade. Assim, nenhum mínimo muda sem necessidade.
   - A justificativa agora começa com [●]: o white paper da Dematic é inacessível.
   - A sensibilidade passa a ser de 2,0 s a 5,5 s, com duas fontes verificadas em outras unidades: a Dematic RapidPick ("up to 1800 items per hour", 2010) e a SSI Schäfer (650 caixas por hora, pessoa ou robô).
   - O limiar só marca tempo não mensurável. Nunca apaga do volume e nunca se aplica a uma cadência isolada.
   - Se Marcus preferir tirar o número, a qualidade usa as duas sensibilidades verificadas.
4. **Peso da separação e tempo do separador.** Caíram para confiança média, com a nota de que são estimativas para separação com papel (Frazelle, 1996; Tompkins, 2003). O indicador de deslocamento também caiu para média.

## Ponto média: implantação, segurança, ergonomia e carga por segmento

**Aceito.** Entraram cinco conhecimentos e perguntas novas.

- **Segurança:** a ISO 3691-4:2023 cobre "autonomous mobile robot" e a preparação da zona de operação (confiança alta). Se o Kappabot foi avaliado: [●], pergunta à engenharia da Acta.
- **Ergonomia:** NR-17, na redação da Portaria MTP 423/2021 (confiança média).
  - 17.5.1: veda transporte manual que comprometa a saúde, sem limite numérico.
  - 17.4.3.1: pausas preventivas contam como trabalho.
  - 17.4.4: a avaliação de desempenho deve considerar a saúde.
  - Ficou como interpretação que tirar caminhada e transporte do separador ajuda a reter pessoal.
- **Carga por segmento:** o K100 leva itens de até 100 kg (base da Acta, confiança baixa). O peso e o volume por item da ração, de cosméticos e de brinquedos ficam [●], com pergunta à Social.
- **Sazonalidade por segmento:** brinquedos concentram 64% do movimento anual da indústria de agosto a dezembro (ABRINQ, 2017; confiança média). Cosméticos e pet food: [●].
- **Implantação do lado da Social:** layout, rede sem fio, TI, treino, queda no go-live e sindicato ficam [●]. Fica a referência do plano da Acta de cerca de 10 semanas (deck, slide 19; confiança baixa). Pergunta nova à Social.

## Ponto média: treino tratado como proficiência (perfil e parecer)

**Aceito na parte do perfil** (ver o ponto de confiança, item 2). O H09 do parecer é do especialista.

## Ponto baixa: modelo híbrido (Perfil 2)

**Aceito, com uma divergência de leitura da fonte.**

- Reli a Fulfill.com em 03/10/2026. O texto é: "Hybrid models mix the above, most often a base subscription plus per-transaction fees beyond an included allowance, or a percentage of order value."
- A redação anterior ("base mais transações acima de uma franquia") batia com a primeira parte, mas omitia a segunda. Agora o perfil cita a frase literal.
- A comparação com a oferta da Acta virou interpretação.
- O Brasil segue [●], e a pergunta sobre como a Social cobra os depositantes continua prioritária.

## Pontos do especialista que tocam o perfil

- **A4 (conservador de 600 s).** O perfil deixou de apoiar qualquer teto pela CLT (ver acima). A correção de A4 e da nota de PAR02 é do especialista e do engenheiro.
- **H02 (horário estendido sem hora extra nem temporário).** Entrou uma armadilha nova: AMR colaborativo exige separador no mesmo horário, e estender o turno custa hora extra (adicional mínimo de 50%), adicional noturno ou nova escala. A correção de H02 é do especialista.
- **F4 (unidade da SSI).** O perfil agora declara a unidade da SSI (caixas por hora, pessoa ou robô) e a da Dematic RapidPick (itens por hora).
- **Art. 58 contra CF, art. 7º, XIII.** O perfil já citava os dois. Agora diz explicitamente: 8 h por dia no art. 58 e 44 h por semana na Constituição.

## Lacunas da revisão

- **Custo da dificuldade de contratação:** coberto pelo primeiro ponto. Seguem [●] a taxa da agência, o tempo de reposição, a rotatividade da própria Social e o custo de reposição no Brasil.
- **Proxy de rotatividade no WMS** (entradas e saídas de logins por mês, em agregado): sugestão para o planejador, não para o perfil.
- **Implantação, segurança e ergonomia:** cobertos acima.
- **Caso brasileiro de AMR em 3PL:** não encontrei. Segue [●], e todos os casos citados são do exterior.
- **Sazonalidade por segmento:** brinquedos coberto; cosméticos e pet food em [●].
- **CLT no Planalto:** a fonte continua fora do ar (503). Os arts. 59, 73 e 487 foram conferidos só em resumos (LegJur, TRT-3). A Lei 6.019 foi conferida na Câmara.
- **Pessoa da operação da Social:** continua [●] (A08).

## Validação

`python -m motor.validar <dv> --fase D1`: depois do recarimbo, nenhum bloqueio no especialista. O JSON é válido e não tem termos proibidos.
