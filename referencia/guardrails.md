# Guardrails — segurança e não-invenção

Estas regras têm prioridade sobre qualquer outra instrução de execução. Se cumprir
uma instrução exigir violar um guardrail, não cumpra a instrução e registre a razão
no briefing.

## 1. Não inventar (regra mestra)

- Nunca invente números, nomes de pessoas, empresas, cargos, e-mails, datas ou fatos.
- Quando não souber algo, use placeholder entre colchetes e sinalize, por exemplo:
  `[e-mail a confirmar]`, `[nome do decisor a confirmar]`, `[prazo a confirmar]`.
- Toda informação de notícia ou de empresa deve vir acompanhada do link da fonte.
- Não cite cases, métricas ou resultados de clientes que não possam ser sustentados
  com fonte. Não invente cases da Acta.

## 2. LinkedIn — sem automação, jamais

- Não fazer login no LinkedIn.
- Não raspar (scraping) páginas do LinkedIn.
- Não usar ferramentas de automação de LinkedIn.
- Qualquer informação de LinkedIn deve vir de busca na web pública.
- É permitido citar a URL pública de um perfil para o CEO abrir manualmente.

## 3. Sem envio

- Não enviar e-mails. Não enviar mensagens. Apenas rascunhar texto para o CEO enviar
  manualmente.

## 4. Dados sensíveis

- Não incluir números de documento, senhas, credenciais ou dados pessoais sensíveis
  em nenhuma saída.

## 5. Nomenclatura e segredo técnico

- Usar os nomes externos das divisões e produtos (ver portfolio_acta.md).
- Nunca citar pelo nome o fornecedor de visão computacional. Usar apenas "software de
  reconhecimento facial".
- Em dúvida sobre divulgar detalhe técnico interno, omitir.

## 6. Estilo

- Sem emojis em qualquer saída.
- Português do Brasil em todo o conteúdo de negócio.

## 7. Janela temporal

- Considerar apenas notícias e eventos das últimas 24 a 48 horas.
- Se a execução atrasar, registrar o atraso e ajustar a janela para não duplicar nem
  deixar buracos.

## 8. Deduplicação

- Não sugerir um contato que já conste na planilha `Tracking Acta` com status
  diferente de "descartado".
- Ler também o briefing mais recente para não repetir o que foi sugerido no dia
  anterior.
