# acta-agentes

<!-- squads:inicio (gerado por ferramentas/montar_nuvem.py; não edite à mão) -->
## Squads da Acta

| Squad | Pasta | Prefixo dos agentes | Comandos |
|---|---|---|---|
| análise de dados | `squad-analise/` | `dados-` | /acompanhar, /analisar, /anexar-analise, /atualizar-analise, /status-analise |
| estratégia | `squad-estrategia/` | `est-` | /anexar-estrategia, /estrategia, /revisao-trimestral, /status-estrategia |
| orçamento | `squad-orcamento/` | `orc-` | /anexar-orcamento, /atualizar-base, /orcar, /retro, /status-orcamento |
| produto | `squad-produto/` | `prod-` | /anexar-produto, /produto, /revisao-produto, /status-produto |

Regras para todos os squads, em especial na nuvem:
- Cada squad tem o seu `CLAUDE.md`, motor e base de conhecimento. Rode os comandos do motor de dentro da pasta do squad (`cd squad-x && python -m motor...`).
- Na nuvem, arquivos de entrada vêm do Google Drive pelo conector: baixe para `<squad>/entrada/<trabalho>/` (fora do git) e importe como no uso local.
- Ao concluir, publique com `python ferramentas/publicar_nuvem.py <squad> <pasta da versão>` e faça commit e push só de `<squad>/publicados/`. Nunca commite `projetos/`, `entrada/`, `dados/` nem chaves.
- Dados com informação pessoal ou de cliente (squad de análise) só na nuvem se Marcus autorizar; a opção padrão é rodar no computador dele com Remote Control.
<!-- squads:fim -->
