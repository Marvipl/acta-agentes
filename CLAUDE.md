# acta-agentes

<!-- squads:inicio (gerado por ferramentas/montar_nuvem.py; não edite à mão) -->
## Squads da Acta

| Squad | Pasta | Prefixo dos agentes | Comandos | Pasta no Drive |
|---|---|---|---|---|
| análise de dados | `squad-analise/` | `dados-` | /acompanhar, /analisar, /anexar-analise, /atualizar-analise, /status-analise | Acta > Análises |
| estratégia | `squad-estrategia/` | `est-` | /anexar-estrategia, /estrategia, /revisao-trimestral, /status-estrategia | Acta > Planejamento Estratégico |
| orçamento | `squad-orcamento/` | `orc-` | /anexar-orcamento, /atualizar-base, /orcar, /retro, /status-orcamento | Acta > Orçamentos |
| produto | `squad-produto/` | `prod-` | /anexar-produto, /produto, /revisao-produto, /status-produto | Acta > Produtos |

Regras para todos os squads, em especial na nuvem:
- Cada squad tem o seu `CLAUDE.md`, motor e base de conhecimento. Rode os comandos do motor de dentro da pasta do squad (`cd squad-x && python -m motor...`).
- Na nuvem, arquivos de entrada vêm do Google Drive pelo conector: baixe para `<squad>/entrada/<trabalho>/` (fora do git) e importe como no uso local.
- Ao concluir, os comandos principais dos squads publicam sozinhos; para publicar de novo ou manualmente, use `/publicar-drive <squad> <pasta da versão>`: ele envia ao Drive o pacote completo (documentos finais e metadados: JSON, CSV, planilha, nós, revisões), igual à publicação local, e faz commit de `<squad>/publicados/`. A publicação do próprio squad (`python -m motor.publicar`) só funciona no computador, com a pasta do Drive sincronizada. Nunca commite `projetos/`, `entrada/`, `dados/` nem chaves.
- Dados com informação pessoal ou de cliente (squad de análise) só na nuvem se Marcus autorizar; a opção padrão é rodar no computador dele com Remote Control.
<!-- squads:fim -->
- Consolidação no main: cada sessão trabalha numa branch `claude/*` e o workflow `Consolidar no main` (`.github/workflows/consolidar-main.yml`) faz o merge no main a cada push e apaga a branch, para a próxima rodada já começar com os agentes enriquecidos. Conflito com o main ou mudança em `.github/workflows` vira PR `[revisar]`. Por isso, faça commit e push do que a rodada aprendeu antes de encerrar.
