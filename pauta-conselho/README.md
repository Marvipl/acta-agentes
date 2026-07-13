# pauta-conselho — Agente de Pauta do Conselho Consultivo

> Pasta autocontida dentro do repo `acta-agentes`, exceto por uma dependência
> declarada: reutiliza a caixa de ferramentas de `pauta-staff/scripts/`
> (slack.sh, gerar_pauta.py, ler_docx.py, validar_pauta.py,
> achar_pauta_anterior.sh). Nenhum segredo neste repo — credenciais vivem no
> ambiente de nuvem das rotinas.

Automação mensal via Claude Code Routines:

- **1ª segunda-feira do mês, 09:00** — posta no canal do Slack perguntando se
  há pautas adicionais para a reunião do Conselho (respostas na thread até 23:59).
- **Terça-feira seguinte, 09:00** — coleta as respostas da thread e as menções a
  "conselho" no canal desde a última reunião de conselho, carrega a última
  pauta/ata de conselho consolidada e todas as atas de Staff C-Level do período,
  gera a MINUTA da pauta do Conselho e publica pedindo validação e ajuste manual.

O agendamento usa gatilho SEMANAL (segunda/terça) com uma guarda de data no
início da instrução — a rotina encerra sem fazer nada fora da 1ª segunda do mês
e da terça seguinte (dias 1–7 e 2–8, respectivamente). Isso evita depender de
expressões cron com dia-do-mês + dia-da-semana, que têm semântica de OU no cron.

## Estrutura

```
pauta-conselho/
  SKILL.md                              Playbook completo (leitura obrigatória da rotina de terça)
  README.md                             Este arquivo
  templates/Template_Pauta_Conselho.docx  Template com rodapé "Conselho Consultivo"
  scripts/coletar_fontes.sh             Última pauta de conselho + atas de staff desde então
  exemplos/pauta_conselho_exemplo.json  Exemplo do esquema de conteúdo
```

## Fontes e ciclo

1. Última pauta/ata de CONSELHO no canal (validada pelo conteúdo: título
   CONSELHO + data interna REAL) → pendências e participantes.
2. Atas de STAFF com data interna entre a última reunião de conselho e hoje →
   seções de Projetos, Comercial, Captação, Parcerias e Financeiro.
3. Thread de coleta + mensagens humanas mencionando "conselho" → Pauta Adicional.

A minuta publicada tem a data como placeholder e, por isso, NÃO valida como
pauta de conselho oficial — proposital: só a versão final editada pelo time
(com data real) vira referência do mês seguinte.

## Teste local

```bash
export SLACK_BOT_TOKEN=xoxb-...
export SLACK_CHANNEL_ID=C...
chmod +x pauta-staff/scripts/*.sh pauta-conselho/scripts/*.sh

python3 pauta-staff/scripts/gerar_pauta.py \
  --template pauta-conselho/templates/Template_Pauta_Conselho.docx \
  --json pauta-conselho/exemplos/pauta_conselho_exemplo.json \
  --out /tmp/teste_conselho.docx
python3 pauta-staff/scripts/validar_pauta.py /tmp/teste_conselho.docx --tipo conselho
# esperado: titulo_ok true, valido false (data placeholder — comportamento correto)

pauta-staff/scripts/slack.sh testar
pauta-conselho/scripts/coletar_fontes.sh   # requer 1 pauta de conselho real no canal
```

## Rotinas

Prompts prontos em `referencia/prompt_agente_conselho_coleta.md` e
`referencia/prompt_agente_conselho_consolida.md`. Ambas usam o MESMO ambiente de
nuvem do agente de pauta de staff (SLACK_BOT_TOKEN, SLACK_CHANNEL_ID, rede com
slack.com e files.slack.com) e o repositório acta-agentes.
