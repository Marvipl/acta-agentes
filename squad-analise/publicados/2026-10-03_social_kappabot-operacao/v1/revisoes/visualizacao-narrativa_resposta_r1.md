# Resposta de visualizacao-narrativa às revisões D4 (sup-comunicacao r1 e r2, sup-negocio D4 r1 e r2)

Entregáveis revisados: `entregaveis/memo_decisao.md.tpl`, `relatorio_executivo.md.tpl`, `oferta_enriquecida.md.tpl`. Rodado com `motor.rodar` na trava; `render_status.json` sem variável faltando; `motor.validar --fase D4` liberado.

## Atendido
- **Limiar e janela coerentes com a configuração recomendada.** Limiar com reserva, sem implementação, com implementação (limite superior) e com desconto do robô que já opera. Janela de preço por cenário (cada linha é um cenário só). Variáveis IMP-REC-* e IMP-INV-PR11-*.
- **Memorando.** Uma página (até 450 palavras renderizadas), ALT1 com um só sentido (portão), ramo "se passar" cotável, ramo "se não passar" com piloto pago e encerrar declarados como fora da lista original e dependentes do aceite de Marcus no G3. Fatos só medidos; estimativas em "Impacto", com margem antes do hardware e hardware máximo pagável (sem e com implementação). Piloto com implantação, custo total e duração. Ressalvas do red team nos Riscos. Linha de "os dados não permitem concluir".
- **Meta do piloto.** Três leituras por teto de intervalo (IMP-PILOTO-META-PR05-T300, T900, T1800), com a folga física (IMP-PILOTO-META-FOLGA-FISICA-*). A leitura do teto conservador é inatingível; só a do teto mais folgado pode valer como critério. Mesmo texto no relatório e na oferta. IMP-INV-PR05-ALT6-SEM-ALTO saiu da meta do piloto.
- **Relatório.** Título "Insights para aprovação no G3 (rascunho até a aprovação)", resumos sem número para os insights longos, INS-052 e INS-070 fora, ressalvas do red team da decisão, glossário. Contato com a Royal Canin sempre pela Social, via Marcus.
- **Oferta.** Aviso de uso interno visível, glossário, proposta-modelo cotável por cenário, cláusulas (go-live, erro de conferência, reserva, garantia de capacidade), V2 e V4 corrigidos, U1 e U5 como hipótese, Q5/N9/N10 sem exposição da Social ou da Royal Canin. Nível da garantia: medido no primeiro trimestre da ALT4, sem o primeiro mês, ou no piloto.
- **Rótulos.** Margem zero por construção quando não há janela; "margem de" no lugar de "ganha".

## Limites
- **IC de bootstrap por dias de INS-015** (ANA-003.excedente_h_p90_escopo_poscolmeia_ic_dias): nenhuma variável do motor o expõe (IMP-CR8-P90-RC-EXCEDENTE tem p10 = p90 = ponto). No relatório e na oferta ele vem pelo texto integral de INS-015; no memorando, só qualitativo ("fração de jornada, mesmo no IC de bootstrap por dias"), por causa do limite de palavras. Se o motor passar a expor o IC (por exemplo, como p10 e p90 do modelo), os três documentos o citam por variável.
- **Tarifas em R$ com desconto** e **hardware máximo com desconto**: sem modelo; aparecem como "não calculado".
- **Painel** (legendas, filtros, gráfico da janela de preço): fora das minhas saídas; fica com o orquestrador.
- **Prazo do próximo passo** segue [●] (data da reunião com a Social não informada).
