# Prompt — Agente de Pauta do Conselho / Rotina 2: Minuta (terça após a 1ª segunda, 09:00)

> Rotina Remote com gatilho SEMANAL (toda terça 09:00, America/Sao_Paulo) e
> guarda de data na instrução. Repositório: acta-agentes. Ambiente: o mesmo do
> agente de pauta de staff. Nenhum segredo na instrução.

---

Guarda de data — execute primeiro:

    python3 -c "import datetime,zoneinfo;d=datetime.datetime.now(zoneinfo.ZoneInfo('America/Sao_Paulo'));print(d.isoweekday(),d.day)"

Prossiga SOMENTE se o resultado for dia da semana 2 (terça) E dia do mês entre
2 e 8 (terça seguinte à primeira segunda-feira do mês). Caso contrário, encerre
imediatamente reportando "fora da janela mensal — nada a fazer".

Preparação: chmod +x pauta-staff/scripts/*.sh pauta-conselho/scripts/*.sh

Passo 0 — Diagnóstico: rode pauta-staff/scripts/slack.sh testar
- "FALHA DE REDE": pare e reporte bloqueio de slack.com no ambiente.
- "TOKEN INVALIDO": pare e reporte o erro exato.

Tarefa: leia pauta-conselho/SKILL.md e siga exatamente o "Fluxo de execucao"
descrito nele para gerar e publicar a MINUTA da pauta da Reunião do Conselho
Consultivo, pedindo validação humana.

Resumo do fluxo (a referência completa é o SKILL.md):
1. Rodar pauta-conselho/scripts/coletar_fontes.sh para obter a última pauta/ata
   de CONSELHO consolidada e TODAS as atas de Staff C-Level desde então.
2. Ler cada fonte com pauta-staff/scripts/ler_docx.py.
3. Coletar itens adicionais: respostas da thread de coleta de ontem + mensagens
   humanas do canal mencionando "conselho" desde a última reunião de conselho
   (cutoff: segunda 23:59, America/Sao_Paulo).
4. Montar o JSON e gerar o DOCX com pauta-staff/scripts/gerar_pauta.py sobre
   pauta-conselho/templates/Template_Pauta_Conselho.docx. Data da reunião como
   placeholder "[ __ ] / MM / AAAA". Nenhuma afirmação sem origem nas fontes.
5. Verificar com ler_docx.py e validar_pauta.py --tipo conselho (titulo_ok deve
   ser true; a data fica placeholder de propósito). Nunca publicar sem verificar.
6. Publicar com slack.sh enviar_arquivo e o comentário de validação definido no
   SKILL.md (pedindo conferência, ajuste manual e correções na thread).

Regras inegociáveis (detalhadas no SKILL.md): nunca inventar dados — toda
afirmação precisa existir nas fontes; itens "Deliberar:" só quando a fonte
sinalizar decisão pendente; 9fleet e Roboteazy; nunca citar Corsight, Venturus
ou SiDi; sem emojis. Nunca imprima o valor do token em nenhuma saída.
