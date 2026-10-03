# Critério de inversão por depositante na ANA-016 (decisão do orquestrador, 2026-10-03, a conferir pelo red team r2 e por Marcus no G3)

- O plano manda tratar "inversão de sinal na robustez" como não confirmação, mas não fixa quando um segmento por depositante conta como inversão.
- O estatístico adotou, depois de ver os sinais: conta como inversão o depositante cujo IC de 95% por operador do segmento inteiro fica do lado oposto. Com isso, PT-D3 e PT-D4 passam a "não confirmada (inversão na robustez)"; PT-D1, PT-H04 e PT-H10 seguem confirmadas.
- Alternativa mais estrita (só sinal): PT-D1 também cairia, por três depositantes pequenos com sinal oposto e IC que contém zero.
- Decisão: manter o critério do IC oposto. Ele é mais conservador que a leitura agregada, porque derruba duas pistas, e evita tratar ruído de segmentos pequenos como inversão. Por ter sido fixado depois de ver os sinais, fica declarado no memorando, junto com o resultado pelo critério só de sinal.
