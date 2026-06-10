# Fontes prioritárias de inteligência (Agente de Notícias)

Stack de fontes em CAMADAS, com CADÊNCIA. A lógica não é ter a maior lista, e sim cruzar
quatro camadas (editorial especializado, wire de negócios, dados/analistas, verticais
brasileiros). Quando elas se cruzam, a qualidade sobe e o ruído promocional cai.

Como o agente usa isto: não é scraping programado (a ferramenta não varre sites
inteiros). O agente faz buscas direcionadas a estes domínios e termos, dentro da janela
de datas, e abre as páginas relevantes. Prioriza estas fontes, mas não se limita: notícia
altamente relevante de fonte confiável fora da lista também entra.

================================================================================
CADÊNCIA (quando consultar cada camada)
================================================================================

TODA EXECUÇÃO (diário, dias úteis):
  Núcleo editorial diário + wire de negócios (camadas 1 e 2) + os verticais brasileiros
  pertinentes ao(s) setor(es) do dia (camada 4).

SEGUNDA-FEIRA (passada semanal de contexto):
  Além do núcleo diário, fazer a passada na camada de DADOS E ANALISTAS (camada 3): IFR,
  Interact Analysis, A3, Automation.com e Robohub. Essas fontes valem menos para a
  notícia de 12h atrás e mais para calibrar contexto, sizing e tendência. O agente deve
  verificar o dia da semana; se for segunda-feira (ou a primeira execução útil da
  semana, caso a segunda seja feriado), incluir esta passada.

JANELAS DE EVENTO (apertar a frequência e a atenção):
  Perto de grandes feiras/conferências, concentra-se lançamento, demo, captação e
  parceria. Nessas janelas, dar peso extra a cobertura de evento e a releases de
  produto. Eventos de referência (confirmar datas a cada ano, pois mudam):
    - ICRA (IEEE Robotics & Automation) — costuma ocorrer no 1º semestre.
    - Automate (A3) — EUA, costuma ocorrer no meio do ano.
    - MODEX / ProMat (alternados) — EUA, intralogística e material handling.
    - RoboBusiness — EUA, 2º semestre.
    - No Brasil: Intermodal e INTRA-LOG Expo (intralogística), Intersolar (solar).
  Regra prática: se a data atual estiver dentro de ~7 dias antes/depois de um desses
  eventos, o agente busca explicitamente por "[nome do evento] [ano]" e por anúncios
  feitos no evento, além do núcleo diário.

================================================================================
CAMADA 1 — EDITORIAL ESPECIALIZADO DIÁRIO (robótica e automação)
================================================================================

- The Robot Report — therobotreport.com — fonte-mãe: robótica comercial, pesquisa
  aplicada, análise e investment tracking. Tem newsletter e podcast próprios.
- Robotics 24/7 — robotics247.com — forte em DEPLOYS REAIS: manufatura, supply chain,
  logística, integradores, usuários finais, eventos.
- IEEE Spectrum, robótica — spectrum.ieee.org/topic/robotics — maior densidade
  editorial-técnica; proteção contra leitura superficial do hype.
- Robotics & Automation News — roboticsandautomationnews.com — boa cadência global
  (industrial, logistics, warehouse, humanoids, investments). REGRA: nunca usar como
  fonte única para claim comercial sensível (o site separa editorial de press release,
  sponsor e publicidade).
- Automated Warehouse — automatedwarehouseonline.com — essencial para AMR, warehouse
  automation, orchestration, fulfillment e intralogística.
- Robohub — robohub.org — complementar (organização sem fins lucrativos, ligada a IEEE
  RAS, AAAI, ACM SIGAI etc.): pesquisa, comunidade, expert views, podcast Robot Talk.
  [Camada 3 na cadência semanal.]
- Automation.com — automation.com — complementar (publicação da ISA, vendor-neutral):
  cruzamento de robótica com automação industrial, motion, IIoT, segurança e operações.
  [Camada 3 na cadência semanal.]

Observação de famílias editoriais (evita redundância): The Robot Report e Automated
Warehouse são do mesmo grupo (WTWH); Robotics 24/7, Logistics Management e Modern
Materials Handling são do mesmo grupo (Peerless). Não varrer todas as irmãs com o mesmo
peso: usar a generalista da família como diária e a de nicho como overlay temático.

================================================================================
CAMADA 2 — IMPRENSA DE NEGÓCIOS, FUNDING E M&A
================================================================================

- Reuters — reuters.com — OBRIGATÓRIA por busca direcionada: melhor fonte para funding
  relevante, IPOs, big tech, fabricantes e movimentos corporativos estruturais.
- TechCrunch — techcrunch.com — SECUNDÁRIA: startups, humanoids, warehouse robotics;
  boa para startup signal e tese, não como base única (cadência irregular).
- Crunchbase News — news.crunchbase.com — camada de venture e agregação de funding.
- Sifted — sifted.eu — radar da Europa para robotics funding e scaling.
- Caixin Global — caixinglobal.com — OPCIONAL, lente regional para China (humanoids,
  IPOs, embodied AI, cadeia asiática), que muitas vezes aparece com antecedência.

