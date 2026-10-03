# Resposta do especialista setorial à revisão do sup-negocio (D1, r1)

- Projeto: `projetos/2026-10-03_social_kappabot-operacao/v1` · 2026-10-03 · agente `dados-especialista-setorial`
- Entrada: `revisoes/sup-negocio_D1_r1.json` (veredito: revisar). Saída corrigida: `revisoes/especialista_D1.md` (r1).
- Conferi o texto do deck (slides 6 e 17) e o relatório 9fleet v1 (p. 12 e 13). Reconferi o parecer contra `nos/contrato.json` (5527342f3195) e `nos/qualidade.json` (73fa3fc27d22).
- Não alterei nenhum nó. As correções nos nós de outros agentes vão como pendências (seção final).
- Números: nenhum resultado de análise digitado.

## Pontos dirigidos ao especialista

### 1. (alta) A4 e F12: cenário conservador de 600 s com premissa falsa
**Aceito. Retiro a justificativa e corrijo.**
- **O erro.** PR16 (dois a três minutos) é o trajeto do **robô** ao faturamento, medido no 9fleet. O relatório 9fleet v1, p. 13, diz que "do operador não existe como pegar". Eu o tratei como parte do intervalo humano.
- **O que a fonte mostra.** O intervalo humano está no deck, slide 6. Ele já inclui a ida ao packing, a nova etiqueta e a primeira coleta, e a mediana e os quartis ficam abaixo de 300 s. Portanto 300 s não corta o ciclo típico documentado: corta só a cauda.
- **Por que o erro importava.** Era o único ajuste meu que favorecia a oferta. Teto maior dá mais horas e mais FTE em CR1 e CR8, e manual mais lento em CR3.
- **Nova recomendação (A4 e F12):**
  - base de 900 s, que reproduz a mediana do slide 6;
  - **conservador de 300 s**;
  - intermediário de 600 s;
  - limite superior de 1.800 s.

  O analista reporta os quatro. Como referência opcional, um teto pela distribuição medida de M10, com percentil declarado antes do resultado, sem trocar o conservador. Não tenho evidência para 600 s que não favoreça a oferta, por isso não o proponho como conservador.
- **Decisão.** Fica marcada como **decisão de Marcus no G2**, com validação da operação da Social (PQ03, E8).
- **Propagação.** A4 já entrou no contrato: PAR02 (`cenario_conservador`, nota e fonte), M11, M12, M28, PQ03 e pendências. Entrou também na qualidade: QD15 e `limiares.PAR02_teto_intervalo_s`. As pendências pedem a reversão ao engenheiro e à qualidade.

### 2. (alta) H02: "sem hora extra nem temporário" com robô colaborativo
**Aceito. Reescrevi H02.**
- **Premissa nova.** Cada hora de robô na janela estendida exige separador na mesma hora. O deck (slide 17) conta FTE também no cenário com robôs e mantém "o robô guia o temporário".
- **Hipótese nova.** Com escala escalonada (entrada e saída deslocadas, dentro de 8 h por dia e 44 h por semana), a frota em janela estendida cobre o excedente dos dias pós-pausa e p90 com **menos pessoas-hora**, menos hora extra e menos temporários do que hoje. Não "sem".
- **Teste.** Três passos:
  - excedente atual em pessoas-hora (M23) e como é coberto hoje (amplitude, jornada ativa e operadores ativos; H10, M24);
  - pessoas-hora e separadores por hora com robô (PR05, com sensibilidade, contra M14), com robôs por hora no máximo a frota (M22);
  - quatro arranjos: manual com hora extra, manual com temporário, robô com escala escalonada, robô com hora extra.

  Regras usadas: hora extra até 2 h (CLT, art. 59), adicional mínimo de 50% (CF, art. 7º, XVI) e adicional noturno depois das 22 h (CLT, art. 73). Custos de hora extra e de temporário: [●], com a nova pergunta E11.
- **Marca.** `validar com pessoa do setor`; decisiva para CR8.
- **Também corrigido.** O item 2 da seção 2 do parecer e a Conclusão. As pendências trocam o texto copiado no contrato (M18) e na qualidade (QD06).

