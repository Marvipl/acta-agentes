# Resposta do analista exploratório ao red team analítico (partes A e B)

Escopo: insights e análises sob minha responsabilidade (ANA-009, ANA-011, ANA-012, ANA-013, ANA-015). Nenhum número está digitado aqui; os valores estão nas chaves citadas.

## ANA-009 (frota, CR8, H02) — INS-054 a INS-059
- **Regime da colmeia (parte A, pendência 3; decisão do orquestrador).** Aceito. ANA-009 passou a ter três leituras da Royal Canin: sem sufixo e `_estresse` = variante do plano (período inteiro, regime pré-colmeia incluído); `_pos_colmeia` = base da oferta (semana ISO da primeira colmeia lida de ANA-008 e conferida com ANA-003, sem 21 a 25/09); `_normal` = janela normal de ANA-002. A conferência do perfil e do p90 com ANA-008 vale para as três (`confere_perfil_ana008`). O excedente de horas vem de ANA-003 pela janela correspondente. O M14 do pós-colmeia usa o mix da janela normal (ANA-004, `_mix_normal`), limitação declarada na nota do script.
- **Frota dia a dia (parte A, ANA-010).** Aceito. ANA-009 não pode ler ANA-010 (a ordem do plano põe a 009 antes), então recalcula com o mesmo código (`frota_diaria`, `p90_inteiro`, método "higher"); conferi que a frota dia a dia dos outros depositantes bate com `ANA-010.robos_adicionais_alt6`. ALT6 usa o dia a dia como primária; ALT2 e ALT3 mantêm a banda do plano e têm o dia a dia como ponta desfavorável (chaves `frota_necessaria_*_mesmo_dia*`, dentro da faixa da grade). A correlação entre depositantes relevantes está em ANA-010.
- **M23 colaborativa (parte B, INS-056).** Aceito. Gravei a leitura colaborativa ao lado da autônoma (`horas_poupadas_colab`, `horas_residuais_colab`, `horas_residuais_colab_em_fte`, `reforco_p90_cr8_colab`, `pr05_para_reforco_zero`, variante com piso zero por tipo para a PR05 no checkout). A autônoma ficou como limite superior da absorção. O INS-056 foi reescrito com as duas leituras e a fração de FTE ao lado do teto inteiro; a leitura é de Marcus no G3.
- **Arranjos pela mesma regra (parte B, INS-059).** Aceito. Os quatro arranjos antigos misturavam duas métricas. Agora há duas regras, cada uma igual no manual e no robô: A (curva de separadores inteiros) e B (excedente de horas de ANA-003, com o residual colaborativo no robô), cada uma com hora extra e escala/temporário (chaves `h02_regraA_*` e `h02_regraB_*`; tabela `h02_arranjos_pessoas_hora`, com a variante do checkout do robô na taxa manual). O INS-059 foi reescrito: a vantagem do robô no pico não aparece com nenhuma das duas regras. A PR05 no checkout segue como premissa a validar com a engenharia (E9); não inventei taxa.
- **INS-057.** Reescrita a frase de privacidade: o zero de `ativos_hoje_horas_estendidas` é convenção, não ausência medida; a descrição da chave e a nota do script também. Incluída a ressalva da PR05 no checkout (E9).
- **INS-054, INS-055, INS-058 (ressalvas).** Texto passa a declarar a ausência de reserva de disponibilidade, que a sobra é condicionada às premissas e não ociosidade medida, e que a frota agrupada é dia a dia.

## ANA-013 — INS-050
Aceito. Acrescentei a ANA-013 as contagens agregadas de entradas com poucos dias ativos (limites do red team, sem fonte setorial, `[●]`), as entradas que também saem dentro da carga e o limiar usado (chaves `logins_entrada_poucos_dias*`, `logins_entram_e_saem_na_carga`, `limiar_poucos_dias_ativos*`; grupos abaixo de PAR07 ficam omitidos). O INS-050 deixou de falar em rotatividade como taxa e passou a "entradas e saídas de logins", sem citar `rotatividade_proxy_periodo`. A definição de saída por dias plenos do red team difere da minha por poucos logins; sem efeito na leitura.

## Textos
- **INS-053**: frase final substituída; a mediana depende do teto e o teto deve ser declarado.
- **INS-083**: cita a faixa dos tetos e S1 a S3 (`ANA-015.fte_separacao_alt3`) e que a jornada ativa é limite inferior da presença.
- **INS-084**: "portanto" trocado por "compatível com", a confirmar com Marcus; declara que o IC da mediana no teto conservador contém o valor do slide.
- **INS-089**: reescrito como estimativa (WMS mais PR11), com a fração vinda de PR11 e a parte de separação como limite inferior.
- **INS-045**: corrigida a frase "menos de dez novatos"; ação inclui ponderar a razão pelas horas do novato.
- **INS-048**: acrescentada a folga da própria equipe e o excedente como limite superior.
- **INS-040 e INS-046**: ações atualizadas (pistas já confirmadas em ANA-016; trilha da descoberta).
- **INS-041 e INS-042**: não editados, por orientação do orquestrador (ficam fora do memorando).
- **INS-085 a INS-088**: base da oferta citada primeiro; INS-087 passa a mostrar que o sinal da margem sem o piso depende da frota (dia a dia, regra por tipo) e da janela; INS-086 cita a dúvida de CR2 sobre a franquia; INS-088 usa a frota agrupada dia a dia e menciona que a adoção pelos outros depositantes pode ser menor (INS-070).

## Re-registros
ANA-013 (chaves novas, valores antigos idênticos), ANA-009 (nova), ANA-015 (lê as novas chaves de ANA-009 e ANA-010; `_normal` = receita da janela normal com a frota pós-colmeia; `_estresse` e sem sufixo = plano). ANA-011 reconferida contra as novas entradas: valores idênticos, sem re-registro.

## Pendências
- Marcus (G3): leitura de M23 (autônoma ou colaborativa), regime da colmeia como base, reserva de disponibilidade da frota.
- Engenharia (E9): PR05 no checkout e taxa com robô.
- Social: quem são os logins com poucos dias ativos; equipe depois da janela.

## Rodada r2 (ajustes finais do red team)
- **ANA-009, frota dia a dia primária também em ALT2 e ALT3.** Aceito. `frota_necessaria_alt2*` e `frota_necessaria_alt3*` passam a ser a frota dia a dia (a mesma regra da ALT6); a banda ficou como variante otimista nas chaves `frota_necessaria_*_banda*` e `sobra_pico_p90_*_banda*`. CR4 é lido com a ponta desfavorável. Re-registradas ANA-009 e depois ANA-015, cuja margem da ALT3 agora usa a frota dia a dia e traz a banda em `margem_robo_alt3_frota_nec_banda*`; a frota necessária é conferida como igual à dia a dia por asserção.
- **INS-054 e INS-087.** INS-054 cita primeiro a frota dia a dia e declara a banda como leitura otimista, sem reserva. INS-087 cita primeiro a margem com a frota necessária pela leitura desfavorável (dia a dia e regra por tipo), depois a banda como ponta otimista, e declara que uma frota mínima não tem reserva de disponibilidade. INS-055 e INS-059 ajustados às chaves novas; em INS-059 o "um separador por hora" virou valor ligado.
- **INS-043 e INS-046.** Afirmação e ação corrigidas: ANA-016 não confirma PT-D3 nem PT-D4 (o sinal se inverte contra um depositante); os dois ficam como trilha da descoberta, fora do memorando, e a revisão depende do critério de inversão que Marcus adotar no G3. Campos `confirmacao` e `red_team_analitico` não foram tocados.