Triangulação de funding/M&A: Reuters para movimentos materiais; TechCrunch para startup
signal; Crunchbase para visão agregada; Sifted para a dinâmica europeia.

================================================================================
CAMADA 3 — DADOS E ANALISTAS (passada SEMANAL — segunda-feira)
================================================================================

Buscar atualização recente; não baixar PDFs pesados; usar o resumo público e citar o
link. Tratar como CONTEXTO/NÚMEROS, não como breaking news.

- IFR — International Federation of Robotics — ifr.org — autoridade global em
  estatísticas e relatório anual "World Robotics" (instalações, densidade, service e
  mobile robots, forecasts).
- Interact Analysis — interactanalysis.com — forte em warehouse automation, mobile
  robots, order intake e forecasts; publica resumos públicos frequentes.
- A3 (Association for Advancing Automation) — automate.org — usar para robot orders na
  América do Norte, market intelligence, standards, safety e eventos. REGRA: o "News
  Hub" mistura institucional com itens assinados por empresas; não tratar como
  jornalismo puro.
- Automation.com e Robohub — ver camada 1; consultar na passada semanal para contexto.

================================================================================
CAMADA 4 — BRASIL (verticais por setor da Acta)
================================================================================

Logística e intralogística:
- Tecnologística — tecnologistica.com.br — principal fonte editorial BR do vertical
  (logística, armazenagem, intralogística, eventos).
- MundoLogística — mundologistica.com.br — SECUNDÁRIA; ignorar automaticamente peças
  marcadas como "publicidade".
- Logistics Management (logisticsmgmt.com) e Modern Materials Handling (mmh.com) — usar
  para surveys/estudos e corroboração pontual, não para checagem diária.

Solar (energia):
- Canal Solar — canalsolar.com.br — diário do mercado fotovoltaico (O&M, limpeza,
  eficiência, operação).
- pv magazine Brasil — pv-magazine-brasil.com — complementar obrigatório do vertical
  solar (solar, armazenamento, tecnologia, mercado).

Óleo e gás:
- TN Petróleo — tnpetroleo.com.br — especialista BR em tecnologia e negócios de O&G.
  Como o volume de robótica em O&G num único veículo é baixo, combinar com busca global
  por: inspection robot, subsea robot, offshore inspection, autonomous inspection.

Facilities:
- InfraFM — infrafm.com.br — hub de facility/property/workplace management na América
  Latina (limpeza, segurança, operação predial). SECUNDÁRIA; filtrar promocional.

Startups e captação no Brasil:
- Startups.com.br — startups.com.br — radar de rounds, deep tech e ecossistema nacional.
- Brazil Journal — OPCIONAL, não prioritário.

Contexto industrial brasileiro (checagem periódica, não diária):
- ABIMAQ — abimaq.org.br — feiras, automação industrial, manufatura avançada, agenda.
- SBA (Sociedade Brasileira de Automática) — sba.org.br — agenda técnica e automação
  inteligente.

================================================================================
PERFIS E NEWSLETTERS PÚBLICAS (apenas canais abertos — NUNCA LinkedIn)
================================================================================

Acompanhar especialistas SOMENTE por canais públicos abertos. NUNCA acessar o LinkedIn
por automação (regra inegociável do projeto).

- Lukas Ziegler — "we all are robots" — ziegler.substack.com — leitura complementar
  SEMANAL, não fonte primária de breaking news. Usar o Substack público; NÃO acessar o
  perfil do LinkedIn.
- Robohub newsletter / Robot Talk — camada pública de comentários, pesquisa e
  entrevistas.
- X/Twitter (best-effort, sem login): usar busca pública "site:x.com <termo>" ou
  "site:twitter.com <termo>" para posts públicos indexados. NÃO logar nem raspar o feed;
  cobertura parcial, apenas sinal complementar.

================================================================================
REGRAS EDITORIAIS DE USO
================================================================================

1. Funding, M&A e IPO só entram no radar quente APÓS confirmação por wire (Reuters),
   veículo de negócios ou release oficial. Rumor não confirmado não vira notícia.
2. Quando a fonte tiver áreas separadas de press release, promoted, sponsor article ou
   páginas assinadas por empresas, tratá-las como SINAL COMPLEMENTAR, não como verdade
   editorial final. Vale especialmente para A3, Robotics & Automation News, Robotics 24/7
   e verticais brasileiros.
3. Priorizar redações independentes para o noticiário principal; associações e analistas
   para dados e contexto.

================================================================================
TERMOS DE BUSCA (rotacionar)
================================================================================

EN: AMR, autonomous mobile robot, warehouse robotics, intralogistics, fleet management,
SLAM navigation, embodied AI, humanoid robot, industrial automation, facility robotics,
solar panel cleaning robot, oil and gas inspection robot, subsea robot, offshore
inspection, robotics funding, robotics acquisition, robotics IPO.
PT: robótica logística, intralogística, robô autônomo, AMR, automação industrial,
robótica para facilities, limpeza de painéis solares robô, inspeção robótica óleo e gás,
captação startup robótica.