### 3. (média) CLT de 15 min como endosso de 900 s
**Aceito.**
- O art. 71, §1º só vale para trabalho de 4 a 6 h. Com PR12 acima de 6 h, a pausa legal é a refeição. A lei não diz se um intervalo de 15 min é trabalho ou pausa.
- Retirei a CLT como âncora de 900 s em F12 e em A4.
- A âncora agora é a distribuição medida (deck, slide 6; M10) e PQ03, com **confiança baixa** até a Social validar.
- O limite de 1.800 s fica como sensibilidade do contrato, sem endosso legal.
- Os arts. 71 e 611-A não foram reconferidos na fonte nesta rodada (Planalto fora do ar, segundo a revisão). Marquei isso em F11.

### 4. (média) Afirmações de setor sem fonte (seção 2, 3.8 e outras)
**Aceito.** Marquei [●] e confiança baixa, ligadas às perguntas existentes, e nenhuma vira premissa:
- Corpus Christi: a data é calculada (alta). Feriado na cidade da Social e fechamento: [●] (E4). Retirei "feriado municipal em muitas cidades e ponto facultativo federal".
- Ponte de 05/06: [●], baixa (E4).
- "Um 3PL de e-commerce raramente para tanto": agora é "leitura sem fonte, [●], confiança baixa" (E4).
- Pico de retomada: virou hipótese a testar em H02 (M17, M18), não fato.
- 3.8, multipedido: virou "hipótese sem fonte, [●], confiança baixa; não usar como premissa até E1".
- Por coerência, também marquei [●] em A8 (encerramento administrativo), A9 (reliberação depois de corte) e F6 (separação por validade).
- Em H03 e H07, separei o que é da fonte do que é interpretação: sazonalidade complementar não é frota; método manual não é AMR. A confiança ficou baixa.

### 5. (média) H09: tempo de treino usado como proficiência
**Aceito.**
- H09 agora separa as duas métricas. Os casos de AMR (DHL; MD Logistics, depoimento de fornecedor) tratam de tempo de treino. O tempo até a proficiência com AMR é [●].
- M25 mede só a curva manual.
- Na oferta, o argumento sai como "treino mais curto, segundo casos dos EUA, confiança baixa". Ganho de proficiência com robô, só depois do teste controlado.

### 6. (média) Custo e prazo de implantação do lado da Social, segurança e ergonomia
**Aceito para a D3 e a D4.** Acrescentei ao parecer (seção 6) que julgarei cada recomendação também por custo e prazo de implantação para a Social:
- layout e corredores;
- rede sem fio;
- integração com o Senior;
- treino;
- queda de produtividade no go-live;
- segurança do AMR com pessoas;
- ergonomia.

Esses temas ainda não têm fonte no perfil: a pendência é do perfilador. Acrescentei também a pergunta E11 (horas extras, temporários e custos).

### 7. (baixa) F4: taxa da SSI Schäfer usada como coleta manual
**Aceito.** F4 declara a unidade: **caixas por hora** na estação goods-to-person, com pessoa ou robô separando. O ≈ 5,5 s fica só como ordem de grandeza da sensibilidade, com confiança baixa. O piso continua sendo **marca**, nunca corte de volume. Se o perfilador rebaixar o piso de 3,6 s para [●], o tratamento não muda.

### 8. (baixa) 44 h atribuídas ao art. 58 da CLT; parecer anterior ao contrato e à qualidade atuais
**Aceito.**
- Corrigi 3.1 e E5: 44 h semanais estão na CF, art. 7º, XIII; o art. 58 da CLT fixa 8 h por dia.
- Tirei o art. 58 da fonte de F11, que trata do limite diário de 12 h.
- Pendência ao engenheiro: o mesmo em PAR09 e PQ05.
- A reconferência contra o contrato e a qualidade atuais está na tabela abaixo.

## Reconferência de F1 a F13 e A1 a A10

Contra o contrato 5527342f3195 e a qualidade 73fa3fc27d22.

| Item | Onde está | Situação |
|---|---|---|
| F1 | QD01 (`tarefa_aberta_lote`), QD17 (`tempo_s_limpo`, `fim_corrigido`) | Aplicado. |
| F1a, A1 | QD08, QD09, `limiares.instante_confirmacao_s` | Aplicado. Teste agregado do engenheiro: sem sinal de bipe por unidade no pedido-a-pedido da Royal Canin. Colmeia fica para a D3 (E3). |
| F2 | QD02, M03, PAR11 (`robo_pre_inicio`) | Aplicado. |
| F3 | QD11 (`abandono_coleta`, `linha_longa`) | Aplicado. |
| F4 | QD10, `limiares.piso_s_por_coleta` | Aplicado. **Ajustar** a fonte da sensibilidade (unidade da SSI; ponto 7). |
| F5 | QD20 (`cauda_enderecos`), QD28 (`nao_pessoal`) | Aplicado. O p99 é limiar de revisão da qualidade, só marca; não é faixa do setor. |
| F6 | QD04 | Aplicado. |
| F7, A6 | QD13 (`linha_palete`), QD14 (`un_extremas`, PAR13) | Aplicado. PAR13 é limiar de revisão sem fonte setorial ([●]): só marca, sem corte. Concordo. |
| F8 | QD21 | Aplicado. |
| F9, A7 | QD19 (`checkout_multiunidade`), M02 | Aplicado. |
| F10 | QD22 | Aplicado. |
| F11 | QD24, PAR12 | Aplicado. |
| F12, A4 | QD15, PAR02, M11, M12, M28, PQ03 | **Corrigir:** conservador de 300 s, intermediário de 600 s, âncora no slide 6 e em PQ03, confiança baixa (ponto 1). |
| F13 | QD25, QD17 | Aplicado. |
| A2 | M09 e M11 por segmentos Início a Início (r2) | Aplicado, e melhor do que eu propus. |
| A3 | PAR11, `pre_robo` em M08, M12, M14 e M26 | Aplicado. |
| A5 | M11: base com a pausa excluída; S1 com a mediana; S2 truncada como limite superior | Aplicado. |
| A8 | QD01 | Aplicado. |
| A9 | M06 com dois limites (soma e máximo) | Aceito: sem código de produto, a deduplicação não é possível. |
| A10 | PAR10, QD05, QD06, QD16, QD26 | Aplicado. **Ajustar** a confiança de 04/06 e 05/06 em PAR10 (ponto 4) e o texto de H02 em M18 e QD06 (ponto 2). |

## Pontos dirigidos só ao perfilador

São os itens 3 (custo da contratação no Brasil), 4 (sete atribuições de fonte), 6 (confiança superestimada) e 12 (modelo híbrido). Sem ação minha no nó dele.

Usei-os no parecer assim:
- a proficiência com AMR ficou [●];
- a leitura de ALT6 ficou com confiança baixa;
- as proporções de tempo ficaram com aplicabilidade média;
- os 13% da ABOL não aparecem como pico.

## Pendências (aos donos dos nós)

- **engenheiro de dados:**
  - PAR02: `cenario_conservador` de 300 s, intermediário de 600 s, nota e fonte sem PR16 e sem o "endosso"; âncora no slide 6 e em PQ03; confiança baixa.
  - M11, M12, M28, PQ03 e pendências: o mesmo cenário.
  - PAR09 e PQ05: CF, art. 7º, XIII.
  - PAR10: confiança de 04/06 e 05/06.
  - M18: o novo texto de H02.
- **qualidade-privacidade:**
  - QD15 e `limiares.PAR02_teto_intervalo_s`: o cenário de 300 s.
  - `limiares.piso_s_por_coleta.fonte_sensibilidade`: a unidade da SSI.
  - QD06: o texto de H02.
- **planejador:**
  - H02 com os quatro arranjos;
  - H09 só com a curva manual;
  - tetos de 300, 600, 900 e 1.800 s, com o conservador de 300 s até o G2.
- **Marcus (G2):** escolha do cenário conservador de teto (PQ03, E8) e as perguntas E4, E5 e E11 à Social.
